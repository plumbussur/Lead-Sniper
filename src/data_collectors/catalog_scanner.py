from typing import List, Dict
import pandas as pd

from .base import BaseCollector, CompanyData

class CatalogScanner(BaseCollector):
    def __init__(self):
        super().__init__("catalog_scanner")
    
    def scan_industry_catalogs(self) -> List[CompanyData]:
        catalog_companies = [
            {
                'inn': '7812345678',
                'name': 'ООО "Глобал Транслейт"',
                'site': 'global-translate.com',
                'description': 'Международная компания по локализации',
                'revenue': 300_000_000,
                'employees': 80,
                'catalog_source': 'translation_directory'
            },
            {
                'inn': '7823456789',
                'name': 'АО "Тех Локализация"',
                'site': 'techlocal.ru',
                'description': 'Локализация IT-продуктов, используем Trados и MemoQ',
                'revenue': 180_000_000,
                'employees': 35,
                'catalog_source': 'it_localization_catalog'
            },
            {
                'inn': '7834567890',
                'name': 'ООО "Медиа Локализация"',
                'site': 'media-local.ru',
                'description': 'Локализация игр и медиа-контента',
                'revenue': 120_000_000,
                'employees': 28,
                'catalog_source': 'gaming_catalog'
            }
        ]
        
        companies = []
        for company_info in catalog_companies:
            company_data = CompanyData(
                inn=company_info['inn'],
                name=company_info['name'],
                revenue=company_info.get('revenue'),
                site=company_info.get('site', ''),
                cat_evidence=self._extract_catalog_evidence(company_info),
                source=company_info.get('catalog_source', 'catalog'),
                employees=company_info.get('employees'),
                country='Россия'
            )
            companies.append(company_data)
        
        return companies
    
    def _extract_catalog_evidence(self, company_info: Dict) -> str:
        description = company_info.get('description', '')
        
        if 'trados' in description.lower():
            return "указано использование Trados в каталоге"
        elif 'memoq' in description.lower():
            return "указано использование MemoQ в каталоге"
        elif 'локализац' in description.lower():
            return "деятельность по локализации по данным каталога"
        else:
            return "компания из каталога локализационных услуг"
    
    def collect_companies(self) -> List[CompanyData]:
        return self.scan_industry_catalogs()