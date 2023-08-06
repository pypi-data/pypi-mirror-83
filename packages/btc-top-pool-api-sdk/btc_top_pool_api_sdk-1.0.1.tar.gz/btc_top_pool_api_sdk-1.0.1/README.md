pool open api sdk
=====================

## setup

```shell script
pip install btc-top-pool-api-sdk
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
