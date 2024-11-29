import os
import pandas as pd
import numpy as np

PATH_DATA = "../Wizards/formulaire/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

def main(results):
    os.makedirs(PATH_POPULATE, exist_ok=True) #Créé le dossier voulu

    ##### COLONNES DU CSV #####
    mails = results['Adresse e-mail']
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
            element = element.split(',')
            for el in element :
                if (el.strip() != '') :
                    el = el.strip()
                    el = el.capitalize()
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

    # _genre : id_genre, libelle_genre
    # EXISTE DEJA
    genre_df = pd.DataFrame({'genre': list(genres_preferes_unique)})
    genre_df.index = genre_df.index+1
    genre_df = genre_df.reset_index(names=['id_genre'])
    genre_df.to_csv(os.path.join(PATH_POPULATE,"genre.csv"), index=False)

    # _livre : id_livre, titre
    # EXISTE DEJA
    livre_df = pd.DataFrame({'livre': list(livres_preferes_unique)})
    livre_df.index = livre_df.index+1
    livre_df = livre_df.reset_index(names=['id_livre'])
    livre_df.to_csv(os.path.join(PATH_POPULATE,"livre.csv"), index=False)

    # _auteur : id_auteur, nom
    # EXISTE DEJA
    auteur_df = pd.DataFrame({'auteur': list(auteurs_preferes_unique)})
    auteur_df.index = auteur_df.index+1
    auteur_df = auteur_df.reset_index(names=['id_auteur'])
    auteur_df.to_csv(os.path.join(PATH_POPULATE,"auteur.csv"), index=False)
    
    # _motivation
    motivation_df = pd.DataFrame({'motivation': list(motivation_unique)})
    motivation_df.index = motivation_df.index+1
    motivation_df = motivation_df.reset_index(names=['id_motivation'])
    motivation_df.to_csv(os.path.join(PATH_POPULATE,"motivation.csv"), index=False)

    # _code_postal
    code_postal_df = pd.DataFrame({'code_postal': list(code_postal_unique)})
    code_postal_df.index = code_postal_df.index+1
    code_postal_df = code_postal_df.reset_index(names=['id_code_postal'])
    code_postal_df.to_csv(os.path.join(PATH_POPULATE,"code_postal.csv"), index=False)

    # _procuration
    procuration_df = pd.DataFrame({'procuration': list(methode_procuration_unique)})
    procuration_df.index = procuration_df.index+1
    procuration_df = procuration_df.reset_index(names=['id_procuration'])
    procuration_df.to_csv(os.path.join(PATH_POPULATE,"procuration.csv"), index=False)

    # _langue
    langue_df = pd.DataFrame({'langue': list(langues_unique)})
    langue_df.index = langue_df.index+1
    langue_df = langue_df.reset_index(names=['id_langue'])
    langue_df.to_csv(os.path.join(PATH_POPULATE,"langue.csv"), index=False)

    # _format
    format_df = pd.DataFrame({'format': list(formats_preferes_unique)})
    format_df.index = format_df.index+1
    format_df = format_df.reset_index(names=['id_format'])
    format_df.to_csv(os.path.join(PATH_POPULATE,"format.csv"), index=False)

    # _raison_achat
    raison_achat_df = pd.DataFrame({'raison_achat': list(raison_achat_unique)})
    raison_achat_df.index = raison_achat_df.index+1
    raison_achat_df = raison_achat_df.reset_index(names=['id_raison_achat'])
    raison_achat_df.to_csv(os.path.join(PATH_POPULATE,"raison_achat.csv"), index=False)

    # _utilisateur
    utilisateur_df = pd.DataFrame({
        'mail_utilisateur': mails,
        'sexe': sexe,
        'age': age,
        'profession': situation_pro,
        'situation_familiale': situation_famille,
        'frequence_lecture': frequence,
        'vitesse_lecture': vitesse,
        'nb_livres_lus': nb_livres_lus
    })
    utilisateur_df.index = utilisateur_df.index+1
    utilisateur_df = utilisateur_df.reset_index(names=['id_utilisateur'])
    utilisateur_df.to_csv(os.path.join(PATH_POPULATE,"utilisateur.csv"), index=False)

    ##### TABLES DE RELATION #####
    
    def table_relation(list, list_multiple, dic, spl=',') :
        dic_mult = {}
        for i in dic.values : 
            i[1] = i[1].strip()
            i[1] = i[1].capitalize()
            dic_mult[i[1]] = i[0]

        res = []
        i = 0
        for element in list_multiple :
            id_user = i

            if (isinstance(element, float) or (element == '')) :
                if ('[non renseigné]' in dic_mult) :
                    id_mult = dic_mult['[non renseigné]']
                else : 
                    id_mult = ''
            else :
                element = element.split(spl)
                
                for el in element :
                    if (el.strip() == ''):
                        if ('[non renseigné]' in dic_mult) :
                            id_mult = dic_mult['[non renseigné]']
                        else : 
                            id_mult = ''
                    else : 
                        el = el.strip()
                        el = el.capitalize()
                        id_mult = dic_mult[el]
                    res.append([i, id_mult])
             
            i += 1
        return res

    # _format_utilisateur : id_format, id_utilisateur
    print("/// format_utilisateur ///")
    list_format_utilisateur = table_relation(mails,formats_preferes, format_df)

    id_utilisateurs = []
    id_formats = []
    for element in list_format_utilisateur :
        id_utilisateurs.append(element[0])
        id_formats.append(element[1])

    format_utilisateur = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_format': id_formats
    })
    format_utilisateur.index = format_utilisateur.index+1
    format_utilisateur.to_csv(os.path.join(PATH_POPULATE,"format_utilisateur.csv"), index=False)

    # _utilisateur_motivation : id_utilisateur, id_motivation
    print("/// utilisateur_motivation ///")
    list_utilisateur_motivation = table_relation(mails, motivation, motivation_df)

    id_utilisateurs = []
    id_motivation = []
    for element in list_utilisateur_motivation :
        id_utilisateurs.append(element[0])
        id_motivation.append(element[1])

    utilisateur_motivation = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_motivation': id_motivation
    })
    utilisateur_motivation.index = utilisateur_motivation.index+1
    utilisateur_motivation.to_csv(os.path.join(PATH_POPULATE,"utilisateur_motivation.csv"), index=False)

    # _utilisateur_procuration : id_utilisateur, id_procuration
    print("/// utilisateur_procuration ///")
    list_utilisateur_procuration = table_relation(mails, methode_procuration, procuration_df)

    id_utilisateurs = []
    id_procuration = []
    for element in list_utilisateur_procuration :
        id_utilisateurs.append(element[0])
        id_procuration.append(element[1])

    utilisateur_procuration = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_procuration': id_procuration
    })
    utilisateur_procuration.index = utilisateur_procuration.index+1
    utilisateur_procuration.to_csv(os.path.join(PATH_POPULATE,"utilisateur_procuration.csv"), index=False)

    # _utilisateur_langue : id_utilisateur, id_langue
    print("/// utilisateur_langue ///")
    list_utilisateur_langue = table_relation(mails, langues, langue_df)

    id_utilisateurs = []
    id_langue = []
    for element in list_utilisateur_langue :
        id_utilisateurs.append(element[0])
        id_langue.append(element[1])

    utilisateur_langue = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_langue': id_langue
    })
    utilisateur_langue.index = utilisateur_langue.index+1
    utilisateur_langue.to_csv(os.path.join(PATH_POPULATE,"utilisateur_langue.csv"), index=False)

    # _utilisateur_raison_achat : id_utilisateur, id_raison_achat
    print("/// utilisateur_raison_achat ///")
    list_utilisateur_raison_achat = table_relation(mails, raison_achat, raison_achat_df)

    id_utilisateurs = []
    id_raison_achat = []
    for element in list_utilisateur_raison_achat :
        id_utilisateurs.append(element[0])
        id_raison_achat.append(element[1])

    utilisateur_raison_achat = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_raison_achat': id_raison_achat
    })
    utilisateur_raison_achat.index = utilisateur_raison_achat.index+1
    utilisateur_raison_achat.to_csv(os.path.join(PATH_POPULATE,"utilisateur_raison_achat.csv"), index=False)
    
    # _utilisateur_genre : id_utilisateur, id_genre
    print("/// utilisateur_genre ///")
    list_utilisateur_genre = table_relation(mails, genres_preferes, genre_df)

    id_utilisateurs = []
    id_genre = []
    for element in list_utilisateur_genre :
        id_utilisateurs.append(element[0])
        id_genre.append(element[1])

    utilisateur_genre = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_genre': id_genre
    })
    utilisateur_genre.index = utilisateur_genre.index+1
    utilisateur_genre.to_csv(os.path.join(PATH_POPULATE,"utilisateur_genre.csv"), index=False)

    # _utilisateur_auteur : id_utilisateur, id_auteur
    print("/// utilisateur_auteur ///")
    
    list_utilisateur_auteur = table_relation(mails, auteurs_preferes, auteur_df, '\n')

    id_utilisateurs = []
    id_auteur = []
    for element in list_utilisateur_auteur :
        id_utilisateurs.append(element[0])
        id_auteur.append(element[1])

    utilisateur_auteur = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_auteur': id_auteur
    })
    utilisateur_auteur.index = utilisateur_auteur.index+1
    utilisateur_auteur.to_csv(os.path.join(PATH_POPULATE,"utilisateur_auteur.csv"), index=False)

    # _livre_utilisateur : id_utilisateur, id_livre
    print("/// livre_utilisateur ///")
    
    list_livre_utilisateur = table_relation(mails, livres_preferes, livre_df, '\n')

    id_utilisateurs = []
    id_livre = []
    for element in list_livre_utilisateur :
        id_utilisateurs.append(element[0])
        id_livre.append(element[1])

    utilisateur_livre = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_livre': id_livre
    })
    utilisateur_livre.index = utilisateur_livre.index+1
    utilisateur_livre.to_csv(os.path.join(PATH_POPULATE,"livre_utilisateur.csv"), index=False)


##### __NAME__ #####

if __name__ == "__main__":
    results = pd.read_csv("../Wizards/formulaire/formulaire.csv", low_memory=False)
    main(results)