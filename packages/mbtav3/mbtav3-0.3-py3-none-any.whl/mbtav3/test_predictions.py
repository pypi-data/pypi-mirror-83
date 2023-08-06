from pytest import fixture
from mbtav3.mbta import MBTA
from mbtav3.auth import Auth
from mbtav3.utils import Page, Sort, SortOrder, Filter, build_params
import aiohttp
import pytest
import asyncio
import os

pytestmark = pytest.mark.asyncio

stop = 'place-sull'
route_type = 1
page_offset = 0
page_limit = 3
sort_field = 'departure_time'
sort_order = 'asc'

async def test_predictions():
    session = aiohttp.ClientSession()
    mbta = MBTA(Auth(session,api_key))
    page = Page(page_offset, page_limit)
    order = SortOrder('asc')
    sort = Sort(sort_field, order)
    stopFilter = Filter('stop',stop)
    typeFilter = Filter('route_type', route_type)
    
    params = build_params(stopFilter, typeFilter, page=page, sort=sort)
    
    preds = await mbta.listPredictions(params)
    
    assert isinstance(preds, dict)
    