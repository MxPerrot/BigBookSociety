import os
import pandas as pd
import numpy as np

PATH_DATA = "../Wizards/formulaire/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

def main(results):
    os.makedirs(PATH_POPULATE, exist_ok=True) #Créé le dossier voulu

    ##### COLONNES DU CSV #####
    mails = results['Nom d\'utilisateur']
    sexe = results['Je suis...']
    age = results['Quel âge avez-vous ?']
    situation_pro = results['Quelle est votre situation professionnelle ? (Optionnel)']
    situation_famille = results['Quelle est votre situation familiale ? (Optionnel)']
    code_postal = results['Code postal, si résident français (Optionnel)']
    frequence = results['A quelle fréquence lisez-vous ?']
    vitesse = results['À quelle vitesse lisez-vous ?']
    nb_livres_lus = results['Combien de livres avez-vous lus en entier au cours de l\'an dernier ? (Optionnel)']
    methode_procuration = results['Comment vous procurez-vous vos livres en général ?']
    motivation = results['Pour quelles raisons lisez-vous généralement ?']
    genres_preferes = results['Quels sont vos genres de livres préférés ?']
    formats_preferes = results['Quel sont vos formats de lecture préférés ?']
    raison_achat = results['Qu\'est-ce qui compte le plus pour vous lors de l\'achat d\'un livre ?']
    langues = results['Dans quelles langues lisez vous ?']
    livres_preferes = results['Quels sont vos livres préférés ? (Optionnel)']
    auteurs_preferes = results['Quels sont vos auteurs préférés ? (Optionnel)']

    ##### COLONNES UNIQUES #####

    def filtrer_choix_multiples(list) :
        res = []
        for element in list : 
            element = element.split(';')
            for el in element :
                res.append(el)
        res = set(res)
        return res
    
    def filtrer_livres_auteurs(list) :
        res = []
        for element in list :
            if (not(isinstance(element, float))) :
                element = element.split('\n')
                for el in element :
                    res.append(el)
        res = set(res)
        return res
        
    code_postal_unique = results['Code postal, si résident français (Optionnel)'].unique()
    methode_procuration_unique = filtrer_choix_multiples(methode_procuration)
    motivation_unique = filtrer_choix_multiples(motivation)
    genres_preferes_unique = filtrer_choix_multiples(genres_preferes)
    formats_preferes_unique = filtrer_choix_multiples(formats_preferes)
    raison_achat_unique = filtrer_choix_multiples(raison_achat)
    langues_unique = filtrer_choix_multiples(langues)
    livres_preferes_unique = filtrer_livres_auteurs(livres_preferes)
    auteurs_preferes_unique = filtrer_livres_auteurs(auteurs_preferes)

    print(livres_preferes_unique)

# Si besoin, croire plutot extract_books_from_authors et extract_authors_from_books qui sont plus ou moins propres
# Mais si possible, faire ça de zéro avec la doc sur le groupe discord

# RENOMMER LES COLONNES - VERSION BIEN
# booksData = booksData.rename(columns={
#    "id": "id_livre",
#    "title": "titre",
#    "rating_count": "nb_notes",
#    "review_count": "nb_critiques",
#    "average_rating": "note_moyenne",
#    "one_star_ratings": "nb_note_1_etoile",
#    "two_star_ratings": "nb_note_2_etoile",
#    "three_star_ratings": "nb_note_3_etoile",
#    "four_star_ratings": "nb_note_4_etoile",
#    "five_star_ratings": "nb_note_5_etoile",
#    "number_of_pages": "nombre_pages",
#    "date_published": "date_publication",
#    "original_title": "titre_original"
# })


if __name__ == "__main__":
    results = pd.read_csv("../Wizards/formulaire/formulaire.csv", low_memory=False)
    main(results)