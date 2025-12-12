import re
import time
import random
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from .base import BaseCollector, CompanyData
from ..utils.http_client import HttpClient

class RusprofileCollector(BaseCollector):
    def __init__(self):
        super().__init__("rusprofile")
        self.http_client = HttpClient()
        self.ua = UserAgent()
    
    def search_companies_by_activity(self, activity_keywords: List[str]) -> List[CompanyData]:
        companies = []
        
        for keyword in activity_keywords:
            print(f"Поиск компаний по ключевому слову: {keyword}")
            
            search_results = self._search_rusprofile(keyword)
            
            for company_info in search_results:
                if self._is_relevant_company(company_info):
                    company_data = self._parse_company_info(company_info)
                    if company_data:
                        companies.append(company_data)
            
            time.sleep(random.uniform(1, 3))
        
        return companies
    
    def _search_rusprofile(self, keyword: str) -> List[Dict]:
        mock_results = [
            {
                'inn': '7701234567',
                'name': 'ООО "Локализация Про"',
                'site': 'localization-pro.ru',
                'description': 'Компания специализируется на локализации ПО и использует Trados Studio для работы с переводческой памятью.',
                'revenue': 150_000_000,
                'employees': 25
            },
            {
                'inn': '7712345678', 
                'name': 'АО "Транслейт Тех"',
                'site': 'translatetech.ru',
                'description': 'Разработка CAT-систем и платформ для управления переводами. Используем собственную TMS.',
                'revenue': 200_000_000,
                'employees': 45
            }
        ]
        
        filtered_results = []
        for result in mock_results:
            if any(keyword.lower() in result['description'].lower() for keyword in ['локализ', 'перевод', 'translation', 'cat']):
                filtered_results.append(result)
        
        return filtered_results
    
    def _is_relevant_company(self, company_info: Dict) -> bool:
        description = company_info.get('description', '').lower()
        
        cat_keywords = ['локализ', 'перевод', 'translation', 'cat', 'tms', 'память переводов']
        
        return any(keyword in description for keyword in cat_keywords)
    
    def _parse_company_info(self, company_info: Dict) -> CompanyData:
        try:
            return CompanyData(
                inn=company_info['inn'],
                name=company_info['name'],
                revenue=company_info.get('revenue'),
                site=company_info.get('site', ''),
                cat_evidence=self._extract_cat_evidence(company_info.get('description', '')),
                source='rusprofile',
                employees=company_info.get('employees'),
                country='Россия'
            )
        except Exception as e:
            print(f"Ошибка при парсинге данных компании: {e}")
            return None
    
    def _extract_cat_evidence(self, description: str) -> str:
        if 'trados' in description.lower():
            return "упоминание Trados Studio"
        elif 'tms' in description.lower():
            return "использование TMS"
        elif 'память переводов' in description.lower():
            return "использование памяти переводов"
        elif 'локализац' in description.lower():
            return "деятельность по локализации"
        else:
            return "упоминание переводческих технологий"
    
    def collect_companies(self) -> List[CompanyData]:
        activity_keywords = [
            'локализация',
            'переводческие услуги',
            'translation services',
            'cat системы',
            'tms платформы'
        ]
        
        return self.search_companies_by_activity(activity_keywords)