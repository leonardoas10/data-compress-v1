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
        print('EVENT => ', event)
        data = json.loads(event['body'])

        sql_get_file="SELECT * from files WHERE id = {}".format(data['id'])
        cursor.execute(sql_get_file)
        file = cursor.fetchall()[0]
        db.commit()
        key = "{}/{}.zip".format(file['user_id'], file['name'])

        if not file['deleted_at']:
            s3.Object('after-compress-files', key).delete()
            sql_update_file = "UPDATE files SET is_compress = 0, s3_url = NULL, deleted_at = CURRENT_TIMESTAMP WHERE id = {}".format(data['id'])
            cursor.execute(sql_update_file)
            db.commit()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'ok': True, 'id': data['id']})
        }
    except Exception as e:
        print('Error handler() => ', e)