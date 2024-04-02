import os
import psycopg2

# Conexiunea la baza de date
conn = psycopg2.connect(
    host="my_postgres",
    database="meteo_db",
    user="robert",
    password="student",
    port=5432
)

cur = conn.cursor()

# Crearea tabelului Tari
cur.execute('DROP TABLE IF EXISTS Tari CASCADE;')
cur.execute('CREATE TABLE Tari (' 
            'id serial PRIMARY KEY,'
            'nume_tara varchar(255) NOT NULL UNIQUE,'
            'latitudine DOUBLE PRECISION NOT NULL,'
            'longitudine DOUBLE PRECISION NOT NULL);'
            )

# Crearea tabelului Orase
cur.execute('DROP TABLE IF EXISTS Orase CASCADE;')
cur.execute('CREATE TABLE Orase ('
            'id serial PRIMARY KEY,'
            'id_tara integer,'
            'nume_oras varchar(255) NOT NULL,'
            'latitudine DOUBLE PRECISION NOT NULL,'
            'longitudine DOUBLE PRECISION NOT NULL,'
            'CONSTRAINT UC_City UNIQUE (id_tara, nume_oras),'
            'CONSTRAINT FK_Country FOREIGN KEY (id_tara)'
                'REFERENCES Tari (id) ON DELETE CASCADE);'
            )

# Crearea tabelului Temperaturi
cur.execute('DROP TABLE IF EXISTS Temperaturi CASCADE;')
cur.execute('CREATE TABLE Temperaturi ('
            'id serial PRIMARY KEY,'
            'valoare DOUBLE PRECISION NOT NULL,'
            'timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'id_oras integer,'
            'CONSTRAINT UC_Temp UNIQUE (id_oras, timestamp),'
            'CONSTRAINT FK_City FOREIGN KEY (id_oras)'
                'REFERENCES Orase (id) ON DELETE CASCADE);'
            )

conn.commit()
cur.close()
conn.close()