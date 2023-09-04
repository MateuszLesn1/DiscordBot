import requests
import sqlite3
import logging 


def init_data(database_name):
    conn = sqlite3.connect(database_name)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS voices(
            uuid INTEGER UNIQUE,
            name TEXT     
        );
            """)
    conn.commit()
    conn.close()
    
def fetch_and_store_data(api_url, database_name):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes      
        data = response.json()

        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        for dict_item in data:
            uuid = dict_item["voicemodel_uuid"]
            name = dict_item["name"]

            cursor.execute("INSERT OR IGNORE INTO voices (uuid, name) VALUES (?, ?);", (uuid, name))

        conn.commit()
        conn.close()

        logging.info("Data successfully fetched and stored.")
        print("")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise  
    
def read_data(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        select_all_data = "SELECT * FROM voices;"
        cursor.execute(select_all_data)
        data = cursor.fetchall()
        for row in data:
            print("UUID:", row[0])
            print("Name:", row[1])
            print("")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
            
        
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    database_name = 'voices.db'
    api_url = "https://api.uberduck.ai/voices?mode=tts-basic"

    init_data(database_name)
    fetch_and_store_data(api_url, database_name)
    read_data(database_name)
    
    