from web3 import Web3
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import json

block_data = pd.DataFrame([])

#set end block
x = 7404401

#tao addresses
addresses = ['0x7065DdA3f8Ec5F6C155648BdeE4420c0525D93C6',
            '0xE12d3c8675a88fEDCf61946089079323342982bB']
#starting block
#get data from covalent api
while x > 7068862:
    x=x-7200
    for address in addresses:
        print(x)
        print(address)
        print("pulling data")
        result = requests.get("https://api.covalenthq.com/v1/56/tokens/{}/token_holders/?block-height={}&page-size=999999999&key=ckey_fdf13a80f62d428cbe85ae4bb16".format(address, x))
        print("pulled data")
        result = result.json()
        df = pd.DataFrame.from_dict(result['data']['items'])
        block_data = block_data.append(df, ignore_index=True, sort=False)
        print("appended data")
    print('done')

#group on data needed
block_grouped = block_data.groupby(['block_height', 'contract_ticker_symbol']).size().unstack(fill_value=0)
block_grouped = block_grouped.reset_index()

#melt df
final_df = pd.melt(block_grouped, id_vars=['block_height'], value_vars=['TAO', 'sTAO'])

#connect to web3
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

#set connection
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

#timestamp conversion
def timestamp_conversion(block):
    timestamp = web3.eth.getBlock(block).timestamp
    return timestamp

#set timestamp
final_df['timestamp'] = final_df['block_height'].apply(timestamp_conversion)

#set data
final_df['date'] = pd.to_datetime(final_df['timestamp'], unit='s')
final_df = final_df.drop(['block_height', 'timestamp'], axis=1)

#to csv
final_df.to_csv('tao_holders.csv')

