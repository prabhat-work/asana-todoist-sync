from todoist.api import TodoistAPI
from django.shortcuts import render
from django.http import JsonResponse
import requests
import json


def req(request):
    requests.post(
        'https://app.asana.com/api/1.0/webhooks',
         headers={"Authorization": "Bearer 0/f2f39a9f7c123cb7fc7ac64d2664d6b7"},
         data={"resource":"1118135221202949" ,"target":"http://localhost:8000/payload"}    
        )

def handle_payload(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body) # convert json data to python dict 
        if 'events' in received_json_data.keys():
            events=received_json_data["events"]


            for event in events:
                id=event["resource"]
                type=event["type"]
                source=None    # by defualt make  url-source none
                if type == "task":
                    source="https://app.asana.com/api/1.0/tasks/" + str(id)

                if not source==None:
                    data=requests.get(
                        url=source,
                        headers={"Authorisation":"Bearer "}
                    )
                
                    jsdata=json.loads(data)
                
                    if jsdata['data']['assignee']['name']=='Stebin Ben':
                        task_name=jsdata['data']['name']
                        api=TodoistAPI('7441fc19459367f6d69efaa79175461b521e257d')
                        api.sync()
                        project_name = jsdata['data']['memberships']['project']['name']
                        project1 = api.projects.add(project_name)
                        api.items.add(task_name,project1['id'])
                        api.commit()

        else:
            headers=request.headers
            x_hook=headers['X-Hook-Secret']   
            return JsonResponse({"X-Hook-Sercret":x_hook})
    