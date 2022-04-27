import boto3

s3 = boto3.resource('s3')

def handler(event, context):
    try:
        key = event['Records'][0]['s3']['object']['key']
        split = key.split(".")
        file_name = split[0]
        # file = s3.Object('after-compress-files','colocolo-architecture.zip')
        original_bucket = s3.Bucket('before-compress-files')
        # split = file.key.split(".")
        # file_name = split[0]

        for f in original_bucket.objects.all():
            split_original_file = f.key.split(".")
            original_name = split_original_file[0]
            if original_name == file_name:
                s3.delete_object('before-compress-files', f)
                print('Delete succesfull archive => ', f.key)      
    except Exception as e:
        print('Error handler() => ', e)