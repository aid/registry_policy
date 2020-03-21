from pathlib import Path
from registry_policy import RegistryPolicy

POLICY_PATH=Path('registry.pol')

policy = RegistryPolicy()
policy.parse(POLICY_PATH)

print (f"Policy loaded with {len(policy)} entries:")
for entry in policy:
    print(f"{entry.key} \\ {entry.value} = {entry.data}")
