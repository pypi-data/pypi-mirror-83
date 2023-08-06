# Switchcraft

![logo](./assets/logo/cover-800X600.jpg)

> ⚠️ Warning: this library is under active development and may take time to reach as stable `v1.0` release.

Switchcraft is a Python library that provides light-weight AWS clients, common patterns, and helper functions that ease development of AWS applications.

## Installation

Switchcraft is available as a Python package.

```bash
pip install switchcraft
```

## Examples

### Access ARN elements as objects

```python
from switchcraft.conversion import Arn

arn = 'arn:aws:clouddirectory:us-west-2:12345678910:schema/published/cognito/1.0'
arn_elements = Arn(arn)

print(arn_elements.account_id)
#> 12345678910

print(arn_elements.region)
#> us-west-2
 
```

### Convert Parameters to Python dictionaries

```python
from switchcraft.conversion import param_list_to_dict

params = [{'Key': 'hello', 'Value': 'world'}, {'Key': 'hi', 'Value': 'there'}]
params_dict = param_list_to_dict(params)

print(params_dict)
#> {'hello': 'world', 'hi': 'there'}

hello = params_dict.get('hello')
print(hello)
#> world

```

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Author(s)

- **Derek Sudduth (AWS)**
