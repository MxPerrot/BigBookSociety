import pandas as pd
import re

file_path = 'books.csv'
data = pd.read_csv(file_path, low_memory=False)

# Fonction pour extraire l'année, gérer les cas où la date est au format BC, et gérer les valeurs manquantes
def extract_year_no_nan(date_str):
    if isinstance(date_str, str):
        date_str = date_str.strip()
        
        # Vérifier les dates avant notre ère (BC) et retourner l'année négative
        if 'BC' in date_str:
            year_match = re.search(r'(\d+)', date_str)
            if year_match:
                return -int(year_match.group(1))
        
        # Extraire l'année des formats de date habituels
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            return int(year_match.group(1))
    
    return 0

data['date_published_formated'] = data['date_published'].apply(extract_year_no_nan)

data['date_published'] = data['date_published_formated']

data = data.drop(columns=['date_published_formated'])

print(data[['date_published']].head(10))

data.to_csv('books_forma_dates.csv', index=False)

print(data.head())
