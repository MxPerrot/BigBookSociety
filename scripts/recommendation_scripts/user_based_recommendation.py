import pandas as pd
import numpy as np
import random as rd
from numpy.linalg import norm
from operator import itemgetter
import recommendation_utilities as ru
import database_functions as bdd

NB_DIMENTION_VECTEUR = 4
NOMBRE_UTILISATEURS_TESTES = 100

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

def defineUserVect(book):
    vecteurUser = []
    # Tout les lignes d'un même utilisateur ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
    vecteurUser.append(int(book["age"].apply(vectorizeAge).iloc[0]))
    vecteurUser.append(int(book["frequence_lecture"].apply(vectorizeReadingFrequence).iloc[0]))
    vecteurUser.append(int(book["vitesse_lecture"].iloc[0]))
    vecteurUser.append(int(book["nb_livres_lus"].apply(vectorizeNbBookRed).iloc[0]))
    return vecteurUser

# ----------------------------
#  Fonction principale
# ----------------------------

def recommendationItemBased(cursor, id_utilisateur_a_recommander, nbRecommendations):
    livresLus = bdd.getIdLivresUtilisateur(cursor, id_utilisateur_a_recommander)

    userData = bdd.getUtilisateurById(cursor, id_utilisateur_a_recommander)
    vecteurUser = defineUserVect(userData)

    utilisateursAEvaluer = bdd.getUtilisateursAEvaluer(cursor, NOMBRE_UTILISATEURS_TESTES)
    simCosUsers = {}
    userSim = []
    i = 0

    for id_userEva, userEva in utilisateursAEvaluer.groupby(by="id_utilisateur"):
        vecteurEva = defineUserVect(userEva)
        simCosUsers[id_userEva] = np.dot(vecteurUser,vecteurEva)/(norm(vecteurUser)*norm(vecteurEva))
        cmpSexe = ru.compareValeur('sexe', userEva, userData)
        cmpProfes = ru.compareValeur('profession', userEva, userData)
        cmpFamille = ru.compareValeur('situation_familiale', userEva, userData)

        cmpLangue = ru.valeursEnCommun('langue', userEva, userData, "id_utilisateur")
        cmpMotiva = ru.valeursEnCommun('motivation', userEva, userData, "id_utilisateur")
        cmpRaison = ru.valeursEnCommun('raison_achat', userEva, userData, "id_utilisateur")
        cmpProcur = ru.valeursEnCommun('procuration', userEva, userData, "id_utilisateur")
        cmpFormat = ru.valeursEnCommun('format', userEva, userData, "id_utilisateur")

        userSim.append((id_userEva,ru.calculateScore(simCosUsers[id_userEva], [cmpSexe, cmpProfes, cmpFamille, cmpLangue, cmpMotiva, cmpRaison, cmpProcur, cmpFormat], NB_DIMENTION_VECTEUR)))
        
        i+=1

    sortUserSim = sorted(userSim, key=itemgetter(1), reverse=True)

    cpt = 0
    nbLivresARec = nbRecommendations
    livreRecommandes = []
    """
    # Première approche
    while nbLivresARec > 0:
        idUser = sortUserSim[cpt][0]
        if idUser != id_utilisateur_a_recommander:
            livres_preferés = bdd.getIdLivresUtilisateur(cursor, idUser)
            print(idUser,livres_preferés)
            if livres_preferés != -1:
                for livreId in livres_preferés:
                    if nbLivresARec > 0:
                        if livresLus != -1:
                            if (livreId not in livresLus):
                                livreRecommandes.append(livreId)
                                nbLivresARec-=1
                        else:
                            livreRecommandes.append(livreId)
                            nbLivresARec-=1
        cpt+=1
        if cpt >= len(sortUserSim):
            break
    """
    # Seconde approche

    sortUserSim = [usr for usr in sortUserSim if usr[0] != id_utilisateur_a_recommander]
    for (idUser,simCos) in sortUserSim:
        livres_preferés = bdd.getIdLivresUtilisateur(cursor, idUser)
        livresTestés = 0
        if livres_preferés != -1:
            for i in range(len(livres_preferés)):
                livre_a_rec = rd.choice(livres_preferés)
                livres_preferés.remove(livre_a_rec)
                livresTestés += 1
                if livresLus != -1:
                    if (livre_a_rec not in livresLus):
                        livreRecommandes.append(livre_a_rec)
                        nbLivresARec-=1
                        break
                else:
                    livreRecommandes.append(livre_a_rec)
                    nbLivresARec-=1
                    break
        if nbLivresARec <= 0:
            break

            

    return livreRecommandes


cursor = ru.setUpCursor()
idLivresRecommandes = recommendationItemBased(cursor, 124, 5)

cursor.execute(f"""
    SELECT DISTINCT _livre.titre, _auteur.nom, _genre.libelle_genre
    FROM _livre

    LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
    LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

    LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
    LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre

    WHERE _livre.id_livre IN {tuple(idLivresRecommandes)};
""")

livresRecommandes = cursor.fetchall()
print(livresRecommandes)