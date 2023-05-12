# kfs

## Usage

### Initialize the database

```shell
kfs db init
```

## Development

### Local environment setup

1. Ensure you have `conda` installed (once)
2. Run `make setup` (initially, or when dependencies are changed)
3. Run `conda activate ./env` (every time)
4. Run `pre-commit install` (once)

## Makefile targets

We use a `Makefile` for automating common development tasks.
Each target in this list can be run with `make <target>`:

<!-- [[[cog
import subprocess
from textwrap import dedent
from typing import NamedTuple

raw_text = dedent(subprocess.check_output("make", text=True))


class MakefileTarget(NamedTuple):
    target: str
    description: str


makefile_targets = []
for line in raw_text.splitlines():
    target, _, description = line.partition(" ")
    makefile_targets.append(
        MakefileTarget(target=target, description=description.strip())
    )

max_target_len = max(len(t.target) for t in makefile_targets)
max_description_len = max(len(t.description) for t in makefile_targets)

cog.outl("<!- THE FOLLOWING CODE IS GENERATED BY COG VIA PRE-COMMIT. ANY MANUAL CHANGES WILL BE LOST. ->".replace("-", "--"))
lines = []
cog.outl(f"| {'Target':{max_target_len + 2}s} | {'Description':{max_description_len}s} |")
cog.outl(f"|{'-'*(max_target_len + 4)}|{'-'*(max_description_len + 2):{max_description_len}s}|")
for t in makefile_targets:
    cog.outl(f"| {'`' + t.target + '`':{max_target_len + 2}s} | {t.description:{max_description_len}s} |")
]]] -->
<!-- THE FOLLOWING CODE IS GENERATED BY COG VIA PRE--COMMIT. ANY MANUAL CHANGES WILL BE LOST. -->
| Target      | Description                                           |
|-------------|-------------------------------------------------------|
| `clean`     | Clean up cache and temporary files                    |
| `clean-all` | Clean up, including build files and conda environment |
| `help`      | Display help on all Makefile targets                  |
| `setup`     | Setup local dev conda environment                     |
| `test`      | Run all the unit tests                                |
| `tox`       | Run tox to test in isolated environments              |
<!-- [[[end]]] -->
