# sample_requests



## Description

Python module can be used for writing API Colab samples. It consists of methods to requested API endpoints, launch report on Process Template and import files. 


## Usage

1.  Import the module within the code in Colab sample. It can be done by next way:

```python 
from subprocess import getstatusoutput
servicePack = "21SP6" #@param ['DEMO', 'SP7','21SP6'] {allow-input: true}

if servicePack == 'DEMO':
  branch = 'main'
else:
  branch = servicePack
print(branch)
rm = getstatusoutput("rm sample_requests -rf ") 
clone = getstatusoutput("git clone -l -s --branch " +  branch + " https://github.com/OlhaLevko/sample_requests.git") 
import importlib
importlib.reload(sample_requests)
from sample_requests import sample_requests
```


2. Use methods inside cell by calling this module name. For example:

```python 
result = sample_requests.run_report(token,'ProssTemp')
```
