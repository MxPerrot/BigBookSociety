DROP SCHEMA IF EXISTS sae CASCADE;
create schema sae;
set schema 'sae';

CREATE TABLE _serie (
    id_serie SERIAL PRIMARY KEY,
    nom_serie VARCHAR NOT NULL
);

CREATE TABLE _editeur (
    id_editeur SERIAL PRIMARY KEY,
    nom_editeur VARCHAR NOT NULL
);

CREATE TABLE _prix (
    id_prix SERIAL PRIMARY KEY,
    nom_prix VARCHAR NOT NULL,
    annee_prix INTEGER
);

CREATE TABLE _pays (
    id_pays SERIAL PRIMARY KEY,
    nom VARCHAR
);

CREATE TABLE _cadre (
    id_cadre SERIAL PRIMARY KEY,
    annee INTEGER, 
    id_pays INTEGER REFERENCES _pays(id_pays),
    localisation VARCHAR
);

CREATE TABLE _livre (
    id_livre SERIAL PRIMARY KEY,
    titre VARCHAR NOT NULL,
    nb_notes INTEGER,
    nb_critiques INTEGER,
    note_moyenne DECIMAL,
    nb_note_1_etoile INTEGER,
    nb_note_2_etoile INTEGER,
    nb_note_3_etoile INTEGER,
    nb_note_4_etoile INTEGER,
    nb_note_5_etoile INTEGER,
    nombre_pages INTEGER,
    date_publication DATE,
    titre_original VARCHAR,
    isbn VARCHAR,
    isbn13 VARCHAR,
    description VARCHAR,
    id_editeur INTEGER REFERENCES _editeur(id_editeur)
-- TODO: éventuellement créer une colonne "format", afin que les nouveaux livres ajoutés puissent avoir un format afin d'enrichir la base.  
);


CREATE TABLE _genre (
    id_genre SERIAL PRIMARY KEY,
    libelle_genre VARCHAR
);


CREATE TABLE _auteur (
    id_auteur SERIAL PRIMARY KEY,
    note_moyenne DECIMAL,
    nom VARCHAR UNIQUE,
    origine VARCHAR,
    nb_reviews INTEGER,
    nb_critiques INTEGER,
    sexe VARCHAR,
    id_genre INTEGER,  -- Clé étrangère pour la relation "écrit" avec Genre
    FOREIGN KEY (id_genre) REFERENCES _genre(id_genre)  -- Relation avec Genre
);


CREATE TABLE _code_postal (
    id_code_postal SERIAL PRIMARY KEY,
    code_postal VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _format (
    id_format SERIAL PRIMARY KEY,
    libelle_format VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    mail_utilisateur VARCHAR UNIQUE NOT NULL,
    sexe VARCHAR NOT NULL,
    age INTEGER,
    profession VARCHAR,
    situation_familiale VARCHAR,
    frequence_lecture VARCHAR,
    vitesse_lecture INTEGER,
    nb_livres_lus INTEGER,
    id_code_postal INTEGER REFERENCES _code_postal(id_code_postal)
);

CREATE TABLE _raison_achat (
    id_raison_achat SERIAL PRIMARY KEY,
    raison_achat VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _langue (
    id_langue SERIAL PRIMARY KEY,
    langue VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _procuration (
    id_procuration SERIAL PRIMARY KEY,
    methode_procuration VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _motivation (
    id_motivation SERIAL PRIMARY KEY,
    motivation VARCHAR UNIQUE NOT NULL
);


-- Table de liaison _auteur_genre pour la relation "préférence" entre Auteur et Genre
CREATE TABLE _auteur_genre (
    id_auteur INTEGER  REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES _genre(id_genre) ON DELETE CASCADE,
    PRIMARY KEY (id_auteur, id_genre)
);



-- Table de liaison _format_utilisateur pour la relation "préférence" entre Utilisateur et Format
CREATE TABLE _format_utilisateur (
    id_format INTEGER  REFERENCES _format(id_format) ON DELETE CASCADE,
    id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
    PRIMARY KEY (id_format, id_utilisateur)
);

-- Table de liaison _utilisateur_genre pour la relation "préférence" entre Utilisateur et Genre
CREATE TABLE _utilisateur_genre (
    id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES _genre(id_genre) ON DELETE CASCADE,
    PRIMARY KEY (id_utilisateur, id_genre)
);

-- Table _utilisateur_auteur pour la relation de "préférence" entre Utilisateur et Auteur
CREATE TABLE _utilisateur_auteur (
    id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_auteur INTEGER REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
    PRIMARY KEY (id_utilisateur, id_auteur)
);

-- Table _livre_utilisateur pour la relation de préférences d'un utilisateur avec ses livres préférés
CREATE TABLE _livre_utilisateur (
  id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_livre)
);

CREATE TABLE _utilisateur_motivation (
  id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_motivation INTEGER REFERENCES _motivation(id_motivation) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_motivation)
);

CREATE TABLE _utilisateur_procuration (
  id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_procuration INTEGER REFERENCES _procuration(id_procuration) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_procuration)
);

CREATE TABLE _utilisateur_langue (
  id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_langue INTEGER REFERENCES _langue(id_langue) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_langue)
);

CREATE TABLE _utilisateur_raison_achat (
  id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_raison_achat INTEGER REFERENCES _raison_achat(id_raison_achat) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_raison_achat)
);



-- Table _prix_livre pour la relation entre un prix et le livre attribué
CREATE TABLE _prix_livre (
  id_prix INTEGER REFERENCES _prix(id_prix) ON DELETE CASCADE,
  id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_prix,id_livre)
);

-- Table _cadre_livre pour la relation entre un livre et ses cadres
CREATE TABLE _cadre_livre (
  id_cadre INTEGER REFERENCES _cadre(id_cadre) ON DELETE CASCADE,
  id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_cadre,id_livre)
);

-- Table _auteur_livre pour la relation entre des auteur et les livre qu'ils ont écrit
CREATE TABLE _auteur_livre (
  id_auteur INTEGER REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
  id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_auteur,id_livre)
);

-- Table _genre_livre pour la relation entre les livres et leur genre, ainsi que le nombre de vote pour ce genre dans cas particuliers
CREATE TABLE _genre_livre (
  id_genre INTEGER REFERENCES _genre(id_genre) ON DELETE CASCADE,
  id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
  nb_votes INTEGER,
  PRIMARY KEY(id_genre,id_livre)
);

-- Table _episode_serie pour la relation entre les livres et les séries 
CREATE TABLE _episode_serie (
    id_livre INTEGER REFERENCES _livre(id_livre) ON DELETE CASCADE,
    id_serie INTEGER REFERENCES _serie(id_serie) ON DELETE CASCADE,
    numero_episode VARCHAR,
    PRIMARY KEY(id_livre, id_serie)
);


-- PEUPLEMENT

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
-file='../data/populate/series.csv'
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


WbImport
-usePgCopy
-type=text
-file='../data/populate/link.csv'
-table=_auteur_livre
-delimiter=','
-header=true;
