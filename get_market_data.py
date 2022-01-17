import json
import requests
START_TIME = 1517450400

call = 'https://min-api.cryptocompare.com/data/\
        v2/histohour?fsym=ETH&tsym=USD&limit=2000'

response = requests.get(call)
total_data = response.json()['Data']['Data']
earliest = 1641614992
while earliest > START_TIME:
    earliest = int(total_data[0]['time'])
    print(earliest)
    call = f'https://min-api.cryptocompare.com/data/v2/histohour\
            ?fsym=ETH&tsym=USD&toTs={str(earliest)}&limit=2000'
    response = requests.get(call)
    temp_data = response.json()['Data']['Data']
    total_data = temp_data + total_data

with open('data.json', 'w') as file:
    json.dump(total_data, file)
