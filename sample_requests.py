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
        print('token ' + token)
        return token
    except Exception as err:
        try:
           message = str(r.status_code)+" "+r.json()['message']
        except:
           message = str(r.status_code)+" "+r.reason
        raise AuthenticationError(message)

class Token:
  token = ''
  def __init__(self):
    raise Exception("Cannot create an istance")

  @staticmethod
  def updateToken():
    Token.token = login()

  @staticmethod
  def getToken():
    if Token.token == '':
       Token.updateToken()
    return Token.token

#@title Get Results
#@markdown This code calls the end point to retrieve data.
#@markdown A result will by return as text response body when return_type is not set up or is 'text'. When return_type set as 'binary'
#@markdown the result will be in binary representation.

def get_results(token, request, return_type = 'text'):
    try:
        token = Token.getToken()
        headers = {"Authorization": "Bearer " + token}
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.get(base_url + request, headers=headers)
        if 200 <= result.status_code < 300:
          if return_type == 'text':
            return result.text
          elif return_type == 'binary':
            return result.content
          else:
            print("return_type is incorrect")
            return
        elif result.status_code == 401:
          err = js.loads(result.text)
          if 'error' in err and err['error'] == 'invalid_token':
            Token.updateToken()
            return get_results(Token.getToken(), request)
          else:
            print(result.text)
        else:
          print(result.text)
          return
    except:
        print(result)
        return

#@title Post results
#@markdown This code allows to POST data in payload or as a stream
def post_results(token, request, payload, files, headers = {}):
    try:
        token = Token.getToken()
        headers["Authorization"] = "Bearer " + token
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.post(base_url + request, headers=headers, data=payload, files = files)
        if 200 <= result.status_code < 300:
          json_data = js.loads(result.text)
          return json_data
        elif result.status_code == 401:
          err = js.loads(result.text)
          if 'error' in err and err['error'] == 'invalid_token':
            Token.updateToken()
            return post_results(Token.getToken(), request, payload, files, headers)
          else:
            print(result.text)
        else:
          print(result.text)
          return
    except:
        print(result)
        return


#@title Put results
#@markdown This code allows to PUT data in payload or as a stream
def put_results(token, request, payload, files, headers = {}):
    try:
        token = Token.getToken()
        headers["Authorization"] = "Bearer " + token
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.put(base_url + request, headers=headers, data=payload, files = files)
        if 200 <= result.status_code < 300:
          json_data = js.loads(result.text)
          return json_data
        elif result.status_code == 401:
          err = js.loads(result.text)
          if 'error' in err and err['error'] == 'invalid_token':
            Token.updateToken()
            return put_results(Token.getToken(), request, payload, files, headers)
          else:
            print(result.text)
        else:
          print(result.text)
          return
    except:
        print(result)
        return

#@title Delete Results
#@markdown This code calls the end point to DELETE data
def delete_results(token, request, headers = {}):
    try:
        token = Token.getToken()
        headers["Authorization"] = "Bearer " + token
        cfg = pd.read_csv("config.csv")
        base_url = cfg['base_url'].values[0]
        result = requests.delete(base_url + request, headers=headers)
        if 200 <= result.status_code < 300:
          json_data = js.loads(result.text)
          return json_data
        elif result.status_code == 401:
          err = js.loads(result.text)
          if 'error' in err and err['error'] == 'invalid_token':
            Token.updateToken()
            return delete_results(Token.getToken(), headers)
          else:
            print(result.text)
        else:
          print(result.text)
          return
    except:
        print(result)
        return


class TaskResponse:
  status = ''
  taskId = ''
  content = ''
  def __init__(self):
    pass


#@title Launch report
#@markdown Code to manage report launch and retrieval of data in one function
#@markdown It launches the task and waits until completion.
#@markdown If task retuns result as binary it should be return_type set as 'binary'.
#@markdown If extended_response is set True the result will be returned as TaskResponse object otherwise
#@markdown as text response body.
def run_report(token, report, traceflag = False, return_type = 'text', extended_response = False):
    try:
        task_response = TaskResponse()
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
                task_response.status = status
                break
                time.sleep(1)
        print('\n')
        result = get_results(token, '/v1/process-templates/'+ report + '/files?taskId=' + taskId , return_type)
        if traceflag:
          logs = get_results(token, '/v1/process-templates/' + taskId + '/details')
          print ('\ntask details')
          print(pp_json(logs))
          print ('\nend task details')
        task_response.taskId = taskId
        task_response.content = result
        if extended_response:
          return task_response
        else:
          return result
    except:
        print(result)
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
          logs = get_results(token, '/v1/process-templates/' + taskId + '/details')
          print ('\ntask details')
          print(pp_json(logs))
          print ('\nend task details')
        return result
    except:
        print(result)
        return

#@title Import Data
#@markdown Code to Import Data in one function
def import_data (token, data, filename, task, isPayload, traceflag = False):
  try:
      if isPayload:
        payload=data
        files= {}
        headers = {'Content-Type': 'text/plain;charset=utf-8'}
        result = post_results(token, '/v1/data?fileName=' + filename, payload, files, headers)
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
        logs = get_results(token, '/v1/process-templates/' + taskId + '/details')
        print ('\ntask details')
        print(pp_json(logs))
        print ('\nend task details')
      return result
  except:
    return 'error'

#@title Pretty print
#@markdown Code to pretty print a json
def pp_json(json_thing, sort=False, indents=2):
    res = ''
    if type(json_thing) is str:
      print(js.dumps(js.loads(json_thing), sort_keys=sort, indent=indents))
    else:
      print(js.dumps(json_thing, sort_keys=sort, indent=indents))
    return res
