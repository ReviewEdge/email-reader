import email_reader_repo
from furtherpy.sample import files_tool
import time


# add send email of error for failure


print("\n[forever_email_reader] Starting email_reader.py")
while 1:
    # checks if any music is playing
    try:
        email_reader_repo.main()

    except Exception as e:
        # saves error file
        files_tool.basic_write_file("email_reader_crash_report", "email_reader crashed with the exception: " + str(e))

        print("\n[forever_email_reader] The error: '" + str(e) +
              "' occurred while running email_reader.py.\nTrying again...\n")

        # waits to restart loop
        time.sleep(30)
