import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CatConfig:
    cat_keywords: List[str] = None
    cat_products: List[str] = None
    cat_phrases: List[str] = None
    min_revenue: int = 100_000_000
    target_countries: List[str] = None
    
    def __post_init__(self):
        if self.cat_keywords is None:
            self.cat_keywords = [
                'translation memory', 'tm', 'терминология', 'терминологическая база',
                'cat tool', 'cat-система', 'tms', 'translation management',
                'локализация', 'localization', 'переводческая память'
            ]
        
        if self.cat_products is None:
            self.cat_products = [
                'trados', 'memoq', 'across', 'wordfast', 'memsource',
                'smartcat', 'phrase', 'lokalise', 'crowdin', 'loc工厂',
                'translation workspace', 'sdl trados', 'across',
                'xbench', 'verifika', 'apertium'
            ]
        
        if self.cat_phrases is None:
            self.cat_phrases = [
                'система управления переводами', 'компьютерная поддержка переводов',
                'платформа локализации', 'translation management system',
                'cat platform', 'collaborative translation'
            ]
        
        if self.target_countries is None:
            self.target_countries = ['Россия', 'RU', 'РФ', 'Russia']

CONFIG = CatConfig()