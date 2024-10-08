import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/Cleaned_authors.csv")

dico={
}

genres = {
    "Historical & Historical Fiction": [
        "historical-fiction", "alternate-history", "historical-thriller", "historical-mystery", 
        "historical-fiction-1970s", "historical-romance", "historical-fantasy", "historical-china", 
        "american-civil-war", "medieval-romance", "reformation", "historical-urban-fantasy", 
        "new-adult-historical-fiction", "regency-romance", "historical", "historical-mystery", 
        "southern-gothic","israeli-palestinian-conflict","greek-mythology","cold-war-politics"
        ,"nuclear-history","cooking-history","scottish-history","canadian-literature","malaysian-literature"
        ,"native-american-sioux","middle-east","alternative-history","africa","military-history"

    ],
    "Literature & Literature Fiction": [
        "literature-fiction", "literary-fiction", "literary-criticism", "contemporary-fiction", 
        "fiction", "modern-contemporary-fiction", "general-fiction", "experimental", 
        "fiction-and-literature", "fiction-literature", "english-literature", "drama", 
        "classics", "book-club-fiction-literary-ficti", "contemporary", "popular-history", 
        "fiction-men-s-adventure", "social-realism", "slice-of-life", "post-apocalyptic","urban-fiction"
        ,"speculative-fiction-paranormal","southern-fiction","rock-fiction","speculative-fiction","biblical-fiction"
        ,"dystopia","children-s-fiction","literature"
    ],
    "Mystery and Thrillers": [
        "mystery-thrillers", "mystery", "mystery-thriller", "mystery-crime", "crime", 
        "mystery-thriller-suspense", "detective-mystery", "suspense", "suspense-thriller-fantasy", 
        "mystery-thrillers-particularl", "hard-boiled", "cozy-mystery", "espionage", 
        "psychological-thrillers", "suspense-paranormal-romance", 
        "murder", "mystery-thriller-suspense", "paranormal-mystery-romance", "detective-western", 
        "splatter-punk","thrillers","thriller-and-horror","mysteries-and-thrillers","crime-fiction"
        ,"thriller-suspense","horror","thriller"
    ],
    "Romance": [
        "romance", "gay-male-romances", "gay-romance", "contemporary-romance", "bdsm-romance", 
        "gay-romance-and-suspense", "dark-romance", "romantic-suspense", "gay-lesbian", 
        "gay-lesbian-yaoi-horror-rom", "dark-erotica-romance", "contemporary-romance-new-adult", 
        "romantic-comedy", "erotic-romance", "paranormal-romance", "paranormal-suspense", 
        "fantasy-paranormal-romance", "new-adult-romance", "romantic-fantasy", "romance-fiction", 
        "lgbtq-contemporary-romance", "gay", "gay-romance", "gay-fiction", "lesbian-fiction", 
        "lesbian-romance", "lesbian-non-fiction", "steamy-romance", "chivalric-romance", 
        "romantic-suspense-biker-fiction", "urban-fantasy-romance", "regency-romance", 
        "cowboy-romance", "contemp-romance", "paranormal-fiction", "m-m-romance", 
        "mm-romance", "dark-erotic-romance-suspense", "bdsm-erotica-erotic-romance", 
        "dark-dominant-men", "dark-suspense-erotica","erotic-suspense","dark-erotic-romance","bdsm"
        ,"erotic","dark-erotica","women-s-fiction-romance","science-fiction-romance","fantasy-romance","gay-and-lesbian-m-f"
        ,"romance-new-adult","yuri","gay-and-lesbian","erotica"

    ],
    "Young Adult": [
        "young-adult", "young-adult-new-adult", "ya-fantasy", "ya-paranormal-romance", 
        "ya-horror", "ya-urban-fantasy", "upper-ya", "young-adult-books", "mature-young-adult", 
        "ya-contemporary", "ya", "young-adult-and-new-adult", "young-adult-paranormal-romance", 
        "ya-paranormal-romance", "ya-na", "young-adult-paranormal-fantasy", "young-adult-new-adult-adult", 
        "children-s-middle-grade", "middle-grade-and-up", "middle-grade", "juvenile", 
        "children-s-young-adult", "coming-of-age", "middle-grade-fantasy", "young-adult-new-adult-adult",
        "new-adult-young-adult","adult-new-adult-young-adult","books-for-young-readers","shoujo","school-life"
        ,"teens","adult-contemporary","adult","new-adult"
    ],
    "Fantasy": [
        "fantasy", "urban-fantasy", "science-fiction-fantasy", "urban-magic", 
        "paranormal-and-fantasy", "epic-fantasy", "dark-fantasy", "speculative", 
        "urban-fantasy-romance", "ya-fantasy", "historical-urban-fantasy", "time-slip", 
        "magic-realism", "mythic-fantasy", "fantasy-science-fiction", "fantasy-paranormal-romance", 
        "paranormal-fantasy", "dark-fantasy-romance", "science-fiction-new-adult", "time-travel", 
        "magical-realism", "steampunk", "cyberpunk-science-fiction","science-fiction-urban-fantasy"
        ,"dystopian","science-fiction"
    ],
    "Non-Fiction": [
        "nonfiction", "memoir", "biographies-memoirs", "autobiography", "creative-nonfiction", 
        "essays", "popular-science", "travel", "science", "philosophy", "political-economy", 
        "economics", "journalism", "sociology", "history", "true-crime", "science-fiction-travel", 
        "psychology", "psychoanalysis", "photojournalism", "military", "anthropology", "law", 
        "politics", "civil-rights", "social-theory", "social-sciences", "linguistics", "neurology", 
        "computers-internet", "innovation", "business", "business-strategy", "corporate-strategy", 
        "business-investing", "motivational-speaker", "popular-history", "cooking-food-wine", 
        "cookbooks", "health-mind-body", "development-economics", "self-help", "goal-achievement", 
        "life-path", "relationships", "social-science-fiction", "history-of-ideas", "education", 
        "animals", "animal-fiction", "race-studies", "political-military-affairs", "women-s-fiction", 
        "nature", "parenting-families", "enviornment", "women-gender-studies", "african-american-studies", 
        "politics-and-social-activism", "style-guide", "gardening", "alcoholism-recovery", "business-success", 
        "nonfiction", "writing", "human-rights", "computers", "pets", "zoology", "horses", "boxing", 
        "sports", "hunting", "pets", "reference","current-events","surrealism","journalist","memoirs"
        ,"physics","metaphysics","literature-nonfiction","biology","evolution","military-art-science"
        ,"politcs","fiction-non-fiction","war-non-fiction","military-science","psychotherapy-psychoanalysis","transactional-analysis"
        ,"professional-technical","legal-issues","home-garden","cooking","novellas","physiology","psychiatry"
        ,"cultural-studies","political-science","existentialism","classical-liberal","political-economist","outdoors-nature"
        ,"non-fiction","biography"

    ],
    "Religion and Spirituality": [
        "religion", "christianity", "catholicism", "lutheranism", "puritan", 
        "calvinism", "catholic-saints", "budhdhism", "christian-fantasy", "theology", 
        "spirituality", "religion-spirituality", "spirituality-philosophy", 
        "christian-fiction", "christian-apologetics", "inspirational", "channeling", 
        "christianity-culture", "religion","atheism","creationism","occult-supernatural"
        ,"christian"
    ],
    "Comedy and Humor": [
        "humor", "humor-and-comedy", "satire", "political-satire", "gentle-satire", 
        "dark-comedy", "humour", "comedy-humor", "dark-comedy", "tragicomedy", 
        "humor-cats-dogs-and-animals", "bizarro-fiction", "gonzo-journalism", 
        "bizarro", "bizzaro", "weird-fiction","playwright","allegory","comedy"
        ,"plays-screenplays"
    ],
    "Adventure and Action": [
        "action", "adventure", "action-adventure", "pulp-technothriller", "superhero-fiction", 
        "military-fiction", "western", "detective-western", "exploration", "war", 
        "superhero", "action-adventure", "u-s-diplomacy-and-culture", "alternate-history"
    ],
    "Miscellaneous": [
        "comics", "graphic-novels", "manga", "fanfiction", "fan-fiction", "ebooks", 
        "litrpg", "screenwriter", "movie-tie-ins", "illustrations", "children-s", 
        "picture-books", "songs-poetry-arts", "cinema", "film", "stage-plays", 
        "plays", "theatre", "plays-and-drama", "comic-books", "comic-books", 
        "superhero", "m-m-sometimes-m-m-m", "shojo", "yaoi", "boys-love", "bl", 
        "sports", "magazine", "mythology", "myths-legends", "folklore", "fairy-tales", 
        "fairytales", "myths-legends", "animals", "dog-training-and-behaviour", 
        "fashion", "art", "art-photojournalism", "arts-photography", "drama", 
        "cinema", "music", "music", "screen-play", "screenwriter", "reference", 
        "essays", "theater", "theatre", "plays","cozy","folk-tales","ethics","game-novelization"
        ,"gothic","language","women","death","firearms","short-story","novel","self-improvement"
        ,"letters","feminism","amish","country-noir","yaya","essayist","diaries","real-life-experiences","slipstream"
        ,"worldview","horror-crime","crafts-hobbies","fiksi-remaja","horse-racing","worldviews"
        ,"editor","humanities","westerns","criticism","strategy","hockey","novels","pseudo-history","nanotechnology","middle-grade-novel","mind-body-spirit"
        ,"poetry","children-s-books","short-stories","comics-graphic-novels","paranormal","chick-lit","entertainment"
    ]
}



