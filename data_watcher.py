import time
import random
from xmlrpc.client import Boolean
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from notification import NotificationService
from data_extractor import DataExtractor
from data_handler import DataHandler
import tools

class DataWatcher:
    
    def __init__(self, url:str, back_up_url:list, refresh_time:list, max_retries:float, data_extractor:DataExtractor, data_handler:DataHandler, notification_service:NotificationService) -> None:
        self.url = url
        self.backup_url = back_up_url
        self.used_backup_url = 0
        self.refresh_time = refresh_time
        self.notification_service = notification_service
        self.data_extractor = data_extractor
        self.data_handler = data_handler
        self.max_retries = max_retries
        self.retry_counter = 0

    def run_web_check(self) -> Boolean:
        ua = UserAgent()
        abort = False

        while not abort:
            time.sleep(random.uniform(self.refresh_time[0], self.refresh_time[1]))
            soup = self.get_new_data(user_agent_random=ua.random)
            if soup is None:
                continue
            results = self.data_extractor.extract_from_soup(soup)
            if results:
                self.no_data_counter = 0
                self.data_handler.handle_results(results, self.notification_service)
            else:
                print("No data to handle")
                abort = self.check_max_retries()
        
        return abort
        
    def get_new_data(self, user_agent_random:str) -> BeautifulSoup:
        
        headers = {'User-Agent': user_agent_random}
        try:
            r = requests.get(self.url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            print("Log error")
            tools.log_error(e)
            return None
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')

        return soup
    
    def switch_backup_url(self) -> Boolean:
        abort = False
        try:
            self.url = self.backup_url[self.used_backup_url]
        except IndexError:
            print("No backup url available")
            abort = True

        return abort

    def check_max_retries(self):
        abort = False

        if self.retry_counter >= self.max_retries:
            print("Max retries reached")
            print("Switch to backup url")
            self.retry_counter = 0
            abort = self.switch_backup_url()
        else:
            self.retry_counter += 1
        return abort