import datetime
import pyzmail
import smtplib
import imapclient
import imaplib
imaplib._MAXLINE = 10000000


def fix_text_format_for_email(text):
    text_ascii = text.encode("ascii", errors="ignore")
    text_decoded = str(text_ascii.decode("ascii"))

    return text_decoded


def get_imap_obj(email, password):
    imap_obj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imap_obj.login(email, password)
    imap_obj.select_folder("INBOX", readonly=True)

    return imap_obj


# gets UIDs of all emails received today:
def get_uids_today(imap_obj):
    now = datetime.datetime.now()
    email_search_date = now.strftime("%Y/%m/%d")
    # chooses search terms (from today)
    uid_list = imap_obj.gmail_search("after:" + email_search_date)
    return uid_list


def get_last_uid(uid_list):
    uid = uid_list[len(uid_list) - 1]
    return uid


# returns list with subject, sender, and readable text
def get_email_data(imap_obj, uid):
    raw_message = imap_obj.fetch(uid, ["BODY[]"])
    message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
    readable_text = ""

    if message.text_part is not None:
        readable_text += str(message.text_part.get_payload().decode())
    subject = message.get_subject()
    sender_address = message.get_address('from')[1]

    return [subject, sender_address, readable_text]


# gets email data list of newest email for entered account (and makes imap obj)
def do_everything_get_email_data(email, password):
    imap_obj = get_imap_obj(email, password)
    uids_today = get_uids_today(imap_obj)
    uid = get_last_uid(uids_today)
    data = get_email_data(imap_obj, uid)
    return data


# gets ONLY email's subject
def get_email_subject(imap_obj, uid):
    raw_message = imap_obj.fetch(uid, ["BODY[]"])
    message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

    subject = message.get_subject()

    return subject


# prints email info
def get_print_email(imap_obj, uids, pos):
    raw_messages = imap_obj.fetch(uids, ["BODY[]"])
    message = pyzmail.PyzMessage.factory(raw_messages[uids[pos]][b'BODY[]'])
    readable_text = ""

    if message.text_part is not None:
        readable_text += str(message.text_part.get_payload().decode())

    print("\nSender: " + str(message.get_address('from')[1]) + "\nSubject: \"" + str(
        message.get_subject()) + "\"\nText: " + readable_text)


def send_email(my_email, my_password, send_address, subject, text, print_on=False):
    # starts connection
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()

    full_message = "Subject: " + subject + " " + " \n" + text

    # sends email
    smtp_obj.login(my_email, my_password)
    smtp_obj.sendmail(my_email, send_address, full_message)

    # quits connection
    smtp_obj.quit()

    if print_on:
        print("\tSent email: \n\t\t" + text + "\n\tto:\n\t\t" + send_address)


# demo
def main():
    data = do_everything_get_email_data(input("Email Address: "), input("Password: "))
    print(data)

    send_email(input("Email Address: "), input("Password: "), input("Send Address: "), "TEST EMAIL",
               "This is a test email.", print_on=True)


# runs main if called directly
if __name__ == '__main__':
    main()

