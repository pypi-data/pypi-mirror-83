# RASB-Python-API
An API wrapper for the Discord RASB bot / service using Python.

### Features
1. Grab if a user is banned or not.
2. Get the full RASB ban list.
3. Grab info about an RASB report.

### Code Examples

```python
from rasb.py import RASBClient
Client = RASBClient()

checkBanned = Client.isUserBanned("ID")
print(checkBanned)

-------------------------------------

from rasb.py import RASBClient
Client = RASBClient()

banList = Client.getBans()
print(banList)

-------------------------------------

from rasb.py import RASBClient
Client = RASBClient()

getReport = Client.getReport("report_id")
print(getReport)
```