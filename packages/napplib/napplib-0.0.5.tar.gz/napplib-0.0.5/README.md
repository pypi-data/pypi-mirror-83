## NappLIB

### About

We created this lib to help your team interact with azure storage or others azure services, our internal hub system, ftp and remote database connections and other stuffs.

### Import

```python
from napplib.download_azure_storage import DownloadAzureStorage
```

### Examples

Return content of latest project/store blob file
```python
DownloadAzureStorage.get_latest_blob(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER', 
    store_name='PROJECT_STORE')
```

Return specific content of project/store blob file
```python
DownloadAzureStorage.get_blob(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER',
    blob_path='project/store/2020/10/23/sample.csv')
```

### Author

```
Leandro Vieira
leandro@nappsolutions.com
```