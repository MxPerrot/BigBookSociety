DROP SCHEMA IF EXISTS BigBookSociety CASCADE;
create schema BigBookSociety;
set schema 'BigBookSociety';
SET search_path TO BigBookSociety;

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
);

CREATE INDEX idx_titre_livre ON _livre(titre);

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
    format VARCHAR UNIQUE NOT NULL
);

CREATE TABLE _utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    mail_utilisateur VARCHAR NOT NULL,
    sexe VARCHAR NOT NULL,
    age VARCHAR,
    profession VARCHAR,
    situation_familiale VARCHAR,
    frequence_lecture VARCHAR,
    vitesse_lecture INTEGER,
    nb_livres_lus VARCHAR,
    
    nom_utilisateur VARCHAR,
    mot_de_passe_hashed VARCHAR,
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



-- TRIGGERS ET FONCTIONS

-- Vue formulaire
CREATE VIEW v_formulaire AS
SELECT
    -- Déclare les colonnes correspondant aux données du formulaire
    NULL::VARCHAR AS mail_utilisateur,
    NULL::VARCHAR AS sexe,
    NULL::VARCHAR AS age,
    NULL::VARCHAR AS profession,
    NULL::VARCHAR AS situation_familiale,
    NULL::INTEGER AS code_postal,
    NULL::VARCHAR AS frequence_lecture,
    NULL::INTEGER AS vitesse_lecture,
    NULL::VARCHAR AS nb_livres_lus,
    NULL::VARCHAR[] AS genres_preferes,     -- Tableau de genres préférés
    NULL::VARCHAR[] AS formats_preferes,    -- Tableau de formats préférés
    NULL::VARCHAR[] AS motivations_lecture, -- Tableau des raisons de lecture
    NULL::VARCHAR[] AS raisons_achat,       -- Tableau des raisons de lecture
    NULL::VARCHAR[] AS langues_lecture,     -- Tableau des langues de lecture
    NULL::VARCHAR[] AS livres_preferes,     -- Tableau des livres préférés
    NULL::VARCHAR[] AS auteurs_preferes,    -- Tableau des auteurs préférés
    NULL::VARCHAR[] AS methodes_procuration -- Tableau des méthodes de procuration
;

CREATE VIEW _info_utilisateur AS SELECT * FROM _utilisateur 
NATURAL JOIN _format_utilisateur
NATURAL JOIN _format

NATURAL JOIN _utilisateur_auteur
NATURAL JOIN _auteur

NATURAL JOIN _utilisateur_genre
NATURAL JOIN _genre

NATURAL JOIN _utilisateur_langue
NATURAL JOIN _langue

NATURAL JOIN _utilisateur_motivation
NATURAL JOIN _motivation

NATURAL JOIN _utilisateur_procuration
NATURAL JOIN _procuration

NATURAL JOIN _utilisateur_raison_achat
NATURAL JOIN _raison_achat

WHERE nom_utilisateur = USER;


--CREATE OR REPLACE FUNCTION grant_rights()
--RETURNS TRIGGER AS $$
--DECLARE
  --utilisateur VARCHAR;
--BEGIN
  -- utilisateur := NEW.mail_utilisateur;
   --GRANT CONNECT ON DATABASE pg_dgoupil TO utilisateur;
   --GRANT SELECT ON _info_utilisateur TO utilisateur;
  -- CREATE ROLE utilisateur;
  -- EXECUTE format('GRANT SELECT, INSERT ON _info_utilisateur TO %I', utilisateur);
  -- RETURN NEW;
--END;
--$$ LANGUAGE plpgsql;


--CREATE OR REPLACE TRIGGER triggerUserRight
--BEFORE INSERT OR UPDATE
--ON _utilisateur FOR EACH ROW
--EXECUTE PROCEDURE grant_rights();

-- PEUPLEMENT

COPY _genre (libelle_genre, id_genre)
FROM '/docker-entrypoint-initdb.d/populate/genre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);;

