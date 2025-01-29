import os
import pandas as pd
import numpy as np

PATH_DATA = "data/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

def main(results):
    os.makedirs(PATH_POPULATE, exist_ok=True) #Créé le dossier voulu

    ##### COLONNES DU CSV #####
    # Extractions de chaque colonne du csv
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
    # Création de listes avec les valeurs uniques de chaque colonne

    # Séparer les valeurs distinctes des résultats à choix multiples
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
    
    # Séparer les valeurs distinctes des livres et auteurs
    def filtrer_livres_auteurs(list, list2) :
        res = []
        for element in list :
            if (not(isinstance(element, float))) :
                element = element.split('\n')
                for el in element :
                    if (el != '' and not(list2.isin([el]).any().any())) :
                        res.append(el)
        res = set(res)
        res = [i.strip() for i in res]
        return res

    livre1_df = pd.read_csv('data/populate/livre.csv')
    auteur1_df = pd.read_csv('data/populate/auteur_sql.csv')
    genre1_df = pd.read_csv('data/populate/genre.csv')

    code_postal_unique = results['Code postal, si résident français (Optionnel)'].unique()
    code_postal_unique = code_postal_unique[~pd.isnull(code_postal_unique)]
    methode_procuration_unique = filtrer_choix_multiples(methode_procuration)
    motivation_unique = filtrer_choix_multiples(motivation)
    genres_preferes_unique = filtrer_choix_multiples(genres_preferes)
    formats_preferes_unique = filtrer_choix_multiples(formats_preferes)
    raison_achat_unique = filtrer_choix_multiples(raison_achat)
    langues_unique = filtrer_choix_multiples(langues)
    livres_preferes_unique = filtrer_livres_auteurs(livres_preferes, livre1_df["titre"])
    auteurs_preferes_unique = filtrer_livres_auteurs(auteurs_preferes, auteur1_df["nom"])


    ##### TABLES SIMPLES #####

    # _genre : id_genre, libelle_genre
    # Fusion avec le csv déjà existant
    max_id_genre1 = genre1_df['id_genre'].max()
    genre_df = pd.DataFrame({'libelle_genre': list(genres_preferes_unique)})
    genre_df.index = genre_df.index+max_id_genre1+1
    genre_df = genre_df.reset_index(names=['id_genre'])
    genre_df.to_csv(os.path.join(PATH_POPULATE,"genre_2.csv"), index=False)

    # _livre : id_livre, titre
    # Fusion avec le csv déjà existant
    max_id_livre1 = livre1_df['id_livre'].max()
    livre_df = pd.DataFrame({'titre': list(livres_preferes_unique)})
    livre_df.index = livre_df.index+max_id_livre1+1
    livre_df = livre_df.reset_index(names=['id_livre'])
    livre_df = pd.concat([livre1_df, livre_df])
    
    livre_df['nb_notes'] = livre_df['nb_notes'].astype('Int64') # force convert numerical values to int
    livre_df['nb_critiques'] = livre_df['nb_critiques'].astype('Int64') # force convert numerical values to int
    livre_df['nb_note_5_etoile'] = livre_df['nb_note_5_etoile'].astype('Int64') # force convert numerical values to int
    livre_df['nb_note_4_etoile'] = livre_df['nb_note_4_etoile'].astype('Int64') # force convert numerical values to int
    livre_df['nb_note_3_etoile'] = livre_df['nb_note_3_etoile'].astype('Int64') # force convert numerical values to int
    livre_df['nb_note_2_etoile'] = livre_df['nb_note_2_etoile'].astype('Int64') # force convert numerical values to int
    livre_df['nb_note_1_etoile'] = livre_df['nb_note_1_etoile'].astype('Int64') # force convert numerical values to int
    livre_df['nombre_pages'] = livre_df['nombre_pages'].astype('Int64') # force convert numerical values to int
    livre_df['isbn13'] = livre_df['isbn13'].astype('Int64') # force convert numerical values to int
    livre_df['id_editeur'] = livre_df['id_editeur'].astype('Int64') # force convert numerical values to int

    livre_df.to_csv(os.path.join(PATH_POPULATE,"livre.csv"), index=False)

    # _auteur : id_auteur, nom
    # Fusion avec le csv déjà existant
    max_id_auteur1 = auteur1_df['id_auteur'].max()
    auteur_df = pd.DataFrame({'nom': list(auteurs_preferes_unique)})
    auteur_df = auteur_df.dropna()
    auteur_df["nom"] = auteur_df["nom"].str.lower()

    auteur_minimised = auteur1_df
    auteur_minimised["nom"] = auteur_minimised['nom'].str.lower()



    #TODO Séparer le grain (Faire en sorte que les auteurs déjà présent dans la bdd ne soit pas répétés.)

    
    common_author_name = np.intersect1d(auteur_minimised['nom'], auteur_df['nom'])
    #BUG certaines des entrées sont des FLOAT au lieu d'être des STR, probablement valeur NaN
    #Tester avec des to_csv?

    print(common_author_name)










    auteur_df.index = auteur_df.index+max_id_auteur1+1
    auteur_df = auteur_df.reset_index(names=['id_auteur'])


    # auteur_df = pd.concat([auteur1_df, auteur_df])
    auteur_df = pd.merge(auteur_df, auteur1_df, on='id_auteur', how='inner')
    print(auteur_df)

    
    auteur_df['nb_critiques'] = auteur_df['nb_critiques'].astype('Int64') # force convert numerical values to int
    auteur_df['nb_reviews'] = auteur_df['nb_reviews'].astype('Int64') # force convert numerical values to int

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
    procuration_df = pd.DataFrame({'methode_procuration': list(methode_procuration_unique)})
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
    
    # Remplace les libelles par leurs ids
    # Gère les valeurs nulles, vides, null, espaces en trop
    def table_relation(list, list_multiple, dic, spl=',') :
        dic_mult = {}
        for i in dic.values :
            i[1] = i[1].strip()
            i[1] = i[1].capitalize()
            dic_mult[i[1]] = i[0]

        res = []
        i = 1
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
                    if (el.strip() != ''): 
                        el = el.strip()
                        el = el.capitalize()
                        id_mult = dic_mult[el]
                    if not([i, id_mult] in res) :
                        res.append([i, id_mult])
             
            i += 1
        return res
    
    # Remplace les libelles par leurs ids
    # Fonction spéciale pour gérer les auteurs
    # Gère les valeurs nulles, vides, null, espaces en trop
    def table_relation_auteur(list, list_multiple, dic, spl='\n') :
        dic_mult = {}
        for i in dic.values :
            if not(isinstance(i[3], float)) :
                i[3] = i[3].strip()
                i[3] = i[3].capitalize()
                dic_mult[i[3]] = i[2]

        res = []
        i = 1
        for element in list_multiple :
            id_user = i

            if (isinstance(element, float) or (element == '')) :
                id_mult = dic_mult['']
            else :
                element = element.split(spl)
                
                for el in element :
                    if (el.strip() == ''):
                        id_mult = dic_mult['']
                    else : 
                        el = el.strip()
                        el = el.capitalize()
                        id_mult = dic_mult[el]
                    res.append([i, id_mult])
             
            i += 1
        return res
    
    # Remplace les libelles par leurs ids
    # Fonction spéciale pour gérer les livres
    # Gère les valeurs nulles, vides, null, espaces en trop
    def table_relation_livre(list, list_multiple, dic, spl='\n') :
        dic_mult = {}
        for i in dic.values :
            i[1] = i[1].strip()
            i[1] = i[1].capitalize()
            dic_mult[i[1]] = i[0]

        res = []
        i = 1
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
                    if (el.strip() != ''):
                        el = el.strip()
                        el = el.capitalize()
                        id_mult = dic_mult[el]
                    if not([i, id_mult] in res) :
                        res.append([i, id_mult])
             
            i += 1
        return res

    # _format_utilisateur : id_format, id_utilisateur
    print("/// format_utilisateur ///")
    list_format_utilisateur = table_relation(mails,formats_preferes, format_df)

    id_utilisateurs = []
    id_formats = []
    for element in list_format_utilisateur : # Séparer les différents éléments
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
    for element in list_utilisateur_motivation : # Séparer les différents éléments
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
    for element in list_utilisateur_procuration : # Séparer les différents éléments
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
    for element in list_utilisateur_langue : # Séparer les différents éléments
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
    for element in list_utilisateur_raison_achat : # Séparer les différents éléments
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
    for element in list_utilisateur_genre : # Séparer les différents éléments
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
    
    list_utilisateur_auteur = table_relation_auteur(mails, auteurs_preferes, auteur_df)

    id_utilisateurs = []
    id_auteur = []
    for element in list_utilisateur_auteur : # Séparer les différents éléments
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
    
    list_livre_utilisateur = table_relation_livre(mails, livres_preferes, livre_df)

    id_utilisateurs = []
    id_livre = []
    for element in list_livre_utilisateur : # Séparer les différents éléments
        id_utilisateurs.append(element[0])
        id_livre.append(element[1])

    utilisateur_livre = pd.DataFrame({
        'id_utilisateur': id_utilisateurs,
        'id_livre': id_livre
    })
    utilisateur_livre.index = utilisateur_livre.index+1
    utilisateur_livre.to_csv(os.path.join(PATH_POPULATE,"livre_utilisateur.csv"), index=False)


##### __NAME__ #####

if __name__ == "__main__" :
    results = pd.read_csv("data/formulaire.csv", low_memory=False)
    main(results)