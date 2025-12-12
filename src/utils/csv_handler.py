import csv
import pandas as pd
import os
from typing import List
from ..data_collectors.base import CompanyData

class CsvHandler:
    @staticmethod
    def save_companies_to_csv(companies: List[CompanyData], filepath: str):
        try:
            print(f"🔍 Отладка CSV: Начинаем сохранение {len(companies)} компаний в {filepath}")
            
            data = []
            for i, company in enumerate(companies):
                try:
                    data.append({
                        'inn': company.inn,
                        'name': company.name,
                        'revenue': company.revenue,
                        'site': company.site,
                        'cat_evidence': company.cat_evidence,
                        'source': company.source,
                        'cat_product': company.cat_product or '',
                        'employees': company.employees or '',
                        'okved_main': company.okved_main or '',
                        'country': company.country or ''
                    })
                    print(f"🔍 Отладка CSV: Обработана компания {i+1}: {company.name}")
                except Exception as e:
                    print(f"❌ Ошибка при обработке компании {i}: {e}")
                    continue
            
            if not data:
                print("❌ Нет данных для сохранения")
                return
            
            df = pd.DataFrame(data)
            print(f"🔍 Отладка CSV: DataFrame создан, размер: {df.shape}")
            
            output_dir = os.path.dirname(filepath)
            if output_dir and not os.path.exists(output_dir):
                print(f"📁 Создаем директорию: {output_dir}")
                os.makedirs(output_dir)
            
            print(f"🔍 Отладка CSV: Сохраняем в файл...")
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"✅ CSV файл успешно сохранен! Размер: {file_size} байт")
            else:
                print(f"❌ CSV файл не был создан!")
            
            print(f"📊 Данные сохранены в {filepath}. Всего компаний: {len(companies)}")
            
        except Exception as e:
            print(f"❌ Критическая ошибка при сохранении CSV: {e}")
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def load_companies_from_csv(filepath: str) -> List[CompanyData]:
        try:
            print(f"🔍 Отладка CSV: Загружаем данные из {filepath}")
            
            if not os.path.exists(filepath):
                print(f"❌ Файл не найден: {filepath}")
                return []
            
            df = pd.read_csv(filepath)
            print(f"🔍 Отладка CSV: Загружен DataFrame размером {df.shape}")
            
            companies = []
            for i, (_, row) in enumerate(df.iterrows()):
                try:
                    company = CompanyData(
                        inn=row['inn'],
                        name=row['name'],
                        revenue=row['revenue'] if pd.notna(row['revenue']) else None,
                        site=row['site'],
                        cat_evidence=row['cat_evidence'],
                        source=row['source'],
                        cat_product=row['cat_product'] if pd.notna(row['cat_product']) else None,
                        employees=row['employees'] if pd.notna(row['employees']) else None,
                        okved_main=row['okved_main'] if pd.notna(row['okved_main']) else None,
                        country=row['country'] if pd.notna(row['country']) else None
                    )
                    companies.append(company)
                except Exception as e:
                    print(f"❌ Ошибка при обработке строки {i}: {e}")
                    continue
            
            print(f"✅ Загружено компаний: {len(companies)}")
            return companies
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке CSV: {e}")
            import traceback
            traceback.print_exc()
            return []