import smtplib
from email import encoders
from email.mime.base import MIMEBase

import yaml
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cold_email_logging import get_logger

logger = get_logger()


def send_mail(email_list):
    logger.info("Initializing email sending method to parsed recipient data...")

    # parse sender credentials
    logger.info("Parsing sender credentials...")
    with open("../ymlFiles/sender_data.yaml") as stream:
        try:
            sender_data = (yaml.safe_load(stream))
            logger.info("Sender data parsed successfully.")
        except yaml.YAMLError as exc:
            logger.info("Sender data parsing unsuccessful. Traceback on next log line.")
            raise exc

    email_list = email_list['email_list']
    for email in email_list:
        recipient = email
        recipient_name = email_list[email][0]
        recipient_company = email_list[email][1]
        email_body_file = "MainEmailHTML.txt"

        logger.info(f"Sending email to {recipient_name} ({recipient}) who works at {recipient_company}...")

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(sender_data['sender']['email'], sender_data['sender']['password'])
            # message to be sent
            # message = open(email_body_file, "r").read()
            # # sending the mail
            # s.sendmail("joshi461@umn.edu", recipient, message.format(name=recipient_name, company=recipient_company))

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Bringing Data Science and Machine Learning Expertise to {recipient_company}"
            # msg['Subject'] = f"Hello to you at {recipient_company}!"
            msg['From'] = "Atharva Joshi <joshi461@umn.edu>"
            msg['To'] = recipient

            message_html = open("MainEmailHTML.txt", "r").read()
            message_html = MIMEText(message_html, 'html')

            msg.attach(message_html)

            # Open the file to be sent
            attachment_file = "AtharvaJResume-11.pdf"
            with open(attachment_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {attachment_file}',
                )
                msg.attach(part)

            # msg.set_content(message.format(name=recipient_name, company=recipient_company))
            s.sendmail("Atharva Joshi <joshi461@umn.edu>", recipient, msg.as_string().format(name=recipient_name, company=recipient_company))

            logger.info(f"Email sent to {recipient_name}({recipient}).")
            # terminating the session
            s.quit()
        except Exception as e:
            logger.info(f"Email sending to {recipient_name}({recipient}) failed. Traceback - {e}")
            logger.info("Terminating smtp server instance...")
            s.quit()
            logger.info("Smtp server instance terminated.")


def get_emails_to_send():
    logger.info("Parsing email recipient data...")
    with open("../ymlFiles/main_email_list.yaml") as stream:
        try:
            emails_list = (yaml.safe_load(stream))
            logger.info("Email recipient data parsed successfully.")
            return emails_list
        except yaml.YAMLError as exc:
            raise exc


if __name__ == '__main__':
    logger.info("Initializing cold email send job...")
    try:
        emails = get_emails_to_send()
        send_mail(emails)
        logger.info("Emails sent to specified recipients.")
    except Exception as exc:
        logger.info(f"Email recipient data parsing unsuccessful: Traceback - {exc}")
    logger.info("Exiting cold emailing script.")