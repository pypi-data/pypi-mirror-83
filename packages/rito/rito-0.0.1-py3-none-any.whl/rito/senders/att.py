from rito.senders import migadu

def send_message(to_number, text):
    migadu.send_message("{}@{}".format(to_number, "txt.att.net"), text + " ")