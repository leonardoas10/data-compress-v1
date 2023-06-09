import boto3
from datetime import datetime
import json
import os
import mysql.connector

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

s3 = boto3.client('s3')

def handler(event, context):
    try:
        # init_time = datetime.now()
        # print('Init Lambda => ', init_time)
        
        data = json.loads(event['body'])
        user = data['user']
        cursor = db.cursor(dictionary=True)

        sql_get_user = "SELECT * FROM users WHERE email = '{}'".format(user['email'])
        cursor.execute(sql_get_user)
        fetch_user = cursor.fetchall()
        exist_user = len(fetch_user)

        if exist_user == 0: ## CREATE NEW USER
            sql_user = "INSERT INTO users (email, firstname, lastname, profile_img) VALUES (%s, %s, %s, %s)" 
            # val = (user['email'], user['givenName'], user['familyName'], user['imageUrl'])
            val = (user['email'], user['given_name'], user['family_name'], user['picture'])
            cursor.execute(sql_user, val)
            db.commit()
            cursor.execute(sql_get_user)
            user_id = cursor.fetchall()[0]['id']
        else:
            user_id = fetch_user[0]['id']

        urls = dict()
        
        files = enumerate(data['files'])
        for index, f in files:
            split_path = data["paths"][index].rsplit(".", 1)
            name = split_path[0]
            extension = split_path[-1]
            sql_file = "INSERT INTO files (user_id, name, extension, type, size, name_extension, original_name) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
            val = (user_id, name, extension, data['types'][index], data['sizes'][index], data["paths"][index], f['path'])
            cursor.execute(sql_file, val)
            db.commit()
            custom_key = "{}/{}".format(user_id, data["paths"][index])
            presigned_url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': os.getenv("S3_BEFORE_COMPRESS_FILES"),
                    'Key': custom_key,
                    'ContentType' : data['types'][index]
                }
            )
            urls[custom_key] = presigned_url

          
        # duration = datetime.now() - init_time
        # print('Finish Time in seconds => ', duration.total_seconds())
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                    'urls': urls,
                    'user_id': user_id
                    }, sort_keys=True)
        }
    except Exception as e:
        print('Error => ', e)


        # temp_url = s3.generate_presigned_url(
        #     ClientMethod='put_object',
        #     Params={
        #         'Bucket': 'before-compress-files',
        #         'Key': 'leo.txt',
        #     }
        # )

        # # Upload a file named 'test.txt' using cURL
        # os.system('curl --request PUT --upload-file ./leo.txt "' + temp_url + '"')
