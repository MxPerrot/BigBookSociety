SET SCHEMA 'BigBookSociety';
SET search_path TO BigBookSociety;

CREATE OR REPLACE FUNCTION insertUser() RETURNS TRIGGER AS $$
  DECLARE
    user_id INT;
    postal_id INT;
    format_ids INT[];
    format_id INT;
    genre_ids INT[];
    genre_id INT;
    auteur_ids INT[];
    auteur_id INT;
    language_ids INT[];
    language_id INT;
    buy_ids INT[];
    buy_id INT;
    book_ids INT[];
    book_id INT;
    motive_ids INT[];
    motive_id INT;
    procuration_ids INT[];
    procuration_id INT;
    note INT;

  BEGIN
    postal_id := (SELECT id_code_postal FROM _code_postal WHERE code_postal = NEW.code_postal);
    IF postal_id IS NULL THEN
      INSERT INTO _code_postal(code_postal) VALUES(NEW.code_postal) RETURNING id_code_postal AS postal_id;
    END IF;

    INSERT INTO _utilisateur(mail_utilisateur, sexe, age, profession, situation_familiale, frequence_lecture, vitesse_lecture, nb_livres_lus, id_code_postal) VALUES(NEW.mail_utilisateur, NEW.sexe, NEW.age, NEW.profession, NEW.situation_familiale, NEW.frequence_lecture, NEW.vitesse_lecture, NEW.nb_livres_lus, postal_id) RETURNING id_utilisateur AS user_id;

    format_ids := (SELECT id_format FROM _format WHERE format IN (NEW.formats_preferes));
    FOREACH format_id IN ARRAY format_ids
    LOOP
      INSERT INTO _format_utilisateur VALUES(format_id, user_id);
    END LOOP;

    genre_ids := (SELECT id_genre FROM _genre WHERE libelle_genre IN (NEW.genres_preferes));
    FOREACH genre_id IN ARRAY genre_ids
    LOOP
      INSERT INTO _utilisateur_genre VALUES(user_id, genre_id);
    END LOOP;

    auteur_ids := (SELECT id_auteur FROM _auteur WHERE nom IN (NEW.auteurs_preferes));
    FOREACH auteur_id IN ARRAY auteur_ids
    LOOP
      INSERT INTO _utilisateur_auteur VALUES(user_id, auteur_id);
    END LOOP;

    book_ids := (SELECT id_livre FROM _livre WHERE titre IN (NEW.livres_preferes));
    FOREACH book_id IN ARRAY book_ids
    LOOP
      INSERT INTO _livre_utilisateur VALUES(user_id, book_id);
    END LOOP;

    motive_ids := (SELECT id_motivation FROM _motivation WHERE motivation IN (NEW.motivations_lecture));
    FOREACH motive_id IN ARRAY motive_ids
    LOOP
      INSERT INTO _utilisateur_motivation VALUES(user_id, motive_id);
    END LOOP;

    procuration_ids := (SELECT id_procuration FROM _procuration WHERE procuration IN (NEW.methodes_procuration));
    FOREACH procuration_id IN ARRAY procuration_ids
    LOOP
      INSERT INTO _utilisateur_procuration VALUES(user_id, procuration_id);
    END LOOP;

    language_ids := (SELECT id_langue FROM _langue WHERE langue IN (NEW.langues_lecture));
    FOREACH language_id IN ARRAY language_ids
    LOOP
      INSERT INTO _utilisateur     evol_exemple := :new.exemple  - :old.exemple;
_langue VALUES(user_id, language_id);
    END LOOP;

    buy_ids := (SELECT id_raison_achat FROM _raison_achat WHERE raison_achat IN (NEW.raisons_achat));
    FOREACH buy_id IN ARRAY buy_ids
    LOOP
      INSERT INTO _utilisateur_raison_achat VALUES(user_id, buy_id);
    END LOOP;
  END;
$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS triggerInsertUser ON v_formulaire;
CREATE TRIGGER triggerInsertUser
INSTEAD OF INSERT
ON v_formulaire FOR EACH ROW
EXECUTE PROCEDURE insertUser();

--------------

CREATE OR REPLACE FUNCTION updateNote() RETURNS TRIGGER AS $$
  DECLARE 
    note_exist INT;
    livre_id INT;
    user_id INT;
    nom_note TEXT;
    old_nom_note TEXT;

  BEGIN
    note_exist := (SELECT note FROM _livre_utilisateur WHERE id_livre = NEW.id_livre AND id_utilisateur = NEW.id_utilisateur);

    /* trouve la caractéristique à augmenter */
    IF NEW.note = 1 THEN
        nom_note := 'nb_note_1_etoile';
    ELSIF NEW.note = 2 THEN
        nom_note := 'nb_note_2_etoile';
    ELSIF NEW.note = 3 THEN
        nom_note := 'nb_note_3_etoile';
    ELSIF NEW.note = 4 THEN
        nom_note := 'nb_note_4_etoile';
    ELSE
        nom_note := 'nb_note_5_etoile';
    END IF;

    IF note_exist IS NULL THEN
      /* nb_notes du livre +1, note correspondante +1 */
      UPDATE _livre SET nb_notes = nb_notes + 1, (nom_note) = (nom_note) + 1 WHERE id_livre = NEW.id_livre;

    ELSE 
      IF OLD.note = 1 THEN
            old_nom_note := 'nb_note_1_etoile';
        ELSIF OLD.note = 2 THEN
            old_nom_note := 'nb_note_2_etoile';
        ELSIF OLD.note = 3 THEN
            old_nom_note := 'nb_note_3_etoile';
        ELSIF OLD.note = 4 THEN
            old_nom_note := 'nb_note_4_etoile';
        ELSE
            old_nom_note := 'nb_note_5_etoile';
        END IF;
        /* ancienne note du livre -1, nouvelle note du livre +1 */
        UPDATE _livre SET (old_nom_note) = (old_nom_note) - 1, (nom_note) = (nom_note) + 1 WHERE id_livre = NEW.id_livre;
      END IF;

      RETURN NEW;
  END;
$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS triggerUpdateNote ON _livre_utilisateur;
CREATE TRIGGER triggerUpdateNote
AFTER UPDATE
ON _livre_utilisateur FOR EACH ROW
EXECUTE PROCEDURE updateNote();

  