from state import BeefreeState
import json
import requests
def convertsimpleschema(state: BeefreeState):
    bearer_token_response=requests.post(
        "https://auth.getbee.io/loginV2",
        headers={'Accept':'application/json','Content-Type':'application/json'},
        json={
        "client_id": '9c45f43d-9c00-4fc9-b5e1-a57240d7ac15',
        "client_secret": '8So8YSELofFayDF0c8VZ6fnT8vgMJ12gxhV6hdqY1ERY4JBzVJTM',
        "uid": "sumanth"
        }
    )
    bearer_token=bearer_token_response.json()['access_token']
    print(state.original_schema)

    response=requests.post(
        "https://api.getbee.io/v1/conversion/full-to-simple-json",
        headers={"Authorization":f"Bearer {bearer_token}", "Content-Type":"application/json"},
        json=state.original_schema
    )
    data=response.json()
    print('Full schema',state.original_schema)
    return {'simple_schema':data}
