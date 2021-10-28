import requests
from datetime import datetime
import hmac
import hashlib
import base64
import json
import csv
import pandas as pd

api_key = '8c456347e709001b05e1bced1048482d'
api_secret = '1a5c57d63e55928e7cc57d050f57831705d4e3e0edb594149511257bef9b73c3'


def sig_generator(key, secret, date=None):
    if date is None:
        print('Date not specified, using current time.')
        date = datetime.utcnow().date().strftime('%d%m%Y')

    joined_string = bytes("{}{}".format(date, key),
                          encoding='utf-8')

    dig = hmac.new(
        bytes(secret, encoding='utf-8'),
        msg=joined_string, digestmod=hashlib.sha256)

    hexdig = bytes(dig.hexdigest(), encoding='utf-8')
    sig = base64.b64encode(hexdig).decode()
    return sig

#print(sig_generator(api_key, api_secret, '01012019'))


def api_url_generator(**kwargs):
    url_args = ''
    allowed_params = ['from_country', 'to_country', 'from_currency', 'to_currency', 'dir', 'type', 'amount',
                      'pay_in_method', 'pay_out_method']

    for param, value in kwargs.items():
        if param in allowed_params:
            url_args += "{0}={1}&".format(param, value)
            print("\nParameter allowed: {0} value: {1}".format(param, value))
            continue
        else:
            print("\nParameter not allowed: ", param)
            continue

    api_url = ("https://fx-pricing-api.fxcintel.com/v3/pricing?" + url_args + "key=" + api_key + "&" + "sig=" + sig_generator(api_key, api_secret))

    return api_url

# Find a way to make this txt file name a variable
def save_to_json(rsp_json):

    file_name = (rsp_json['call_timestamp']+" RAW.txt").replace(':', '_')
    output_file = open(file_name, 'w+')
    json.dump(rsp_json, output_file)
    return

def call_api():
    api_url = api_url_generator(wrong_arg="Hi",
                             from_country='HK',
                             from_currency='HKD',
                             to_country='GB',
                             to_currency='GBP',
                             amount='1000',
                             pay_in_method='',
                             pay_out_method='Bank%20Account')

    response = requests.get(api_url)
    rsp_json = response.json()
    print("Response: ", response)
    print('\n\nJSON:', rsp_json)
    save_to_json(rsp_json)

    return rsp_json

def json_manipulation(new_rsp_json):

    file_name_lookup = (new_rsp_json['call_timestamp'] + " RAW.txt").replace(':', '_')
    file = open(file_name_lookup, "r")

    # read the content of file
    data = file.read()

    start_loc = data.find("[")
    end_loc = data.find("]")

    # save body of data in string
    data = data[(start_loc):(end_loc + 1)]

    # converts body of data to list
    data_json = json.loads(data)

    # loading body of data as dataframe
    df = pd.DataFrame(data_json)

    csv_file_name = (new_rsp_json['call_timestamp'] + " BODY.csv").replace(':', '_')
    df.to_csv(csv_file_name)
    print('Saved body of data as: '+csv_file_name)

    #print("Number of rows and colums:", df.shape)
    print("Colums: ", df.columns)
    print(df)

    return


new_rsp_json = call_api()
json_manipulation(new_rsp_json)