Male=0
Female=0
Other=0
for index, row in data.iterrows():
    if row['author_gender']=='male':
        Male+=1
    elif(row['author_gender']=='female'): 
        Female+=1
    else:
        Other+=1
    for i in row['author_genres'].split(','):
        if(i not in dico):
            dico[i] = [['Male',0],['Female',0]]
        if row['author_gender']=='male':
            dico[i][0][1] = dico[i][0][1]+1
        else:
            dico[i][1][1] = dico[i][1][1]+1


# for i in listeAsupr:
#     dico.pop(i)

a=0
for i in dico:
    if ((dico[i][0][1]+dico[i][1][1])>=10):
        for y in genres:
            if i in genres[y]:
                a=+1
        if(a>1):
            print(i)
        a=0

lengenre=0
for i in genres:
    lengenre=lengenre+len(genres[i])

print(lengenre, len(dico))

for i in genres:
    listeTot = [['Male',0],['Female',0]]
    for y in genres[i]:
        listeTot[0][1]=listeTot[0][1]+dico[y][0][1]
        listeTot[1][1]=listeTot[1][1]+dico[y][1][1]
    genres[i] = listeTot



dfHomme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])

dfFemme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])


#Pourcentage Homme
for i in genres:
    if(genres[i][1][1]!=0):
        dfHomme.loc[len(dfHomme.index)] = [i, genres[i][0][1]/(genres[i][0][1] + genres[i][1][1])*100] 
    else:
        dfHomme.loc[len(dfHomme.index)] = [i, 100] 

