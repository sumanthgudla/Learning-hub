import json
from pathlib import Path
from state import BeefreeState
def validate(state: BeefreeState):
    ai_schema_json=state.ai_schema
    print('json of ai schema',ai_schema_json)

    
    return {'is_validated':True}