
import json
import logging
import psycopg2

logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


with open ("./Config/DBConfig.json", "r") as conf_db:
        dataConf = json.load(conf_db)
        host = dataConf["host"]
        database = dataConf["database"]
        user = dataConf["user"]
        password =dataConf["password"]

def connect():
    
        
    logger.info('Connecting to the PostgreSQL database...')
    try:
        # Connexion à la base de données
        connexion = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        # Création d'un curseur
        cursor = connexion.cursor()
        print("connection etablie")
        
    except (Exception, psycopg2.Error) as error:
        logger.error(f"\nErreur lors de la connexion à PostgreSQL :{error}\n")
    
    
    finally:
      
        if connexion:
            return cursor,connexion
        else:
            return None,None

def create_trigger(cursor, connexion):
    
    try:
        cursor.execute("""
        CREATE OR REPLACE FUNCTION insert_into_history()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO cac40_history_data (date, share, symbol, open, high, low, close, adj_Close, volume)
            VALUES (NEW.date, NEW.share,NEW.symbol, NEW.open, NEW.high, NEW.low, NEW.close, NEW.adj_Close, NEW.volume);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

        cursor.execute("""
            CREATE TRIGGER daily_to_history
            AFTER INSERT ON cac40_daily_data
            FOR EACH ROW
            EXECUTE FUNCTION insert_into_history();
        """)

        connexion.commit()
        print("\nDéclencheur ajouté avec succès.\n")
        
    except psycopg2.Error as e:
        
        if "already exists" in str(e):
            print("\nLe déclencheur existe déjà.\n")
        else:
            print(f"\nErreur lors de l'ajout du déclencheur :{e}\n")
    

def create_table(table_name,cursor,connexion):
    
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        date TIMESTAMP WITH TIME ZONE,
        share VARCHAR(255),
        symbol VARCHAR(25),
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume FLOAT
    );
    '''
    
    cursor.execute(create_table_query)
    connexion.commit()
    print("\ntable crée\n")
    


def insert_data(table_name, cursor, connexion, row):
    insert_query = f'''
        INSERT INTO {table_name} (date, share, symbol, open, high, low, close, adj_close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    try:
        
        formatted_date = row['date'].isoformat()

        data_tuple = (
            formatted_date, row['share'], row['symbol'], row['open'], row['high'], 
            row['low'], row['close'], row['adj_close'], row['volume']
        )
        
        cursor.execute(insert_query, data_tuple)
        connexion.commit()
        print("\nLigne insérée dans la table\n")
    except Exception as e:
        print(f"\nOupsss, un problème est survenu lors de l'insertion dans la base de données: {e}\n")
        connexion.rollback()

