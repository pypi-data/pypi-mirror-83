from ..authorization.authorization_api import AuthorizationApi
from ..common.common_funcs import CommonFuncs
import json
import requests


class InstancesApi:
    def __init__(
            self,
            application_name: str,
            environment_id: str,
            authorization_api: AuthorizationApi,
            common_funcs: CommonFuncs,
    ):
        self._applicationName = application_name
        self.environmentId = environment_id
        self.authorization_api = authorization_api
        self.common_funcs = common_funcs
        self.base_url = f"https://{self.environmentId}.env.timeseries.azure.com/timeseries/"

    def getInstances(self):
        """Gets all instances (timeseries) from the specified TSI environment.

        Returns:
            dict: The instances in form of the response from the TSI api call.
            Contains typeId, timeSeriesId, name, description, hierarchyIds and instanceFields per instance.

        Example:
            >>> from pyTSI import pyTSI as tsi
            >>> client = tsi.pyTSI()
            >>> instances = client._instances_api.getInstances()
        """

        authorizationToken = self.authorization_api.get_token()

        querystring = self.common_funcs.get_query_string()
        payload = ""

        headers = {
            'x-ms-client-application-name': self._applicationName,
            'Authorization': authorizationToken,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", f'{self.base_url}/instances/', data=payload,
                                    headers=headers, params=querystring)

        json_response = response.json()
        result = response.json()

        while len(json_response['instances']) > 999 and 'continuationToken' in list(json_response.keys()):
            headers = {
                'x-ms-client-application-name': self._applicationName,
                'Authorization': authorizationToken,
                'x-ms-continuation': json_response['continuationToken'],
                'Content-Type': "application/json",
                'cache-control': "no-cache"
            }
            response = requests.request("GET", f'{self.base_url}/instances/', data=payload,
                                        headers=headers, params=querystring)
            json_response = response.json()

            result['instances'].extend(json_response['instances'])
        return result

    def delete_instances_by_id(self, instances):
        """ instances are the list of the timeseries ids to delete"""
        payload = {"delete": {"timeSeriesIds": [i for i in instances if i is not None]}}

        headers = {
            'x-ms-client-application-name': self._applicationName,
            'Authorization': self.authorization_api.get_token(),
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", f'{self.base_url}/instances/$batch',
                                    data=json.dumps(payload), headers=headers,
                                    params=self.common_funcs.get_query_string())

        # Raise an exception if status code OK was not returned
        response.raise_for_status()
