# email, name: ("johny.boy@fake.mail", "John")
PARTICIPANTS = ()

# use names, for example: ("Diana", "John")
EXCLUDE = ()

# default GMail options
SMTP = {
    "host": "smtp.gmail.com",
    "port": 465
}
SMTP_USE_SSL = True
SMTP_CREDENTIALS = ("user_name", "very_secret_password")

SEND_FROM = "email_from"

# Email context: sender_name, sender_email, receiver_name, receiver_name
EMAIL_SUBJECT = "Secret Santa made his choice"
EMAIL_TEXT = """
Hello, dear {sender_name}!

Ho! Ho! Ho!
Secret Santa has made his choice. You have to make a present for {receiver_name}.

The maximum limit is $100.00


This message was automatically generated by a script
You can check it out here:
https://github.com/vindexins/python-secret-santa/ 
"""
EMAIL_HTML = """
<html>
    <head></head>
    <body>
        <p>Hello, dear {sender_name}!</p>
        <p>Ho! Ho! Ho!<br/>
        Secret Santa has made his choice. You have to make a present for {receiver_name}.<br/>
        The maximum limit is $100.00</p>
        <br/>
        <p>This message was automatically generated by a script<br/>
        You can check it out here:<br/>
        <a href="https://github.com/vindexins/python-secret-santa/">Secret Santa</a></p>
    </body>
</html>
"""

MAX_REVIEWS = 1000
