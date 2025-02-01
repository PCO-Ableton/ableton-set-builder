
import json
import os

from lambda_function import lambda_handler

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "event.json"
    eventpath = os.path.join(script_dir, rel_path)
    with open(eventpath, "r") as f:
        event = f.read()
        event = json.loads(event)
        resp = lambda_handler(event, None)
        print(resp)