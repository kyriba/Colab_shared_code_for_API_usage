# Colab_shared_code_for_API_usage



## Description

Python module can be used for writing API Colab samples. It consists of methods to requested API endpoints, launch report on Process Template and import files. 


## Usage

1.  Import the module within the code in Colab sample. It can be done by next way:

```python 
#@title Select **servicePack** the Sample should run
from subprocess import getstatusoutput
servicePack = "DEMO" #@param ['DEMO', '21SP8', '21SP7','21SP6'] {allow-input: true}

if servicePack == 'DEMO':
  branch = 'main'
else:
  branch = servicePack
print(branch)
rm = getstatusoutput("rm sample_requests -rf ") 
clone = getstatusoutput("git clone -l -s --branch " +  branch + " https://github.com/kyriba/Colab-shared-code-for-API-usage.git") 
import importlib
try:  
  importlib.reload(sample_requests)
except:
  print()
from sample_requests import sample_requests
```


2. Use methods inside cell by calling this module name. For example:

```python 
result = sample_requests.run_report(token,'ProcessTemplate')
```
