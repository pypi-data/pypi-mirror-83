import time
import requests

requests.packages.urllib3.disable_warnings()


# Collapsing multiple REST calls into single function
def execute_rest(method, url, bearertoken, payload):
    headers = {
        'Authorization': 'BEARER ' + bearertoken + '',
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    json = response.json()  # type: object

    return json


# Execute tenant workflow based on evaluation criteria supplied by child functions
# Returns job execution ID for status check
def call_tenant_workflow(bearertoken, ostype, instanceid):
    workflow = get_tenant_workflow_id(instanceid, ostype, bearertoken)

    url = "https://morpheus.tomcartlab.com/api/task-sets/" + str(workflow) + "/execute"

    payload = ('{"job":{ "targetType": "instance", "instances": [' + instanceid + '] }}')

    response = execute_rest("POST", url, bearertoken, payload)

    return response["job"]["id"]


# Execute tenant workflow based on evaluation criteria supplied by child functions
# Returns job execution ID for status check
def call_group_workflow(bearertoken, ostype, instanceid):
    workflow = get_group_workflow_id(instanceid, ostype, bearertoken)

    url = "https://morpheus.tomcartlab.com/api/task-sets/" + str(workflow) + "/execute"

    payload = ('{"job":{ "targetType": "instance", "instances": [' + instanceid + '] }}')

    response = execute_rest("POST", url, bearertoken, payload)

    return response["job"]["id"]


def get_instance_tenant_id(instanceid, bearertoken):
    url = "https://morpheus.tomcartlab.com/api/instances/" + str(instanceid) + ""
    response = execute_rest("GET", url, bearertoken, "")
    tenantName = response["instance"]["accountId"]
    return tenantName

def get_group_workflow_id(instanceid, ostype, bearertoken):
    url = "https://morpheus.tomcartlab.com/public-archives/download/gnma/workflow_id.json"

    response = requests.get(url, verify=False)
    group_code = get_group_code(instanceid, bearertoken)
    account_id = get_instance_tenant_id(instanceid, bearertoken)
    data = response.json()
    group_id = data["tenantIds"][str(account_id)]["groupCode"][group_code][ostype]
    return group_id

def get_tenant_workflow_id(instanceid, ostype, bearertoken):
    url = "https://morpheus.tomcartlab.com/public-archives/download/gnma/workflow_id.json"

    response = requests.get(url, verify=False)
    group_code = "all"
    account_id = get_instance_tenant_id(instanceid, bearertoken)
    data = response.json()
    group_id = data["tenantIds"][str(account_id)]["groupCode"][group_code][ostype]
    return group_id

def await_job_exec_status(jobid, bearertoken):
    url = "https://morpheus.tomcartlab.com/api/job-executions/" + str(jobid) + ""
    status = ""
    while status == "queued" or status == "running" or status == "":
        response = execute_rest("GET", url, bearertoken, "")
        status = response["jobExecution"]["status"]
        time.sleep(2)
    return status


def get_group_code(instanceid, bearertoken):
    url = "https://morpheus.tomcartlab.com/api/instances/" + str(instanceid) + ""

    response_group_id = execute_rest("GET", url, bearertoken, "")

    group_id = response_group_id["instance"]["group"]["id"]
    url2 = "https://morpheus.tomcartlab.com/api/groups/" + str(group_id) + ""

    response_group_code = execute_rest("GET", url2, bearertoken, "")

    group_code = response_group_code
    return group_code["group"]["code"]


