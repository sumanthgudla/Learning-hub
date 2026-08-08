import json
from pathlib import Path
from state import BeefreeState
def validate(state: BeefreeState):
    json1=state.simple_schema
    Allowed_list=('heading','paragraph')
    data=json.loads(json1)
    template=data['template']
    rows=template['rows']
    for rowidx,row in enumerate(rows):
        coulms=row['columns']
        for colidx,col in enumerate(coulms):
            modules=col['modules']
            for modix,mod in enumerate(modules):
                if mod['type'].lower() in Allowed_list:
                    print(mod['type'])
    return {'is_validated':True}