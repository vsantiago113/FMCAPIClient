# FMCClient

## Cisco Firepower Management Center (FMC) API Wrapper

### Description
This is a wrapper to make it easier to use the API to interact with the FMC to get, update, delete and create records.

---

### Class Usage

#### Class.get(method='')
The class method is the a url part for example: devices/devicerecords/device_uuid

On the FMC the example url you will see is the full url part like this example: /api/fmc_config/v1/domain/DomainUUID/devices/devicerecords/device_uuid

You do not need this part: /api/fmc_config/v1/domain/DomainUUID
That part is adding automatically by the Class.

Check the examples for get, put, post and delete.

---

#### Class.get(method='', limit=1000, offset=0, expanded=True)
The parameters limit, offset, expanded any other parameter required for the API call need to pass it as a kwarg.

#### Import and create connection
Import the package FMCClient then create an instance of the class Client and use the class instance to create a connection. To close the connection use the close method.
```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')

client.close()
```

---

### To get records - Class.get(method='', **kwargs)
Import the package FMCClient then create an instance of the class Client and use the class instance to create a connection. To close the connection use the close method.

#### Method
```text
devices/devicerecords
```

```text
devices/devicerecords/device_uuid
```

```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')

response = client.get(method='devices/devicerecords', limist=1000, offset=0, expanded=True)
for device in response['items']:
    print(f'Hostname: {device["name"]}')
    print(f'IP Address: {device["hostName"]}')
client.close()
```

```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')

device = client.get(method='devices/devicerecords/device_uuid')
print(f'Hostname: {device["name"]}')
print(f'IP Address: {device["hostName"]}')
client.close()
```

#### Response Data
Response Status Code200
```json
{
  "id": "device_uuid",
  "hostName": "<host name>",
  "name": "nachos",
  "type": "Device",
  "license_caps": [
    "PROTECT",
    "MALWARE"
  ]
}
```
---

### Update records - Class.update(method='', **kwargs)
To update a record you need to pass a json object with all the required data, check out the example below:
#### Method
```text
devices/devicerecords/device_uuid
```

#### Data
```json
{
  "id": "device_uuid",
  "name": "nachos_updated",
  "type": "Device",
  "hostName": "10.20.30.40",
  "prohibitPacketTransfer": true
}
```
```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')
data = {
  "id": "device_uuid",
  "name": "nachos_updated",
  "type": "Device",
  "hostName": "10.20.30.40",
  "prohibitPacketTransfer": True
}

response = client.update(method='devices/devicerecords/device_uuid', data=data)

client.close()
```

#### Request Data
Response Status Code200
```json
{
  "name": "newDevice",
  "regKey": "test",
  "hostName": "10.1.1.10",
  "type": "Device",
  "license_caps": [
    "PROTECT",
    "MALWARE"
  ]
}
```

---

### Create records - Class.add(method='', **kwargs)
To create a record you need to pass a json object with all the required data, check out the example below:
#### Method
```text
devices/devicerecords
```

#### Data
```json
{
  "name": "<name>",
  "hostName": "<host name>",
  "natID": "cisco123",
  "regKey": "regkey",
  "type": "Device",
  "license_caps": [
    "MALWARE",
    "URLFilter",
    "PROTECT",
    "CONTROL",
    "VPN"
  ],
  "accessPolicy": {
    "id": "accessPolicyUUID",
    "type": "AccessPolicy"
  }
}
```
```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')
data = {
  "name": "<name>",
  "hostName": "<host name>",
  "natID": "cisco123",
  "regKey": "regkey",
  "type": "Device",
  "license_caps": [
    "MALWARE",
    "URLFilter",
    "PROTECT",
    "CONTROL",
    "VPN"
  ],
  "accessPolicy": {
    "id": "accessPolicyUUID",
    "type": "AccessPolicy"
  }
}

response = client.add(method='devices/devicerecords', data=data)

client.close()
```

#### Request Data
Response Status Code202
```json
{
  "name": "<name>",
  "hostName": "<host name>",
  "natID": "cisco123",
  "regKey": "regkey",
  "type": "Device",
  "license_caps": [
    "BASE",
    "MALWARE",
    "URLFilter",
    "THREAT"
  ],
  "accessPolicy": {
    "id": "accessPolicyUUID",
    "type": "AccessPolicy"
  }
}
```

---

### To delete records - Class.delete(method='', **kwargs)
To delete the record you only need to pass the device or object id on the method.

```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')

response = client.delete(method='devices/devicerecords/device_uuid')
print(response)

client.close()
```

#### Response Data
Response Status Code200
```json
{
  "id": "device_uuid",
  "name": "nachos_updated",
  "type": "Device",
  "license_caps": [
    "PROTECT",
    "MALWARE"
  ]
}
```
