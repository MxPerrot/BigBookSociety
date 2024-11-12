set schema 'sae';
DROP table IF EXISTS temp_awards CASCADE;

CREATE TEMP TABLE temp_awards (
    awardName VARCHAR,
    awardDate DATE
);

\copy temp_awards(awardName, awardDate) FROM '../data/Cleaned_books2.csv' DELIMITER ',' CSV HEADER;


INSERT INTO _prix (nom_prix, annee_prix)
SELECT DISTINCT awardName, EXTRACT(YEAR FROM awardDate)::INT
FROM temp_awards
WHERE awardName IS NOT NULL AND awardDate IS NOT NULL;
