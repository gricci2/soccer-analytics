import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=SoccerAnalytics;"
    "Trusted_Connection=yes;"
)

query = open("../../sql/pass_locations_all.sql").read()
all_passes_df = pd.read_sql(query, conn)

all_passes_df.to_csv("../../data/processed/pass_locations_all.csv", index=False)