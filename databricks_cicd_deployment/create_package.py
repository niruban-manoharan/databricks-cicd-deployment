import json
import os
from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
import requests

DATABRICKS_API_KEY = os.environ["DATABRICKS_API_KEY"]
DATABRICKS_URL = os.environ["DEV_DATABRICKS_URL"]


f2 = open('/home/runner/work/databricks/databricks/components.yml')

component_data = load(f2, Loader=Loader)

headers = {}

headers["Authorization"] = f"{DATABRICKS_API_KEY}"

url = f"{DATABRICKS_URL}"

for migration_job_id in component_data["jobs"]:
    job_raw = {}
    job_raw["job_id"] = str(migration_job_id)
    #job = "'"+json.dumps(job_raw)+"'"
    job = json.dumps(job_raw)
    #print(job)
    #print(type(job))
    response = requests.get(url, data=job, headers=headers, timeout=30)
    response_json = response.json()
    #print(response_json)
    job_name = response_json["settings"]["name"].replace(" ","")
    filename = f"job_json_export/"+job_name+".json"
    jsonfilename = f"job_json_export/"+job_name+"_converted.json"
    yamlfilename = f"databricks_cicd_deployment/resources/"+job_name+".yml"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    input_json_file = open(filename, "w")
    json.dump(response_json, input_json_file)
    input_json_file.close()
    f = open(filename)
    data = json.load(f)
    output = {}
    output = {data["settings"]["name"]: data["settings"]}
    output_2 = {"resources": {"jobs": output}}
    output_json_file = open(jsonfilename, "w")
    json.dump(output_2, output_json_file)
    output_json_file.close()
    os.system("cat "+jsonfilename+" | python json2yaml.py > "+yamlfilename)