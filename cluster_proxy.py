"""
  This Python Flask script is intended to intercept Databricks cluster API requests, 
  modify or 'munge' the request and then foward the request on to DATABRICKS_HOST. 
  The response from DATABRICKS_HOST is then returned to the user of this HTTP proxy.
  
  This proxy runs by default on localhost, port 8080.
  Example invocation:
    curl --netrc \
          -v \
          -X POST \
          -H "Content-Type: application/json" \
          -d @cluster.json \
          http://localhost:8080/api/2.0/clusters/create

  cluster.json contains the JSON configuration of a cluster from the application (e.g. Informatica BDM)

  Example Usage:
    export DATABRICKS_HOST="https://myorg-myworkspace.cloud.databricks.com" python cluster_proxy.py


  Returns:
      : response from the DATABRICKS_HOST
"""
from flask import Flask, redirect, url_for, request
from requests import get, post
import os
import datetime

import logging
from http.client import HTTPConnection # py3


HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
)



def munge_request(data:dict):
    """Customize cluster request

    Args:
        data (dict): Create Cluster POST body data (JSON) type
    """
    # add components to the request
    data["policy_id"] = "E064568AAE0027DB"
    

    now = datetime.datetime.now()
    data["custom_tags"]["create_datetime"] = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    # modify components to the request
    if data["autotermination_minutes"]:
        if int(data["autotermination_minutes"]> 10):
            data["autotermination_minutes"] = 10

    # delete components of the policy
    if data["runtime_engine"]:
      del data["runtime_engine"]
    
    return data
  

app = Flask('__main__')
assert os.getenv("DATABRICKS_HOST", None) is not None
host = os.getenv("DATABRICKS_HOST", None)

@app.route('/', defaults={'path': ''},methods = ['POST', 'GET'])
@app.route('/<path:path>',methods = ['POST', 'GET'])
def proxy(path):
  if request.method == 'POST':
    """POST request is used to create things"""
    app.logger.debug(f'POST path: {path}')
    try:
      # Pull requester's Bearer token (PAT)
      headers = request.headers
      bearer = headers.get('Authorization')    # Bearer YourTokenHere
      token = bearer.split()[1]  # YourTokenHere
      
      #Make request to Databricks API
      return post(f'{host}/{path}', 
                  headers={"Authorization": f"Bearer {token}"}, 
                  json=munge_request(request.json)).content
      
    except Exception as e:
      app.logger.error(e)
      return f"Error see {__name__} logs"

  elif request.method == 'GET':   
    app.logger.debug(f'GET path: {path}')
    try:
      # Pull requester's Bearer token (PAT)
      headers = request.headers
      bearer = headers.get('Authorization')    # Bearer YourTokenHere
      token = bearer.split()[1]  # YourTokenHere
      
      # make request to Databricks
      return get(f'{host}/{path}',
                     headers={"Authorization": f"Bearer {token}"})
    except Exception as e:
      app.logger.error(e)
      return f"Error see {__name__} logs"
  else:
    return f"Request type not supported"

## -------------------------------------
app.run(host='127.0.0.1', port=8080, debug=False)
