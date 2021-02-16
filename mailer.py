from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# 参考  http://trade-and-develop.hatenablog.com/entry/2017/03/12/145514


class sendGmailAttach:

    def __init__(self, username, password, to, sub, body, attach_files):
        host, port = 'smtp.gmail.com', 465
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = username
        msg['To'] = to

        # メール本文
        body = MIMEText(body)
        msg.attach(body)

        # 添付ファイルの設定
        # attachment = MIMEBase('image', 'png')
        # file = open(attach_file['path'], 'rb+')
        # attachment.set_payload(file.read())
        # file.close()
        # encoders.encode_base64(attachment)
        # attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
        # msg.attach(attachment)
        for attach_file in attach_files:
            attachment = MIMEBase('image', 'png')
            file = open(attach_file['path'], 'rb+')
            attachment.set_payload(file.read())
            file.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
            msg.attach(attachment)

        smtp = smtplib.SMTP_SSL(host, port)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.mail(username)
        smtp.rcpt(to)
        smtp.data(msg.as_string())
        smtp.quit()
