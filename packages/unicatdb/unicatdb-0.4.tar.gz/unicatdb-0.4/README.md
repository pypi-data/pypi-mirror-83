# UniCatDB API library

Python library for accessing API of the UniCatDB - Universal Catalog Database for biological findings.

> UniCatDB is a coherent yet flexible interdisciplinary storage solution for cataloging findings data of various research groups, focused mainly on green biology. Configurable by the researchers themselves, provides shared access enabling interoperability if desired, and is accessible by user-friendly interface on either desktop, laptop or tablet - both in the lab and on the go.

See www.unicatdb.org for more details and contact.

# Getting started

1) Install the library to your Python environment.

    Typically, for local Python on your desktop, run pip install command in shell:
    
    ```shell script
    pip install unicatdb
    ```
    
    For other environments, such as Jupiter notebook, see respective documentation for instructions on how to install pip packages.
    
    For example, in Jupiter notebook, paste this snippet the top (source: [here for details](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/#How-to-use-Pip-from-the-Jupyter-Notebook)):
    
    ```python
    # Install a pip package in the current Jupyter kernel
    
    import sys
    !{sys.executable} -m pip install unicatdb
    ```

2) Login to the UniCatDB (https://app.unicatdb.org)
3) Obtain your API credentials (API key and Personal access token) - click on your profile in toolbar, then on *API Access* button
4) Use credentials in API client configuration, see usage examples bellow


# Structure

The core of the library is in module `unicatdb.opeapi_client` which consists of code generated via the modified
[OpenAPI Generator](https://openapi-generator.tech/) and the interface corresponds to the UniCatDB API specifications available at https://api.unicatdb.org

For more convenient access, wrappers are provided in `unicatdb.api` module - this is your entrypoint for most common tasks.


# Usage examples

## The "Hello world"

**What this does:** Get first ten findings from the database

```python
import unicatdb
from pprint import pprint

# %% Paste your API key and Personal access token from https://app.unicatdb.org/

configuration = unicatdb.Configuration(
    api_key='<PASTE YOUR API KEY HERE>',
    access_token='<PASTE YOUR ACCESS TOKEN HERE>'
)

# %% Query some data

from unicatdb.openapi_client import FindingArrayResponse

with unicatdb.Client(configuration) as client:
    findings: FindingArrayResponse = client.findings.api_findings_get()

    pprint(findings)
```

## Advanced query example

**What this does:** Get only the *name*, *amount* and *dynamic data* of the top 10 findings sorted by *amount* greatest-first,
of which taxonomy's genus contains 'vulgare':


```python
import unicatdb
from pprint import pprint

# %% Paste your API key and Personal access token from https://app.unicatdb.org/

configuration = unicatdb.Configuration(
    api_key='<PASTE YOUR API KEY HERE>',
    access_token='<PASTE YOUR ACCESS TOKEN HERE>'
)

# %% Query some data - e.g. apply filtering, sorting and paging during the API call to leave the heavy-lifting to the server

from unicatdb.openapi_client import FindingArrayResponse, FindingFieldsQuery, PageQuery

with unicatdb.Client(configuration) as client:

    filter_expressions = {
        "taxonomyName.species": "like:vulgare"
    }

    fetch_only_fields = FindingFieldsQuery(findings="documentName,amount,dynamicData")

    findings: FindingArrayResponse = client.findings.api_findings_get(
        sort="-amount",
        filter=filter_expressions,
        fields=fetch_only_fields,
        page=PageQuery(number=1,size=10)
    )

    pprint(findings)
```



 