#Pourcentage Femme
for i in genres:
    if(genres[i][0][1]!=0):
        dfFemme.loc[len(dfFemme.index)] = [i, genres[i][1][1]/(genres[i][0][1] + genres[i][1][1])*100] 
    else:
        dfFemme.loc[len(dfFemme.index)] = [i, 100] 


# fig = plt.figure(figsize = (10, 5))

# # creating the bar plot
# plt.bar(dfHomme['genre'], dfHomme['pourcentageSexe'], color ='maroon', width = 0.4)

# plt.xlabel("Genre Littéraire")
# plt.ylabel("Pourcentage d'Homme/Femme")
# plt.title("Genre littéraire en fonction du pourcentage d'homme et de femmes écrivant dans celui-ci")
# plt.show()

N = 11
ind = np.arange(N)
width = 0.35

fig, ax = plt.subplots(figsize =(10, 7))
p1 = ax.bar(ind, dfHomme['pourcentageSexe'], width)
p2 = ax.bar(ind, dfFemme['pourcentageSexe'], width, bottom = dfHomme['pourcentageSexe'])

ax.set_ylabel('Percentage of authors which are men or women')
ax.set_title('Percentage of authors of each sex which consider the genre their main one')
ax.set_xticks(ind)
ax.set_xticklabels(dfHomme['genre'])
ax.set_yticks(np.arange(0, 81, 10))
ax.set_yticks(np.arange(0, 101, 10))
ax.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.setp(ax.get_xticklabels(), rotation=20, ha="right", rotation_mode="anchor")

plt.show()

# https://www.geeksforgeeks.org/bar-plot-in-matplotlib/




dfNbrHomme = pd.DataFrame(columns=['genre', 'nbr'])

#Nbr Homme
for i in genres:
    dfNbrHomme.loc[len(dfNbrHomme.index)] = [i, genres[i][0][1]] 

dfNbrHomme = dfNbrHomme.sort_values("nbr")

plt.pie(dfNbrHomme['nbr'], labels=dfNbrHomme['genre'])
plt.title('Main genre of Male authors')
plt.show()



dfNbrFemme = pd.DataFrame(columns=['genre', 'nbr'])

#Nbr Femme
for i in genres:
    dfNbrFemme.loc[len(dfNbrFemme.index)] = [i, genres[i][1][1]] 

dfNbrFemme = dfNbrFemme.sort_values("nbr")

plt.pie(dfNbrFemme['nbr'], labels=dfNbrFemme['genre'])
plt.title('Main genre of Female authors')
plt.show()





