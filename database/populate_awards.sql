set schema 'sae';

WbImport
-usePgCopy
-type=text
-file='../SQL/prix.csv'
-table=_prix
-delimiter=','
-header=true;
