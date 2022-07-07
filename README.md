# samwise
Tools for running interruptible jobs in containers

## Installation
```bash
pip install .
```

## Basic usage - file synchronization
Python callables
```python3
from samwise import run

dirmapping = {remote: local for remote, local in things_i_want_to_sync.items()}

run(process_i_want_documented, dirmapping)
```

Shell commands
```bash
python scripts/run.py commandfilename remote1::local1 remote2::local2
```
