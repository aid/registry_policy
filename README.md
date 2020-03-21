# Microsoft Registry File Parser

## Introduction

This **python3** package – `registry_policy` – parses Microsoft Windows Registry Policy Files as used by Microsoft's Group Policy system.  These files typically use the extension `.pol`. 

The project's homepage is on Guthub at:

[https://github.com/aid/registry_policy/](https://github.com/aid/registry_policy/)

The parsing of this file type is based upon the Microsoft's documentation located at:

[https://docs.microsoft.com/](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/policy/registry-policy-file-format)


## Usage

### Overview

Usage is straightforward:

1. Import the `registry_policy` module.
1. Create a `RegistryPolicy` object.
1. Call the `parse()` method on your new `RegistryPolicy` object with a single parameter of type `Path` pointing to the `.pol` file you wish to parse.
1. The `RegistryPolicy` object can now be treated as a list who's contentas arethe policy entries from the `.pol` file, each entry represented as a `RegistryPolicyEntry` object.

### Registry Policy Entries

Each of the registry policy entries are of type `RegistryPolicyEntry`; and that class contains the following fields:

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

for entry in policy:
    print(f"{entry.key} \\ {entry.value} = {entry.data}")
```
