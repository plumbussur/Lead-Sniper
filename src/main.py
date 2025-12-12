import argparse
import sys
import os
import traceback
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("Отладка: Проверяем пути...")
    print(f"   Текущая директория: {os.getcwd()}")
    print(f"   Файл main.py: {os.path.abspath(__file__)}")
    print(f"   Родительская директория: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    
    parser = argparse.ArgumentParser(description='Анализатор российских компаний, использующих CAT-системы')
    parser.add_argument('--output', '-o', default='data/companies.csv', help='Путь для сохранения результата')
    parser.add_argument('--collect', '-c', action='store_true', help='Собрать новые данные')
    parser.add_argument('--analyze', '-a', action='store_true', help='Анализировать существующие данные')
    parser.add_argument('--sources', nargs='+', default=['all'], 
                       choices=['rusprofile', 'catalog', 'all'], 
                       help='Источники данных для сбора')
    
    args = parser.parse_args()
    
    print(f"Отладка: Аргументы - {args}")
    
    try:
        if args.collect:
            collect_and_process_data(args.output, args.sources)
        elif args.analyze:
            analyze_existing_data(args.output)
        else:
            collect_and_process_data(args.output, args.sources)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        print("Полная трассировка:")
        traceback.print_exc()

def collect_and_process_data(output_path: str, sources: List[str]):
    print("Начинаем сбор и обработку данных...")
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"Создаем директорию: {output_dir}")
        os.makedirs(output_dir)
    
    try:
        from src.data_collectors.rusprofile_collector import RusprofileCollector
        from src.data_collectors.catalog_scanner import CatalogScanner
        from src.data_collectors.website_parser import WebsiteParser
        from src.processors.data_cleaner import DataCleaner
        from src.processors.revenue_validator import RevenueValidator
        from src.processors.cat_classifier import CatClassifier
        from src.utils.csv_handler import CsvHandler
        from config.settings import CONFIG
        
        all_companies = []
        
        if 'rusprofile' in sources or 'all' in sources:
            print("\nСбор данных с Rusprofile...")
            rusprofile_collector = RusprofileCollector()
            rusprofile_companies = rusprofile_collector.collect_companies()
            all_companies.extend(rusprofile_companies)
            print(f"   Найдено компаний: {len(rusprofile_companies)}")
        
        if 'catalog' in sources or 'all' in sources:
            print("\nСбор данных из каталогов...")
            catalog_scanner = CatalogScanner()
            catalog_companies = catalog_scanner.collect_companies()
            all_companies.extend(catalog_companies)
            print(f"   Найдено компаний: {len(catalog_companies)}")
        
        print(f"Отладка: Всего собрано компаний: {len(all_companies)}")
        
        if not all_companies:
            print("Не удалось собрать данные из указанных источников")
            print("Создаем демонстрационный файл...")
            create_demo_file(output_path)
            return
        
        print("\nОчистка данных...")
        cleaned_companies = DataCleaner.clean_company_data(all_companies)
        print(f"   После очистки: {len(cleaned_companies)}")
        
        print("\nФильтрация по выручке...")
        revenue_filtered = RevenueValidator.filter_by_revenue(cleaned_companies)
        print(f"   После фильтрации по выручке: {len(revenue_filtered)}")
        
        print("\nКлассификация по CAT-системам...")
        cat_classified = CatClassifier.classify_companies(revenue_filtered)
        print(f"   После классификации CAT: {len(cat_classified)}")
        
        if not cat_classified:
            print("Компании после фильтрации отсутствуют. Создаем демонстрационные данные...")
            create_demo_file(output_path)
            return
        
        print("\nАнализ сайтов компаний...")
        website_parser = WebsiteParser()
        final_companies = website_parser.analyze_multiple_companies(cat_classified)
        
        print("\nУлучшение доказательств CAT...")
        enhanced_companies = CatClassifier.enhance_cat_evidence(final_companies)
        
        print(f"\nСохранение результата в {output_path}...")
        print(f"Отладка: Путь к файлу: {os.path.abspath(output_path)}")
        
        CsvHandler.save_companies_to_csv(enhanced_companies, output_path)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"Файл успешно создан! Размер: {file_size} байт")
        else:
            print(f"Файл не был создан по пути: {output_path}")
        
        print("\nАнализ завершен!")
        print(f"Итоговый результат: {len(enhanced_companies)} компаний")
        
    except Exception as e:
        print(f"Ошибка в процессе обработки: {e}")
        print("Полная трассировка:")
        traceback.print_exc()
        
        print("Создаем демонстрационный файл...")
        create_demo_file(output_path)

def create_demo_file(output_path: str):
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        demo_data = [
            {
                'inn': '7701234567',
                'name': 'ООО "Локализация Про"',
                'revenue': 150000000,
                'site': 'localization-pro.ru',
                'cat_evidence': 'упоминание Trados Studio',
                'source': 'demo',
                'cat_product': 'Trados Studio',
                'employees': '25',
                'okved_main': '62.01',
                'country': 'Россия'
            },
            {
                'inn': '7712345678',
                'name': 'АО "Транслейт Тех"',
                'revenue': 200000000,
                'site': 'translatetech.ru',
                'cat_evidence': 'использование TMS',
                'source': 'demo',
                'cat_product': 'Собственная TMS',
                'employees': '45',
                'okved_main': '62.02',
                'country': 'Россия'
            },
            {
                'inn': '7812345678',
                'name': 'ООО "Глобал Транслейт"',
                'revenue': 300000000,
                'site': 'global-translate.com',
                'cat_evidence': 'использование MemoQ; упоминание памяти переводов',
                'source': 'demo',
                'cat_product': 'MemoQ',
                'employees': '80',
                'okved_main': '74.30',
                'country': 'Россия'
            }
        ]
        
        import pandas as pd
        df = pd.DataFrame(demo_data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"Демонстрационный файл создан: {output_path}")
        
    except Exception as e:
        print(f"Ошибка при создании демонстрационного файла: {e}")

def analyze_existing_data(csv_path: str):
    print(f"Анализ существующих данных из {csv_path}...")
    
    try:
        from src.utils.csv_handler import CsvHandler
        
        companies = CsvHandler.load_companies_from_csv(csv_path)
        if not companies:
            print("Не удалось загрузить данные")
            return
        
        print(f"Загружено компаний: {len(companies)}")
        
        revenues = [c.revenue for c in companies if c.revenue]
        if revenues:
            print(f"Средняя выручка: {sum(revenues) / len(revenues):,.0f} ₽")
            print(f"Максимальная выручка: {max(revenues):,.0f} ₽")
            print(f"Минимальная выручка: {min(revenues):,.0f} ₽")
        
        sources = {}
        for company in companies:
            source = company.source
            sources[source] = sources.get(source, 0) + 1
        
        print("\nСтатистика по источникам:")
        for source, count in sources.items():
            print(f"   {source}: {count}")
            
    except Exception as e:
        print(f"Ошибка при анализе данных: {e}")

if __name__ == "__main__":
    main()