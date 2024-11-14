# SAE 5.C.01

## Context

IUT de Lannion            
BUT Informatique 3     
2024-2025 

**SAE 5.C.01 : Datamining**
Propose an optimised solution based on internal and external data
 - Create a business intelligence application
 - Team development of a technical solution
 - Design of a multi-dimensional database
 - Extract and analyse information to make it available to users

## Team

**Wizards of the West Coast**

- Nathan Bracquart
- Damien Goupil
- Ewan Lansonneur
- Florian Normand
- Maxime Perrot

## How to use

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Clean data (not necessary)

```bash
python3 clean_data.py
```

## How to run the data analysis

### 3. Run analysis

```bash
python3 launch_analysis.py
```

### Run single analysis

You can run a single analysis like so:

```bash
python3 analysis_scripts/<analysis_name>.py
```

e.g.

```bash
python3 analysis_scripts/acm_genre_by_era.py
```

## How to run database creation and population

Place your original data file in `./data/` and name them
- `authors.csv` for the authors data
- `books.csv` for the books data

```bash
python3 transform_load.py
```

The resulting population csv are in `./data/populate/`
You now need to open your SGBD and run the script `create_database.sql`
This will create and populate the database.
***NOTE**: The script uses **PostgreSQL***