DROP SCHEMA IF EXISTS tp1 CASCADE;
create schema tp1;
set schema 'tp1';

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
    nom_prix VARCHAR NOT NULL
);

CREATE TABLE _cadre (
    id_cadre SERIAL PRIMARY KEY,
    libelle_cadre VARCHAR NOT NULL
);


CREATE TABLE _livre (
    id_livre SERIAL PRIMARY KEY,
    titre VARCHAR(255) UNIQUE NOT NULL,
    nb_notes INTEGER,
    nb_critiques INTEGER,
    note_moyenne FLOAT,
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
    id_serie INTEGER REFERENCES _serie(id_serie),
    id_editeur INTEGER REFERENCES _editeur(id_editeur)
);




CREATE TABLE IF NOT EXISTS _genre (
    id_genre SERIAL PRIMARY KEY,
    libelle_genre VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS _auteur (
    id_auteur SERIAL PRIMARY KEY,
    note_moyenne FLOAT,
    nom VARCHAR(100) UNIQUE,
    origine VARCHAR(100),
    id_genre INTEGER,  -- Clé étrangère pour la relation "écrit" avec Genre
    FOREIGN KEY (id_genre) REFERENCES _genre(id_genre)  -- Relation avec Genre
);


CREATE TABLE IF NOT EXISTS _code_postal (
    code_postal VARCHAR PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS _format (
    id_format SERIAL PRIMARY KEY,
    libelle_format VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS _utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    mail_utilisateur VARCHAR NOT NULL,
    age INTEGER,
    profession VARCHAR,
    situation_familial VARCHAR,
    frequence_lecture VARCHAR,
    vitesse_lecture VARCHAR,
    nbr_livre_lue INTEGER,
    code_postal VARCHAR REFERENCES _code_postal(code_postal),
    id_format INTEGER REFERENCES _format(id_format)
);



-- Table de liaison _auteur_genre pour la relation "préférence" entre Auteur et Genre
CREATE TABLE IF NOT EXISTS _auteur_genre (
    id_auteur INTEGER  REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES _genre(id_genre) ON DELETE CASCADE,
    PRIMARY KEY (id_auteur, id_genre)
);


-- Table de liaison _utilisateur_genre pour la relation "préférence" entre Utilisateur et Genre
CREATE TABLE IF NOT EXISTS _utilisateur_genre (
    id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES _genre(id_genre) ON DELETE CASCADE,
    PRIMARY KEY (id_utilisateur, id_genre)
);

-- Table _utilisateur_auteur pour la relation de "préférence" entre Utilisateur et Auteur
CREATE TABLE IF NOT EXISTS _utilisateur_auteur (
    id_utilisateur INTEGER REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
    id_auteur INTEGER REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
    PRIMARY KEY (id_utilisateur, id_auteur)
);

-- Table _prix_livre pour la relation entre un prix et le livre attribué
CREATE TABLE _prix_livre (
  id_prix SERIAL REFERENCES _prix(id_prix) ON DELETE CASCADE,
  id_livre SERIAL REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_prix,id_livre)
);

-- Table _cadre_livre pour la relation entre un livre et ses cadres
CREATE TABLE _cadre_livre (
  id_cadre SERIAL REFERENCES _cadre(id_cadre) ON DELETE CASCADE,
  id_livre SERIAL REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_cadre,id_livre)
);

-- Table _livre_prefere_utilisateur pour la relation de préférences d'un utilisateur avec ses livres préférés
CREATE TABLE _livre_prefere_utilisateur (
  id_utilisateur SERIAL REFERENCES _utilisateur(id_utilisateur) ON DELETE CASCADE,
  id_livre SERIAL REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_utilisateur,id_livre)
);

-- Table _auteur_livre pour la relation entre des auteur et les livre qu'ils ont écrit
CREATE TABLE _auteur_livre (
  id_auteur SERIAL REFERENCES _auteur(id_auteur) ON DELETE CASCADE,
  id_livre SERIAL REFERENCES _livre(id_livre) ON DELETE CASCADE,
  PRIMARY KEY(id_auteur,id_livre)
);

-- Table _genre_livre pour la relation entre les livres et leur genre, ainsi que le nombre de vote pour ce genre dans cas particuliers
CREATE TABLE _genre_livre (
  id_genre SERIAL REFERENCES _genre(id_genre) ON DELETE CASCADE,
  id_livre SERIAL REFERENCES _livre(id_livre) ON DELETE CASCADE,
  nb_votes INTEGER,
  PRIMARY KEY(id_genre,id_livre)
);
