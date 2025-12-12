import re
from typing import List
from ..data_collectors.base import CompanyData

class DataCleaner:
    @staticmethod
    def clean_company_data(companies: List[CompanyData]) -> List[CompanyData]:
        cleaned_companies = []
        
        for company in companies:
            cleaned_company = DataCleaner._clean_single_company(company)
            if cleaned_company:
                cleaned_companies.append(cleaned_company)
        
        return cleaned_companies
    
    @staticmethod
    def _clean_single_company(company: CompanyData) -> CompanyData:
        try:
            company.inn = DataCleaner._clean_inn(company.inn)
            company.name = DataCleaner._clean_name(company.name)
            company.site = DataCleaner._clean_site(company.site)
            company.revenue = DataCleaner._clean_revenue(company.revenue)
            company.employees = DataCleaner._clean_employees(company.employees)
            company.cat_evidence = DataCleaner._clean_text(company.cat_evidence)
            
            return company
            
        except Exception as e:
            print(f"Ошибка при очистке данных компании {company.name}: {e}")
            return None
    
    @staticmethod
    def _clean_inn(inn: str) -> str:
        if not inn:
            return ""
        
        cleaned = re.sub(r'[^\d]', '', str(inn))
        
        if len(cleaned) in [10, 12]:
            return cleaned
        
        return ""
    
    @staticmethod
    def _clean_name(name: str) -> str:
        if not name:
            return ""
        
        cleaned = re.sub(r'\s+', ' ', str(name).strip())
        cleaned = re.sub(r'[^\w\s\-\.\(\)]', '', cleaned)
        
        return cleaned.strip()
    
    @staticmethod
    def _clean_site(site: str) -> str:
        if not site:
            return ""
        
        site = str(site).strip().lower()
        site = re.sub(r'^https?://', '', site)
        site = re.sub(r'^www\.', '', site)
        
        return site
    
    @staticmethod
    def _clean_revenue(revenue) -> float:
        if revenue is None:
            return None
        
        try:
            if isinstance(revenue, (int, float)):
                return float(revenue)
            
            revenue_str = str(revenue)
            cleaned = re.sub(r'[^\d\.]', '', revenue_str)
            
            if cleaned:
                return float(cleaned)
            
            return None
            
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _clean_employees(employees) -> int:
        if employees is None:
            return None
        
        try:
            if isinstance(employees, (int, str)):
                employees_str = str(employees)
                
                numbers = re.findall(r'\d+', employees_str)
                if numbers:
                    return int(numbers[0])
            
            return None
            
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _clean_text(text: str) -> str:
        if not text:
            return ""
        
        cleaned = re.sub(r'\s+', ' ', str(text).strip())
        
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        
        return cleaned