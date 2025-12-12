from typing import List
from ..data_collectors.base import CompanyData
from config.settings import CONFIG

class CatClassifier:
    @staticmethod
    def classify_companies(companies: List[CompanyData]) -> List[CompanyData]:
        classified_companies = []
        
        for company in companies:
            if CatClassifier._has_cat_system(company):
                classified_companies.append(company)
            else:
                print(f"Компания {company.name} исключена: не найдены признаки CAT-систем")
        
        return classified_companies
    
    @staticmethod
    def _has_cat_system(company: CompanyData) -> bool:
        text_to_analyze = " ".join([
            company.name or "",
            company.cat_evidence or "",
            company.cat_product or ""
        ]).lower()
        
        cat_indicators = 0
        
        for keyword in CONFIG.cat_keywords:
            if keyword in text_to_analyze:
                cat_indicators += 1
        
        for product in CONFIG.cat_products:
            if product in text_to_analyze:
                cat_indicators += 2
        
        for phrase in CONFIG.cat_phrases:
            if phrase in text_to_analyze:
                cat_indicators += 1
        
        return cat_indicators >= 2
    
    @staticmethod
    def enhance_cat_evidence(companies: List[CompanyData]) -> List[CompanyData]:
        enhanced_companies = []
        
        for company in companies:
            enhanced_company = CatClassifier._enhance_single_company(company)
            enhanced_companies.append(enhanced_company)
        
        return enhanced_companies
    
    @staticmethod
    def _enhance_single_company(company: CompanyData) -> CompanyData:
        text_to_analyze = " ".join([
            company.name or "",
            company.cat_evidence or ""
        ]).lower()
        
        if 'trados' in text_to_analyze:
            company.cat_product = company.cat_product or "Trados"
            if 'упоминание' not in company.cat_evidence.lower():
                company.cat_evidence = f"использование {company.cat_product} ({company.cat_evidence})"
        elif 'memoq' in text_to_analyze:
            company.cat_product = company.cat_product or "MemoQ"
        elif 'tms' in text_to_analyze:
            company.cat_product = company.cat_product or "TMS"
        
        return company