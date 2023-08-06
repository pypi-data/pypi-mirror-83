pool open api sdk
=====================

## setup

1. download sdk code package:
```shell script
git clone https://github.com/btc-top/pool-api-sdk-python3.git
```
2. enter directory:
```shell script
cd pool-api-sdk-python3
```
3. setup package:
```shell script
python setup.py install
```

## usage

example code:
```python

from btc_top_pool_api_sdk import Client


open_api_url='https://test/open-api/'
client_id='xxx'
secret_key='xxxx'
secret_salt='xxxxx'

client = Client(
    url=open_api_url,
    client_id=client_id,
    secret_key=secret_key,
    secret_salt=secret_salt)

result = client.call_api(
    'Speed.GetSubAccountAllWorkersHourlySpeedBulk',
    {'userName': 'test1', 'start': '2020-01-01 00:00:00', 'end': '2020-01-01 23:00:00'})

print(result)
```
