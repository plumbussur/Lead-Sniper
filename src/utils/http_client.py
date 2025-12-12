import time
import random
from typing import Optional
import requests
from fake_useragent import UserAgent

class HttpClient:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.last_request_time = 0
    
    def get(self, url: str, timeout: int = 10) -> Optional[requests.Response]:
        try:
            self._respectful_delay()
            
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            return response
            
        except requests.RequestException as e:
            print(f"Ошибка HTTP запроса к {url}: {e}")
            return None
    
    def _respectful_delay(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        min_delay = 1.0
        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            time.sleep(sleep_time + random.uniform(0, 0.5))
        
        self.last_request_time = time.time()