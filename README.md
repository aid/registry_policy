# Microsoft Registry File Parser

The **`registry_policy`** package parses Microsoft Windows Registry Policy Files – files typically with the extension `.pol` – as used by Microsoft's Group Policy system.

The parsing of this file type is based upon the Microsoft's documentation located at:

[Registry Policy File Format](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/policy/registry-policy-file-format)


## Home Page

[Github Homepage](https://github.com/aid/registry_policy/)

## Usage

### Overview
Usage is simple:

1. Import the `registry_policy` module.
1. Create a `RegistryPolicy` object.
1. Call the `parse()` method on your new `RegistryPolicy` object with a Path pointing to the `.pol` file you wish to parse.
1. The `RegistryPolicy` object can now be tread as a list containing the policy values from the `.pol` file.

### Group Policy Values

The group policy values are of type `RegistryPolicyEntry` and that class contains the following items:

*   **key** – A `str` object with the path within the Windows Registry for this item
*   **value** – A `str` object which is the *name* of the key
*   **type** – A `REG_TYPE` object which states the type of the data
*   **size** – An `int` object containing the length of the data
*   **data** – The actual data itself, the type depending upon the value of the type field

### Group Policy Value Types

The `type` field can be one of the following values, with the corresponding type of the data feld:

|Type Value                      |Data Field Type |Description                  |
|--------------------------------|----------------|-----------------------------|
|REG_SZ                          |str             |String                       |
|REG_BINARY                      |bytes           |Binary data                  |
|REG_DWORD                       |int             |32-bit integer               |
|REG_DWORD_LITTLE_ENDIAN         |int             |32-bit integer               |
|REG_DWORD_BIG_ENDIAN            |int             |32-bit integer               |
|REG_LINK                        |str             |Symbolic link                |
|REG_MULTI_SZ                    |List[str]       |Multiple strings as a list   |
|REG_QWORD                       |int             |64-bit integer               |
|REG_QWORD_LITTLE_ENDIAN         |int             |64-bit integer               |

### Example

A simple example of the usage of this module:

```python
from pathlib import Path
from registry_policy import RegistryPolicy

policy = RegistryPolicy()
policy.parse(Path('registry.pol'))

for item in policy:
    print(f"{item.key} \\ {item.value} = {item.data}")
```
