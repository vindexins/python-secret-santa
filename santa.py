import argparse
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import shuffle

from conf_default import *
try:
    from conf import *
except ModuleNotFoundError:
    print("You have to create \"conf.py\" file and fill it with options.")
    sys.exit()


VERSION = "1.0.0"


def get_server():
    server = smtplib.SMTP
    if SMTP_USE_SSL:
        server = smtplib.SMTP_SSL
    try:
        server = server(**SMTP)
        # server.ehlo()
        server.login(*SMTP_CREDENTIALS)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPException):
        print("I can not connect to the provided server, check the options.")
        sys.exit()
    return server


def get_pairs(participants):
    for index in range(len(participants) - 1):
        sender = participants[index]
        receiver = participants[index + 1]
        yield sender, receiver


def get_participants():
    if len(PARTICIPANTS) < 2:
        print("There is not enough participants, provide more through the options.")
        sys.exit()
    # simple shuffle
    participants = list(set(PARTICIPANTS))
    shuffle(participants)

    # magic with restrictions
    if RESTRICT:
        counter = 0
        need_review = True
        length = len(participants)
        while need_review and counter < MAX_REVIEWS:
            need_review = False
            for pair in RESTRICT:
                for index in range(length):
                    if participants[index][1] in pair and \
                            ((index + 1 == length and participants[0][1] in pair) or
                             (index + 1 < length and participants[index + 1][1] in pair)):
                        person = participants.pop(index)
                        if index % 2:
                            participants.insert(0, person)
                        else:
                            participants.append(person)
                        need_review = True
            counter += 1
        if need_review:
            print("I can not satisfy all restrictions, try to change the participants list, "
                  "or the restrictions, or MAX_REVIEWS value.")
            sys.exit()

    # duplicate the first one sender as the last one receiver
    participants.append(participants[0])
    return participants


def run(send):
    participants = get_participants()
    if send:
        server = get_server()
        for sender, receiver in get_pairs(participants):
            context = {
                'sender_name': sender[1],
                'sender_email': sender[0],
                'receiver_name': receiver[1],
                'receiver_email': receiver[0]
            }
            msg = MIMEMultipart('alternative')
            msg["Subject"] = EMAIL_SUBJECT.format(**context)
            msg["From"] = SEND_FROM
            msg["To"] = context['sender_email']
            text = MIMEText(EMAIL_TEXT.format(**context), "plain")
            msg.attach(text)
            if EMAIL_HTML:
                html = MIMEText(EMAIL_HTML.format(**context), "html")
                msg.attach(html)
            server.sendmail(SEND_FROM, context['sender_email'], msg.as_string())
        print("I have sent all emails. Happy Secret Santa party!")
        server.quit()
    else:
        print("Test mode:\n")
        for sender, receiver in get_pairs(participants):
            print("{0:15} => {1:15}".format(sender[1], receiver[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Randomly sends emails to the Secret Santa participants. "
        "For more information, see README file.",
        epilog="Happy Secret Santa party!")
    parser.add_argument(
        "-v", "--version", action="version", version="Secret-Santa {}".format(VERSION),
        help="show script's version")
    parser.add_argument(
        "-s", "--send", action="store_true", help="send real emails")
    args = parser.parse_args()

    run(args.send)
