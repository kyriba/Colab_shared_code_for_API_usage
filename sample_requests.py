#@title Import modules
import requests, base64
import re
import json as js
import pandas as pd
from io import StringIO
import csv
import copy

#@title Token generation
#@markdown This code calls the token end point with client-id and secret
class AuthenticationError(Exception):
    pass

def login():
    cfg = pd.read_csv("/content/config.csv")
    client_id = cfg['client_id'].values[0]
    client_secret = cfg['client_secret'].values[0]
    token_endpoint = cfg['token_url'].values[0]

    data = {'grant_type': 'client_credentials'}

    userpass = client_id + ':' + client_secret
    encoded_u = base64.b64encode(userpass.encode()).decode()
    auth_header = "Basic " + encoded_u
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': auth_header
    }

    r = requests.post(token_endpoint, headers=headers, data=data)
    try:
        response = r.json()
        token = response['access_token']
        # Put token in the session
        print(token)
        return token
    except Exception as err:
        try:
           message = str(r.status_code)+" "+r.json()['message']
        except:
           message = str(r.status_code)+" "+r.reason
        raise AuthenticationError(message)

#@title Get Results
#@markdown This code calls the end point to retrieve data
def get_results(token, request):
    try:
        headers = {"Authorization": "Bearer " + token}
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.get(base_url + request, headers=headers)
        if 200 <= result.status_code < 300:
          return result.text
        else:
          print(result.text)
          return
    except:
        return

#@title Post results
#@markdown This code allows to POST data in payload or as a stream
def post_results(token, request, payload, files, headers = {}):
    try:
        headers["Authorization"] = "Bearer " + token
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.post(base_url + request, headers=headers, data=payload, files = files)
        if 200 <= result.status_code < 300:
          json_data = js.loads(result.text)
          return json_data
        else:
          print(result.text)
          return
    except:
        return

#@title Pretty print
#@markdown Code to pretty print a json
def pp_json(json_thing, sort=False, indents=2):
    res = ''
    if type(json_thing) is str:
      print(js.dumps(js.loads(json_thing), sort_keys=sort, indent=indents))
    else:
      print(js.dumps(json_thing, sort_keys=sort, indent=indents))
    return res

#@title Launch report
#@markdown Code to manage report launch and retrieval of data in one function
#@markdown It launches the task and waits until completion
def run_report(token, report, traceflag = False):
    try:
        result = post_results(token, '/v1/process-templates/'+ report +'/run',"","")
        taskId = result[0]['taskId']
        if traceflag:
            print('\n Run task ' + str(taskId))
        while True:
            result = get_results(token, '/v1/process-templates/'+ taskId +'/status')
            json = js.loads(result)
            status = json["status"]
            if status == "Pending" or status == "In progress" or status == "Cancelling":
                print ('.', end='')
            else:
                print ('\n' + status)
            if status == "Warning" or status == "Complete" or status == "Error" or status == "Cancelled":
                break
                time.sleep(1)
        print('\n')
        result = get_results(token, '/v1/process-templates/'+ report + '/files?taskId=' + taskId )
        if traceflag:
          logs = get_results(token, '/v1/tasks/' + taskId + '/details')
          print(logs)
          print ('\ntask details')
          print(pp_json(logs, False, 2))
          print ('\nend task details\n')
        return result
    except:
        return

#@title Launch process
#@markdown Code to manage process launch
#@markdown It launchs the task and waits until completion
def run_process(token, report, traceflag = False):
    try:
        result = post_results(token, '/v1/process-templates/'+ report +'/run',"","")
        taskId = result[0]['taskId']
        if traceflag:
            print('\n Run task ' + str(taskId))
        while True:
            result = get_results(token, '/v1/process-templates/'+ taskId +'/status')
            json = js.loads(result)
            status = json["status"]
            if status == "Pending" or status == "In progress" or status == "Cancelling":
                print ('.', end='')
            else:
                print ('\n' + status)
            if status == "Warning" or status == "Complete" or status == "Error" or status == "Cancelled":
                break
                time.sleep(1)
        if traceflag:
            logs = get_results(token, '/v1/tasks/' + taskId + '/details')
            print ('\ntask details')
            print(pp_json(logs))
            print ('\nend task details\n')
        return result
    except:
        return


#@title Import Data
#@markdown Code to Import Data in one function
def import_data (token, data, filename, task, isPayload, traceflag):
  try:
      if isPayload:
        payload=data
        files= {}
        headers = {'Content-Type': 'text/plain;charset=utf-8'}
        result = post_results(token, '/v1/data?fileName=test', payload, files, headers)
        fileId = result['fileId']
      else:
        payload={}
        files=[
          ('file0', (filename, data, 'text/plain'))
        ]
        result = post_results(token, '/v1/data/files', payload, files)
        fileId = result[0]['fileId']

      if traceflag:
          print (result)

    # run task with file
      result = post_results(token, '/v1/process-templates/' + task + '/run?fileIds=' + fileId, "","")
      if traceflag:
        print (result)
      taskId = result[0]['taskId']

    # wait until process complete
      while True:
        result = get_results(token, '/v1/process-templates/' + taskId + '/status')
        json = js.loads(result)
        status = json["status"]
        if status == "Pending" or status == "In progress" or status == "Cancelling":
            print ('.', end='')
        else:
            print ('\n' + status)
        if status == "Warning" or status == "Complete" or status == "Error" or status == "Cancelled":
            break
            time.sleep(1)
      if traceflag:
        logs = get_results(token, '/v1/tasks/' + taskId + '/details')
        print ('\ntask details')
        print(pp_json(logs))
        print ('\nend task details\n')
      return result
  except:
    return 'error'