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
                if (el != '') :
                    res.append(el)
        res = set(res)
        return res
    
    def filtrer_livres_auteurs(list) :
        res = []
        for element in list :
            if (not(isinstance(element, float))) :
                element = element.split('\n')
                for el in element :
                    if (el != '') :
                        res.append(el)
        res = set(res)
        return res
        
    code_postal_unique = results['Code postal, si résident français (Optionnel)'].unique()
    code_postal_unique = code_postal_unique[~pd.isnull(code_postal_unique)]
    methode_procuration_unique = filtrer_choix_multiples(methode_procuration)
    motivation_unique = filtrer_choix_multiples(motivation)
    genres_preferes_unique = filtrer_choix_multiples(genres_preferes)
    formats_preferes_unique = filtrer_choix_multiples(formats_preferes)
    raison_achat_unique = filtrer_choix_multiples(raison_achat)
    langues_unique = filtrer_choix_multiples(langues)
    livres_preferes_unique = filtrer_livres_auteurs(livres_preferes)
    auteurs_preferes_unique = filtrer_livres_auteurs(auteurs_preferes)

    ##### TABLES SIMPLES #####

    # _motivation
    motivation = pd.DataFrame({'motivation': list(motivation_unique)})
    motivation.index = motivation.index+1
    motivation = motivation.reset_index(names=['id_motivation'])
    motivation.to_csv(os.path.join(PATH_POPULATE,"motivation.csv"), index=False)

    # _code_postal
    code_postal = pd.DataFrame({'code_postal': list(code_postal_unique)})
    code_postal.index = code_postal.index+1
    code_postal = code_postal.reset_index(names=['id_code_postal'])
    code_postal.to_csv(os.path.join(PATH_POPULATE,"code_postal.csv"), index=False)

    # _procuration
    procuration = pd.DataFrame({'procuration': list(methode_procuration_unique)})
    procuration.index = procuration.index+1
    procuration = procuration.reset_index(names=['id_procuration'])
    procuration.to_csv(os.path.join(PATH_POPULATE,"procuration.csv"), index=False)

    # _langue
    langue = pd.DataFrame({'langue': list(langues_unique)})
    langue.index = langue.index+1
    langue = langue.reset_index(names=['id_langue'])
    langue.to_csv(os.path.join(PATH_POPULATE,"langue.csv"), index=False)

    # _format
    format = pd.DataFrame({'format': list(formats_preferes_unique)})
    format.index = format.index+1
    format = format.reset_index(names=['id_format'])
    format.to_csv(os.path.join(PATH_POPULATE,"format.csv"), index=False)

    # _raison_achat
    raison_achat = pd.DataFrame({'raison_achat': list(raison_achat_unique)})
    raison_achat.index = raison_achat.index+1
    raison_achat = raison_achat.reset_index(names=['id_raison_achat'])
    raison_achat.to_csv(os.path.join(PATH_POPULATE,"raison_achat.csv"), index=False)

    # _utilisateur
    utilisateur = pd.DataFrame({
        'mail_utilisateur': mails,
        'sexe': sexe,
        'age': age,
        'profession': situation_pro,
        'situation_familiale': situation_famille,
        'frequence_lecture': frequence,
        'vitesse_lecture': vitesse,
        'nb_livres_lus': nb_livres_lus
    })
    utilisateur.index = utilisateur.index+1
    utilisateur = utilisateur.reset_index(names=['id_utilisateur'])
    utilisateur.to_csv(os.path.join(PATH_POPULATE,"utilisateur.csv"), index=False)

    ##### TABLES DE RELATION #####

    # _auteur_genre : id_auteur, id_genre

    # _format_utilisateur : id_format, id_utilisateur

    # _utilisateur_genre : id_utilisateur, id_genre

    # _utilisateur_auteur : id_utilisateur, id_auteur

    # _livre_utilisateur : id_utilisateur, id_livre

    # _utilisateur_motivation : id_utilisateur, id_motivation

    # _utilisateur_procuration : _utilisateur, _procuration

    # _utilisateur_langue : id_utilisateur, id_langue

    # _utilisateur_raison_achat : id_utilisateur, id_raison_achat


##### __NAME__ #####

if __name__ == "__main__":
    results = pd.read_csv("../Wizards/formulaire/formulaire.csv", low_memory=False)
    main(results)