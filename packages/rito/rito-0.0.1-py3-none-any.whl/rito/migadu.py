import os
from email.header import Header
import email
import json
import time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import sys

if 'RITO_MIGADU_ACCOUNT' not in os.environ or 'RITO_MIGADU_PASSWORD' not in os.environ:
    print("To use Rito's Migadu functions, you need to create a Migadu domain and create a bot mailbox on your domain with no privileges.")
    print("Put the bot account's credentials in the environment variables RITO_MIGADU_ACCOUNT and RITO_MIGADU_PASSWORD, then try again.")
    exit(1)

account = os.environ['RITO_MIGADU_ACCOUNT']
password = os.environ['RITO_MIGADU_PASSWORD']

def __with_smtp(func):
    with smtplib.SMTP_SSL("smtp.migadu.com", 465) as smtp:
        # Log in to the email account
        smtp.login(account, password)
        func(smtp)

def __send_message(self, recipients, subject, content, encoding, files=[]):
    # Construct the message as a MIMEMultipart with MIMEText

    message = MIMEMultipart()
    message['From'] = self._email_address
    message['To'] = COMMASPACE.join(recipients)
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = Header(subject.encode('utf-8'), 'utf-8')

    message.attach(MIMEText(content.encode('utf-8'), encoding, 'utf-8'))

    # source of attachment code: https://stackoverflow.com/a/3363254
    for f in files:
        if f != "":
            try:
                with open(f, 'rb') as ff:
                    part = MIMEApplication(
                        ff.read(),
                        Name=basename(f),
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(f))
                message.attach(part)
            except:
                raise "Couldn't attach {}.".format(f)

        self._smtp_server.sendmail(self._email_address, recipients,
                                   message.as_string())

    def send_message_plain(self, recipients, subject, body_text, files=[]):
        """ Send a plain utf8 email to the specified list of addresses
        """
        self._send_message(recipients, subject, body_text, 'plain', files)

    def send_message_markdown(self, recipients, subject, body_markdown, files=[]):
        """ Send a markdown-formatted email to the specified list of addresses
        """
        # Convert the markdown to HTML
        body_html = markdown.markdown(body_markdown)
        self._send_message(recipients, subject, body_html, 'html', files)


# TODO eventually we'll want to handle other types of payloads
def all_payload_text(email):
    text = ''

    if isinstance(email.get_payload(), basestring):
        text = email.get_payload()
    else:
        for part in email.get_payload():
            if part.get_content_type() == 'text/plain':
                text += part.get_payload()

    return text

import time

class SMSInterface(object):
    ''' Class that manages a Gmail account to send and receive texts '''

    def __init__(self, phone_number, carrier_server):
        self._mail_account = MailAccount()
        self._phone_number = phone_number
        self._carrier_server = carrier_server

    def send_text(self, text):
        # TODO for the darnedest reason, the last two characters get chopped, so we add 2 blank spaces
        text += "  "
        self._mail_account.send_message_plain([str(self._phone_number) + '@' + self._carrier_server], '', text)

    def first_line(self, text):
        return text.split('\n')[0].strip()

    def get_texts(self, first_line=True, num=0, mark_read=True):
        messages = self._mail_account.get_unread_messages(num, 'TEXT', mark_read)

        messages = [message.get_payload() for message in messages]
        if first_line:
            messages = [self.first_line(message) for message in messages]

        return messages

    def get_line(self, prompt, time_delay=3, timeout=60):
        # Clear previous unconsumed inputs
        self.get_texts()

        # Send the prompt text
        if len(prompt) != 0:
            self.send_text(prompt)

        elapsed = 0
        # A timeout of 0 means this check will never time out
        while elapsed < timeout or timeout == 0:
            # Only get the first line of 1 text
            texts = self.get_texts(True, 1)
            if len(texts) > 0:
                return self.first_line(texts[0])

            time.sleep(time_delay)
            elapsed += time_delay

        return -1

if __name__ == "__main__":
    name = sys.argv[1]
    message = "thing"
    if len(sys.argv) > 2:
        message = sys.argv[2]
    
    message = "Hey your {} is finished".format(message)
    
    if name.lower() == "nat":
        SMSInterface("8014935262", "txt.att.net").send_text(message)
    elif name.lower() == "becca":
        MailAccount().send_message_plain(["R.Pfeiffer@utah.edu"], message, message)