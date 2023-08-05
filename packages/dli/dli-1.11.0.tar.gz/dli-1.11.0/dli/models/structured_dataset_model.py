#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import datetime
import http.client
import json
import logging
import textwrap
import uuid
import warnings
from typing import List, Optional
from urllib.parse import urljoin

import pandas
import pyarrow
from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import consumption_urls, dataset_urls
from dli.client.exceptions import DataframeStreamingException
from dli.models import log_public_functions_calls_using, SampleData
from dli.models.dictionary_model import DictionaryModel
from dli.models.dataset_model import DatasetModel
from pyarrow.lib import ArrowInvalid
from tabulate import tabulate
from urllib3.exceptions import ProtocolError  # noqa: I900

trace_logger = logging.getLogger('trace_logger')


class StructuredDatasetModel(DatasetModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs,)
        self.instances = self._client._InstancesCollection(dataset=self)
        self.fields_metadata = None

    @property
    def sample_data(self) -> SampleData:
        return SampleData(self)

    def dask_dataframe(
        self,
        # Parameters for reading from .parquet and .csv format files:
        partitions: Optional[List[str]] = None,
        # Parameters for reading from .parquet format files:
        columns=None,
        filters=None,
        categories=None,
        index=None,
        engine="auto",
        gather_statistics=None,
        split_row_groups=None,
        chunksize=None,
        # Parameters for reading from .csv format files:
        blocksize='default',
        lineterminator=None,
        compression=None,
        sample=256000,
        enforce=False,
        assume_missing=False,
        include_path_column=False,
        # Parameters for reading from .parquet and .csv formats:
        **kwargs
    ):
        """
        Read a dataset into a Dask DataFrame.

        WARNING: The dependency Pandas 1.0.4 has an issue reading parquet due
        to an pandas library mismatch. This was fixed in Pandas 1.0.5. We
        advise users to not use Pandas 1.0.4.

        Background on Dask:

        A Dask DataFrame can be used to compute a Pandas Dataframe. Dask has
        the advantage of being able to process data that would be too large
        to fit into memory in a single Pandas Dataframe. The use case is to
        read the files with Dask, apply operations such as filtering and
        sorting to the Dask Dataframe (which implements most of the Pandas
        API) and finally compute the result to a Pandas Dataframe. As you
        have already done the filtering in Dask, the resulting Pandas
        Dataframe will be smaller in memory than if you tried to do
        everything in a single Pandas Dataframe.

        * Memory:

            *   Like Spark, when low on RAM it can save intermediate results to a temp directory on disk. This means more data can be processed.
            *   Copies of data will be removed from RAM when they are written to disk. Dask has the advantage of being able to process data that would be too large to fit into memory in a single Pandas Dataframe. As you have done the filtering in Dask, the Pandas Dataframe will be smaller in memory than if you tried to do everything in a single Pandas Dataframe.
            *   Lazy evaluation - Data is processed only when it is needed (like Spark). This means that less data needs to be in memory at one time before processing begins, unlike Pandas.

        * Speed - Can use a local or a remote cluster to process data in parallel. A cluster of 3 nodes would in an ideal world be 3 times faster (but usually it will be less due to network transfer speed between nodes). A Jupyter Notebook plugin is available to visualise the cluster. It is possible to have the nodes on your:

            * Local laptop.
            * Remote laptops (so a group of laptops can share the load).
            * Kubernetes cluster.

        *	Schema mismatch - clear instructions are given to the user for solving schema type mismatch. However, this is not automatically resolved (unlike Spark) and requires the user to add a `dtype` parameter (explained in the example below). Unfortunatly out-of-the-box it uses the pyarrow engine (the same as Pandas) which does not automatically support additive schemas. For dealing with additive schemas, you can:

            1. Change your code to read one file at a time as a Dask DataFrame, then `concat` the DataFrames together. The `concat` behaviour is the same as Pandas and will merge the schemas.
            2. Or switch the `engine` parameter from `pyarrow` to `fastparquet` and install `pip install fastparquet python-snappy`. Note this is difficult to install on Windows 10.

        *	API stability - Supports the API for Pandas, however they promise more stability between versions so if Pandas change something in their API, the Dask API should not change.
        *	Community support - Enterprise support is available through Coiled.io which is run by the creators of Dask.

        You can use the SDK to get a dataset, and then use the `dask_dataframe` endpoint which will return a Dask task that is setup to read the data files directly from S3 without downloading the files to the local machine.

        Please install or upgrade the SDK using the command `pip install dli[dask]` so that all of the dask plugins are installed.

        This endpoint can read data files in the following file formats:

            * .parquet
            * .csv

        into a Dask.dataframe, one file per partition.  It selects the index among the sorted columns if any exist.

        Examples
        --------

        .. code-block:: python

            dataset.dask_dataframe()

        The Dask dataframe will calculate the tasks that need to be run, but
        it does not evaluate until you call an action on it. To run a full
        evaluation across the whole dataset and return a Pandas dataframe, run:

        .. code-block:: python

            dataset.dask_dataframe().compute()

        To run the evaluation and only return the first ten results:

        .. code-block:: python

            dataset.dask_dataframe().compute(10)

        An additional parameter needs to be added when you are reading from
        compressed .csv files, for example the .csv.gz format.

        .. code-block:: python

            dataset.dask_dataframe(compression='gzip')

        Some datasets have problems with the column types changing between
        different data files. Dask will stop with an error message that
        explains the types you should pass. For example, if the error message
        that looks like this:

        /*
        ValueError: Mismatched dtypes found in `pd.read_csv`/`pd.read_table`.

        +------------+---------+----------+
        | Column     | Found   | Expected |
        +------------+---------+----------+
        | STATE_FIPS | float64 | int64    |
        +------------+---------+----------+

        Usually this is due to dask's dtype inference failing, and
        *may* be fixed by specifying dtypes manually by adding:

        dtype={'STATE_FIPS': 'float64'}
        */

        then you should do as the message says and add the parameters, then
        re-run. In this case the fix would look like this:

        .. code-block:: python

            dataset.dask_dataframe(dtype = {'STATE_FIPS': 'float64'})


        You are able to provide extra parameters to this endpoint that will
        be used by dask.

        The following parameters are used to reading from
        .parquet and .csv format files:

        Parameters
        ----------
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

            The supported operators are: `<=`, `<`, `=`, `>`, `>=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.dask_dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])


        The following parameters are used to reading from
        .parquet format files:

        Parameters
        ----------
        columns : string, list or None (default)
            Field name(s) to read in as columns in the output. By default all
            non-index fields will be read (as determined by the pandas parquet
            metadata, if present). Provide a single field name instead of a list to
            read in the data as a Series.
        filters : Union[List[Tuple[str, str, Any]], List[List[Tuple[str, str, Any]]]]
            List of filters to apply, like ``[[('x', '=', 0), ...], ...]``. This
            implements partition-level (hive) filtering only, i.e., to prevent the
            loading of some row-groups and/or files.

            Predicates can be expressed in disjunctive normal form (DNF). This means
            that the innermost tuple describes a single column predicate. These
            inner predicates are combined with an AND conjunction into a larger
            predicate. The outer-most list then combines all of the combined
            filters with an OR disjunction.

            Predicates can also be expressed as a List[Tuple]. These are evaluated
            as an AND conjunction. To express OR in predictates, one must use the
            (preferred) List[List[Tuple]] notation.
        index : string, list, False or None (default)
            Field name(s) to use as the output frame index. By default will be
            inferred from the pandas parquet file metadata (if present). Use False
            to read all fields as columns.
        categories : list, dict or None
            For any fields listed here, if the parquet encoding is Dictionary,
            the column will be created with dtype category. Use only if it is
            guaranteed that the column is encoded as dictionary in all row-groups.
            If a list, assumes up to 2**16-1 labels; if a dict, specify the number
            of labels expected; if None, will load categories automatically for
            data written by dask/fastparquet, not otherwise.
        engine : {'auto', 'fastparquet', 'pyarrow'}, default 'auto'
            Parquet reader library to use. If only one library is installed, it
            will use that one; if both, it will use 'fastparquet'
        gather_statistics : bool or None (default).
            Gather the statistics for each dataset partition. By default,
            this will only be done if the _metadata file is available. Otherwise,
            statistics will only be gathered if True, because the footer of
            every file will be parsed (which is very slow on some systems).
        split_row_groups : bool or int
            Default is True if a _metadata file is available or if
            the dataset is composed of a single file (otherwise defult is False).
            If True, then each output dataframe partition will correspond to a single
            parquet-file row-group. If False, each partition will correspond to a
            complete file.  If a positive integer value is given, each dataframe
            partition will correspond to that number of parquet row-groups (or fewer).
            Only the "pyarrow" engine supports this argument.
        chunksize : int, str
            The target task partition size.  If set, consecutive row-groups
            from the same file will be aggregated into the same output
            partition until the aggregate size reaches this value.
        **kwargs: dict (of dicts)
            Passthrough key-word arguments for read backend.
            The top-level keys correspond to the appropriate operation type, and
            the second level corresponds to the kwargs that will be passed on to
            the underlying `pyarrow` or `fastparquet` function.
            Supported top-level keys: 'dataset' (for opening a `pyarrow` dataset),
            'file' (for opening a `fastparquet` `ParquetFile`), 'read' (for the
            backend read function), 'arrow_to_pandas' (for controlling the arguments
            passed to convert from a `pyarrow.Table.to_pandas()`)

        The following parameters are used to reading from
        .csv format files:

        Parameters
        ----------

        blocksize:str, int or None, optional
            Number of bytes by which to cut up larger files. Default value is
            computed based on available physical memory and the number of
            cores, up to a maximum of 64MB. Can be a number like 64000000` or
            a string like ``"64MB". If None, a single block is used for each
            file.
        lineterminator:str (length 1), optional
            Character to break file into lines. Only valid with C parser.
        compression: {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default
            ‘infer’
            For on-the-fly decompression of on-disk data.
        sample:int, optional
            Number of bytes to use when determining dtypes
        enforce:bool
        assume_missing:bool, optional
            If True, all integer columns that aren’t specified in dtype are
            assumed to contain missing values, and are converted to floats.
            Default is False.
        include_path_column:bool or str, optional
            Whether or not to include the path to each particular file. If
            True a new column is added to the dataframe called path. If str,
            sets new column name. Default is False.
        **kwargs
            Extra keyword arguments. See the docstring for pandas.read_csv()
            for more information on available keyword arguments.
        """
        try:
            import dask.dataframe as dd
        except ImportError:
            raise RuntimeError(
                'Before you can use Dask it must be installed into '
                'your virtual environment.'
                '\nNote: If you are running you code in a Jupyter Notebook, '
                'then before installing you will need to quit the '
                '`jupyter notebook` process that is running on the command '
                'line and start it again so that your notebooks see the '
                'version of Dask you have now installed.'
                '\nPlease install dask using one of the following options:'
                '\n1. Run `pip install dli[dask]` to install this SDK '
                'with a compatible version of dask.'
                '\n2. Run `pip install dask[dataframe]` to install the latest '
                'version of dask (which may be untested with this version '
                'of the SDK).'
            )

        self._check_access()

        start = datetime.datetime.now()
        request_id = str(uuid.uuid4())

        paths = self.list(
            request_id=request_id,
            partitions=partitions
        )

        storage_options = {
            'client_kwargs': {
                'endpoint_url': self._DatasetModel__endpoint_url(),
            },
            'key': self._client.session.auth_key,
            'secret': 'noop',
        }

        data_format = self.data_format.lower()

        trace_logger.info(
            'dask_dataframe endpoint:'
            f"\nrequest_id: '{request_id}'"
            f"\nendpoint_url: '{self._DatasetModel__endpoint_url()}'"
            f"\ndata_format: '{data_format}'"
            '\nlisting paths elapsed time: '
            f"'{datetime.datetime.now() - start}'"
        )

        if data_format == 'parquet':
            return dd.read_parquet(
                path=paths,
                columns=columns,
                filters=filters,
                categories=categories,
                index=index,
                storage_options=storage_options,
                engine=engine,
                gather_statistics=gather_statistics,
                split_row_groups=split_row_groups,
                chunksize=chunksize,
                **kwargs
            )
        elif data_format == 'csv':
            return dd.read_csv(
                urlpath=paths,
                blocksize=blocksize,
                lineterminator=lineterminator,
                compression=compression,
                sample=sample,
                enforce=enforce,
                assume_missing=assume_missing,
                storage_options=storage_options,
                include_path_column=include_path_column,
                **kwargs
            )
        else:
            print(
                f"Sorry, the dataset is in the format '{data_format}'. This "
                'endpoint is only setup to handle parquet and csv.'
            )
            return None

    def dataframe(
        self,
        nrows: Optional[int] = None,
        partitions: Optional[List[str]] = None,
        raise_: bool = True,
        use_compression: bool = False
    ) -> pandas.DataFrame:
        """
        Return the data from the files in the latest instance of the dataset
        as a pandas DataFrame.

        WARNING: The dependency Pandas 1.0.4 has an issue reading parquet due
        to an pandas library mismatch. This was fixed in Pandas 1.0.5.

        We currently support .csv and .parquet as our data file formats. The
        data files in the latest instance could all be .csv format or all be
        .parquet format. If there is a mix of .csv and .parquet or some other
        file format then we will not be able to parse the data and will
        return an error message.

        :param int nrows: Optional. The max number of rows to return.
            We use the nrows parameter to limit the amount of rows that are
            returned, otherwise for very large dataset it will take a long time
            or you could run out of RAM on your machine!
            If you want all of the rows, then leave this parameter set to the
            default None.

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

            The supported operators are: `<=`, `<`, `=`, `>`, `>=`.

            For a partition where the key is named `as_of_date`, the value
            is treated as a Python datetime object, so comparisons are done
            between dates. This means that the `>=` and `<=` operators can
            be used to get data in a date range where more than one
            `as_of_date` exists. For example, to get data from only dates in
            January 2020:

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'as_of_date<=2020-01-31',
                ])

            Other key names will have their values treated as string, so the
            operators will perform Python string comparisons.

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'country=US'
                ])

            A list of partitions is applied as a logical AND. So specifying
            `as_of_date` and `country` will match only those paths that
            match both `as_of_date` AND `country`.

            .. code-block:: python

                dataset.dataframe(partitions=[
                    'as_of_date>=2020-01-01',
                    'country=US',
                ])

        :param bool raise_: Optional. Raise exception if the dataframe stream
            stopped prematurely

        :param use_compression: Optional. Whether the response from the
        backend should use compression. Setting to false should result
        in a faster initial response before the streaming begins.

        :example:

            Basic usage:

            .. code-block:: python

                    dataframe = dataset.dataframe()

        :example:

            Dataframe filtered by partition with nrows (partitions can be
            fetched using the `dataset.partitions()` endpoint:

            .. code-block:: python

                    dataframe = dataset.dataframe(
                        nrows=1000,
                        partitions=["as_of_date=2017-03-07"]
                    )
        """

        self._check_access()

        params = {}

        if nrows is not None:
            params['filter[nrows]'] = nrows

        if partitions is not None:
            params['filter[partitions]'] = partitions

        dataframe_url = urljoin(
            self._client._environment.consumption,
            consumption_urls.consumption_dataframe.format(id=self.id)
        )

        headers = {}
        if not use_compression:
            headers['Accept-Encoding'] = 'identity;q=0'

        response = self._client.session.get(
            dataframe_url, stream=True,
            params=params,
            headers=headers,
        )

        try:
            # native_file only reads until end of dataframe
            # the rest of the stream has to be read from response raw.
            native_file = pyarrow.PythonFile(response.raw, mode='rb')

            # Now native_file "contains the complete stream as an in-memory
            # byte buffer. An important point is that if the input source
            # supports zero-copy reads (e.g. like a memory map,
            # or pyarrow.BufferReader), then the returned batches are also
            # zero-copy and do not allocate any new memory on read."
            reader = pyarrow.ipc.open_stream(native_file)

            dataframe = reader.read_pandas()
        except (
                ArrowInvalid,
                http.client.IncompleteRead,
                ProtocolError
        ) as ex:

            message = 'Sorry, the dataframe you are trying to read is too ' \
                      'large to fit into memory. Please consider one of ' \
                      'these alternatives:' \
                      '\n\n1. Run the same code on a machine that has more ' \
                      'RAM, for example a Jupyter Notebook hosted on an ' \
                      'AWS environment.' \
                      '\n2. Use a big data tool such as Spark, Dask or ' \
                      'similar to read the data via our S3 proxy. Unlike ' \
                      'Pandas, these big data tools are able to apply some ' \
                      'operations such as filtering without having to hold ' \
                      'all of the data into memory. See ' \
                      'https://supportlibrary.ihsmarkit.com/display/DLSL/' \
                      'Using+the+S3+Proxy+with+Big+Data+tooling' \
                      f'\n\nOriginal exception: {ex}'

            raise ArrowInvalid(message) from ex

        # The pyarrow buffered stream reader stops once it
        # reaches the end of the IPC message. Afterwards we
        # get the rest of the data which contains the summary
        # of what we've downloaded including an error message.
        last_packet = response.raw.read()
        summary = json.loads(last_packet)

        if summary['status'] >= 400:
            exception = DataframeStreamingException(
                summary, dataframe_url, response=response,
            )

            # Optionally ignore bad data
            if raise_:
                raise exception
            else:
                warnings.warn(
                    str(exception),
                    UserWarning
                )

        return dataframe

    def contents(self):
        """
        Print IDs for all the instances in this dataset.

        Example output:

            INSTANCE 1111aaa-11aa-11aa-11aa-111111aaaaaa
        """
        for p in self.instances.all():
            print(str(p))

    def dictionary(self) -> List[dict]:
        """
        List of dictionaries for each field in the dataset's dictionary as
        returned by the Catalogue.

        If there are multiple historical values for the dataset's `dictionary`
        in the Catalogue, then you will see more than one item in the list,
        otherwise there will only be a single item in the list containing a
        dictionary of the current fields.

        Field names may include:

        * name
        * type
        * nullable
        * description
        * comment
        * validation
        * short_name
        * sample_value
        * is_derived
        * metadata

        Example usage:

        .. code:: python

            dataset = client.datasets.get('example-dataset-short-code')
            print(dataset.dictionary())

        Example output:

        .. code:: python

            [
              {
                'name': 'some-name',
                'type': 'String',
                'nullable': True,
                'description': 'some-description'
              }
            ]

        :return: List of each field in the dataset.
        """

        if self.fields_metadata is None:
            # we have to do two calls
            # to get the latest dictionary id for the dataset
            try:
                response = self._client.session.get(
                    dataset_urls.dictionary_by_dataset_lastest.format(id=self.id)
                ).json()
            except:
                print("There is no current dictionary available.")
                return []

            # followed by the fields for the dictionary...

            self.fields_metadata = DictionaryModel(
                {'id': response["data"]["id"], 'attributes': {}},
                client=self._client
            ).fields

            def subdict(field_dict):
                return {k: v for k, v in field_dict.items()}

            self.fields_metadata = list(
                map(lambda field: subdict(field),
                    self.fields_metadata)
            )

        return self.fields_metadata

    def info(self):
        fields = self.dictionary()

        df = pandas.DataFrame(fields)
        if df.shape[1] > 0:
            df["type"] = df.apply(
                lambda row: row["type"] + (" (Nullable)" if row["nullable"] else ""),
                axis=1)
            df = df[["name", "type"]]

            print(tabulate(df, showindex=False, headers=df.columns))
        else:
            print("No columns/info available.")

    def __repr__(self):
        return f'<Structured Dataset short_code={self.short_code}>'

    def __str__(self):
        separator = "-" * 80
        splits = "\n".join(textwrap.wrap(self.description))

        return f"\nDATASET \"{self.short_code}\" [{self.data_format}]\n" \
               f">> Shortcode: {self.short_code}\n"\
               f">> Available Date Range: {self.first_datafile_at} to {self.last_datafile_at}\n" \
               f">> ID: {self.id}\n" \
               f">> Published: {self.publishing_frequency} by {self.organisation_name}\n" \
               f">> Accessible: {self.has_access}\n" \
               f"\n" \
               f"{splits}\n" \
               f"{separator}"


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['dataset_id']
)(StructuredDatasetModel)
