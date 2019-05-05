### Description
This project consists of:
 - Python modules which can be ran individually or as a group for processing 
 macOS artifacts of interest.
 - APOLLO modules ([Apple Pattern of Life Lazy Output'er (APOLLO)](https://github.com/mac4n6/APOLLO))

### Usage
Change the current working directory to the directory containing the scripts
from this repository.

To parse all artifacts directly from a filesystem, enter the following command
and follow the instructions:
 - `python3 process_coreduet.py`

To parse a database with a single module, enter the following command and follow
the instructions:
 - `python3 modlues/{modlue_name}.py`

<b>Note</b>: You may need root privileges to access the databases parsed by the
scripts.
