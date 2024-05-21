import smtplib
from email import encoders
from email.mime.base import MIMEBase
import pandas as pd
import yaml
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cold_email_logging import get_logger

logger = get_logger()


def create_session_and_login(sender_data):
    logger.info("Creating SMTP Session...")
    try:
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        logger.info("Logging in...")
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(sender_data['sender']['email'], sender_data['sender']['password'])
        logger.info("Login Successful!")
        return s
    except Exception as e:
        logger.info(f"SMTP session creation / login unsuccessful. Traceback: {e}")
        return -1


def send_mail(email_list_df, recipent_file_name):
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

    # get new entries
    emails_to_be_sent = email_list_df[email_list_df['Cold Email Sent?'] != 'Sent']
    emails_to_be_sent = email_list_df.fillna('')
    if len(emails_to_be_sent) == 0:
        logger.info("No recipients to send emails to. Exiting process...")
    else:
        email_list = []
        for i in range(len(emails_to_be_sent)):
            email_list.append({emails_to_be_sent.iloc[i]['Email']: [(emails_to_be_sent.iloc[i]['Name']).split(' ')[0],
                                                                    emails_to_be_sent.iloc[i]['Company'],
                                                                    emails_to_be_sent.iloc[i]['Comma separated position(s) for application if any']]})
    
        s = create_session_and_login(sender_data)
    
        if s != -1:
            for email in email_list:
                recipient = list(email.keys())[0]
                recipient_name = email[recipient][0]
                recipient_company = email[recipient][1]
                recipient_positions = (email[recipient][2]).split(',')
    
                logger.info(f"Sending email to {recipient_name} ({recipient}) who works at {recipient_company}...")
    
                try:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = f"Bringing Data Analytics and Machine Learning Expertise to {recipient_company}"
                    # msg['Subject'] = f"Hello to you at {recipient_company}!"
                    msg['From'] = "Atharva Joshi <joshi461@umn.edu>"
                    msg['To'] = recipient
    
                    message_html = open("MainEmailHTML.txt", "r").read()
                    message_html = MIMEText(message_html, 'html')

                    msg.attach(message_html)

                    # attach links to job posting if specified in the Excel sheet.
                    link_text = ''
                    if len(recipient_positions) >= 1 and recipient_positions != ['']:
                        link_text = '<p>Below are links to some of the roles from the current job postings which ' \
                                    'I think align with my skills and experience to a great extent.</p>'
                        for i in range(len(recipient_positions)):
                            link_text += f"<a href={recipient_positions[i]}>Link{i+1}</a> | "
                        link_text += "<br>"

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
                    s.sendmail("Atharva Joshi <joshi461@umn.edu>", recipient,
                               msg.as_string().format(name=recipient_name, company=recipient_company, links=link_text))
    
                    logger.info(f"Email sent to {recipient_name}({recipient}).")
                    # terminating the session
                    # s.quit()
    
                    email_list_df.loc[email_list_df['Email'] == recipient, 'Cold Email Sent?'] = 'Sent'
                except Exception as e:
                    logger.info(f"Email sending to {recipient_name}({recipient}) failed. Traceback - {e}")
                    logger.info("Terminating smtp server instance...")
                    s.quit()
                    logger.info("Smtp server instance terminated.")
    
            logger.info("Ending session and logging out...")
            s.quit()
    
            try:
                logger.info("Updating Excel")
                email_list_df.to_excel(recipent_file_name, index=False)
            except Exception as e:
                logger.info(f"File Update unsuccessful. Please update manually. Traceback - {e}")


def get_emails_to_send(recipient_file_name):
    logger.info("Parsing email recipient data...")
    emails_list = pd.read_excel(recipient_file_name)
    return emails_list


if __name__ == '__main__':
    logger.info("Initializing cold email send job...")
    recipient_filename = 'ColdEmailTrackingSample.xlsx'
    try:
        emails = get_emails_to_send(recipient_filename)
        send_mail(emails, recipient_filename)
        logger.info("Emails sent to specified recipients.")
    except Exception as exc:
        logger.info(f"Email recipient data parsing unsuccessful: Traceback - {exc}")
    logger.info("Exiting cold emailing script.")
