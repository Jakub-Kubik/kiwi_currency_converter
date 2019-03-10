# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 09.03.2019

from urllib.request import urlopen
from urllib.error import HTTPError
from xml.etree import ElementTree
from typing import Union


def download_exchange_rates() -> Union[None, dict]:
    """ Download currency rates from European Central Bank. Currencies
        are daily actualized. Referential currency is euro.
    """
    try:
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        response = urlopen(url)
    except HTTPError:
        return None

    rates = dict()
    root = ElementTree.fromstring(response.read())
    # https://stackoverflow.com/questions/17250660/
    # how-to-parse-xml-file-from-european-central-bank-with-python
    namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):  # XPath
        key = cube.attrib['currency']
        value = cube.attrib['rate']
        rates[key] = float(value)
    rates['EUR'] = 1
    return rates

