import boto3
import json
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
        # id_token = event['headers']['Authorization'].split(" ")
        id_token = event['authorizationToken']
        ## carlos id_t = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZjYmQ3ZjQ4MWE4MjVkMTEzZTBkMDNkZDk0ZTYwYjY5ZmYxNjY1YTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTE0OTgxMjg2Njk0MTg4OTg0NTE4IiwiZW1haWwiOiJjYXJsb3NzcGYyNEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6InJDVVIwRGQ3dFM2MXVxQ1FoRmdpeGciLCJuYW1lIjoiQ2FybG9zIFBhbGFjaW9zIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdpMFJIWGdKQ0RwYWI5cnhEM1JCLUxRRWlFQkMxcVBSQVlEUlo1NXlnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkNhcmxvcyIsImZhbWlseV9uYW1lIjoiUGFsYWNpb3MiLCJsb2NhbGUiOiJlcyIsImlhdCI6MTY1MTY4NTIzMSwiZXhwIjoxNjUxNjg4ODMxLCJqdGkiOiJjMDc1YTAyYTBjZjg3MGNlMmE3YWQ5OWMzZTc5ZjUzNGU5NGU0NWU2In0.LvP-dUbUDzOXXN9OJFAd6Y4x_PZ5aB7LbMya_od6WPniQ99ha3Joi6KZshdChgGDZDMhDiZRrNEB_vWa2NvP-9VF8FQu_dBwxFahX4e0jes0nXPEFEm_DcV6AxhmW8Phz-ZOP5sZ3_3MshhUkn0d9xZDClo0lFMPFMyw8zKBKtxK3izJ9-vvab0JoBPMWXpMEa2dA9YAJpMPzQuxUjhtFNh9FsNvIB7bDcxOVNgL5GfiQNsdskNs-cZB4AJEzIttutyiZGHHlPHm-9KtybD5XrsqitGI2iblSrakKelnIep2oZp6b74qMX5CS1LeKtSds_N_IpdF47KR5zbW64CEHA"
        id_t = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2MTY0OWU0NTAzMTUzODNmNmI5ZDUxMGI3Y2Q0ZTkyMjZjM2NkODgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNzI3NDYyNTMzODkyLXV0amUxc21tamVia2RxZzI1azFuZjY4bzdjbWthZDBuLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA2NzQwMDU3Nzc4MDIyMTI1MDE5IiwiZW1haWwiOiJsZW9hcmFuZ3VyZW4xMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImtiYmltOWpmc0ZCN1N4bDUyZnZZUHciLCJuYW1lIjoiTGVvbmFyZG8gQXJhbmd1cmVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqamE4aHFjOVhjOU03UXgwX2dBSnhNS3dDeTF5ZVJ0UF9xS3pUdlVtaz1zOTYtYyIsImdpdmVuX25hbWUiOiJMZW9uYXJkbyIsImZhbWlseV9uYW1lIjoiQXJhbmd1cmVuIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2NTE2ODU2NTUsImV4cCI6MTY1MTY4OTI1NSwianRpIjoiMDUyMDIyMjJkN2U1OGNiMzgzNDNkYjJlNWY0NGI5OWE3NzA1MDAxNiJ9.eA6SWXNjFvqXOajCDK1eop8YJ5AzVOI3kEiIcloG3KDc7QAzLtvF-LAYWsM9CNXBTm4tYOQ9NM0MDj8wtLlSQul90hdvQ9fsO8fxox9uov5SxGtFdBOPFaAwgpr_vwqZoBoyUdAX6yteebsvRw2hPht9bjT2pz41Z7RMrwdWrDlpM_9RtnePETQERUse_-MFpu-8uILZotU9UIfSDswNelDNT4NlsbQbYdDOrEy0IqqSt-CZ4ce1EXH9mXr02S862UplxTuKOHx0MPDfBUmj_qWjo7QbvwTEpEY7aqAJlAiOhOEgY0PC16SzHR_wvcUc7M9Ejdy4rZh18c8d0nd2dg"

        # idInformation = id_token.verify_oauth2_token(
        #     id_t,
        #     Request(),
        #     '727462533892-utje1smmjebkdqg25k1nf68o7cmkad0n.apps.googleusercontent.com')
        # print(idInformation)

        identity_client = boto3.client('cognito-identity')

        id_response = identity_client.get_id(
            IdentityPoolId= os.getenv('IDENTITY_POOL_ID'),
            Logins={
                'accounts.google.com': id_token
            }
        )

        # print(id_response)
        # # print('PASO 1')
        # response = identity_client.get_credentials_for_identity(
        #     IdentityId=id_response['IdentityId'],
        #     Logins={
        #         'accounts.google.com': id_t
        #     })
        
        # d = identity_client.describe_identity(IdentityId=id_response['IdentityId'])
        # # print('Describe => ', d)

        # # print('PASO 2')

        # access_key = response['Credentials']['AccessKeyId']
        # secret_key = response['Credentials']['SecretKey']
        # session_key = response['Credentials']['SessionToken']
        # print('Access Key => ', access_key)
        # print('Secret Key => ', secret_key)
        # print('Session Key => ', session_key)
        # print('response[]', response['Credentials'])
        # r = {
        #     'access-key': access_key,
        #     'secret_key': secret_key,
        #     'session_key': session_key
        # }
        policy = generatePolicy(id_response['IdentityId'], 'Allow', event['methodArn'])
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(policy),
        }
    except Exception as e:
        print('Error handler() => ', e)