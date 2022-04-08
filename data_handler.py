import os
from os.path import exists

import tools
from notification import NotificationService

class DataHandler:

    def __init__(self) -> None:
        pass
    
    def handle_results(self, results:list, notification_service:NotificationService) -> None:
        if results is not None:
            prices = [results[price] for price in range(1, len(results), 2) ]
            log_file = 'product_log.txt'
            file_exists = exists(log_file)
            if not file_exists:
                with open(log_file, 'w') as f:
                    for i in range(0, len(results), 2):
                        string_to_save = f'{results[i]}\n{results[i+1]}\n'
                        f.write(string_to_save)
            else:
                lines = tools.read_logfiles(log_file)

                identical = tools.check_lists(lines, results)
                if not identical:
                    notify = notification_service.check_treshold_price(prices)
                    notify = notification_service.check_decreasing_stock(results, lines)
                    if notify:    
                        notification_service.trigger_notification(lines)
                    os.remove(log_file)
        else:
            print("no_data")