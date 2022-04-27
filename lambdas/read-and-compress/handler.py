import boto3
from datetime import datetime
from io import BytesIO
import zipfile

s3 = boto3.resource('s3')

def handler(input, context) -> str:
    try:
        init_time = datetime.now()
        print('Init Lambda => ', init_time)

### ZIP WITH LIBRARY LZW. ###
        # s3.Bucket('before-compress-files').download_file('leo.txt', '/tmp/leo.txt')
        # print(os.path.isfile('/tmp/leo.txt'))
        # infile = lzw.readbytes("/tmp/leo.txt")
        # print('infile => ', infile)
        # compressed = lzw.compress(infile)
        # print('compressed => ', compressed)
        # lzw.writebytes("/tmp/leo-vscode.lzw", compressed)
        # print(os.path.isfile('/tmp/leo-vscode.lzw'))
        # s3.Bucket('before-compress-files').upload_file('/tmp/leo-vscode.lzw', 'leo-vscode.lzw')
### ZIP WITH LIBRARY LZW. ###

### ZIP FILE WITH PYTHON ZIP PACKAGE ###
        file = s3.Object('before-compress-files','ubuntu14.04.img')
        body = file.get()['Body'].read()
        archive = BytesIO()
        print('archive => ', archive)
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
            print('inside zip_archive')
            with zip_archive.open(file.key, 'w') as file1:
                print('inside file1')
                file1.write(body)
                print('Wroted and closed')  

        print('Upload file to s3.')
        archive.seek(0)
        s3.Object('before-compress-files','ubuntu14.04.zip').upload_fileobj(archive)
        archive.close()
### ZIP FILE WITH PYTHON ZIP PACKAGE ###

        duration = datetime.now() - init_time
        print('Finish Time in seconds => ', duration.total_seconds())
        return 'Success Job'
    except Exception as e:
        print('Error handler() => ', e)