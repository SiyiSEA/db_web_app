import sqlite3

# create a connection to our SQlite database
DatabaseName = './Team2_Siyi.db'
connection = sqlite3.connect(DatabaseName)
cur = connection.cursor()

# CREATE TABLE of pheno in database
cur.executescript("""
        CREATE TABLE PHENO (
            SampleKey INT UNIQUE,
            Age INT,
            Sex char(2) NOT NULL,
            PRIMARY KEY (SampleKey)
        );
    """)

cur.executescript("""
        CREATE TABLE EPIC (
        ProbeName varchar(255) NOT NULL,
        ProbeKey INT UNIQUE,
        Chr INT,
        GeneName varchar(255),
        RefGeneGroup varchar(255), 
        CpGIsland varchar(255),
        PRIMARY KEY (ProbeKey)
        );
    """)


cur.executescript("""
        CREATE TABLE PROBEINFO (
        ProbeName varchar(255) NOT NULL,
        ProbeKey INT UNIQUE
        );
    """)

cur.executescript("""
        CREATE TABLE AAAVALUE (
        ProbeKey INT,
        SampleKey INT,
        Value decimal(10, 10),
        FOREIGN KEY (ProbeKey) REFERENCES RPOBEINFO(ProbeKey)
        );
    """)

cur.executescript("""
        CREATE TABLE BBBVALUE (
        ProbeKey INT,
        SampleKey INT,
        Value decimal(10, 10),
        FOREIGN KEY (ProbeKey) REFERENCES RPOBEINFO(ProbeKey)
        );
    """)

cur.executescript("""
        CREATE TABLE CCCVALUE (
        ProbeKey INT,
        SampleKey INT,
        Value decimal(10, 10),
        FOREIGN KEY (ProbeKey) REFERENCES RPOBEINFO(ProbeKey)
        );
    """)

cur.executescript("""
        CREATE TABLE DDDVALUE (
        ProbeKey INT,
        SampleKey INT,
        Value decimal(10, 10),
        FOREIGN KEY (ProbeKey) REFERENCES RPOBEINFO(ProbeKey)
        );
    """)

# INSERT the data
import csv

with open('Siyi_Phen.csv', 'r') as phe:
    reader = csv.reader(phe)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO PHENO VALUES (?,?,?);", tuple(line))
    print("PHENO table is finished!!!!!")

with open('Siyi_epic.csv', 'r') as epi:
    reader = csv.reader(epi)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO EPIC VALUES (?,?,?,?,?,?);", tuple(line))
    print("EPIC table is finished!!!!!")

with open('Siyi_CpG_info_more.csv', 'r') as cpg:
    reader = csv.reader(cpg)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO PROBEINFO VALUES (?,?);", tuple(line))
    print("PROBEINFO table is finished!!!!!")

with open('Siyi_A_betas.csv', 'r') as aaa:
    reader = csv.reader(aaa)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO AAAVALUE VALUES (?,?,?);", tuple(line))
    print("AAAVALUE table is finished!!!!!")

with open('Siyi_B_betas.csv', 'r') as bbb:
    reader = csv.reader(bbb)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO BBBVALUE VALUES (?,?,?);", tuple(line))
    print("BBBVALUE table is finished!!!!!")

with open('Siyi_C_betas.csv', 'r') as ccc:
    reader = csv.reader(ccc)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO CCCVALUE VALUES (?,?,?);", tuple(line))
    print("CCCVALUE table is finished!!!!!")

with open('Siyi_D_betas.csv', 'r') as ddd:
    reader = csv.reader(ddd)
    next(reader)
    for line in reader:
        connection.execute("INSERT INTO DDDVALUE VALUES (?,?,?);", tuple(line))
    print("DDDVALUE table is finished!!!!!")

connection.commit()
connection.close()

