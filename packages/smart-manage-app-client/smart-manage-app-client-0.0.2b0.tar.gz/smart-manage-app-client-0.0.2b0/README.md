# Manage App client

## Install

    Install using `pip`...

        pip install smart-manage-app-client

## settings

```python
## befora start your app(for django in settings file)
from manage_app_client import ManageClientConfig
ManageClientConfig(
    manage_system_id='<secure system_id>',
    manage_system_url='<manage app backend url>',
    manage_system_token='<secure system token>',
)
```

### event decorators

```python

from manage_app_client.decorator import event, list_value_event

@event(keys=['integration_id', 'cred_id']) # for basic function
def test(integration_id, cred_id):
    return 'test1'


task_list = [{'integration_id': 2310, 'cred_id': 123}]

@list_value_event(
    keys=['integration_id', 'cred_id'], list_value='task_list', iter_key='key'
) # for list_value tasks
def test1(task_list, key):
    return 'test2'

```

### log exception

```python
from manage_app_client.utils import create_event_definition

@event(keys=['site_id', 'selection'])
def function(selection, site_id):
    ...
    try:
        ...
    except Exception as e:
        definition = create_event_definition(['site_id', 'selection'], locals()) # if list_value_event create_event_definition(['site_id', 'selection'], <list_value>, <iter_key>)
        log_exception(defition, str(e), is_auth=False) # push error to manage app backend

```

### decrypt request data

```python
from json import dumps
from manage_app_client.utils import decrypt_request_data
from manage_app_client.utils import Crypt
c = Crypt()
salt = c.set_random_salt()
data = {'integration_id': 13}
js = dumps(data)
token = '123'
ds = c.encrypt(js, token)
decrypt_request_data(ds, salt, token)
```
