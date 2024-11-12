set schema 'sae';
DROP table IF EXISTS temp_awards CASCADE;

CREATE TEMP TABLE temp_awards (
    awardName VARCHAR,
    awardDate DATE
);

WbImport
-usePgCopy
-type=text
-file='../data/Cleaned_books2.csv'
-table=temp_awards
-delimiter=','
-header=true;

INSERT INTO _prix (nom_prix, annee_prix)
SELECT DISTINCT awardName, EXTRACT(YEAR FROM awardDate)::INT
FROM temp_awards
WHERE awardName IS NOT NULL AND awardDate IS NOT NULL;
