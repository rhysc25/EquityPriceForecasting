import Global
import pandas as pd
from sqlalchemy import text

def exportDataframeCSV():

    Global.marketDataFrame.to_csv('MarketData.csv')


def exportDataframeSQL(parameters):

    instrument = parameters["symbols"]
    try: insertIgnoreDataframe(Global.marketDataFrame, Global.engine, instrument)
    except: 
        print("boo")
        pass

def exportToSQL(parameters):

    instrument = parameters["symbols"]

    # Push DataFrame into MariaDB table
    Global.marketDataFrame.to_sql(instrument, con=Global.engine, if_exists='append', index=False)

def importFromSQL(parameters):

    instrument = parameters["symbols"]

    start = Global.marketDataFrame["t"].iloc[0]
    end   = Global.marketDataFrame["t"].iloc[-1]

    # If t is datetime.date or datetime64, convert to string first
    start_str = start.strftime('%Y-%m-%d')
    end_str   = end.strftime('%Y-%m-%d')

    query = f"SELECT t FROM {instrument} WHERE t BETWEEN '{start_str}' AND '{end_str}';"

    dfFromSQL = pd.read_sql(query, con=Global.engine)

    shape = dfFromSQL.shape
    rowsTotal= shape[0]

    return dfFromSQL, rowsTotal

def checkForExistence(parameters):

    instrument = parameters["symbols"]
    query = "SELECT t FROM " + instrument + ";"

    try: tColumn = pd.read_sql(query, con=Global.engine)
    except: return False

    allIn = Global.marketDataFrame["t"].isin(tColumn["t"]).all()

    return allIn


def upsertDataframe(df, engine, table_name, key_columns):

    # All columns from the DataFrame
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

    # Execute in one transaction
    with engine.begin() as conn:
        conn.execute(upsert_sql, df.to_dict(orient='records'))


def insertIgnoreDataframe(df, engine, table_name):
    all_cols = list(df.columns)
    cols_sql = ", ".join(f"`{c}`" for c in all_cols)
    params_sql = ", ".join(f":{c}" for c in all_cols)

    insert_sql = text(f"""
        INSERT IGNORE INTO {table_name} ({cols_sql})
        VALUES ({params_sql})
    """)

    with engine.begin() as conn:
        conn.execute(insert_sql, df.to_dict(orient='records'))