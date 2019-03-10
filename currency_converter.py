# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 09.03.2019

from entry_task.arguments import parse_arguments, check_currency_args_validity, adjust_from_to_currency
from entry_task.download import download_exchange_rates
from entry_task.conversion import convert
from sys import exit, stderr
from json import dumps


if __name__ == '__main__':
    args = parse_arguments()
    if check_currency_args_validity(args) is False or args.amount < 0:
        stderr.write('Wrong arguments')
        exit(2)

    amount = args.amount
    currency_from, currency_to = adjust_from_to_currency(args.input_currency, args.output_currency)

    exchange_rates = download_exchange_rates()
    if exchange_rates is None:
        stderr.write('Can\'t download today\'s currency rates')
        exit(3)

    converted_currency = convert(amount, currency_from, currency_to, exchange_rates)

    print(
        dumps({'input': {'amount': str(amount), 'currency': currency_from},
               'output': converted_currency},
              indent=4))
