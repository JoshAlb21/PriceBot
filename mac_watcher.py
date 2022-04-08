from xml.dom.minidom import Element
from data_watcher import DataWatcher
from data_extractor import DataExtractor
from data_handler import DataHandler
from notification import NotificationService
import tools

if __name__ == '__main__':
    config = tools.load_config_from_file('config.json')
    url = config['target_info']['url']
    backup_url = config['target_info']['backup_url']
    treshold_price = config['notification_mode']['ignore_price_above_eur']
    refresh_time = config['target_info']['retry_time']
    max_retries = config['target_info']['max_retries']
    email_information = config['notification_adress']

    elements_to_watch = config["data_extractor_settings"]
    data_extractor = DataExtractor(elements_to_watch)
    data_handler = DataHandler()
    notification_service = NotificationService(treshold_price, email_information)

    mac_watcher = DataWatcher(url, backup_url, refresh_time, max_retries, data_extractor, data_handler, notification_service)
    mac_watcher.run_web_check()