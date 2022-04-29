import boto3
from urllib.parse import unquote_plus

s3 = boto3.resource('s3')

def handler(event, context):
    try:
        print(event['Records'])
        key = event['Records'][0]['s3']['object']['key']
        key_decoded = unquote_plus(key)
        split = key_decoded.rsplit(".", 1)
        file_name = split[0]
        original_bucket = s3.Bucket('before-compress-files')

        for f in original_bucket.objects.all():
            split_original_file = f.key.rsplit(".", 1)
            original_name = split_original_file[0]
            if original_name == file_name:
                s3.Object('before-compress-files', f.key).delete()
                print('Delete succesfull archive => ', f.key)      
    except Exception as e:
        print('Error handler() => ', e)