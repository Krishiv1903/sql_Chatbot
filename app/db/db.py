import pyodbc

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.12.141\MSSQL2022;"
    "DATABASE=KrishivTest;"
    "UID=crmnext;"
    "PWD=Secure#9922$;"
    "TrustServerCertificate=yes;"
)

def get_connection():
    try:
        conn = pyodbc.connect(CONN_STR)
        print("✅ DB CONNECTED")
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None
