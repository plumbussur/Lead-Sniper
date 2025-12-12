from typing import List
from ..data_collectors.base import CompanyData
from config.settings import CONFIG

class RevenueValidator:
    @staticmethod
    def filter_by_revenue(companies: List[CompanyData]) -> List[CompanyData]:
        filtered_companies = []
        
        for company in companies:
            if RevenueValidator._has_sufficient_revenue(company):
                filtered_companies.append(company)
            else:
                print(f"Компания {company.name} исключена: выручка {company.revenue} < {CONFIG.min_revenue}")
        
        return filtered_companies
    
    @staticmethod
    def _has_sufficient_revenue(company: CompanyData) -> bool:
        if company.revenue is None:
            return False
        
        return company.revenue >= CONFIG.min_revenue
    
    @staticmethod
    def validate_revenue_data(companies: List[CompanyData]) -> List[CompanyData]:
        validated_companies = []
        
        for company in companies:
            if RevenueValidator._validate_revenue_entry(company):
                validated_companies.append(company)
            else:
                print(f"Компания {company.name} исключена: некорректные данные о выручке")
        
        return validated_companies
    
    @staticmethod
    def _validate_revenue_entry(company: CompanyData) -> bool:
        if company.revenue is None:
            return False
        
        if company.revenue <= 0:
            return False
        
        if company.revenue > 1_000_000_000_000:
            return False
        
        return True