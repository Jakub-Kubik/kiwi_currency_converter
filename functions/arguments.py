# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 09.03.2019

from argparse import ArgumentParser
import argparse
from typing import Union
from typing import Tuple


def parse_arguments() -> argparse.Namespace:
    """ Return parsed program arguments in argparse.Namespace. """
    parser = ArgumentParser()
    parser.add_argument('--amount', type=float, required=True, dest='amount',
                        help='Amount of money to be converted.')
    parser.add_argument('--input_currency', type=str, required=True, dest='input_currency',
                        help='Currency to be converted from. Currency is symbol or 3 letter name.')
    parser.add_argument('--output_currency', type=str, dest='output_currency',
                        help='Currency to be converted to. Currency is symbol or 3 letter name.')
    return parser.parse_args()


def check_currency_args_validity(program_args: argparse.Namespace) -> bool:
    """ Check currency symbol or 3 letter name validity. """
    valid_currencies = get_valid_currencies()
    if program_args.input_currency not in valid_currencies.keys() and \
       program_args.input_currency not in valid_currencies.values():
        return False
    if program_args.output_currency is not None:
        if program_args.output_currency not in valid_currencies.keys() and \
           program_args.output_currency not in valid_currencies.values():
            return False
    return True


def key_from_value(value: str, dictionary: dict) -> str:
    """ If value is currency symbol return currency 3 letter name
        else return 3 letter name.
    """
    if value in dictionary.values():
        for key, val in dictionary.items():
            if val == value:
                return key
    return value


def adjust_from_to_currency(currency_from: str, currency_to: Union[None, str]) -> Tuple[str, Union[tuple, str]]:
    valid_currencies = get_valid_currencies()
    curr_from = key_from_value(currency_from, valid_currencies)
    if currency_to is None:
        curr_to = tuple(k for k in get_valid_currencies().keys())
    else:
        curr_to = key_from_value(currency_to, valid_currencies)
    return curr_from, curr_to


def get_valid_currencies() -> dict:
    """ Some currencies have the same symbol.
        Currencies 'USD, CAD, AUD, MXN, NZD' have symbol '$'. 'USD' is main currency for '$' symbol.
        Currencies 'DKK, SEK, ISK, NOK' have symbol 'kr'. 'DKK' is main currency for 'kr' symbol.
        Currencies 'CNY, JPY' have symbol '¥'. 'CNY' is main currency for '¥' symbol.
    """
    return {
        "EUR": "€",
        "USD": "$",
        "CAD": "",
        "AUD": "",
        "MXN": "",
        "NZD": "",
        "HKD": "HK$",
        "SGD": "S$",
        "BRL": "R$",
        "DKK": "kr",
        "SEK": "",
        "ISK": "",
        "NOK": "",
        "CNY": "¥",
        "JPY": "",
        "BGN": "лв",
        "CZK": "Kč",
        "GBP": "£",
        "HUF": "Ft",
        "PLN": "zł",
        "RON": "lei",
        "CHF": "Fr",
        "HRK": "kn",
        "RUB": "₽",
        "TRY": "₺",
        "IDR": "Rp",
        "ILS": "₪",
        "INR": "₻",
        "KRW": "₩",
        "MYR": "RM",
        "PHP": "₱",
        "THB": "฿",
        "ZAR": "R"
    }
