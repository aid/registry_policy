# Microsoft Windows Group Policy FileParser

The **`gpo`** package parses Microsoft Windows Group Policy Files – files typically with the extension `.pol`.

The parsing of this file is based upon the Windows documentation located at:

[Registry Policy File Format](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/policy/registry-policy-file-format)


## Home Page

[Github Homepage](https://github.com/aid/gpo/)

## Usage

### Overview
Usage is simple:

1. Import the `gpo` module.
1. Create a `GroupPolicy` object.
1. Call the `parse()` method on your new `GroupPolicy` object with a Path pointing to the `.pol` file you wish to parse.
1. The `GroupPolicy` object can now be tread as a list containing the policy values from the `.pol` file.

### Group Policy Values

The group policy values are of type `GroupPolicyValue` and that class contains the following items:

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
from gpo import GroupPolicy

gp = GroupPolicy()
gp.parse(Path('registry.pol'))

for item in gp:
    print(f"{item.key} \\ {item.value} = {item.data}")
```
