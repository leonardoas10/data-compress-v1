import boto3
import os

def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
    policyDocument = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'FirstStatement',
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': methodArn
            }
        ]
    }

    authResponse['policyDocument'] = policyDocument

    print(authResponse)
 
    return authResponse

def handler(event, context) -> str:
    try:
        print('Event => ', event)
        id_token = event['authorizationToken']

        identity_client = boto3.client('cognito-identity')

        id_response = identity_client.get_id(
            IdentityPoolId= os.getenv('IDENTITY_POOL_ID'),
            Logins={
                'accounts.google.com': id_token
            }
        )

        response = identity_client.get_credentials_for_identity(
            IdentityId=id_response['IdentityId'],
            Logins={
                'accounts.google.com': id_token
            })
    
        if 'Credentials' in response:
            return generatePolicy(id_response['IdentityId'], 'Allow', event['methodArn'])

    except Exception as e:
        print('Error handler() => ', e)
        return generatePolicy(None, 'Deny', event['methodArn'])


        #os.system("aws s3 cp {} - | split -d -l {} --filter 'aws s3 cp - {}.$FILE.sh' -".format(infile, linecount,outfile))