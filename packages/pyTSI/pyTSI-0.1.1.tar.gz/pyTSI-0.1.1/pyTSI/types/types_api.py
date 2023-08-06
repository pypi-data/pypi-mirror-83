from ..authorization.authorization_api import AuthorizationApi
from ..common.common_funcs import CommonFuncs
import requests
import logging


class TypesApi:
    def __init__(
            self,
            application_name: str,
            environment_id: str,
            authorization_api: AuthorizationApi,
            common_funcs: CommonFuncs
    ):

        self.authorization_api = authorization_api
        self._applicationName = application_name
        self.environmentId = environment_id
        self.common_funcs = common_funcs

    def getTypes(self):
        """Gets all types from the specified TSI environment.

        Returns:
            dict: The types in form of the response from the TSI api call.
            Contains id, name, description and variables per type.
            
        Example:
            >>> from pyTSI import TSIClient as tsi
            >>> client = tsi.TSIClient()
            >>> types = client._types_api.getTypes()
        """

        url = "https://" + self.environmentId + ".env.timeseries.azure.com/timeseries/types"
        payload = ""
        headers = {
            'x-ms-client-application-name': self._applicationName,
            'Authorization': self.authorization_api.get_token(),
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        try:
            response = requests.request(
                "GET",
                url,
                data=payload,
                headers=headers,
                params=self.common_funcs.get_query_string(),
                timeout=10
            )
            response.raise_for_status()

        except requests.exceptions.ConnectTimeout:
            logging.error("pyTSI: The request to the TSI api timed out.")
            raise
        except requests.exceptions.HTTPError:
            logging.error("pyTSI: The request to the TSI api returned an unsuccessfull status code.")
            raise

        return response.json()
