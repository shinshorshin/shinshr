import pytest
import requests
import xml.etree.ElementTree as ET


def test_xml_validity():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002')
    data = response.content.decode('windows-1251')

    try:
        ET.fromstring(data)
    except ET.ParseError:
        pytest.fail("Invalid XML format")


def test_required_fields_present():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002')
    data = response.content.decode('windows-1251')

    root = ET.fromstring(data)
    valute_elements = root.findall('Valute')

    assert len(valute_elements) > 0, "No Valute elements found"

    required_fields = ['CharCode', 'Name', 'Value']
    for valute_element in valute_elements:
        for field in required_fields:
            assert valute_element.find(field) is not None, f"Missing {field} element in Valute"


def test_numeric_values_valid():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002')
    data = response.content.decode('windows-1251')

    root = ET.fromstring(data)
    valute_elements = root.findall('Valute')

    for valute_element in valute_elements:
        value_element = valute_element.find('Value')
        try:
            float(value_element.text.replace(',', '.'))
        except ValueError:
            pytest.fail(f"Invalid numeric value in Valute: {value_element.text}")


def test_currency_codes_valid():
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002')
    data = response.content.decode('windows-1251')

    root = ET.fromstring(data)
    valute_elements = root.findall('Valute')

    valid_currency_codes = ['AUD', 'GBP', 'BYR', 'DKK', 'USD', 'EUR', 'ISK', 'KZT', 'CAD', 'NOK', 'XDR', 'SGD', 'TRL',
                            'UAH', 'SEK', 'CHF', 'JPY']

    for valute_element in valute_elements:
        charcode_element = valute_element.find('CharCode')
        assert charcode_element.text in valid_currency_codes, f"Invalid currency code in Valute: {charcode_element.text}"
