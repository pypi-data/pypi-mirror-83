#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import os
import uuid
import warnings
from abc import ABCMeta
from typing import List, Optional
from urllib.parse import urljoin

from dli.client.components.urls import consumption_urls
from s3transfer.manager import TransferManager, TransferConfig

from dli.aws import create_refreshing_session, trace_logger, match_partitions
from dli.client import utils
from dli.models import AttributesDict
from dli.models.file_model import get_or_create_os_path


class DatasetModel(AttributesDict, metaclass=ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, )

    def __endpoint_url(self):
        return f'https://{self._client._environment.s3_proxy}'

    def _check_access(self):
        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

    @property
    def id(self):
        return self.dataset_id

    def list(
            self,
            request_id=None,
            partitions: Optional[List[str]] = None,
            filter_path: Optional[str] = None,
            absolute_path: bool = True,
            skip_hidden_files: bool = True,
    ):
        """
        List all the paths to files in the dataset. Calls go via the
        Datalake's S3 proxy, so the returned paths will be returned in the
        style of the S3 proxy, so in the pattern
        `s3://organisation_short_code/dataset_short_code/<path>`.
        S3 proxy does not return direct paths to the real location on S3 as
        they may be sensitive.

        The list will filter out paths where:
        * The size is zero bytes.
        * The name of any partition within the path is prefixed with a `.` or
        a `_` as that means it is intended as a hidden file.
        * The name of any partition within the path is exactly the word
        `metadata`.
        * It is a directory rather than a file.
        * Files with the wrong extension for the dataset's type i.e for
        a .parquet dataset we will return only .parquet files, zero .csv
        files.

        This list will filter based on `load_type` of the dataset. When the
        dataset's `load_type` is `Incremental Load` then files will be listed
        from all of the `as_of_date` partitions on S3. When the
        dataset's `load_type` is `Full Load` then files will be listed only
        the most recent `as_of_date` partition on S3.
        Please see the support library documentation for more information
        about how the `load type` affects the data you can access in a dataset:
        https://supportlibrary.ihsmarkit.com/display/DLSL/Exploring+Datasets#ExploringDatasets-Howthe%60loadtype%60affectsthedatayoucanaccessinadataset

        Parameters
        ----------
        :param str request_id: Optional. Automatically generated value
            used by our logs to correlate a user journey across several
            requests and across multiple services.

        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=` and
            `!=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.list(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.list(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :param str filter_path: Optional. If provided only a subpath matching
            the filter_path will be matched. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset.list(filter_path='as_of_date=2020')

        :param bool absolute_path: True (default) for returning an
            absolute path to the path on the S3 proxy. False to return a
            relative path (this is useful if using a TransferManager).

        :param bool skip_hidden_files: True (default) skips files that have
            been uploaded to S3 by Spark jobs. These usually start with a
            `.` or `_`.
        """

        self._check_access()

        if request_id is None:
            request_id = str(uuid.uuid4())

        def add_request_id_to_session(**kwargs):
            kwargs["request"].headers['X-Request-ID'] = request_id
            trace_logger.info(
                f'GET Request to https://{self.__endpoint_url()} '
                f'with request_id: {request_id}'
            )

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=add_request_id_to_session
        ).resource(
            's3',
            endpoint_url=self.__endpoint_url()
        )

        bucket = s3_resource.Bucket(
            self.organisation_short_code
        )

        filter_prefix = self.short_code + (
            '' if self.short_code.endswith('/') else '/'
        )

        if filter_path:
            filter_prefix = filter_prefix + filter_path.lstrip('/')

        def _to_s3_proxy_path(object_summary) -> str:
            if absolute_path:
                return f"s3://{self.organisation_short_code}/" \
                       f"{object_summary.key}"
            else:
                return object_summary.key

        # Convert each object_summary into an S3 proxy path.
        object_summaries = [
            object_summary for object_summary in bucket.objects.filter(
                # Prefix searches for exact matches and folders
                Prefix=filter_prefix
            )
        ]

        self._client.logger.info(
            "Number of paths on S3 for this dataset: "
            f"'{len(object_summaries)}'"
        )

        # Convert each object_summary into an S3 proxy path.
        paths: List[str] = [
            _to_s3_proxy_path(object_summary) for object_summary in
            object_summaries if not object_summary.key.endswith('/')
        ]

        self._client.logger.info(
            "Number of paths on S3 for this dataset "
            f"after filtering out empty directories: '{len(paths)}'"
        )

        if skip_hidden_files:
            # [DL-4545][DL-4536][DL-5209] Do not read into files or
            # directories that are cruft from Spark which Spark will ignore
            # on read, e.g. files/dirs starting with `.` or `_` are hidden
            # to Spark.

            # Skip as_of_date=latest as it is a Spark temporary folder.

            def is_hidden_file(path: str):
                return (
                        path.startswith('.') or
                        path.startswith('_') or
                        (
                            path == 'metadata' and
                            self.content_type != "Unstructured"
                        ) or
                        path == 'as_of_date=latest'
                )

            paths: List[str] = [
                path for path in paths
                if not any(is_hidden_file(split) for split in path.split('/'))
            ]

            self._client.logger.info(
                f"Number of paths on S3 for this dataset "
                f"after filtering out hidden files: '{len(paths)}'"
            )

        if partitions:
            # Filter paths to only those that match the partitions.
            paths = [
                path for path in
                paths if match_partitions(path, partitions)
            ]

            self._client.logger.info(
                'Number of paths for this dataset '
                f"after filtering with partitions: {len(paths)}'"
            )

        return paths

    def partitions(self) -> dict:
        """
        Retrieves the list of available partitions for a given dataset.

        The data onboarding team have structured the file paths on S3 with
        simple partitions e.g. `as_of_date` or `location`.

        Their aim was to separate the data to reduce the size of the
        individual files. For example, data that has a `location` column with
        the options `us`, `eu` and `asia` can be separated into S3 paths like
        so:

        .. code-block::

            package-name/dataset/as_of_date=2019-09-10/location=eu/filename.csv
            package-name/dataset/as_of_date=2019-09-10/location=us/filename.csv

        in this case the `partitions` will be returned as:

        .. code-block::

            {'as_of_date': ['2019-09-10'], 'location': ['eu', 'us]}
        """
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_partitions.format(id=self.id)
            )
        )

        return response.json()["data"]["attributes"]["partitions"]

    def download(
        self,
        destination_path: str,
        flatten: Optional[bool] = False,
        filter_path: Optional[str] = None,
        partitions: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Downloads the original dataset files from the data lake to local copy
        destination of your choice.

        The flatten parameter retains only the file name, and places the
        files in the directory specified, else the files will be downloaded
        matching the directory structure as housed on the data lake.

        The filter path and partitions parameters specify that only a subset
        of the S3 path should be downloaded.

        Parameters
        ----------
        :param destination_path: required. The path on the system, where the
            files should be saved. Must be a directory, if doesn't exist, will
            be created.

        :param bool flatten: The default behaviour (=False) is to use the s3
            file structure when writing the downloaded files to disk.

        :param str filter_path: Optional. If provided only a subpath matching
            the filter_path will be matched. This is less flexible than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order, but filter_path relies
            on a fixed order of partitions that the user needs to know ahead
            of time.

            Example usage to get all paths that start with the `as_of_date`
            2020. Note this is a string comparison, not a datetime comparison.

            .. code-block:: python

                dataset.download(filter_path='as_of_date=2020')

        :param List[str] partitions: Optional. A list of filters (partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to read from
            before they  have to read any data. This will reduce the amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file.extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list of partitions you want to get data from by
            passing in a list in the format `<key><operator><value>`. Please
            note that you should not include any extra quotation marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=` and
            `!=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.download(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :return: the list of the files that were downloaded successfully. Any
            failures will be printed.


        :example:

            Downloading without flatten:

            .. code-block:: python

                dataset.download('./local/path/')

                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'as_of_date=2019-09-11/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]

        :example:

            Downloading with ``filter_path``

            .. code-block:: python

                dataset.download(
                    './local/path/', filter_path='as_of_date=2019-09-10/'
                )
                [
                  'as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                ]


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                dataset.download('./local/path/', flatten=True)
                [
                  'StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
                  'StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]


        """

        return self.__download(destination_path, flatten, filter_path, partitions)

    def __download(
        self,
        destination_path: str,
        flatten: Optional[bool] = False,
        filter_path: Optional[str] = None,
        partitions: Optional[List[str]] = None,
        custom_filter=None
    ) -> List[str]:
        """
        Equivalent to the exposed `download` method except for final argument.

        Additional Parameters
        ----------
        :param custom_filter: A function which may optionally filter the s3 paths returned during the first
        stage of download (namely path lookup as part of list is filtered).
        """
        self._check_access()
        request_id = str(uuid.uuid4())

        paths = self.list(
            request_id=request_id,
            partitions=partitions,
            filter_path=filter_path,
            absolute_path=False,  # TransferManager uses relative paths.
        )
        if custom_filter:
            paths = custom_filter(paths)

        def __add_request_id_to_session(**kwargs):
            kwargs["request"].headers['X-Request-ID'] = request_id
            trace_logger.info(
                f'GET Request to {self.__endpoint_url()} '
                f'with request_id: {request_id}'
            )

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session,
            event_hooks=__add_request_id_to_session
        ).resource(
            's3',
            endpoint_url=self.__endpoint_url()
        )

        s3_client = s3_resource.meta.client

        # multipart_threshold -- The transfer size threshold for which
        # multipart uploads, downloads, and copies will automatically
        # be triggered.
        # 500 GB should be a large enough number so that the download never
        # triggers multipart download on cloudfront.
        KB = 1024
        GB = KB * KB * KB
        multipart_threshold = 500 * GB
        config = TransferConfig(
            multipart_threshold=multipart_threshold
        )

        with TransferManager(s3_client, config=config) as transfer_manager:
            _paths_and_futures = []

            for path in paths:
                if not path.endswith('/'):
                    to_path = get_or_create_os_path(
                        s3_path=path,
                        to=destination_path,
                        flatten=flatten
                    )

                    self._client.logger.info(
                        f'Downloading {path} to: {to_path}...'
                    )

                    if os.path.exists(to_path):
                        warnings.warn(
                            'File already exists. Overwriting.'
                        )

                    # returns a future
                    future = transfer_manager.download(
                        self.organisation_short_code,
                        path,
                        to_path
                    )

                    _paths_and_futures.append((to_path, future))

            _successful_paths = []
            for path, future in _paths_and_futures:
                try:
                    # This will block for this future to complete, but other
                    # futures will keep running in the background.
                    future.result()
                    _successful_paths.append(path)
                except Exception as e:
                    message = f'Problem while downloading:' \
                              f'\nfile path: {path}' \
                              f'\nError message: {e}\n\n'

                    self._client.logger.error(message)
                    print(message)

            return _successful_paths

    def metadata(self):
        """
        Once you have selected a dataset, you can print the metadata (the
        available fields and values).

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> datasets = client.datasets()

                # Get metadata of the 'ExampleDatasetShortCode' dataset.
                >>> datasets['ExampleDatasetShortCode'].metadata()

        :example:

            .. code-block:: python
                # Get an exact dataset using the dataset_short_code and
                # organisation_short_code.
                >>> dataset = client.get_dataset(dataset_short_code='ExampleDatasetShortCode', organisation_short_code='IHSMarkit')
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :example:

            .. code-block:: python
                # Get all datasets.
                >>> dataset = client.datasets()['ExampleDatasetShortCode']
                # Get metadata of the dataset.
                >>> dataset.metadata()

        :return: Prints the metadata.
        """
        utils.print_model_metadata(self)
