import os
from .authorization.authorization_api import AuthorizationApi
from .common.common_funcs import CommonFuncs
from .environment.environment_api import EnvironmentApi
from .hierarchies.hierarchies_api import HierarchiesApi
from .instances.instances_api import InstancesApi
from .query.query_api import QueryApi
from .types.types_api import TypesApi
from .instances.TimeSeriesInstance import TimeSeriesInstance
from .types.Type import Type
from .variables.Variable import variable_helper


class TSIClient:
    """TSIClient. Holds methods to interact with an Azure TSI environment.

    This class can be used to retrieve time series data from Azure TSI. Data
    is retrieved in form of a pandas dataframe, which allows subsequent analysis
    by data analysts, data scientists and developers.

    It can be instantiated either by arguments or by environment variables (if arguments
    are specified, they take precedence even when environment variables are set).

    Args:
        environment_name (str): The name of the Azure TSI environment.
        client_id (str): The client id of the service principal used to authenticate with Azure TSI.
        client_secret (str): The client secret of the service principal used to authenticate with Azure TSI.
        tenant_id (str): The tenant id of the service principal used to authenticate with Azure TSI.
        application_name (str): The name can be an arbitrary string. For informational purpose.
        api_version (str): The TSI api version (optional, allowed values: '2018-11-01-preview' and '2020-07-31').
            Defaults to '2020-07-31'.

    Examples:
        The TSIClient is the entry point to the SDK. You can instantiate it like this:

            >>> from pyTSI import TSIClient as tsi
            >>> client = tsi.TSIClient(
            ...     environment="<your-tsi-env-name>",
            ...     client_id="<your-client-id>",
            ...     client_secret="<your-client-secret>",
            ...     tenant_id="<your-tenant-id>",
            ...     applicationName="<your-app-name>">,
            ...     api_version="2020-07-31"
            ... )

        You might find it useful to specify environment variables to instantiate the TSIClient.
        To do so, you need to set the following environment variables:

        * ``TSICLIENT_APPLICATION_NAME``
        * ``TSICLIENT_ENVIRONMENT_NAME``
        * ``TSICLIENT_CLIENT_ID``
        * ``TSICLIENT_CLIENT_SECRET``
        * ``TSICLIENT_TENANT_ID``
        * ``TSI_API_VERSION``
        
        Now you can instantiate the TSIClient without passing any arguments:

            >>> from pyTSI import TSIClient as tsi
            >>> client = tsi.TSIClient()
    """

    def __init__(
            self,
            environment_name=None,
            client_id=None,
            client_secret=None,
            application_name=None,
            tenant_id=None,
            api_version=None
    ):
        self._applicationName = application_name if application_name is not None else os.environ[
            "TSICLIENT_APPLICATION_NAME"]
        self._environmentName = environment_name if environment_name is not None else os.environ[
            "TSICLIENT_ENVIRONMENT_NAME"]
        self._client_id = client_id if client_id is not None else os.environ["TSICLIENT_CLIENT_ID"]
        self._client_secret = client_secret if client_secret is not None else os.environ["TSICLIENT_CLIENT_SECRET"]
        self._tenant_id = tenant_id if tenant_id is not None else os.environ["TSICLIENT_TENANT_ID"]

        allowed_api_versions = ["2020-07-31", "2018-11-01-preview"]
        if api_version in allowed_api_versions:
            self._apiVersion = api_version
        elif "TSI_API_VERSION" in os.environ:
            if os.environ["TSI_API_VERSION"] in allowed_api_versions:
                self._apiVersion = os.environ["TSI_API_VERSION"]
        else:
            self._apiVersion = "2020-07-31"

        self.authorization = AuthorizationApi(
            client_id=self._client_id,
            client_secret=self._client_secret,
            tenant_id=self._tenant_id,
            api_version=self._apiVersion
        )

        self.common_funcs = CommonFuncs(
            api_version=self._apiVersion
        )

        self.environment = EnvironmentApi(
            application_name=self._applicationName,
            environment=self._environmentName,
            authorization_api=self.authorization,
            common_funcs=self.common_funcs
        )
        self._environmentId = self.environment.getEnvironmentId()

        self._instances_api = InstancesApi(
            application_name=self._applicationName,
            environment_id=self._environmentId,
            authorization_api=self.authorization,
            common_funcs=self.common_funcs
        )

        self._types_api = TypesApi(
            application_name=self._applicationName,
            environment_id=self._environmentId,
            authorization_api=self.authorization,
            common_funcs=self.common_funcs
        )

        self.query = QueryApi(
            application_name=self._applicationName,
            environment_id=self._environmentId,
            authorization_api=self.authorization,
            common_funcs=self.common_funcs
        )

        self.hierarchies = HierarchiesApi(
            application_name=self._applicationName,
            environment_id=self._environmentId,
            authorization_api=self.authorization,
            common_funcs=self.common_funcs
        )

        # Lazy-loaded vars
        self.__time_series = None
        self.__types = None

    @property
    def types(self):
        """
        List of Type objects
        """
        if self.__types is None:
            self.__types = []
            for t in self._types_api.getTypes()['types']:
                self.__types.append(Type(type_id=t['id'],
                                         type_name=t['name'],
                                         type_description=t.get('description'),
                                         type_vars=[variable_helper(k, v)
                                                    for k, v in t['variables'].items()]))

        return self.__types

    @property
    def time_series(self):
        if self.__time_series is None:
            self.__time_series = [TimeSeriesInstance(client=self,
                                                     series_type=[t for t in self.types
                                                                  if ts['typeId'] == t.type_id][0],
                                                     series_id=ts['timeSeriesId'],
                                                     series_name=ts.get('name'),
                                                     series_description=ts.get('description'))
                                  for ts in self._instances_api.getInstances()['instances']]

        return self.__time_series
