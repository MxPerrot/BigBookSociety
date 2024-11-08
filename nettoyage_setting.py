import pandas as pd
import re

df = pd.read_csv("data/Cleaned_books.csv")

countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", 
    "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", 
    "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", 
    "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", 
    "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", 
    "Chile", "China", "Colombia", "Comoros", "Congo", "Congo", "Costa Rica", "Croatia", 
    "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", 
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", 
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", 
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", 
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", 
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "North Korea", 
    "South Korea", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", 
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", 
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
    "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", 
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", 
    "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", 
    "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", 
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", 
    "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", 
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", 
    "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", 
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Récupère les informations propres au différents settings du livre et les sépares
patternGlobal = r'(?:[A-Za-z\.]+(?:, |\s)?)+(?:,\d+)?(?:\([a-zA-Z\s]+\))?'

df['settingsClean'] = df['settings'].str.findall(patternGlobal)
# Crée une ligne pour chaque setting
df = df.explode('settingsClean', ignore_index=True)

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
        
patternPays = r'\([a-zA-Z\s]+\)'
df['settingCountry'] = df['settingsClean'].str.findall(patternPays).apply(extractCountry)
#print(df['settingCountry'].to_string())

patternDate = r'\d+'
df['settingDate'] = df['settingsClean'].str.findall(patternDate).apply(extract)
#print(df['settingDate'])

patternName = r'^(?:[A-Za-z\.]+(?:, |\s)?)+'
df['settingLoc'] = df['settingsClean'].str.findall(patternName).apply(extract)
#print(df['settingLoc'])

# Extraire les awards
df['awardsClean'] = df['awards'].str.split(',')
df = df.explode('awardsClean', ignore_index=True)

#print(df['awardsClean'])

df['awardDate'] = df['awardsClean'].str.findall(patternDate).apply(extract)
#print(df['awardDate'])

df['awardName'] = df['awardsClean'].str.findall(patternName).apply(extract)
#print(df['awardName'])

df = df.drop(columns = ['settings'])
df = df.drop(columns = ['awards'])
df = df.drop(columns = ['settingsClean'])
df = df.drop(columns = ['awardsClean'])

print(f"\n--- Purge colonnes unnamed    ---\n")

str_column="Unnamed: "
for i in range(27,65):
    df = df.drop(columns=[str_column+str(i)])

df.to_csv('./data/Cleaned_books2.csv', index=False)