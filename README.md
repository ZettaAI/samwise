# samwise
Tools for running interruptible jobs in containers

## Installation
```bash
pip install .
```
```bash
pip install git+https://github.com/ZettaAI/samwise.git
```

## Basic usage - file synchronization
#### Python callables
The simplest use of this tool is as a wrapper around a python Callable that regularly synchronizes files within some directories to some external storage.
```python3
from samwise import run

dirmapping = {remote: local for (remote, local) in things_i_want_to_sync.items()}

run(process_i_want_documented, dirmapping)
```

#### Shell commands
You can also wrap arbitrary shell commands in a similar way.
```python3
from samwise import runcmd

dirmapping = {remote: local for (remote, local) in things_i_want_to_sync.items()}

runcmd(["longrunningcmd", "arg1", "arg2"], dirmapping)
```

...or using the command line
```bash
python scripts/run.py commandfilename remote1::local1 remote2::local2
```

## Running compatible containers in the cloud
This package also provides some small wrappers to make launching containers running commands easier. Using this part of the tools means that you don't need to worry about configuring instances and coordinating jobs. Simply wrap the relevant code into a docker container and launch your instances from any other machine you'd like.
```bash
python scripts/fly.py ${commandfilename} ${dockerimage} ${instancename}
```

See the scripts help documentation for more information and arguments.
