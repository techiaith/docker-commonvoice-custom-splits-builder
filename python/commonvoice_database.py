import os
import sqlite3

import pandas as pd

from tqdm import tqdm
from mutagen.mp3 import MP3

os.makedirs('/data/commonvoice/', exist_ok=True)
conn = sqlite3.connect('/data/commonvoice/cv.db')

# client_id	path	sentence	up_votes	down_votes	age	gender	accents	locale	segment
def create():
    conn.execute('''
        CREATE TABLE "commonvoice" (
            "version"	    TEXT,
            "split"	        TEXT,
            "client_id"     TEXT,
            "path"	        TEXT,
            "sentence"	    TEXT,
            "up_votes"      INTEGER,
            "down_votes"    INTEGER,
            "age"           TEXT,
            "gender"        TEXT,
            "accents"       TEXT,
            "locale"        TEXT,
            "segment"       TEXT,
            "duration"	    REAL
        )
    ''')
    conn.commit()


def tsv_columns():
    return ["client_id","path","sentence","up_votes","down_votes","age","gender","accents","locale","segment"]


def drop():
    conn.execute("DROP TABLE IF EXISTS commonvoice")
    conn.commit()


def add_records(records):
    sql = """
        INSERT INTO commonvoice (version, split, client_id, path, sentence, up_votes, down_votes, age, gender, accents, locale, segment, duration) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    c = conn.cursor()
    c.executemany(sql, records)
    print ("Inserted ", c.rowcount, " rows.")
    conn.commit()


def import_tsv_file(version, split, tsv_file_path):
    print (version, split, ".....")

    df = pd.read_csv(tsv_file_path, sep='\t', engine='python', quotechar='"', on_bad_lines='skip')
    db_entries = list()
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        mp3file_file_path = os.path.join(os.path.dirname(tsv_file_path), "clips", row["path"])
        audio = MP3(mp3file_file_path)
        db_entries.append((
            version, split, row["client_id"], row["path"], row["sentence"], row["up_votes"], row["down_votes"], 
            row["age"], row["gender"], row["accents"], row["locale"], row["segment"], audio.info.length
        ))
    add_records(db_entries)


def get_duration_from_path(mp3_path):
    return query_scalar("""
        SELECT duration FROM commonvoice 
        WHERE path LIKE ?
    """, (mp3_path,))


def get_duration_from_sentence(version, split, sentence):
    return query_scalar("""
        SELECT duration FROM commonvoice 
        WHERE version=?
        AND split LIKE ?
        AND sentence LIKE ?
    """, (version, split, sentence))


def get_split(version, split):
    return query("""
        SELECT client_id, path, sentence, up_votes, down_votes, age, gender, accents, locale, segment FROM commonvoice
        WHERE version=?
        AND split LIKE ?
    """, (version, split))

def get_split_with_accent(version, accent, split):
    return query("""
        SELECT client_id, path, sentence, up_votes, down_votes, age, gender, accents, locale, segment FROM commonvoice
        WHERE version=?
        AND accents LIKE ?
        AND split LIKE ?
    """, (version, accent, split))

def get_split_row(version, split, sentence):
    return query("""
        SELECT client_id, path, sentence, up_votes, down_votes, age, gender, accents, locale, segment FROM commonvoice
        WHERE version=?
        AND split LIKE ?
        AND sentence LIKE ?
    """, (version, split, sentence))


def query(sql, params):
    c = conn.cursor()
    query = c.execute(sql, params)
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)
    c.close()

    return results


def query_scalar(sql, params):
    c = conn.cursor()
    c.execute(sql, params)
    result,=c.fetchone()
    c.close()
    return result

