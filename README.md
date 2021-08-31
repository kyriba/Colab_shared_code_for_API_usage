# dev-portal-Two-ways-of-exporting-Third-Parties-sample



## Description

Python module can be used for writing API Colab samples. It consists of methods to requested API endpoints, launch report on Process Template and import files. 


## Usage

1.  Import the module within the code in Colab sample. It can be done by next way:

```python 
from subprocess import getoutput
getoutput("git clone -l -s https://github.com/OlhaLevko/sample_requests.git")
from sample_requests import sample_requests
```


2. Use methods inside cell by calling this module name. For example:

```python 
result = sample_requests.run_report(token,'ProssTemp')
```
