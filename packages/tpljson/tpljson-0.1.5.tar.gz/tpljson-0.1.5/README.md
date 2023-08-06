# tpljson
![PyPI](https://img.shields.io/pypi/v/tpljson)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tpljson)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tpljson)  
![tests](https://github.com/OpenBigDataPlatform/tpljson/workflows/tests/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/OpenBigDataPlatform/tpljson/badge.svg?branch=master)](https://coveralls.io/github/OpenBigDataPlatform/tpljson?branch=master)
[![Docs](https://readthedocs.org/projects/tpljson/badge/?style=flat)](https://github.com/OpenBigDataPlatform/tpljson)


A Templating Json package that implements the official **Python** `json` interface.

`tpljson` works by referencing placeholder template strings into your json file... like `{$.mykey}`  
These template values will be filled with other values that appear in the document.


## Features
- template json, referencing other fields in the current document via `{$.key}`
- comments
- colorized and context on errors
- built-in `json` module compatible, all json errors raise `json.JSONDecodeError` and `TypeError` - 
identical to the built-in `json` module.
  
## Installation
```properties
pip3 install tpljson
```

## Usage Example 1
**Define `contact.json` as**
```json
// this is another comment, multi-line comments are not supported.
{
  "first_name": "Peter", // first_name - comments can appear at the end of a line
  "last_name": "Henderson",
  "phone": "3338675309",
  "email": "{$.first_name}.{$.last_name}@example.org", // construct email address from 
  "contact": "{$.first_name} {$.last_name}\nCell: {$.phone}\nEmail: {$.email}"
}
```

**Load `contact.json` using `tpljson`**
```python
import tpljson as json
d = json.load(open('contact.json'))
print(json.dumps(d, indent=4))
```
**Output**
```json
{
    "first_name": "Peter",
    "last_name": "Henderson",
    "phone": "3338675309",
    "email": "Peter.Henderson@example.org",
    "contact": "Peter Henderson\nCell: 3338675309\nEmail: Peter.Henderson@example.org"
}
```


## Usage Example 2
A more 

**Define `permissions.json` as:**
```json
{
  "user_id": "u381815",
  "cluster": "hive-cluster",
  "groups": ["finance", "accounting"],
  "description": "Permissions for user Nicholas",
  "create_role": [
    {"role": "{$.user_id}"}
  ],
  "grant_role": [
    {"group": "{$.user_id}", "role": "{$.user_id}"}
  ],
  "grant_privilege": [
    {"privilege": "select",  "object": "database",  "patterns": "{$.groups}", "role": "{$.user_id}"},
    {"privilege": "all",  "object": "database",  "name": "{$.user_id}", "role": "{$.user_id}"},
    {"privilege": "all",  "object": "uri",  "name": "'hdfs://{$.cluster}/user/{$.user_id}'", "role": "{$.user_id}"}
  ],
  "create_database": [
    {"name": "{$.user_id}", "owner": "{$.user_id}"}
  ],
  "sql": [
    "SHOW GRANT ROLE {$.user_id}",
    "SHOW ROLE GRANT GROUP {$.user_id}"
  ]
}
```

**Load `permissions.json` using `tpljson`**
```python
import tpljson as json
d = json.load(open('permissions.json'))
print(json.dumps(d, indent=4))
```

**Output**:
```json
{
    "user_id": "u381815",
    "cluster": "hive-cluster",
    "groups": [
        "finance",
        "accounting"
    ],
    "description": "Permissions for user Nicholas",
    "create_role": [
        {
            "role": "u381815"
        }
    ],
    "grant_role": [
        {
            "group": "u381815",
            "role": "u381815"
        }
    ],
    "grant_privilege": [
        {
            "privilege": "select",
            "object": "database",
            "patterns": [
                "finance",
                "accounting"
            ],
            "role": "u381815"
        },
        {
            "privilege": "all",
            "object": "database",
            "name": "u381815",
            "role": "u381815"
        },
        {
            "privilege": "all",
            "object": "uri",
            "name": "'hdfs://hive-cluster/user/u381815'",
            "role": "u381815"
        }
    ],
    "create_database": [
        {
            "name": "u381815",
            "owner": "u381815"
        }
    ],
    "sql": [
        "SHOW GRANT ROLE u381815",
        "SHOW ROLE GRANT GROUP u381815"
    ]
}
```

## Implementation
- Note that the order of values matters in the `json`, if one value depends on another.
- `commentjson` is used internally to render comments, can be disabled via `comments=false` in `load` and `loads`.
- errors are colorized by default via `colorama`

