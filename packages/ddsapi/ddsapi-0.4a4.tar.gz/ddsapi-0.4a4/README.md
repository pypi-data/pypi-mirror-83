# DDSAPI-Client
Python API Client to access and download data from CMCC Data Delivery System (DDS)

## Requirements
Python 3.7, Python 3.8

### Installation  
Conda Installation
```bash
$ conda install -c fondazione-cmcc ddsapi 
```

Pip installation
```bash
$ pip install ddsapi
```
Cloning the repository
```bash
$ git clone https://github.com/CMCC-Foundation/ddsapi-client
$ cd ddsapi-client
$ python setup.py install
```

### Configuration
To use the tool a file `$HOME/.ddsapirc` must be created as following

```bash
url: http://dias.cmcc.scc:8282/api/v1
key: <uid>:<api-key>
```

### Examples

For some examples how to use the tool see [here](examples/)

