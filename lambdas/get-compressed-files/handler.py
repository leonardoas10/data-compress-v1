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

        sql_get_files= "SELECT files.id, files.name_extension, files.updated_at, files.s3_url FROM users, files WHERE users.email = '{}' AND files.is_compress = 1".format(user['email'])
        cursor.execute(sql_get_files)
        files = cursor.fetchall()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(files)
        }
    except Exception as e:
        print('Error handler() => ', e)