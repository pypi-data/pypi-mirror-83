# mbtav3
mbtav3 is an asynchronous python wrapper for the mbta v3 api intended for use with Home Assistant.

### Installation
`$ pip install mbtav3`

## Set your environment variable for MBTA API Key
1. Register a developer account with the MBTA [Dev Portal Link](https://api-v3.mbta.com/)
2. Set your env var: `MBTA_API_KEY = my_mbta_api_key`, or alternatively pass in the API key from somewhere else, like a Home Assistant Configuration as an argument of Auth.

## Usage

#### Get Predictions
```
from mbtav3.mbta import MBTA
from mbtav3.auth import Auth
from mbtav3.utils import Page, Sort, SortOrder, Filter, build_params
import aiohttp

session = aiohttp.ClientSession()
mbta = MBTA(Auth(session))
page = Page(0, 3)
order = SortOrder('asc')
sort = Sort('departure_time', order)
stopFilter = Filter('stop','place-sull')
typeFilter = Filter('route_type', 1)

params = build_params(stopFilter, typeFilter, page=page, sort=sort)

preds = await mbta.listPredictions(params)

print(preds);
```

`{'data': [{'attributes': {'arrival_time': '2020-10-21T07:57:37-04:00', 'departure_time': '2020-10-21T07:58:26-04:00', 'direction_id': 0, 'schedule_relationship': None, 'status': None, 'stop_sequence': 40}, 'id': 'prediction-45616342-70030-40', 'relationships': {'route': {'data': {'id': 'Orange', 'type': 'route'}}, 'stop': {'data': {'id': '70030', 'type': 'stop'}}, 'trip': {'data': {'id': '45616342', 'type': 'trip'}}, 'vehicle': {'data': {'id': 'O-54673877', 'type': 'vehicle'}}}, 'type': 'prediction'}, {'attributes': {'arrival_time': '2020-10-21T08:02:29-04:00', 'departure_time': '2020-10-21T08:03:18-04:00', 'direction_id': 0, 'schedule_relationship': None, 'status': None, 'stop_sequence': 40}, 'id': 'prediction-45616343-70030-40', 'relationships': {'route': {'data': {'id': 'Orange', 'type': 'route'}}, 'stop': {'data': {'id': '70030', 'type': 'stop'}}, 'trip': {'data': {'id': '45616343', 'type': 'trip'}}, 'vehicle': {'data': {'id': 'O-54673867', 'type': 'vehicle'}}}, 'type': 'prediction'}, {'attributes': {'arrival_time': '2020-10-21T08:04:37-04:00', 'departure_time': '2020-10-21T08:05:50-04:00', 'direction_id': 1, 'schedule_relationship': None, 'status': None, 'stop_sequence': 150}, 'id': 'prediction-45616466-70031-150', 'relationships': {'route': {'data': {'id': 'Orange', 'type': 'route'}}, 'stop': {'data': {'id': '70031', 'type': 'stop'}}, 'trip': {'data': {'id': '45616466', 'type': 'trip'}}, 'vehicle': {'data': {'id': 'O-5467340A', 'type': 'vehicle'}}}, 'type': 'prediction'}], 'jsonapi': {'version': '1.0'}, 'links': {'first': 'https://api-v3.mbta.com/predictions?filter[route_type]=1&filter[stop]=place-sull&page[limit]=3&page[offset]=0&sort=departure_time', 'last': 'https://api-v3.mbta.com/predictions?filter[route_type]=1&filter[stop]=place-sull&page[limit]=3&page[offset]=24&sort=departure_time', 'next': 'https://api-v3.mbta.com/predictions?filter[route_type]=1&filter[stop]=place-sull&page[limit]=3&page[offset]=3&sort=departure_time'}}`