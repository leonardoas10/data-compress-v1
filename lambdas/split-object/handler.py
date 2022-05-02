import os
from datetime import datetime

def handler(event, context):
    try:
        # print(event['Records'])
        init_time = datetime.now()
        print('Init Lambda => ', init_time)
        bucket = 'before-split'
        key = 'Anaconda3-2021.11-Linux-x86_64.sh'
        linecount = 100000

        infile = 's3://{}/{}'.format(bucket, key)
        outfile = 's3://after-split/{}'.format(key)

        print('Stating s3 file splitter using line coount of {} lines'.format(linecount))
        print('Splitting file: {}'.format(infile))

        os.system("aws s3 cp {} - | split -d -l {} --filter 'aws s3 cp - {}.$FILE.sh' -".format(infile, linecount,outfile))
        duration = datetime.now() - init_time
        print('Finish Time in seconds => ', duration.total_seconds())
    except Exception as e:
        print('Error handler() => ', e)