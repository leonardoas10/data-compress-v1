from datetime import datetime
import os
import mysql.connector
import boto3

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
cursor = db.cursor(dictionary=True)

client = boto3.client('ses')

def handler(event, context):
    try:
        init_time = datetime.now()
        print('Init Lambda => ', init_time)

        sql_get_users="SELECT u.email from users u inner join files f on f.user_id = u.id WHERE f.is_compress = 1"
        cursor.execute(sql_get_users)
        users_db = cursor.fetchall()
        db.commit()

        emails = []

        for user in users_db:
            emails.append(user['email'])

        datas = []

        for email in list(set(emails)): # delete duplicated users
            sql_get_files="SELECT f.s3_url FROM users u  inner join files f on  f.user_id = u.id WHERE u.email = '{}'  AND f.is_compress = 1  ORDER BY f.updated_at DESC".format(email)
            cursor.execute(sql_get_files)
            files = cursor.fetchall()
            db.commit()
            fi = []
            for file in files:
                fi.append(file['s3_url'])
            datas.append({email: fi})

        for data in datas:
            email = list(data.keys())[0]
            s3_urls = data[email]
            template_data = ''
            for s3_url in s3_urls:
                template_data += "<li><a href='{}'>{}</a></li>".format(s3_url, s3_url)

            #print(template_data)
            #print(email)

            order_template_data = '"URLS": "{}" '.format(template_data)
            order = '{{{}}}'.format(order_template_data)
            # email_s = '{}'.format(email)
            # print(email_s, email)
            print('email =>' + email+"leo")

            client.send_templated_email(
                Source='leoaranguren10@gmail.com',
                Destination={
                    'ToAddresses': [
                        email
                    ]
                },
                TemplateData= order,
                #TemplateData='{"URLS": "<li> http </li><li> http </li><li> http </li><li> http </li>"}',
                Template='COMPRESSES_FILES_IN_RANGE_OF_HOUR'
            )
        duration = datetime.now() - init_time
        print('Finish Time in seconds => ', duration.total_seconds())

    except Exception as e:
        print('Error => ', e)