import pandas as pd
import re

CHEMIN_FICHIER_LIVRES = "Big_book.csv"

# extrait le résultat d'une recherche findall
def extract(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0]
    else :
        return None

# extrait le résultat d'une recherche findall pour le pays (retire les parenthèses)
def extractWP(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0].replace('(','').replace(')','')
    else :
        return None

# transforme une date au format "April 15th 1988" en "1988-04-15" pour correspondre au format date de SQL
def reformatDate(dateString):

    # Au nom d'un mois associe son numéro
    month_dict = {
        "January": '01',
        "February": '02',
        "March": '03',
        "April": '04',
        "May": '05',
        "June": '06',
        "July": '07',
        "August": '08',
        "September": '09',
        "October": '10',
        "November": '11',
        "December": '12'
    }

    # Prend en compte le cas null
    if pd.isnull(dateString):
        return None

    # Récupère l'année et la formate
    year = re.findall(r'\d{4}$', dateString)
    if len(year) == 0:
        return None
    else:
        year = year[0]

    # Récupère le mois et le formate
    month = re.findall(r'^[a-zA-Z]+', dateString)
    if len(month) == 0:
        month = '01'
    else:
        month = month_dict[month[0]]

    # Récupère le jour et le formate
    day = re.findall(r'\d{1,2}(?:(?:st)|(?:nd)|(?:rd)|(?:th))', dateString)
    if len(day) == 0:
        day = '01'
    else:
        day = day[0].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
        if len(day) < 2:
            day = '0'+day

    return year+'-'+month+'-'+day

# Lit le fichier CSV avec les données brutes
df = pd.read_csv(CHEMIN_FICHIER_LIVRES)

# Pattern regex pour séparer les différents settings
patternSetting = r'(?:[A-Za-z\.]+(?:, |\s)?)+(?:,\d+)?(?:\([a-zA-Z\s]+\))?'
# Pattern regex pour extraire le nom du pays dans le setting
patternPays = r'\([a-zA-Z\s]+\)'
# Pattern regex pour extraire un nombre d'une chaîne de caratères 
patternChiffre = r'\d+'
# Pattern regex pour extraire un nom d'une chaîne
patternName = r'^(?:[\w\.\/\-\'\:éèïôçêùæœëüâ€©¤ãűúöäà]+(?:, |\s)?)+[\w\.\/\-\'\:éèïôçêùæœëüâ€©¤ãűúöäà]+'
# Pattern regex pour extraire une date entourée de parenthèses 
patternDate = r'\(\d+\)'
# Pattern regex pour extraire un numéro d'épisode 
patternEpNum = r'#[\d.-]+'

# Crée une liste contenant les différents settings séparés
df['settingsClean'] = df['settings'].str.findall(patternSetting)
# Duplique les lignes pour n'avoir qu'un setting par ligne
df = df.explode('settingsClean', ignore_index=True)

# Crée une colonne contenant le nom du pays du setting
df['settingCountry'] = df['settingsClean'].str.findall(patternPays).apply(extractWP)

# Crée une colonne contenant la date du setting
df['settingDate'] = df['settingsClean'].str.findall(patternChiffre).apply(extract)

# Crée une colonne contenant le lieu du setting
df['settingLoc'] = df['settingsClean'].str.findall(patternName).apply(extract)

# Crée une liste contenant les différents awards séparés
df['awardsClean'] = df['awards'].str.split(', ')

# Duplique les lignes pour n'avoir qu'un award par ligne
df = df.explode('awardsClean', ignore_index=True)

# Crée une colonne contenant la date d'obtention de l'award
df['awardDate'] = df['awardsClean'].str.findall(patternDate).apply(extractWP)

# Crée une colonne contenant le nom de l'award
df['awardName'] = df['awardsClean'].str.findall(patternName).apply(extract)

# Crée une colonne contenant le nombre de l'épisode d'une série de livres
df['episodeNumber'] = df['series'].str.findall(patternEpNum).apply(extract).str.replace('#','')

# Crée une colonne contenant le nom de la série
df['seriesName'] = df['series'].str.replace('(','').str.findall(patternName).apply(extract)

# Crée une colonne contenant la date de publication du livre au bon format (Date SQL)
df['date_published'] = df['date_published'].apply(reformatDate)

# Supprime les colonnes non utilisées
df = df.drop(columns = ['settings'])
df = df.drop(columns = ['awards'])
df = df.drop(columns = ['settingsClean'])
df = df.drop(columns = ['awardsClean'])
df = df.drop(columns = ['series'])

df.to_csv('./data/Cleaned_books2.csv', index=False)