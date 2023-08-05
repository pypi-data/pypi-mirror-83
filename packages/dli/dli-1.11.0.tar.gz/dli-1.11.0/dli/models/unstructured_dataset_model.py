#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
from typing import Optional, List

from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import dataset_urls
from dli.models import log_public_functions_calls_using
from dli.models.dataset_model import DatasetModel

trace_logger = logging.getLogger('trace_logger')


class UnstructuredDatasetModel(DatasetModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs,)

    def __getattr__(self, name):

        blurb = """
        Unstructured datasets are different to structured datasets. They have different methods and properties.
        You can tell if it is an Unstructured dataset using `ds.content_type` or by `print(ds)`.
        Please see our documentation on using Structured or Unstructured dataset type respectively.
        """

        class DeferInCaseCall(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                raise AttributeError(
                    f"This is an Unstructured dataset. There is no such property `{name}`.\n{blurb}"
                )

            def __call__(self, *args, **kwargs):
                raise AttributeError(
                    f"This is an Unstructured dataset. There is no such method `{name}(...)`.\n{blurb}"
                )

        def wrapper(*args, **kwargs):
            return DeferInCaseCall(name)

        return wrapper()

    def download(
        self,
        # pass through
        destination_path: str,
        filter_path: Optional[str] = None,
        partitions: Optional[List[str]] = None,

        # required for filtering
        with_attachments=True,
        with_metadata=True,
        document_type=None
    ) -> List[str]:
        """
        Downloads the original dataset files from the data lake to
        local copy
        destination of your choice.

        The flatten parameter retains only the file name, and places
        the
        files in the directory specified, else the files will be
        downloaded
        matching the directory structure as housed on the data lake.

        The filter path and partitions parameters specify that only
        a subset
        of the S3 path should be downloaded.

        Parameters
        ----------
        :param destination_path: required. The path on the system,
        where the
            files should be saved. Must be a directory, if doesn't
            exist, will
            be created.

        :param str filter_path: Optional. If provided only a subpath
        matching
            the filter_path will be matched. This is less flexible
            than using
            the `partitions` parameter, so we recommend you pass in
            `partitions` instead. The `partitions` can deal with the
            partitions in the path being in any order,
            but filter_path relies
            on a fixed order of partitions that the user needs to
            know ahead
            of time.

            Example usage to get all paths that start with the
            `as_of_date`
            2020. Note this is a string comparison, not a datetime
            comparison.

            .. code-block:: python

                dataset.download(filter_path='as_of_date=2020')

        :param List[str] partitions: Optional. A list of filters (
        partitions)
            to apply to the file paths on S3.

            This allows the user to filter the files they want to
            read from
            before they  have to read any data. This will reduce the
            amount
            of redundant data that is transferred over the network and
            reduce the amount of memory required on the user's machine.

            For any dataset, the paths on S3 may contain
            partitions that are key-value pairs in the format
            `<key>=<value>`, for example in the path:

                s3://example/as_of_date=2020-01-01/country=US/file
                .extension

            there are the partitions:

            * `country=US`
            * `as_of_date=2020-01-01`.

            You can find the available list of partitions for a
            dataset by
            calling the dataset's `.partitions()` endpoint.

            You can specify a list of partitions you want to get
            data from by
            passing in a list in the format
            `<key><operator><value>`. Please
            note that you should not include any extra quotation
            marks around
            the value, so `as_of_date=2020-01-01` is valid but
            `as_of_date='2020-01-01'` is invalid.

            The supported operators are: `<=`, `<`, `=`, `>`, `>=` and
            `!=`.

            For a partition where the key is named `as_of_date`,
            the value
            is treated as a Python datetime object, so comparisons
            are done
            between dates. This means that the `>=` and `<=`
            operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only
            dates in
            January 2020:

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as
            string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.download(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So
            specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.download(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :return: the list of the files that were downloaded
        successfully. Any
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
                    './local/path/',
                    filter_path='as_of_date=2019-09-10/'
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
                  'StormEvents_details-ftp_v1.0_d1950_c20170120.csv
                  .gz',
                  'StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
                ]
        """

        def custom_filter(paths: List[str]) -> List[str]:
            if not with_attachments:
                # TODO: filter.
                pass

            if not with_metadata:
                # TODO: filter.
                pass

            if document_type:
                # TODO: filter.
                pass

            return paths

        return self._DatasetModel__download(
            destination_path=destination_path,
            # It makes no sense to flatten unstructured datasets as the file
            # names have no meaning (they are like body.html) so:
            # 1. The name clashes will end up with files overwriting each
            # other.
            # 2. The data only makes sense when grouped into a document=ID
            # folder and compared to a separate folder.
            flatten=False,
            filter_path=filter_path,
            partitions=partitions,
            custom_filter=custom_filter,
        )

    @property
    def documents(self):
        # return document_models?
        return self._client.session.get(
            dataset_urls.v2_unstructured_document.format(id=self.dataset_id)
        ).json()["data"]

    @property
    def attachments(self):
        raise NotImplemented()

    @property
    def sample_data(self):
        raise NotImplemented()

    def __repr__(self):
        return f'<Unstructured Dataset short_code={self.short_code}>'


    def __str__(self):
        separator = "-" * 80
        return f"UNSTRUCTURED DATASET \"{self.short_code}\""


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['dataset_id']
)(UnstructuredDatasetModel)
