"""
Базовые классы для сбора данных о компаниях.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class CompanyData:
    """Структура данных компании."""
    inn: str
    name: str
    revenue: Optional[float]
    site: str
    cat_evidence: str
    source: str
    cat_product: Optional[str] = None
    employees: Optional[int] = None
    okved_main: Optional[str] = None
    country: Optional[str] = None

class BaseCollector(ABC):
    """Базовый класс для сбора данных."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def collect_companies(self) -> List[CompanyData]:
        pass
    
    def validate_data(self, company: CompanyData) -> bool:
        if not company.inn or not company.name:
            return False
        
        if company.revenue is not None and company.revenue < 100_000_000:
            return False
            
        return True