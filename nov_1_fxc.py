#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:57:43 2021

@author: callumzs
"""
import os

import requests
from datetime import datetime
import hmac
import hashlib
import base64
import json
import time
import pandas as pd
import numpy as np

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
            #print("\nParameter allowed: {0} value: {1}".format(param, value))
            continue
        else:
            print("\nParameter not allowed: ", param)
            continue

    api_url = ("https://fx-pricing-api.fxcintel.com/v3/pricing?" + url_args + "key=" + api_key + "&" + "sig=" + sig_generator(api_key, api_secret))

    return api_url

def make_folder(new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

# Find a way to make this txt file name a variable
def save_to_json(rsp_json):

    #create new output folder
    call_timestamp_string = rsp_json['call_timestamp'].replace(':', '_')
    folder_name = (call_timestamp_string[0:10])
    new_folder = r'.\output\%s' % (folder_name)
    make_folder(new_folder)

    #added "to_country" as well as "amount" to the file name to distinguish output
    file_name = (rsp_json['call_timestamp']+' HK to '+rsp_json['to_country']+" "+rsp_json['amount']+" RAW.txt").replace(':', '_')
    output_file = open(".\output\%s\%s" % (folder_name, file_name), 'w+')
    json.dump(rsp_json, output_file)
    return

def call_api(fx_amount, to_country_code, to_currency_code):
    api_url = api_url_generator(
                             from_country = 'HK',
                             from_currency = 'HKD',
                             
                             to_country = to_country_code,
                             to_currency = to_currency_code,
                             amount = float(fx_amount),
                             
                             pay_in_method='',
                             pay_out_method='Bank%20Account')

    response = requests.get(api_url)
    rsp_json = response.json()
   # print("Response: ", response)
   # print('\n\nJSON:', rsp_json)
    save_to_json(rsp_json)
    print("Call Success")
    return rsp_json

def json_manipulation(rsp_json, to_country=None, to_currency=None):

    # damn it Will make this code neater! --> write a wrapper function for save_to_json and json_manipulation, make folder_name and
    # the first part of the file name global

    call_timestamp_string = rsp_json['call_timestamp'].replace(':', '_')
    #this extracts the date only
    folder_name = (call_timestamp_string[0:10])
    file_name_lookup = (rsp_json['call_timestamp']+' HK to '+rsp_json['to_country']+" "+rsp_json['amount']+" RAW.txt").replace(':', '_')
    file = open(".\output\%s\%s" % (folder_name, file_name_lookup), "r")

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
    
    #if using array inputs for multiple countries/currencies append these to 
    #dataframe/CSV
    if to_currency and to_country is not None:
    
        #Adding 'to country & currency' to dataframe

        df.insert(len(df.columns)-1, "to_country", to_country)
        df.insert(len(df.columns)-1, "to_currency", to_currency)

    csv_file_name = (rsp_json['call_timestamp']+' HK to '+rsp_json['to_country']+" "+rsp_json['amount']+" BODY.csv").replace(':', '_')
    df.to_csv(".\output\%s\%s" % (folder_name, csv_file_name))
    print('Saved body of data as: '+csv_file_name)

    #print("Number of rows and colums:", df.shape)
    #print("Colums: ", df.columns)
    #print(df)

    return df


'''
Create an excel file for a range of exchance amounts. Can then copy these into 1 to 
do analysis 

Manually change to currency & country in 'call-api' func and then run again

I have used USD (US); GBP (GB) , CNY (CN), SGD (SG), EUR (DE), JPY (JP)

'''





def run_single(fx_amount, to_country_code, to_currency_code):
    '''
    Function call the FXC API and saves the CSV for provided single fx amount
    and to country/currency

    Parameters
    ----------
    fx_amount : Float
        Amount of money user is sending
    to_country_code : String
        2-letter (ISO Alpha-2) country code.
    to_currency_code : String
        3-letter (ISO 4217) currency code.

    Returns
    -------
    None.

    '''
    rsp_json = call_api(fx_amount, to_country_code, to_currency_code)
    json_manipulation(rsp_json)
    return


#Information which has been ran for the daily calls
fx_amounts = [100,1000,10000,100000,500000,1000000]

# conv_to =np.array([['US','GB','CN','SG','DE','JP'],
#            ['USD','GBP','CNY','SGD','EUR','JPY']])

conv_to =np.array([['US','GB'],
           ['USD','GBP']])

def run_batch(fx_amounts, conv_to):
    '''
    Function takes a list of fx amounts, and array of countries&currency codes.
    The API is then called for each fx amount and country/currency and CSV saved.
    len (fx_amounts) = len(conv_to[0])
    len(conv_to[0]) = len(conv_to[1])

    Parameters
    ----------
    fx_amounts : List
        List of amounts the user is sending (float's).
    conv_to : NumPy Array
        2d array of the fx transaction to country (2-letter country code) and 
        to currency (3-letter currency code).
        In format: ([to_countries],[to_currencies]) in which 
        len(to_cuntries)=len(to_currencies)
        

    Returns
    -------
    None.

    '''
    print (np.shape(conv_to))
    print (len(conv_to[0]))
               
    #take 1 country/currency pair
    for i in range (len(conv_to[0])):
        
        for j in range (len(fx_amounts)):
            #Call FXC for each fx_amount on the given country/currency pair 
        
            rsp_json = call_api(fx_amounts[j], conv_to[0][i], conv_to[1][i])
            
            json_manipulation(rsp_json, conv_to[0][i], conv_to[1][i])
            
            print ('FX amount: {}, To Country: {}, To Currency: {}'.format(fx_amounts[j], conv_to[0][i], conv_to[1][i]))
            
            #To ennsure filename are unique and prevent overwrites
            time.sleep(1)
            
    return



#run_single(1000, "GB", "GBP")
run_batch(fx_amounts, conv_to)

























