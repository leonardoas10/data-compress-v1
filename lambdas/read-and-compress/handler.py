import boto3
from io import BytesIO
import zipfile
from urllib.parse import unquote_plus
import mysql.connector
import os

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

cursor = db.cursor(dictionary=True)

s3 = boto3.resource('s3')
# client = boto3.client('s3')

def handler(event, context):
    try:
        print(event['Records'])
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        size = event['Records'][0]['s3']['object']['size']
        key_decoded = unquote_plus(key)
        split = key_decoded.rsplit(".", 1)
        file_name = split[0]
        complete_file_name = '{}.zip'.format(file_name)
        print('split => ', split, 'bucket => ',bucket, 'key => ', key, 'key decoded => ', key_decoded)
        
## ZIP FILE WITH PYTHON ZIP PACKAGE ###
        file = s3.Object(bucket,key_decoded)
        body = file.get()['Body'].read()
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
            print('inside zip_archive')
            with zip_archive.open(file.key, 'w') as file1:
                print('inside file1')
                file1.write(body)
                print('Wroted and closed')  


        print('Upload file to s3.')
        archive.seek(0)
        s3.Object('after-compress-files',complete_file_name).upload_fileobj(archive)
        archive.close()
## ZIP FILE WITH PYTHON ZIP PACKAGE ###

        # zip_file = client.head_object(Bucket='after-compress-files',Key=complete_file_name)
        # print('zip_file => ', zip_file)

        split_key_decoded = key_decoded.split("/", 1)
        print(split_key_decoded)

        sql_get_file = "SELECT * FROM files WHERE name_extension = '{}' AND size = '{}' ORDER BY created_at DESC LIMIT 1".format(split_key_decoded[1], size)
        cursor.execute(sql_get_file)
        fetch_file = cursor.fetchall()[0]
        s3_url = os.getenv("S3_URL")
        path = s3_url + complete_file_name

        sql_file = "UPDATE files SET is_compress = 1, s3_url = '{}' WHERE id = '{}'".format(path, fetch_file['id'])
        cursor.execute(sql_file)
        db.commit()
        print('Updated Archive = ', cursor.rowcount)

    except Exception as e:
        print('Error handler() => ', e)