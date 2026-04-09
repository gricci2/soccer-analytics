import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=SoccerAnalytics;"
    "Trusted_Connection=yes;"
)

query = open("../../sql/shot_model.sql").read()
shots_df = pd.read_sql(query, conn)

shots_df.to_csv("../../data/processed/shot_model.csv", index=False)