import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
from operator import itemgetter

NB_DIMENTION_VECTEUR = 4
NOMBRE_UTILISATEURS_TESTES = 100

def setUpCursor():
    # loading variables from .env file
    load_dotenv() 

    connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"), 
        user=os.getenv("USERNAME"), 
        password=os.getenv("PASSWORD"), 
        host=os.getenv("HOST"), 
        port=os.getenv("PORT")
    )

    cursor = connection.cursor()
    cursor.execute("SET SCHEMA 'sae';")

    return cursor

def getUtilisateur(cursor, id_utilisateur):
    cursor.execute(f"""
        SELECT 
            _utilisateur.id_utilisateur, 
            _utilisateur.sexe, 
            _utilisateur.age, 
            _utilisateur.profession, 
            _utilisateur.situation_familiale, 
            _utilisateur.frequence_lecture, 
            _utilisateur.vitesse_lecture, 
            _utilisateur.nb_livres_lus
                   
        FROM _utilisateur
        
        WHERE _utilisateur.id_utilisateur = {id_utilisateur}
    """)

    utilisateur = cursor.fetchall()

    return pd.DataFrame(utilisateur, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus"])

def getUtilisateursAEvaluer(cursor):
    cursor.execute(f"""
        SELECT _utilisateur.id_utilisateur
        FROM _utilisateur
        ORDER BY random()
        LIMIT {NOMBRE_UTILISATEURS_TESTES};
    """)
    
    idUtilisateursAEvaluerRaw = cursor.fetchall()
    idUtilisateursAEvaluer = tuple([utilisateur[0] for utilisateur in idUtilisateursAEvaluerRaw])
    

    cursor.execute(f"""
        SELECT 
            _utilisateur.id_utilisateur, 
            _utilisateur.sexe, 
            _utilisateur.age, 
            _utilisateur.profession, 
            _utilisateur.situation_familiale, 
            _utilisateur.frequence_lecture, 
            _utilisateur.vitesse_lecture, 
            _utilisateur.nb_livres_lus
                   
        FROM _utilisateur
        
        WHERE _utilisateur.id_utilisateur IN {idUtilisateursAEvaluer}
    """)

    userData = cursor.fetchall()
    
    if len(userData) == 0:
        return -1
    
    userList = [list(user) for user in userData]
    return pd.DataFrame(userList, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus"])

def getIdLivresUtilisateur(cursor, id_utilisateur):
    cursor.execute(f"""
        SELECT DISTINCT _livre.id_livre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        WHERE _utilisateur.id_utilisateur = {id_utilisateur};
    """)

    userData = cursor.fetchall()

    if len(userData) == 0:
        return -1
    
    userIdBookList = [list(book)[0] for book in userData]

    return userIdBookList


# ----------------------------------
#  Fonctions de vectorisation 
# ----------------------------------

def vectorizeAge(age):
    """
    """
    if age == "+ de 65 ans":
        indAge = 4
    elif age == "Entre 40 et 65 ans":
        indAge = 3
    elif age == "Entre 25 et 39 ans":
        indAge = 2
    elif age == "Entre 18 et 24 ans":
        indAge = 1
    else :
        indAge = 0
    return indAge

def vectorizeReadingFrequence(frequ):
    """
    """
    if frequ == "Quotidiennement":
        indFrequ = 4
    elif frequ == "Plusieurs fois par semaine":
        indFrequ = 3
    elif frequ == "Une fois par mois":
        indFrequ = 2
    elif frequ == "Plus rarement":
        indFrequ = 1
    else :
        indFrequ = 0
    return indFrequ

def vectorizeNbBookRed(nbBook):
    """
    """
    if nbBook == "Plus de 20":
        indNbBook = 4
    elif nbBook == "De 11 à 20":
        indNbBook = 3
    elif nbBook == "De 6 à 10":
        indNbBook = 2
    elif nbBook == "De 1 à 5":
        indNbBook = 1
    else :
        indNbBook = 0
    return indNbBook

"""
def indexSexe(gender):
"""
# test
"""
    if gender == "Femme":
        indGen = 2
    elif gender == "Homme":
        indGen = 1
    else :
        indGen = 0
    return indGen

def indexSituationProfessionelle(situPro):
"""
"""
    if situPro == "Etudiant":
        indAge = 7
    elif situPro == "Alternant":
        indAge = 6
    elif situPro == "Employé":
        indAge = 5
    elif situPro == "Patron/Auto-entrepreuneur":
        indAge = 4
    elif situPro == "Fonctionnaire":
        indAge = 3
    elif situPro == "Sans emploi":
        indAge = 2
    elif situPro == "Retraité":
        indAge = 1
    else :
        indAge = 0
    return indAge

def indexSituationProfessionelle(situPro):
"""
"""
    if situPro == "Célibataire":
        indAge = 6
    elif situPro == "Concubinage":
        indAge = 5
    elif situPro == "Pacsée":
        indAge = 4
    elif situPro == "Marié(e)":
        indAge = 3
    elif situPro == "Divorcé":
        indAge = 2
    elif situPro == "Veuf/Veuve":
        indAge = 1
    else :
        indAge = 0
    return indAge
"""

def defineUserVect(book):
    vecteurUser = []
    # Tout les lignes d'un même livre ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
    vecteurUser.append(int(book["age"].apply(vectorizeAge).iloc[0]))
    vecteurUser.append(int(book["frequence_lecture"].apply(vectorizeReadingFrequence).iloc[0]))
    vecteurUser.append(int(book["vitesse_lecture"].iloc[0]))
    vecteurUser.append(int(book["nb_livres_lus"].apply(vectorizeNbBookRed).iloc[0]))
    return vecteurUser

def compareValeur(nomValeur, livreX, livreY):
    """
    Renvoie True si ces livres partagent la même valeur indiquée par le paramétre nomValeur
    """
    return bool(livreX[nomValeur].iloc[0] == livreY[nomValeur].iloc[0])

def calculateScore(cossim, listSim):
    """
    Calcule le Score global de similarité d'une comparaison entre deux objets
    Fait la moyenne des indices de similarités et pondérant celui de la similarité cosine dû au fait qu'elle prends plus de valeurs en compte
    """
    scoreSum = cossim * NB_DIMENTION_VECTEUR
    cmpt = NB_DIMENTION_VECTEUR
    for sim in listSim:
        scoreSum += sim
        cmpt += 1
    return float(scoreSum/cmpt)

def recommendationItemBased(cursor, id_utilisateur, nbRecommendations):
    userData = getUtilisateur(cursor, id_utilisateur)
    vecteurUser = defineUserVect(userData)

    utilisateursAEvaluer = getUtilisateursAEvaluer(cursor)
    # TODO: retirer l'utilisateur en paramétre de la liste à évaluer si pris
    simCosUsers = {}
    livresPref = {}
    userSim = []
    i = 0

    for id_userEva, userEva in utilisateursAEvaluer.groupby(by="id_utilisateur"):
        vecteurEva = defineUserVect(userEva)
        simCosUsers[id_userEva] = np.dot(vecteurUser,vecteurEva)/(norm(vecteurUser)*norm(vecteurEva))
        livresPref[id_userEva] = getIdLivresUtilisateur(cursor, id_userEva)
        cmpSexe = compareValeur('sexe', userEva, userData)
        cmpPro = compareValeur('profession', userEva, userData)
        cmpFami = compareValeur('situation_familiale', userEva, userData)

        userSim.append((id_userEva,calculateScore(simCosUsers[id_userEva], [cmpSexe, cmpPro, cmpFami])))
        
        i+=1

    sortUserSim = sorted(userSim, key=itemgetter(1))
    print(sortUserSim)

    

    # TODO: retirer livres préférés de l'utilisateur avant de recommander
    return None


cursor = setUpCursor()
print(recommendationItemBased(cursor, 11, 5))