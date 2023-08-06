from ..authorization.authorization_api import AuthorizationApi
from ..common.common_funcs import CommonFuncs
import requests
import json
import logging
import pandas as pd
import datetime
from pyTSI.variables.Variable import NumericVariable


class QueryApi:
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

    def get_events(self, variables, start, end, filter_tsx=None,
                   use_warm_store=False):
        """
        Get the raw events for the given Time Series Variables

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#getevents

        Parameters
        ----------
        variables : dict [ TimeSeriesInstance, NumericVariables ]
                    Variables whose events should be retrieved for the given
                    time series instances
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        # Input data sanity check
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        for ts, ts_vars in variables.items():
            for ts_var in ts_vars:
                if not isinstance(ts_var, NumericVariable):
                    raise ValueError(f'Cannot operate on non-numeric var {ts_var} for {ts}')

        # The empty DataFrame that we'll fill with data from the TSI
        df = None
        for ts, ts_vars in variables.items():
            # authorization_token = self.authorization_api.get_token()
            logging.info(f'Retrieving {ts_vars} for time series {ts}')

            # TODO: Setting the type as I do below will crash
            payload = {
                'getEvents': {
                    "timeSeriesId": ts.series_id,
                    "searchSpan": {"from": f'{start.isoformat()}Z',
                                   "to": f'{end.isoformat()}Z'},
                    "filter": filter_tsx,
                    "take": 250000,
                    "projectedProperties": [{'name': v.var_name,
                                             'type': v.var_value_tsx.split('.')[-1]}
                                            for v in ts_vars]
                }
            }

            # Retrieve the DataFrame for the Time Series vars,
            # then merge into the final one (if needed)
            ts_df = self._get_data(payload=payload, use_warm_store=use_warm_store)
            ts_df.columns = pd.MultiIndex.from_product([ts.series_id, ts_df.columns],
                                                       names=['Series ID', 'Variable'])
            if df is None:
                df = ts_df
            else:
                logging.warning('Merging different DataFrames not yet thoroughly tested')
                df = pd.merge_asof(df, ts_df, left_index=True, right_index=True,
                                   direction='nearest', tolerance=pd.Timedelta(seconds=30))

        return df

    def get_series(self, variables, start, end, filter_tsx=None,
                   use_warm_store=False):
        """
        Retrieve time series of calculated variable values from events

        This method will return the series data for the given timespan.
        This method is different from `get_events` because `get_events`
        can only retrieve events as sent to the TSI, whereas this method
        will also return computed series (the log of a series of events
        or two series summed).

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#getseries

        Parameters
        ----------
        variables : dict [ TimeSeriesInstance, NumericVariables ]
                    Variables whose events should be retrieved for the given
                    time series instances
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        # The empty DataFrame that we'll fill with data from the TSI
        df = None
        for ts, ts_vars in variables.items():
            # authorization_token = self.authorization_api.get_token()
            logging.info(f'Retrieving {ts_vars} for time series {ts}')

            payload = {
                'getSeries': {
                    'timeSeriesId': ts.series_id,
                    'searchSpan': {"from": f'{start.isoformat()}Z',
                                   "to": f'{end.isoformat()}Z'},
                    'filter': filter_tsx,
                    'take': 250000,
                    "projectedVariables": [ts_var.var_name for ts_var in ts_vars],
                    'inlineVariables': {var_name: body
                                        for ts_var in ts_vars
                                        for var_name, body in ts_var.as_dict().items()}
                }
            }

            # Retrieve the DataFrame for the Time Series vars,
            # then merge into the final one (if needed)
            ts_df = self._get_data(payload=payload, use_warm_store=use_warm_store)
            ts_df.columns = pd.MultiIndex.from_product([ts.series_id, ts_df.columns],
                                                       names=['Series ID', 'Variable'])
            if df is None:
                df = ts_df
            else:
                logging.warning('Merging different DataFrames not yet thoroughly tested')
                df = pd.merge_asof(df, ts_df, left_index=True, right_index=True,
                                   direction='nearest', tolerance=pd.Timedelta(seconds=30))

        return df

    def aggregate_series(self, variables, start, end, interval,
                         filter_tsx=None, use_warm_store=False):
        """
        Retrieve an aggregation of time series

        This method will return the series data for the given timespan.
        This method is different from `get_events` because `get_events`
        can only retrieve events as sent to the TSI, whereas this method
        will also return computed series (the log of a series of events
        or two series summed).

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#aggregateseries

        Parameters
        ----------
        variables : dict [ TimeSeriesInstance, NumericVariables ]
                    Variables whose events should be retrieved for the given
                    time series instances
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        interval : str
                   Interval size between outputs, given in ISO-8601 format.
                   For example: `PT1S` corresponds to an interval of 1 second
                   and `PT1M` corresponds to an interval of 1 minute.
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        # The empty DataFrame that we'll fill with data from the TSI
        df = None
        for ts, ts_vars in variables.items():
            # authorization_token = self.authorization_api.get_token()
            logging.info(f'Retrieving {ts_vars} for time series {ts}')

            payload = {
                'aggregateSeries': {
                    'timeSeriesId': ts.series_id,
                    'searchSpan': {"from": f'{start.isoformat()}Z',
                                   "to": f'{end.isoformat()}Z'},
                    'filter': filter_tsx,
                    "projectedVariables": [ts_var.var_name for ts_var in ts_vars],
                    'inlineVariables': {var_name: body
                                        for ts_var in ts_vars
                                        for var_name, body in ts_var.as_dict().items()},
                    'take': 250000,
                    'interval': interval
                }
            }

            # Retrieve the DataFrame for the Time Series vars,
            # then merge into the final one (if needed)
            ts_df = self._get_data(payload=payload, use_warm_store=use_warm_store)
            ts_df.columns = pd.MultiIndex.from_product([ts.series_id, ts_df.columns],
                                                       names=['Series ID', 'Variable'])
            if df is None:
                df = ts_df
            else:
                logging.warning('Merging different DataFrames not yet thoroughly tested')
                df = pd.merge_asof(df, ts_df, left_index=True, right_index=True,
                                   direction='nearest', tolerance=pd.Timedelta(seconds=30))

        return df

    def _get_data(self, payload, use_warm_store):
        """
        Helper method used for performing the query to the TSI

        This method will perform the query with the given payload
        and handle low-level tasks like pagination & converting
        the information returned by the server in JSON format into
        a Pandas DataFrame.

        Parameters
        ----------
        payload : dict
                  Dictionary with the request payload
        use_warm_store : bool
                         Flag indicating whether the warm store should
                         be used for the query.

        Returns
        -------
        pd.DataFrame
                    The information provided by the TSI, in DataFrame format.
        """
        # Query params
        url = "https://" + self.environmentId + ".env.timeseries.azure.com/timeseries/query?"
        querystring = self.common_funcs.get_query_string(use_warm_store=use_warm_store)
        authorization_token = self.authorization_api.get_token()
        headers = {
            "x-ms-client-application-name": self._applicationName,
            "Authorization": authorization_token,
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        }

        # Perform the query & handle paging
        try:
            r = requests.request("POST",
                                 url,
                                 data=json.dumps(payload),
                                 headers=headers,
                                 params=querystring)
            r.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            logging.error("pyTSI: The request to the TSI API timed out.")
            raise
        except requests.exceptions.HTTPError:
            logging.error("pyTSI: The request to the TSI API returned "
                          "an unsuccessful status code.")
            raise

        # Construct the dictionary we'll use for the DataFrame
        json_data = r.json()
        df_data = {'timestamp': json_data['timestamps']}
        for p in json_data['properties']:
            df_data[p['name']] = p['values']

        # Handle the pagination token, untested
        while 'continuationToken' in json_data.keys():
            headers['x-ms-continuation'] = json_data['continuationToken']
            r = requests.request('POST',
                                 url,
                                 data=json.dumps(payload),
                                 headers=headers,
                                 params=querystring)
            r.raise_for_status()

            if r.text:
                json_data = r.json()
                df_data['timestamps'].extend(json_data['timestamps'])
                for p in json_data['properties']:
                    df_data[p['name']].extend(p['values'])

        # Construct the DataFrame from the info we just received
        df = pd.DataFrame.from_dict(df_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.set_index('timestamp')
