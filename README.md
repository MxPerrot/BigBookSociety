# BigBookSociety

## Overview

> IUT de Lannion            
> BUT Informatique 3     
> 2024-2025 

**SAE 5.C.01 : Datamining**

BigBookSociety is a dynamic book recommandation website that uses user data to propose interesting books to an user according to its preferences and information. 

The project includes:

- **ETL Service:** Processes input CSV files and generates transformed CSVs in `data/populate/`.
- **Database Service:** A PostgreSQL instance that is initialized with SQL scripts and imports data from the ETL output.
- **API Service:** A FastAPI backend that connects to the PostgreSQL database.
- **Web Service:** An NGINX-based dynamic web server.
- **Cleanup Service:** An optional one-off service to remove temporary CSV files after the database has been populated.

## Prerequisites

- [Docker](https://www.docker.com/) 

## Environment Variables

The project uses a `.env` file (located in the project root) to manage environment-specific variables. For example, your `.env` file might look like:

```env
DATABASE_NAME=db_sae
DB_USERNAME=postgres
PASSWORD=password 
HOST=db
PORT=5432
```

These variables are referenced in your `docker-compose.yml` and used by the API and DB services to ensure consistency.
Make sure to not share this file with anyone as it contains your db password

## Setup Instructions

0. **Clone this repository**
   ```sh
   git clone https://github.com/MxPerrot/BigBookSociety.git 
   cd ./BigBookSociety/
   ```

1. **Prepare Input Data:**  
   Place your input CSV files (`Big_Boss_authors.csv`, `bigboss_book.csv`, `formulaire.csv`) into the `data/` directory.
   You might need to create this directory.

2. **Run the ETL Process:**  
   The ETL service will process these CSV files and output transformed files to `data/populate/`.  
   To run the ETL service, execute:
   
   ```sh
   docker-compose up --build etl
   ```

   **NOTE**
   This might a few minutes, do not worry, if something goes wrong you will get an error message.

3. **Set up Environment**
    Create the `.env` file in your project root (BigBookSociety/)

4. **Initialize the Database:**  
   The PostgreSQL container will automatically run the SQL scripts located in the `database/` folder on its first initialization.  
   The scripts import data from the CSV files in `data/populate/`.  
   **Note:** If you change any credentials, you may need to remove the persistent volume (using `docker-compose down -v`) so the DB reinitializes.

5. **Start API and Web Services:**  

   To start the remaining services, run:
   
   ```sh
   docker-compose up --build db api web
   ```
   
   - **API Service:**  
     Accessible at [http://localhost:8000](http://localhost:8000) (try [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive docs).  
   - **Web Service:**  
     Accessible at [http://localhost](http://localhost).

6. **Cleanup Temporary CSV Files (Optional):**  
   Once the database is populated and the system is running, you can clean up the CSV files by running the cleanup service:
   
   ```sh
   docker-compose run cleanup
   ```
   
   **WARNING**
   This will erase all files in the data folder, including the three files of step 1

## Troubleshooting

- **Database Connection Issues:**  
  Ensure that your API connects using `HOST=db` (as defined in the `.env` file) and that the DB service is fully initialized before the API attempts to connect. Consider using a wait script if needed.

- **ETL Not Producing Expected Output:**  
  Verify that the ETL process writes output to the `data/populate/` folder and that the file paths in your SQL scripts correctly point to these files (taking into account the volume mounts in Docker Compose).

- **Web Server Not Serving Files:**  
  Check that your static files are correctly located in the `web/` directory and that the Dockerfile for the web service is properly copying them to NGINX’s default directory.

## Team

**Wizards of the West Coast**

- Nathan Bracquart
- Miliaw Chesné
- Asaïah Cosson
- Damien Goupil
- Ewan Lansonneur
- Florian Normand
- Maxime Perrot

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [NGINX](https://www.nginx.com/)
- [Jquery](https://jquery.com/)
- [Openlibrary API](https://openlibrary.org/developers/api)
