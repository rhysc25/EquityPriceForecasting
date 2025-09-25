import Global
import pandas as pd
from sqlalchemy import text

def chopDateFrame(parameters):
    start = pd.to_datetime(parameters["start"]).dt.date
    mask = Global.marketDataFrame['t'] >= start
    filtered_df = Global.marketDataFrame[mask]
    return filtered_df

def exportDataframeCSV():

    Global.marketDataFrame.to_csv('MarketData.csv')


def exportDataframeSQL(parameters):

    instrument = parameters["symbols"]
    try: insertIgnoreDataframe(Global.marketDataFrame, Global.engine, instrument)
    except: pass


def importFromSQL(parameters):

    instrument = parameters["symbols"]

    start = pd.to_datetime(parameters["start"].split("T")[0]).date()
    end = pd.to_datetime(parameters["end"].split("T")[0]).date()

    query = f"SELECT * FROM {instrument} WHERE t BETWEEN '{start}' AND '{end}';"

    dfFromSQL = pd.read_sql(query, con=Global.engine)

    shape = dfFromSQL.shape
    rowsTotal= shape[0]

    return dfFromSQL, rowsTotal

def checkForExistence(parameters):

    instrument = parameters["symbols"]
    query = "SELECT t FROM " + instrument + ";"

    try: tColumn = pd.read_sql(query, con=Global.engine)
    except: return False

    start = pd.to_datetime(parameters["start"].split("T")[0]).date()
    end = pd.to_datetime(parameters["end"].split("T")[0]).date()

    if (start in tColumn['t'].values) and (end in tColumn['t'].values):
        allIn = True
    else:
        allIn = False

    return allIn


def insertIgnoreDataframe(df, engine, table_name):

    command1 = text(f"""CREATE TABLE IF NOT EXISTS `{table_name}` (
        t DATE NOT NULL,      
        o DECIMAL(10,2),          
        h DECIMAL(10,2),         
        l DECIMAL(10,2),    
        c DECIMAL(10,2),  
        n BIGINT,      
        v BIGINT,
        vw DECIMAL(10,2),
        PRIMARY KEY (t)
    );""")

    with engine.begin() as conn:
        conn.execute(command1)
    
    all_cols = list(df.columns)
    cols_sql = ", ".join(f"`{c}`" for c in all_cols)
    params_sql = ", ".join(f":{c}" for c in all_cols)

    insert_sql = text(f"""
        INSERT IGNORE INTO {table_name} ({cols_sql})
        VALUES ({params_sql})
    """)

    with engine.begin() as conn:
        conn.execute(insert_sql, df.to_dict(orient='records'))


def upsertDataframe(df, engine, table_name, key_columns):

    all_cols = list(df.columns)

    # Columns to insert
    cols_sql = ", ".join(f"`{c}`" for c in all_cols)
    params_sql = ", ".join(f":{c}" for c in all_cols)

    # Columns to update (exclude the key columns)
    update_cols = [c for c in all_cols if c not in key_columns]
    update_sql = ", ".join(f"`{c}`=VALUES(`{c}`)" for c in update_cols)

    upsert_sql = text(f"""
        INSERT INTO {table_name} ({cols_sql})
        VALUES ({params_sql})
        ON DUPLICATE KEY UPDATE {update_sql}
    """)

    with engine.begin() as conn:
        conn.execute(upsert_sql, df.to_dict(orient='records'))