COPY _genre (id_genre, libelle_genre)
FROM '/docker-entrypoint-initdb.d/populate/genre_2.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _auteur (id_auteur,nom,note_moyenne,sexe,nb_critiques,nb_reviews,origine)
FROM '/docker-entrypoint-initdb.d/populate/auteur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _auteur_genre (id_auteur,id_genre)
FROM '/docker-entrypoint-initdb.d/populate/auteur_genre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _editeur (id_editeur,nom_editeur)
FROM '/docker-entrypoint-initdb.d/populate/editeur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _livre (id_livre,titre,nb_notes,nb_critiques,nb_note_5_etoile,nb_note_4_etoile,nb_note_3_etoile,nb_note_2_etoile,nb_note_1_etoile,nombre_pages,date_publication,titre_original,isbn,isbn13,description,id_editeur)
FROM '/docker-entrypoint-initdb.d/populate/livre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _genre_livre (id_livre,nb_votes,id_genre)
FROM '/docker-entrypoint-initdb.d/populate/livre_genre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _prix (id_prix,nom_prix,annee_prix)
FROM '/docker-entrypoint-initdb.d/populate/prix.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _prix_livre (id_prix,id_livre)
FROM '/docker-entrypoint-initdb.d/populate/prix_livre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _pays (id_pays,nom)
FROM '/docker-entrypoint-initdb.d/populate/pays.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _cadre (id_cadre,annee,localisation,id_pays)
FROM '/docker-entrypoint-initdb.d/populate/cadre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _cadre_livre (id_cadre,id_livre)
FROM '/docker-entrypoint-initdb.d/populate/cadre_livre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _serie (id_serie,nom_serie)
FROM '/docker-entrypoint-initdb.d/populate/series.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _episode_serie (id_serie,id_livre,numero_episode)
FROM '/docker-entrypoint-initdb.d/populate/episode_serie.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);


COPY _auteur_livre (id_livre,id_auteur)
FROM '/docker-entrypoint-initdb.d/populate/link.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

-- Asaiah

COPY _code_postal (id_code_postal,code_postal)
FROM '/docker-entrypoint-initdb.d/populate/code_postal.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _format (id_format,format)
FROM '/docker-entrypoint-initdb.d/populate/format.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur (id_utilisateur,mail_utilisateur,sexe,age,profession,situation_familiale,frequence_lecture,vitesse_lecture,nb_livres_lus)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _raison_achat (id_raison_achat,raison_achat)
FROM '/docker-entrypoint-initdb.d/populate/raison_achat.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _langue (id_langue,langue)
FROM '/docker-entrypoint-initdb.d/populate/langue.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _procuration (id_procuration,methode_procuration)
FROM '/docker-entrypoint-initdb.d/populate/procuration.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _motivation (id_motivation,motivation)
FROM '/docker-entrypoint-initdb.d/populate/motivation.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _format_utilisateur (id_utilisateur,id_format)
FROM '/docker-entrypoint-initdb.d/populate/format_utilisateur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_genre (id_utilisateur,id_genre)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_genre.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_auteur (id_utilisateur,id_auteur)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_auteur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _livre_utilisateur (id_utilisateur,id_livre)
FROM '/docker-entrypoint-initdb.d/populate/livre_utilisateur.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_motivation (id_utilisateur,id_motivation)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_motivation.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_procuration (id_utilisateur,id_procuration)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_procuration.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_langue (id_utilisateur,id_langue)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_langue.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

COPY _utilisateur_raison_achat (id_utilisateur,id_raison_achat)
FROM '/docker-entrypoint-initdb.d/populate/utilisateur_raison_achat.csv'
WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER ','
);

ALTER TABLE _livre 
ADD COLUMN note_moyenne DECIMAL GENERATED ALWAYS AS ((nb_note_1_etoile*1.0+nb_note_2_etoile*2.0+nb_note_3_etoile*3.0+nb_note_4_etoile*4.0+nb_note_5_etoile*5.0)/CAST (NULLIF(nb_notes,0) AS DECIMAL)) STORED;

-- SELECT setval('_utilisateur_id_utilisateur_seq', (SELECT MAX(id_utilisateur) () FROM _utilisateur));

-- SELECT * () FROM _info_utilisateur;


--GRANT CONNECT ON DATABASE pg_dgoupil TO USER;
--GRANT SELECT ON _info_utilisateur TO USER;


UPDATE _utilisateur
SET nom_utilisateur = 'max', mot_de_passe_hashed = '$2b$12$RNDlH8mt0ehyiOnWNsAqDOFO098cNrNSfqU1FRF.TrQZG4D.ubQIu'
WHERE id_utilisateur=131;
