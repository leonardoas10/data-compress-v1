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

        sql_get_users="SELECT u.email FROM users u inner join files f on f.user_id = u.id WHERE f.is_compress = 1 AND f.updated_at > DATE_SUB(NOW(), INTERVAL '1' HOUR) "
        cursor.execute(sql_get_users)
        users_db = cursor.fetchall()
        db.commit()

        emails = []

        for user in users_db:
            emails.append(user['email'])

        datas = []
        fi = []

        for email in list(set(emails)): # delete duplicated users
            sql_get_files="SELECT f.s3_url FROM users u inner join files f on  f.user_id = u.id WHERE u.email = '{}'  AND f.is_compress = 1 AND f.updated_at > DATE_SUB(NOW(), INTERVAL '1' HOUR) ORDER BY f.updated_at DESC".format(email)
            cursor.execute(sql_get_files)
            files = cursor.fetchall()
            db.commit()
            for file in files:
                fi.append(file['s3_url'])
            datas.append({email: fi})

        if len(fi) > 0 :
            for data in datas:
                email = list(data.keys())[0]
                s3_urls = data[email]
                template_data = ''
                for s3_url in s3_urls:
                    template_data += "<li><a href='{}'>{}</a></li>".format(s3_url, s3_url)

                order_template_data = '"URLS": "{}" '.format(template_data)
                final_template_data_order = '{{{}}}'.format(order_template_data)

                print('email =>' + email)
                print('final_template_data_order => ', final_template_data_order)

                client.send_templated_email(
                    Source=os.getenv("SENDER_EMAIL"),
                    Destination={
                        'ToAddresses': [
                            email
                        ]
                    },
                    TemplateData= final_template_data_order,
                    Template='COMPRESSES_FILES_IN_RANGE_OF_HOUR'
                )

    except Exception as e:
        print('Error => ', e)