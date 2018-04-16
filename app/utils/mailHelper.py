from mailer import Mailer
from mailer import Message
from config import MAIL_HOST, MAIL_PORT, MAIL_ADD, MAIL_PW


def send(toAdd, subject, content):
    message = Message(From=MAIL_ADD,
                      To=toAdd,
                      charset="utf-8")
    message.Subject = subject
    message.Html = content

    sender = Mailer(host=MAIL_HOST,
                    port=MAIL_PORT,
                    usr=MAIL_ADD,
                    pwd=MAIL_PW,
                    use_ssl=True)  # required for 163 mail
    sender.send(message)
    print("verivication code sent")

# if __name__ == "__main__":
#     send("yks2005@qq.com", "test", "test")
