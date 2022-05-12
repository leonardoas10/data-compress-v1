import boto3
import mysql.connector
import os
import json

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

cursor = db.cursor(dictionary=True)

s3 = boto3.resource('s3')

def handler(event, context):
    try:
        data = json.loads(event['body'])
        user = data['user']

        sql_get_files="SELECT f.id, f.name_extension, f.size, f.updated_at, f.s3_url, f.original_name FROM users u  inner join files f on  f.user_id = u.id WHERE u.email = '{}'  AND f.is_compress = 1  ORDER BY f.updated_at DESC".format(user['email'])
        cursor.execute(sql_get_files)
        files = cursor.fetchall()
        db.commit()

        print('files => ', files)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(files,indent=4, sort_keys=True, default=str)
        }
    except Exception as e:
        print('Error handler() => ', e)