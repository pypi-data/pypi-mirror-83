import json
import requests


class CommonFuncs:
    def __init__(self, api_version):
        self.api_version = api_version

    def get_query_string(self, use_warm_store=None):
        """Creates the querystring for an api request.
        
        Can be used in all api requests in pyTSI.

        Args:
            use_warm_store (bool): A boolean to indicate the storeType. Defaults to None,
                in which case no storeType param is included in the querystring.

        Returns:
            dict: The querystring with the api-version and optionally the storeType.
        """

        if use_warm_store is None:
            return {"api-version": self.api_version}

        else:
            return {
                "api-version": self.api_version,
                "storeType": "WarmStore" if use_warm_store else "ColdStore"
            }

    def _updateTimeSeries(self, payload, timeseries, applicationName, environmentId, authorizationToken):
        """Writes instances to the TSI environment.

        Args:
            payload (str): A json-serializable payload that is posted to the TSI environment.
                The format of the payload is specified in the Azure TSI documentation.

        Returns:
            dict: The response of the TSI api call.
        """

        url = "https://{environmentId}.env.timeseries.azure.com/timeseries/{timeseries}/$batch".format(
            environmentId=environmentId, timeseries=timeseries)

        querystring = self.get_query_string()

        headers = {
            'x-ms-client-application-name': applicationName,
            'Authorization': authorizationToken,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)

        if response.text:
            jsonResponse = json.loads(response.text)

        return jsonResponse
