
import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    print('Bucket name : ', bucket)
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print('Key name : ', key)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("RESPONSE HEADERS : " , dict(response))
        #res_json = response['Body'].read().decode("utf-8")
        
        ### Upload the file into a different Bucket.
        AWS_BUCKET_NAME = 'your destination bucket here..'
        
        stream = response['Body'].read()
        s3.put_object(Body=stream, Bucket=AWS_BUCKET_NAME, Key=key)
        print('put object is completed.')

        # Send response
        body = {
            "uploaded": "true",
            "bucket": AWS_BUCKET_NAME,
            "path": key,
        }
        return {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
