# hns_sunshine_api
Zendesk sunshine API.

## Installation
`pip install hns-sunshine-api`

## Usage
```python
from hns_sunshine_api import Sunshine

with Sunshine('test_domain', 'testemail@example.com', 'sunshine_api_key') as shine:
    # Call API here
```
