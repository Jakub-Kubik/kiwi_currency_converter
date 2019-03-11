# Currency converter
Currency converter is CLI and web API application. The goal of project is to create 
application for currency conversion based on everyday coins exchange rates. Source of 
live data is European Central Bank with address: ```https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml```.

## Getting Started
You need to clone this repository, create virtual environment for python 3.7 and activate it
and install all required packages from ```requirements.txt```.

## API and CLI app parameters
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

## Functionality
- if output_currency param is missing, convert to all known currencies

## CLI application
CLI application uses ```functions``` and python standard library.

### Run CLI app
```
(venv) <python3> ./currency_converter.py <parameters>
```

### Examples 
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2564.1
    }
}
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.19
    }
}
```

## Web API application
Web API application is created in Flask and uses ```functions```.

### localhost
Application runs on port 5000. If you want to change server to be accessible on local network, you 
must change IP address of server to 0.0.0.0.

#### Run API application
```
export FLASK_APP=api/web_api_app.py
flask run
```

### Examples
```
http://localhost:5000/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD
"input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.19
    }
```

```
http://localhost:5000/currency_converter?amount=10.92&input_currency=£
{
  "input": {
    "amount": 10.92,
    "currency_from": "GBP"
  },
  "output": {
    "AUD": 20.29,
    "BGN": 24.86,
    "BRL": 55.43,
    "CAD": 19.19,
    "CHF": 14.39,
    "CNY": 95.91,
    "CZK": 325.94,
    "DKK": 94.83,
    "EUR": 12.71,
    "GBP": 10.92,
    .
    .
    .
   }
}
```


### Deployed application
Application is deployed on pythonanywhere.com with address ```https://xkubik32.pythonanywhere.com/```.


### Examples
```
https://xkubik32.pythonanywhere.com/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD
"input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.19
    }
```

```
https://xkubik32.pythonanywhere.com/currency_converter?amount=10.92&input_currency=£
{
  "input": {
    "amount": 10.92,
    "currency_from": "GBP"
  },
  "output": {
    "AUD": 20.29,
    "BGN": 24.86,
    "BRL": 55.43,
    "CAD": 19.19,
    "CHF": 14.39,
    "CNY": 95.91,
    "CZK": 325.94,
    "DKK": 94.83,
    "EUR": 12.71,
    "GBP": 10.92,
    .
    .
    .
   }
}
```

## Tests
Tests are for CLI and for web API application. They are written in pytest and
pytest-flask.

### Run tests
```
pytest ./tests/tests.py -v
```

## Author
Jakub Kubík (jakupkubik@gmail.com)
