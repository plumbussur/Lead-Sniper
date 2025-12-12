"""
Парсер сайтов компаний для поиска признаков CAT-систем.
"""
import re
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from .base import BaseCollector, CompanyData
from ..utils.http_client import HttpClient
from config.settings import CONFIG

class WebsiteParser(BaseCollector):
    def __init__(self):
        super().__init__("website_parser")
        self.http_client = HttpClient()
    
    def analyze_company_website(self, company_data: CompanyData) -> Optional[CompanyData]:
        try:
            content = self._fetch_website_content(company_data.site)
            if not content:
                return company_data
            
            cat_evidence = self._find_cat_evidence(content)
            cat_product = self._detect_cat_product(content)
            
            company_data.cat_evidence = cat_evidence
            company_data.cat_product = cat_product
            
            return company_data
            
        except Exception as e:
            print(f"Ошибка при анализе сайта {company_data.site}: {e}")
            return company_data
    
    def _fetch_website_content(self, site_url: str) -> Optional[str]:
        try:
            if not site_url.startswith(('http://', 'https://')):
                site_url = 'https://' + site_url
            
            response = self.http_client.get(site_url, timeout=10)
            return response.text if response else None
            
        except Exception as e:
            print(f"Не удалось получить содержимое сайта {site_url}: {e}")
            return None
    
    def _find_cat_evidence(self, content: str) -> str:
        content_lower = content.lower()
        
        evidence_items = []
        
        for keyword in CONFIG.cat_keywords:
            if keyword in content_lower:
                evidence_items.append(f"упоминание '{keyword}'")
        
        for product in CONFIG.cat_products:
            if product in content_lower:
                evidence_items.append(f"использование продукта {product}")
        
        for phrase in CONFIG.cat_phrases:
            if phrase in content_lower:
                evidence_items.append(f"наличие описания '{phrase}'")
        
        if evidence_items:
            return "; ".join(evidence_items[:3])
        else:
            return "не найдено явных доказательств CAT"
    
    def _detect_cat_product(self, content: str) -> Optional[str]:
        content_lower = content.lower()
        
        for product in CONFIG.cat_products:
            if product in content_lower:
                return product
        
        return None
    
    def analyze_multiple_companies(self, companies: List[CompanyData]) -> List[CompanyData]:
        analyzed_companies = []
        
        for company in companies:
            print(f"Анализ сайта: {company.site}")
            analyzed_company = self.analyze_company_website(company)
            analyzed_companies.append(analyzed_company)
            
            time.sleep(1)
        
        return analyzed_companies
    
    def collect_companies(self) -> List[CompanyData]:
        return []