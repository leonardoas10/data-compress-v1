import boto3
import json

identity_pool_id = 'us-east-1:d8b354dc-890e-449a-aa63-3fb78ecaee88'

def handler(event, context) -> str:
    try:
        id_token = event['headers']['Authorization']

        identity_client = boto3.client('cognito-identity')

        id_response = identity_client.get_id(
            IdentityPoolId='us-east-1:d8b354dc-890e-449a-aa63-3fb78ecaee88',
            Logins={
                'accounts.google.com': id_token
            }
        )
        print('PASO 1')
        response = identity_client.get_credentials_for_identity(
            IdentityId=id_response['IdentityId'],
            Logins={
                'accounts.google.com': id_token
            })
        
        d = identity_client.describe_identity(IdentityId=id_response['IdentityId'])
        print('Describe => ', d)

        print('PASO 2')

        access_key = response['Credentials']['AccessKeyId']
        secret_key = response['Credentials']['SecretKey']
        session_key = response['Credentials']['SessionToken']
        print('Access Key => ', access_key)
        print('Secret Key => ', secret_key)
        print('Session Key => ', session_key)
        print('response[]', response['Credentials'])
        r = {
            'access-key': access_key,
            'secret_key': secret_key,
            'session_key': session_key
        }
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(r),
        }
    except Exception as e:
        print('Error handler() => ', e)