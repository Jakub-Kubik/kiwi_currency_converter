# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 09.03.2019

from typing import Union


def convert_item(amount: float, c_from: str, c_to: str, conv_rates: dict) -> dict:
    return {c_to: round((amount / conv_rates[c_from]) * conv_rates[c_to], 2)}


def convert(amount: float, currency_from: str, currency_to: Union[str, tuple], conversion_rates: dict) -> dict:
    """ Create dictionary with currencies 3 letter name: converted values. """
    converted = dict()
    if isinstance(currency_to, str):
        converted.update(convert_item(amount, currency_from, currency_to, conversion_rates))
    else:
        for item in currency_to:
            converted.update(convert_item(amount, currency_from, item, conversion_rates))
    return converted
