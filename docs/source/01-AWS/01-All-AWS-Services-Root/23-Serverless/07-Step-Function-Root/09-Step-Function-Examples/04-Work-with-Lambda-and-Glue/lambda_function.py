import json

def lambda_handler(event, context):
    print("event:")
    print(json.dumps(event))
    return event
