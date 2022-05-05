import boto3
import os
# from google.auth.transport.requests import Request
# from google.oauth2 import id_token

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
        # id_token = event['authorizationToken']
        id_t = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA2NzQwMDU3Nzc4MDIyMTI1MDE5IiwiZW1haWwiOiJsZW9hcmFuZ3VyZW4xMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IlFNbl84QzVWakZDeWJLUVJmeFlWQVEiLCJuYW1lIjoiTGVvbmFyZG8gQXJhbmd1cmVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqamE4aHFjOVhjOU03UXgwX2dBSnhNS3dDeTF5ZVJ0UF9xS3pUdlVtaz1zOTYtYyIsImdpdmVuX25hbWUiOiJMZW9uYXJkbyIsImZhbWlseV9uYW1lIjoiQXJhbmd1cmVuIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2NTE3NjQyMjYsImV4cCI6MTY1MTc2NzgyNiwianRpIjoiNmRiYWZjMzA2MDRkY2ZlNmE0ZWQ5M2YwYzg5ZmZlNjkzMmUxNDU4YyJ9.hnDPR9L7hw_yQT-qPZvrAmSrEYpflMqMmrm6crsLKkd5fZp0ihfJG8A3YUwlZ119Ik45hac8W-OLn03MoVx_Av3bFJ99UNlhGj5IZZVOJdCbww_6omUMB8fOdcglscc4lzJW6hONNTRJChkVSDrMWH6zK3Y4do8zpgrIxlI0hhANsGsQOwO3ay9GC8-hZwd2SujfP06-16xLjF8atIv5sSWZLfhFBIdF8NEWoyQBH2pWiDs85U8Rjvvt4j8_BDT2kF_fSJpbNdP1V813J8sJLy3WyHjv98uT8nt2Lr0JmPppWtOECMTp-jakLMrTduf-HnJg8Uux_2RdHQauLJgnLw"
        # idInformation = id_token.verify_oauth2_token(
        #     id_t,
        #     Request(),
        #     '727462533892-utje1smmjebkdqg25k1nf68o7cmkad0n.apps.googleusercontent.com')
        # print(idInformation)

        identity_client = boto3.client('cognito-identity')

        id_response = identity_client.get_id(
            IdentityPoolId= os.getenv('IDENTITY_POOL_ID'),
            Logins={
                'accounts.google.com': id_t
            }
        )

        response = identity_client.get_credentials_for_identity(
            IdentityId=id_response['IdentityId'],
            Logins={
                'accounts.google.com': id_t
            })
    
        if 'Credentials' in response:
            return generatePolicy(id_response['IdentityId'], 'Allow', event['methodArn'])

    except Exception as e:
        print('Error handler() => ', e)
        return generatePolicy(None, 'Deny', event['methodArn'])