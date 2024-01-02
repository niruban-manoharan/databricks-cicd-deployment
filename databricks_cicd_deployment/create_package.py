import json
import os
from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
import requests

DATABRICKS_API_KEY = os.environ["DATABRICKS_API_KEY"]
DATABRICKS_URL = os.environ["DEV_DATABRICKS_URL"]
HOME = os.environ["HOME"]


f2 = open(f"{HOME}"+'/components.yml')

component_data = load(f2, Loader=Loader)

headers = {}

headers["Authorization"] = f"Bearer {DATABRICKS_API_KEY}"

url = f"{DATABRICKS_URL}+/api/2.1/jobs/get"

for migration_job_id in component_data["jobs"]:
    job_raw = {}
    job_raw["job_id"] = str(migration_job_id)
    job = json.dumps(job_raw)
    
    response = requests.get(url, data=job, headers=headers, timeout=30)
    print(response.json())
    
    try:
        response_json = response.json()
    except JSONDecodeError:
        print('Response could not be serialized')
    job_name = response_json["settings"]["name"].replace(" ","")
    filename = f"{HOME}/job_json_export/"+job_name+".json"
    jsonfilename = f"{HOME}/job_json_export/"+job_name+"_converted.json"
    yamlfilename = f"{HOME}/databricks-cicd-deployment/databricks_cicd_deployment/resources/"+job_name+".yml"
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
