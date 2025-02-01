import base64
import json
import os
from ableton_set_builder import AbletonSetBuilder

def time_signature_to_id(time_signature):
    if time_signature == "3/4" or time_signature == "3/8":
        return 200
    elif time_signature == "4/4" or time_signature == "4/8":
        return 201
    elif time_signature == "6/4" or time_signature == "6/8":
        return 203
    else:
        return 201
    
# Lambda function input format (POST):
lambda_input = { 
    "name": "string", 
    "bpm": 120, 
    "measure": "4/4", 
    "color": 13
}

def lambda_handler(event, context):
    try:
        method = event['requestContext']['http']['method']

        if method != 'POST':
            return {
                'statusCode': 401,
            }
            
        # check if the request has the body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "message": "body not found",
                })
            }
        
        body = event['body']
        
        # check if the body is a json
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "message": "body is not a json",
                })
            }
        
        # check if body is list:
        if not isinstance(body, list):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "message": "body is not a list",
                })
            }
        
        if len(body) == 0:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "message": "body is empty",
                })
            }
            
        # check if body has the required keys: name (string), bpm (int), measure (string)
        for item in body:
            if lambda_input.keys() != item.keys():
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        "message": "body does not have the required keys",
                    })
                }
            
            for key, tif in lambda_input.items():
                print(key, tif)
                if not isinstance(item[key], type(tif)):
                    return {
                        'statusCode': 400,
                        'body': json.dumps({
                            "message": "body has wrong types",
                        })
                    }
        
        # all checks passed, lets create some ableton files

        # Create an instance of AbletonSetBuilder with the template XML or ALS file
        
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "templates/click-manuel.als"
        als_file_path = os.path.join(script_dir, rel_path)

        builder = AbletonSetBuilder(als_file_path)
        
        # Clear the scenes and tracks in the template file
        builder.clearScenes()
        
        # Add scenes
        for i, item in enumerate(body):
            builder.add_scene(
                i+1, 
                item['name'], 
                color=item['color'], 
                tempo=item['bpm'], 
                time_signature_id=time_signature_to_id(item["measure"])
            )
        
        # Build the new Ableton Live set
        xml = builder.to_xml()

        message_bytes = xml.encode("utf-8")
        base64_bytes = base64.b64encode(message_bytes)
        xml_encoded_string = base64_bytes.decode('ascii')
        
        print("Ableton Live set created successfully!")

        return {
            'statusCode': 200,
            'body': json.dumps({
                "status": "success",
                "data": xml_encoded_string,
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": str(e),
            })
        }