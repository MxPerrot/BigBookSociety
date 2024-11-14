set schema 'sae';


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/auteur_sql.csv'
-table=_auteur
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/genre.csv'
-table=_genre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/auteur_genre.csv'
-table=_auteur_genre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/editeur.csv'
-table=_editeur
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/livre.csv'
-table=_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/livre_genre.csv'
-table=_genre_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/prix.csv'
-table=_prix
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/prix_livre.csv'
-table=_prix_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/pays.csv'
-table=_pays
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/cadre.csv'
-table=_cadre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/cadre_livre.csv'
-table=_cadre_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/serie.csv'
-table=_serie
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../csv_to_load/episode_serie.csv'
-table=_episode_serie
-delimiter=','
-header=true;


