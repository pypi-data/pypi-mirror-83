## NappLIB

### About

We created this lib to help your team interact with azure storage or others azure services, our internal hub system, ftp and remote database connections and other stuffs.

## Functions

### Install

```
pip install napplib
```

### Azure Storage

```python
from napplib.azure_storage_blob import BlobStorage
```

Return content of latest project/store blob file
```python
BlobStorage.get_latest_blob(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER', 
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

Return specific content of project/store blob file
```python
BlobStorage.get_blob(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER',
    blob_path='project/store/2020/10/23/sample.csv')
```

Upload local file to azure blob storage with napp pattern based on project/store/year/month/day/file
```python
BlobStorage.upload_blob(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME',
    output_file='./files/sample.csv')
```

List all blobs from project/store folder
```python
BlobStorage.list_all_blobs(
    account_name='AZURE_ACCOUNT_NAME', 
    account_key='AZURE_ACCOUNT_KEY', 
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

### Others

--

## Author

```
Leandro Vieira
leandro@nappsolutions.com
```