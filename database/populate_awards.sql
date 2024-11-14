set schema 'sae';


WbImport
-usePgCopy
-type=text
-file='../data/populate/auteur_sql.csv'
-table=_auteur
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/genre.csv'
-table=_genre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/auteur_genre.csv'
-table=_auteur_genre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/editeur.csv'
-table=_editeur
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/livre.csv'
-table=_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/livre_genre.csv'
-table=_genre_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/prix.csv'
-table=_prix
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/prix_livre.csv'
-table=_prix_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/pays.csv'
-table=_pays
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/cadre.csv'
-table=_cadre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/cadre_livre.csv'
-table=_cadre_livre
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/serie.csv'
-table=_serie
-delimiter=','
-header=true;


WbImport
-usePgCopy
-type=text
-file='../data/populate/episode_serie.csv'
-table=_episode_serie
-delimiter=','
-header=true;


