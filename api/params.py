from dataclasses import dataclass
from typing import Optional, List

from pydantic import BaseModel, validator


class RequestParam(BaseModel):
    partner_parent: Optional[List[str]] = None
    partner_account: Optional[List[str]] = None
    distributor_parent: Optional[List[str]] = None
    distributor_account: Optional[List[str]] = None
    geo: Optional[List[str]] = None
    subregion: Optional[List[str]] = None
    country: Optional[List[str]] = None
    start_month: Optional[str] = None
    start_year: Optional[str] = None
    end_month: Optional[str] = None
    end_year: Optional[str] = None
    incumbent_partner: Optional[str] = None
    account_segment: Optional[str] = None
    partner_tier: List[str] = None
    total_or_annualized: str = 'TB'
    currency_code: str = 'USD'
    sub_type: str = 'partner'
    user_type: str = 'partner'

    @validator('total_or_annualized')
    def total_annualized_validation(cls, param):
        if param and param not in ['TB', 'SYB']:
            raise ValueError("Invalid Total or Annualized parameter. It needs to be TB or SYB.")
        return param

    @validator('currency_code')
    def currency_code_validation(cls, currency_code):
        if currency_code and currency_code not in ['AED', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'CZK',
                                                   'DKK', 'EUR', 'GBP', 'HKD', 'IDR', 'ILS', 'INR', 'JPY', 'KRW', 'LKR',
                                                   'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RUB', 'SEK', 'SGD', 'THB',
                                                   'USD',
                                                   'ZAR']:
            raise ValueError("Invalid Currency Code.")
        return currency_code

    @validator('start_month', 'end_month')
    def month_validation(cls, param):
        if param:
            if not param.isdigit() or int(param) > 12 or int(param) <= 0:
                raise ValueError("Invalid Month. It must be numbers from 1 to 12.")
        return param

    @validator('start_year', 'end_year')
    def year_validation(cls, param):
        if param:
            if not param.isdigit() or int(param) < 0:
                raise ValueError("Invalid Year.")
        return param

    @validator('incumbent_partner')
    def incumbent_validation(cls, param):
        if param and param not in ['Yes', 'No']:
            raise ValueError("Invalid Incumbent Partner parameter. It needs to be Yes or No.")
        return param

    @validator('partner_parent', 'partner_account', 'distributor_parent', 'distributor_account', 'geo', 'subregion',
               'country', 'incumbent_partner', 'account_segment', each_item=True)
    def string_validation(cls, param):
        if param and param.isnumeric():
            raise ValueError("Invalid String. It cannot be a number.")
        return param

    '''
    @validator('*', check_fields=False)
    def sanitize(cls, param):
        if isinstance(param, list):
            return [bleach.clean(x).strip() if x else x for x in param]
        elif param:
            return bleach.clean(param.strip())
    '''


class ReviewRequestParam(RequestParam):
    x: Optional[str] = 'est_opp_amount'
    y: Optional[str] = 'perf_percent'

    @validator('x', 'y')
    def x_validation(param):
        if param and param not in ['est_opp_amount', 'on_time_percent', 'par_percent', 'upsell_percent',
                                   'cross_sell_percent',
                                   'perf_percent']:
            raise ValueError("Invalid x. It needs to be est_opp_amount, on_time_percent, par_percent, upsell_percent, "
                             "cross_sell_percent, or perf_percent")
        return param


class DealRequestParam(RequestParam):
    deal_type: Optional[str]

    @validator('deal_type')
    def type_validation(cls, param):
        if param:
            if param and param not in ['in', 'out', 'closed', 'renewed', 'partners']:
                raise ValueError("Invalid Deal Type. It needs to be in, out, closed, renewed, or partners.")
        return param


class CustomerPerformanceRequestParam(RequestParam):
    x: Optional[str] = 'est_opp_amount'
    y: Optional[str] = 'perf_percent'

    @validator('x', 'y')
    def x_validation(param):
        if param and param not in ['est_opp_amount', 'on_time_percent', 'par_percent', 'upsell_percent',
                                   'cross_sell_percent',
                                   'perf_percent']:
            raise ValueError("Invalid x. It needs to be est_opp_amount, on_time_percent, par_percent, upsell_percent, "
                             "cross_sell_percent, or perf_percent")
        return param


class CustomerGroupRequestParam(RequestParam):
    customer_group: Optional[str]


class PerformanceRequestParam(RequestParam, BaseModel):
    customer_group: Optional[str]
    deal_type: Optional[str]

    @validator('deal_type')
    def type_validation(cls, param):
        if param:
            if param and param not in ['in', 'out', 'closed', 'renewed', 'partners', 'original', 'distributors']:
                raise ValueError(
                    "Invalid Deal Type. It needs to be in, out, closed, renewed, original, distributors or partners.")
        return param
