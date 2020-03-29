# Local:
import run_track
import sheets
import use_files
import use_email
import send_wiki

import os
import time
import imaplib
imaplib._MAXLINE = 10000000


# NOTES:
# NO NEW EMAILS PRINT IS DISABLED
# make it so it's not just getting emails from today? (from last few minutes?)
# make dictionary with subject and action-(modules)?
# have email receiver sheets that stores everything on the cloud -last_email
# maybe make it so it gets all unchecked UIDs, then goes through just the unchecked one? prints how many unchecked?
# add way to manually enter run date/time for run tracker


def main():
    # Sets email account
    email = "receiver.server56@gmail.com"
    password = "2belugas"

    # finds last_email logged from THE LAST TIME THE SCRIPT WAS RUN
    if use_files.basic_read_file("last_email") == "FILE NOT FOUND":
        last_email = -1
    else:
        last_email = int(use_files.basic_read_file("last_email"))

    while 1:
        # connects to imap server for email account
        imap_obj = use_email.get_imap_obj(email, password)

        # gets UIDs of all emails received today:
        # chooses search terms (from today)
        today_uids = use_email.get_uids_today(imap_obj)

        new_uid = use_email.get_last_uid(today_uids)

        # checks if it was the last email to be checked
        if new_uid == last_email:
            # print("[email_reader] No new emails.")

            # this is the loop refresh time
            time.sleep(10)

        # if new email:
        else:
            # Subject is NOT case sensitive
            sub = use_email.get_email_subject(imap_obj, new_uid).lower()
            if sub == "run":
                # should this be here?
                service = sheets.authenticate_sheets_api()

                dist = use_email.get_email_data(imap_obj, new_uid)[2].strip()
                run_track.log_run(service, dist)
                print("[email_reader] Logged " + dist + " mile run.")

            elif sub == "command":
                command = use_email.get_email_data(imap_obj, new_uid)[2].strip()

                # runs Linux command
                os.system(command)

            elif sub == "status":
                received_address = use_email.get_email_data(imap_obj, new_uid)[1]
                # sends status update
                print("[email_reader] ", end="")
                use_email.send_email(email, password, received_address,
                                     "The Email Receiver is running.", " ", True)

            # Automatically adds sender's email address to send_wiki list if they
            #   send email with the subject "add me wiki"
            elif sub == "add me wiki":
                received_address = str(use_email.get_email_data(imap_obj, new_uid)[1])

                print("[email_reader] Found new 'add me' request for Wiki of the Day from: " + received_address
                      + ". Adding to email list...")

                send_wiki.add_email_to_list(received_address)

            else:
                print("[email_reader] Found email with subject: " + sub + ". No action taken.")

            # marks email as last email acted upon:
            last_email = new_uid

            # Logs last checked email to file so it's not acted on the next time the script is run:
            use_files.basic_write_file("last_email", str(last_email))

            # this is the loop refresh time
            time.sleep(10)


# runs main if called directly
if __name__ == '__main__':
    main()
