
# Colab_shared_code_for_API_usage


## Description

Python module can be used for writing API Colab samples. It consists of methods to requested API endpoints, launch report on Process Template and import files. 


## Usage

1.  Import the module within the code in Colab sample. It can be done by next way:

```python 
#@title Select **servicePack** the Sample should run
from subprocess import getstatusoutput
servicePack = "DEMO" #@param ['DEMO'] {allow-input: true}

if servicePack == 'DEMO':
  branch = 'main'
else:
  branch = servicePack
print(branch)
rm = getstatusoutput("rm Colab_shared_code_for_API_usage -rf ") 
clone = getstatusoutput("git clone -l -s --branch " +  branch + " https://github.com/kyriba/Colab_shared_code_for_API_usage.git") 
import importlib

enableFormatterDF = True #@param {type:"boolean"}
from google.colab import data_table

if enableFormatterDF is True:
  data_table.enable_dataframe_formatter()
else:
  data_table.disable_dataframe_formatter()

try:  
  importlib.reload(sample_requests)
except:
  print()
from Colab_shared_code_for_API_usage import sample_requests
from Colab_shared_code_for_API_usage.sample_requests import Token
```


2. Use methods inside cell by calling this module name and use Token.getToken() expresion to put token parameter. For example:

```python 
result = sample_requests.run_report(Token.getToken(),'ProcessTemplate')
```
