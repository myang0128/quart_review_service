import asyncio
import json
import tracemalloc
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import aiohttp
from dateutil.relativedelta import relativedelta
from quart import Quart, jsonify
from quart_schema import QuartSchema, validate_querystring, RequestSchemaValidationError

from api.params import RequestParam
from config import appConfig

tracemalloc.start()
start = tracemalloc.take_snapshot()
app = Quart(__name__)
QuartSchema(app)


@dataclass
class Query:
    a: Optional[int] = None

@app.route("/")
async def hello():
    return "aaaaa"

@app.route("/api/v1/review")
@validate_querystring(RequestParam)
async def async_get(query_args: RequestParam):
    params = set_default_dates(query_args)
    for key, value in dict(params).items():
        if value is None:
            del params[key]
    async with aiohttp.ClientSession() as client:
        tasks = []
        if params.get('sub_type') == 'distributor' or params.get('user_type') == 'distributor':
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.TOP_SUMMARY_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.CUSTOMER_SEGMENT_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_VALUES_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_OVER_TIME_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PEER_PERFORMANCE_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.NUMBER_OF_OPPS_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_DATA_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.OPP_AMOUNT_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.GROSS_REVENUE_RETENTION_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.DATE_UPDATED_URL)))
        else:
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.TOTAL_AND_ANNUALIZED_OPP_AMOUNT_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.OPPORTUNITIES_BOOKED_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.CUSTOMER_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.CUSTOMER_SEGMENT_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_VALUES_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_OVER_TIME_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PEER_PERFORMANCE_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.NUMBER_OF_OPPS_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.PERFORMANCE_DATA_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.OPP_AMOUNT_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.GROSS_REVENUE_RETENTION_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.GET_CUSTOMER_RETENTION_URL)))
            tasks.append(asyncio.ensure_future(call_url(client, appConfig.DATE_UPDATED_URL)))
        results = await asyncio.gather(*tasks)
        return jsonify({"a": results})


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error):
    return {"errors": error.validation_error.json()}, 400


async def call_url(session, url):
    print(f'call {url}')
    async with session.get(url) as resp:
        r = await resp.json()
        return r


def set_default_dates(request_params):
    now = datetime.now()
    print(request_params)
    end_date = now + relativedelta(months=-1)
    start_date = end_date + relativedelta(months=-11)
    data = json.loads(request_params.json())
    data.update({
        'start_month': request_params.start_month or f'{start_date.month}',
        'start_year': request_params.start_year or f'{start_date.year}',
        'end_month': request_params.end_month or f'{end_date.month}',
        'end_year': request_params.end_year or f'{end_date.year}',
    })
    return data
