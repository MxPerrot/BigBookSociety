-- Table temporaire pour stocker les données du fichier CSV
CREATE TEMP TABLE temp_livre (
    id_livre SERIAL PRIMARY KEY,
    titre VARCHAR,
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
    description TEXT,
    series VARCHAR,
    author VARCHAR,
    rating_count INTEGER,
    review_count INTEGER,
    publisher VARCHAR,
    genre_1 VARCHAR,
    genre_2 VARCHAR
);

-- Charger le fichier CSV dans la table temporaire
COPY temp_livre FROM '/path/to/Big_book.csv' DELIMITER ',' CSV HEADER;

-- Insérer les séries uniques dans la table `_serie`
INSERT INTO _serie (nom_serie)
SELECT DISTINCT TRIM(series)
FROM temp_livre
WHERE series IS NOT NULL
  AND series <> ''
ON CONFLICT (nom_serie) DO NOTHING;

-- Supprimer la table temporaire
DROP TABLE temp_livre;
