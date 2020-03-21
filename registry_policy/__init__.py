# -*- coding: utf-8 -*-

"""
Microsoft Registry File Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple example of the usage of this module:

    from pathlib import Path
    from registry_policy import RegistryPolicy

    policy = RegistryPolicy()
    policy.parse(Path('registry.pol'))

    print (f"Policy loaded with {len(policy)} entries:")
    for entry in policy:
        print(f"{entry.key} \\ {entry.value} = {entry.data}")

Project page and futher documentation available at:

    <https://github.com/aid/registry_policy>


:copyright: (c) 2020 by Adrian Bool.
:license: MIT License, see LICENSE for more details.

"""

from .registry_policy import REG_TYPE
from .registry_policy import RegistryPolicyEntryException
from .registry_policy import RegistryPolicyEntry
from .registry_policy import RegistryPolicyException
from .registry_policy import RegistryPolicy
