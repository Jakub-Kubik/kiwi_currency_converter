# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 10.03.2019

from flask import Flask, request, jsonify, render_template
from argparse import Namespace
from entry_task.arguments import check_currency_args_validity, adjust_from_to_currency
from entry_task.download import download_exchange_rates
from entry_task.conversion import convert

GET_PARAM_ERR = 1

app = Flask(__name__)


@app.errorhandler(404)
def error(e):
    if e == GET_PARAM_ERR:
        return render_template('error.html', GET_error=True), 404
    else:
        return render_template('error.html', GET_error=False), 404


@app.route('/currency_converter/')
def currency_converter():
    args = Namespace(amount=request.args.get('amount'),
                     input_currency=request.args.get('input_currency'),
                     output_currency=request.args.get('output_currency'))
    if not args.amount or not args.input_currency:
        return error(GET_PARAM_ERR)
    try:
        amount = float(args.amount)
    except ValueError:
        return error(GET_PARAM_ERR)
    if check_currency_args_validity(args) is False or amount < 0:
        return error(GET_PARAM_ERR)

    currency_from, currency_to = adjust_from_to_currency(args.input_currency, args.output_currency)

    exchange_rates = download_exchange_rates()

    converted_currency = convert(amount, currency_from, currency_to, exchange_rates)

    return jsonify({'input': {'amount': str(amount), 'currency_from': currency_from},
                    'output': converted_currency})
