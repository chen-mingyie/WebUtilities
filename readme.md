# Web Utilities

Retrieve company descriptions from Google. Retrieve lat/lon from Open Street Map.

## Installation

1. Install Anaconda as your Python package manager ([Anaconda download page](https://www.anaconda.com/download/success))
2. SRO-lightweight-env.zip contains the Python environment necessary to run the web utils. Unzip and place it in the director(ies) used by Anaconda to store environments
3. To check the director(ies) where Anaconda stores environments in your machine, open Anaconda prompt and enter the cli command `conda config --show envs_dirs` to display the env_dirs.

```bash
(base) C:\Users\admin>conda config --show envs_dirs
envs_dirs:
  - C:\Users\admin\Anaconda3\envs
  - C:\Users\admin\.conda\envs
  - C:\Users\admin\AppData\Local\conda\conda\envs
```
4. To activate the environment

```bash
(base) C:\Users\admin>conda activate SRO-lightweight-env
```

## Usage
Change  the current directory to the one containing the Web Utilities source files.
```bash
(SRO-lightweight-env) C:\Users\admin>d:
(SRO-lightweight-env) D:\>cd D:\cmingyi\PycharmProjects\WebUtilities
```

### get-supplier-desc.py

Get help using the following command `python get-supplier-desc.py -help`
```bash
(SRO-lightweight-env) D:\cmingyi\PycharmProjects\WebUtilities>python get-supplier-desc.py -help
usage: get-supplier-desc.py [-h] --supplierfile

Scrape supplier descriptions from internet. Results will be exported to parent folder of the input file.

options:
  -h, --help       show this help message and exit
  --supplierfile   filepath containing a list of supplier names; must contain a column called "name".
```
Start the get-supplier-desc function using `python get supplier-desc.py --supplierfile <your input file path>`
```bash
(SRO-lightweight-env) D:\cmingyi\PycharmProjects\WebUtilities>python get-supplier-desc.py --supplierfile <your input file path>
```

### retrieve-latlon.py
Get help using the following command `python get-supplier-desc.py -help`
```bash
(SRO-lightweight-env) D:\cmingyi\PycharmProjects\WebUtilities>python retrieve-latlon.py -help
usage: retrieve-latlon.py [-h] --searchtextsfile

Call Open Stream Map API to retrieve lat, lon, address of a search query. Results will be exported to parent folder of
the input file.

options:
  -h, --help          show this help message and exit
  --searchtextsfile   filepath containing a list of search queries; must contain a column called "searchtext".
```
Start the retrieve-latlon function using `python retrieve-latlon.py --searchtextsfile <your input file path>`
```bash
(SRO-lightweight-env) D:\cmingyi\PycharmProjects\WebUtilities>python retrieve-latlon.py --searchtextsfile <your input file path>
```
### Automation Open Street Map.xlsm

This macro-enabled Excel file serves the same functionality as retrieve-latlon.py