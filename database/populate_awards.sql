set schema 'sae';

WbImport
-usePgCopy
-type=text
-file='../SQL/prix.csv'
-table=_prix
-delimiter=','
-header=true;

WbImport
-usePgCopy
-type=text
-file='../SQL/prix_livre.csv'
-table=_prix_livre
-delimiter=','
-header=true;