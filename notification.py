import unicodedata
import ssl
import smtplib

import tools

class NotificationService:
    def __init__(self, treshold_price:float, email_information:dict) -> None:
        self.treshold_price = treshold_price
        self.email_information = email_information
    
    def trigger_notification(self, new_lines):
        print(f'{tools.get_current_time()} CHANGE!!!')
        self.send_email(new_lines)

    def read_email_pass(self, pass_file:str) -> str:
        '''Read password from file. DISCLAIMER: make sure you do no commit the password file (-> git ignore)'''
        with open(pass_file, 'r') as f:
            lines = f.readlines()
        return lines[0].strip()

    def send_email(self, message:list):

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = self.email_information['sender_email']
        password = self.read_email_pass(self.email_information['sender_password'])
        receiver_email = self.email_information['receiver_email']
        
        list_as_str = ' '.join(message)
        list_as_str = unicodedata.normalize("NFKD", list_as_str)
        #TODO send price etc with mail
        text_message = f"""\
        Price Change!

        MacBook price has changed
        """

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text_message)
    
    def check_decreasing_stock(self, new_list:list, old_list:list) -> bool:
        '''Notify condition'''
        notify = False
        if len(new_list) >= len(old_list):
            notify = True
        return notify
    
    def check_treshold_price(self, prices:list) -> bool:
        '''Notify condition'''
        notify = False
        for price in prices:
            price_f = tools.extract_float_from_price(price)
            if float(price_f) < self.treshold_price:
                notify = True
        return notify