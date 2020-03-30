# DON'T put txt in file name argument
def basic_write_file(file_name, text):
    file_name = file_name + ".txt"
    file_1 = open(file_name, "w")
    file_1.write(text)
    file_1.close()


# DON'T put txt in file name argument
def basic_read_file(file_name):
    file_name += ".txt"
    try:
        open_file = open(file_name, "r")
    except IOError:
        return "FILE NOT FOUND"
    file_text = open_file.read()
    open_file.close()

    return file_text
