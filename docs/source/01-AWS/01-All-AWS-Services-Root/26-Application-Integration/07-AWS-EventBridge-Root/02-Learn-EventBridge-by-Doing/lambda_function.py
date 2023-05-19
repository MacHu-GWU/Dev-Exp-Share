import json


def jprint(data):
    text = "\n".join([
        "| " + line
        for line in json.dumps(data, indent=4).split("\n")
    ])
    print(text)


def lambda_handler(event, context):
    print("received event:")
    jprint(event)
    return {"status": "success"}
