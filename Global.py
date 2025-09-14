from sqlalchemy import create_engine
from AlpacaKeys import mariaDBpassword, mariaDBIP

marketDataFrame, rowsTotal = None, None

# Connect to MariaDB on your Pi
engine = create_engine("mysql+pymysql://rhys:"+mariaDBpassword+"@"+mariaDBIP+"/quantdb")
