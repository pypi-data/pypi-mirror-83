# pyTSI

pyTSI is a Python SDK for Microsoft Azure time series insights. 
It provides methods to conveniently retrieve your data and is designed
for analysts, data scientists and developers working with time series 
data in Azure TSI.

## Documentation
- Azure time series REST APIs: <https://docs.microsoft.com/en-us/rest/api/time-series-insights/>

## Quickstart
Instantiate the TSIClient to query your TSI environment. Use the credentials 
from your service principal in Azure that has access to the TSI environment 
(you can also use environment variables to instantiate the pyTSI or provide 
a specific TSI API version, check the documentation).

```python
from pyTSI import TSIClient as tsi

client = tsi.TSIClient(
    enviroment='<your-tsi-env-name>',
    client_id='<your-client-id>',
    client_secret='<your-client-secret>',
    tenant_id='<your-tenant-id>',
    application_name='<your-app-name>')

# List the instances in the TSI, also list their types
# and variables.
for instance in client.time_series:
    print(f'\t{instance}')
    print('\tInstance type description:')
    print(f'\t\t{instance.series_type}')
    print('\t\tType vars:')
    for v in instance.series_type.type_vars:
        print(f'\t\t\t{v}')
```

You can now query each instance

You can query your timeseries data by timeseries id, timeseries name or timeseries 
description. The Microsoft TSI apis support aggregation, so you can specify a 
sampling freqency and an aggregation method. Refer to the documentation for detailed 
information.

```python
import datetime

# Define the start & end times for the series that we want to retrieve
t0 = datetime.datetime(year=2020, month=10, day=22, hour=10, minute=53, second=00,
                       tzinfo=datetime.timezone.utc)
t1 = datetime.datetime(year=2020, month=10, day=22, hour=11, minute=53, second=30,
                       tzinfo=datetime.timezone.utc)

# Choose a single TimeSeries
ts = client.time_series[0]

# Get raw event data
raw_data = client.query.get_events({ts: [v for v in ts.series_type.type_vars
                                         if v.var_name in ('temperature', 'humidity')]},
                                   t0, t1)
# Get series data for raw events & composed variables
series_data = client.query.get_series({ts: [v for v in ts.series_type.type_vars
                                         if v.var_name in ('temperature', 'humidity', 'series_sum')]},
                                   t0, t1)
# Aggregate series
selected_vars = [v for v in ts.series_type.type_vars if v.var_name in ('temperature', 'EventCount')]
aggregated_data = client.query.aggregate_series({ts: selected_vars}, t0, t1, 'PT1M')

# Retrieve aggregates for two different time series
ts2 = client.time_series[1]
selected_vars2 = [v for v in ts2.series_type.type_vars if v.var_name in ('humidity', 'EventCount')]
aggregated_data = client.query.aggregate_series({ts: selected_vars, ts2: selected_vars2}, t0, t1, 'PT1M')
```

Each of these functions return a Multi-index DataFrame, where the first index corresponds to the
Time Series ID whereas the second index corresponds to the variable name.

## Contributing
Contributions are welcome. See the [developer reference](docs/source/developer.rst) 
for details.

## License
pyTSI is licensed under the MIT license. See [LICENSE](LICENSE.txt) file for details.
