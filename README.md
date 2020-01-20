# FMCClient

## Cisco Firepower Management Center (FMC) API Wrapper

### Description
This is a wrapper to make it easier to use the API to interact with the FMC to get, update, delete and create records.

---

### Class Usage

#### Import
Import the package FMCClient then create an instance of the class Client and use the class instance to create a connection. To close the connection use the close method.
```python
import FMCClient

client = FMCClient.Client()
client.connect(server='myfmc.local', username='myusername', password='mypassword')

client.close()
```
