import pandas as pd
import re

def extract(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0]
    else :
        return None

def extractCountry(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0].replace('(','').replace(')','')
    else :
        return None

def reformatDate(dateString):
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

    if pd.isnull(dateString):
        return None

    year = re.findall(r'\d{4}$', dateString)
    if len(year) == 0:
        return None
    else:
        year = year[0]

    month = re.findall(r'^[a-zA-Z]+', dateString)
    if len(month) == 0:
        month = '01'
    else:
        month = month_dict[month[0]]

    day = re.findall(r'\d{1,2}(?:(?:st)|(?:nd)|(?:rd)|(?:th))', dateString)
    if len(day) == 0:
        day = '01'
    else:
        day = day[0].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
        if len(day) < 2:
            day = '0'+day

    return year+'-'+month+'-'+day

df = pd.read_csv("data/Cleaned_books.csv")

# Récupère les informations propres au différents settings du livre et les sépares
patternGlobal = r'(?:[A-Za-z\.]+(?:, |\s)?)+(?:,\d+)?(?:\([a-zA-Z\s]+\))?'

df['settingsClean'] = df['settings'].str.findall(patternGlobal)
# Crée une ligne pour chaque setting
df = df.explode('settingsClean', ignore_index=True)

patternPays = r'\([a-zA-Z\s]+\)'
df['settingCountry'] = df['settingsClean'].str.findall(patternPays).apply(extractCountry)
#print(df['settingCountry'].to_string())

patternChiffre = r'\d+'
df['settingDate'] = df['settingsClean'].str.findall(patternChiffre).apply(extract)
#print(df['settingDate'])

patternName = r'^(?:[A-Za-z\.]+(?:, |\s)?)+'
df['settingLoc'] = df['settingsClean'].str.findall(patternName).apply(extract)
#print(df['settingLoc'])

# Extraire les awards
df['awardsClean'] = df['awards'].str.split(',')
df = df.explode('awardsClean', ignore_index=True)

#print(df['awardsClean'])

df['awardDate'] = df['awardsClean'].str.findall(patternChiffre).apply(extract)
#print(df['awardDate'])

df['awardName'] = df['awardsClean'].str.findall(patternName).apply(extract)
#print(df['awardName'])

df['episodeNumber'] = df['series'].str.findall(patternChiffre).apply(extract)
print(df['episodeNumber'])

df['seriesName'] = df['series'].str.replace('(','').str.findall(patternName).apply(extract)
print(df['seriesName'])

df['date_published'] = df['date_published'].apply(reformatDate)
print(df['date_published'])

# Supprime les colonnes non utilisées
df = df.drop(columns = ['settings'])
df = df.drop(columns = ['awards'])
df = df.drop(columns = ['settingsClean'])
df = df.drop(columns = ['awardsClean'])
df = df.drop(columns = ['series'])

#df.to_csv('./data/Cleaned_books2.csv', index=False)