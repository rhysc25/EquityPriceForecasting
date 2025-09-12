from DataFetch import dataFetch
from Parameters import parameters
from sqlalchemy import create_engine
from AlpacaKeys import mariaDBpassword, mariaDBIP

marketDataFrame, rowsTotal = dataFetch(parameters=parameters)

# Connect to MariaDB on your Pi
engine = create_engine("mysql+pymysql://rhys:"+mariaDBpassword+"@"+mariaDBIP+"/quantdb")
