from textwrap import dedent
from enum import Enum
from struct import unpack_from
from pathlib import Path
from dataclasses import dataclass


_ENCODING        = 'utf_16_le'

_VALUE_START     = '['.encode(_ENCODING)
_VALUE_SEP       = ';'.encode(_ENCODING)
_VALUE_END       = ']'.encode(_ENCODING)

_LEN_START       = len(_VALUE_START)
_LEN_SEP         = len(_VALUE_SEP)
_LEN_END         = len(_VALUE_END)

_get_le_dword    = lambda x: unpack_from('<L', x, 0)[0]      # Little Endian 32 Bit Integer
_get_be_dword    = lambda x: unpack_from('>L', x, 0)[0]      # Big Endian 32 Bit Integer
_get_le_qword    = lambda x: unpack_from('<Q', x, 0)[0]      # Little Endian 64 Bit Integer
_get_be_qword    = lambda x: unpack_from('>Q', x, 0)[0]      # Big Endian 64 Bit Integer

class REG_TYPE(Enum):
    REG_NONE                        = 0     # no type
    REG_SZ                          = 1     # string type (ASCII)
    REG_EXPAND_SZ                   = 2     # string, includes %ENVVAR% (expanded by caller) (ASCII)
    REG_BINARY                      = 3     # binary format, callerspecific
    REG_DWORD                       = 4     # DWORD in little endian format
    REG_DWORD_LITTLE_ENDIAN         = 4     # DWORD in little endian format
    REG_DWORD_BIG_ENDIAN            = 5     # DWORD in big endian format 
    REG_LINK                        = 6     # symbolic link (UNICODE)
    REG_MULTI_SZ                    = 7     # multiple strings, delimited by \0, terminated by \0\0 (ASCII)
    REG_RESOURCE_LIST               = 8     # resource list? huh?
    REG_FULL_RESOURCE_DESCRIPTOR    = 9     # full resource descriptor? huh?
    REG_RESOURCE_REQUIREMENTS_LIST  = 10    #
    REG_QWORD                       = 11    # QWORD in little endian format
    REG_QWORD_LITTLE_ENDIAN         = 11    # QWORD in little endian format

class RegistryPolicyEntryException(Exception):
    pass

@dataclass
class RegistryPolicyEntry():
    key: str = None
    value: str = None
    type: REG_TYPE = None
    size: int = None
    data: bytes = None

    def parse(self, buffer: bytes) -> int:
        # Check we start with a [
        if not buffer.startswith(_VALUE_START):
            raise RegistryPolicyEntryException(f"Expected [")
        
        # Get the raw data
        raw_key, raw_value, raw_type, raw_size, raw_data = buffer[2:].split(sep=';'.encode(_ENCODING), maxsplit=4)

        # Set our values by processing the raw items
        self.key = raw_key.decode(_ENCODING).rstrip('\0')
        self.value = raw_value.decode(_ENCODING).rstrip('\0')
        self.type = REG_TYPE(_get_le_dword(raw_type))
        self.size = _get_le_dword(raw_size)

        # Set the self.data attribute based upon self.type and limited to self.size
        if self.type == REG_TYPE.REG_BINARY:
            self.data = raw_data[0:self.size]
        elif self.type in (REG_TYPE.REG_DWORD, REG_TYPE.REG_DWORD_LITTLE_ENDIAN):
            self.data = _get_le_dword(raw_data)
        elif self.type == REG_TYPE.REG_DWORD_BIG_ENDIAN:
            self.data = _get_be_dword(raw_data)
        elif self.type in (REG_TYPE.REG_SZ, REG_TYPE.REG_LINK):
            self.data = raw_data[0:self.size].decode(_ENCODING)
        elif self.type == REG_TYPE.REG_MULTI_SZ:
            raw_strings = raw_data[0:self.size].split(b'\0')
            self.data = [s.decode(_ENCODING) for s in raw_strings]
        elif self.type in (REG_TYPE.REG_QWORD, REG_TYPE.REG_QWORD_LITTLE_ENDIAN):
            self.data = _get_le_qword(raw_data)
        else:
            raise RegistryPolicyEntryException(f"Do not know how to decode type: {self.type}")

        # Calculate expected position of the value end marker
        end_position = (_LEN_START + len(raw_key) + _LEN_SEP + len(raw_value) + _LEN_SEP +
            len(raw_type) + _LEN_SEP + len(raw_size) + _LEN_SEP + self.size)

        # Check we have the end seperator at the expected position
        if not buffer.startswith(_VALUE_END, end_position):
            raise RegistryPolicyEntryException(f"Could not find ] at position {end_position}")

        # Return the total length of this value
        return end_position + _LEN_END

def RegistryPolicyException(Exception):
    pass

class RegistryPolicy(list):
    HEADER_LENGTH   = 8
    RP_SIGNATURE    = 0x67655250
    RP_VERSION      = 0x00000001

    def __init__(self):
        self.signature: int = None
        self.version: int = None
        self._file_bytes: bytes = None
    
    def _parse_header(self):
        # Check File Validity
        self.signature, self.version = unpack_from('<LL', self._file_bytes, 0)
        if self.signature != self.RP_SIGNATURE:
            raise RegistryPolicyException("Bad file - signature not matched")
        if self.version != self.RP_VERSION:
            raise RegistryPolicyException("Bad file - version not 0x1")

    def _parse_entries(self) -> int:
        offset = self.HEADER_LENGTH
        while offset < len(self._file_bytes):
            entry = RegistryPolicyEntry()
            offset += entry.parse(self._file_bytes[offset:])
            self.append(entry)
        
    def parse(self, policy_path):
        self._file_bytes = policy_path.read_bytes()
        self._parse_header()
        self._parse_entries()
