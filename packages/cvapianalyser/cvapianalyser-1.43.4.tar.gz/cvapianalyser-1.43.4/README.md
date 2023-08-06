# CV-APIAnalyser

cvapianalyser is a Python library for analysing the api traffic captured by CloudVector's APIShark against an APISPEC for identifying the gap in API coverage mostly useful in a QA environment to understand the gap in test coverage. 

Visit https://www.cloudvector.com/api-shark-free-observability-security-monitoring-tool/#apishark

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install cvapianalyser
```

## Usage

```python 
cvapianalyser 

****************************************************************************************************
CloudVector CommunityEdition - Coverage analysis plugin
****************************************************************************************************

Enter CommunityEdition(CE) host in format <host>:<port> : x.x.x.x:y
Enter your CommunityEdition(CE) username : sandeep
CommunityEdition(CE) password:
Enter recording in CE to compare with : recording1
```

instead of giving inputs every single time you can also alternatively create a file called my_cesetup.yaml in the path from where you are running the tool

```yaml 
ce_host:
ce_username:
ce_recording:
input_apispec:
```
you can have multiple such my_cesetup.yaml for different CE setup or different recordings and run them from specific paths for its corresponding reports

## License
[MIT](https://choosealicense.com/licenses/mit/)