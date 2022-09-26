import os
import json
import shutil
import pandas as pd

import text_preprocess

import commonvoice_database as cvdb

from pathlib import Path

from tqdm import tqdm

src_corpora = [
    {"id":"CV11_CY", "lang":"cy", "train":"train.tsv", "dev":"dev.tsv", "test":"test.tsv"}, 
    {"id":"CV11_EN", "lang":"en", "train":"train.tsv", "dev":"dev.tsv", "test":"test.tsv"}
]

trgt_corpora = {"train":"train.tsv", "dev":"dev.tsv", "test":"test.tsv"}

destination_dir = "/data/commonvoice/CV11_EN_CY/cv-corpus-11.0-2022-09-21/cy/"
destination_clips_dir = os.path.join(destination_dir, "clips")
if Path(destination_clips_dir).is_dir(): shutil.rmtree(destination_clips_dir)
Path(destination_clips_dir).mkdir(parents=True, exist_ok=True)

#
with open("vocab.json", 'r', encoding='utf-8') as json_file:
    vocab = set(json.load(json_file).keys())
    
print (vocab)

# train, dev, test...    
for split in ["test", "dev", "train"]:
    # {"id":"CV9_CY", "lang":"cy", "train":"train_plus.tsv", "dev":"dev.tsv", "test":"test.tsv"}, 
    dfSplitBiling = pd.DataFrame(columns=cvdb.tsv_columns())
    
    en_split_file_name = next(item for item in src_corpora if item["id"]=="CV11_EN")[split]
    cy_split_file_name = next(item for item in src_corpora if item["id"]=="CV11_CY")[split]
    
    print ("Building biling %s split" % split, en_split_file_name, cy_split_file_name)

    dfSplitCY = cvdb.get_split("CV11_CY", cy_split_file_name)

    print ("Getting priority English sentences")
    dfSplitEN = cvdb.get_split_with_accent("CV11_EN", "Welsh English", en_split_file_name)
    print ("Welsh English {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
    dfSplitEN = pd.concat([dfSplitEN, cvdb.get_split_with_accent("CV11_EN", "England English", en_split_file_name)])
    print ("England English {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
    dfSplitEN = pd.concat([dfSplitEN, cvdb.get_split_with_accent("CV11_EN", "Scottish English", en_split_file_name)])
    print ("Scottish English {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
    dfSplitEN = pd.concat([dfSplitEN, cvdb.get_split_with_accent("CV11_EN", "Northern Irish", en_split_file_name)])
    print ("Northern Irish {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
    dfSplitEN = pd.concat([dfSplitEN, cvdb.get_split_with_accent("CV11_EN", "Irish English", en_split_file_name)])
    print ("Irish English {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
    dfSplitEN = pd.concat([dfSplitEN, cvdb.get_split("CV11_EN", en_split_file_name)])
    print ("Remainder of {} {} recordings".format(en_split_file_name, len(dfSplitEN)))
           
    source_clips_dir = "/data/commonvoice/CV11_CY/cv-corpus-11.0-2022-09-21/cy/clips"
    dfSplitBiling = pd.concat([dfSplitCY])
    dfFilteredSplitEN = pd.DataFrame()

    print ("Length split biling", len(dfSplitBiling))

    for mp3file in dfSplitCY["path"].tolist():
        #print (mp3file)
        shutil.copyfile(os.path.join(source_clips_dir, mp3file),
                        os.path.join(destination_clips_dir, mp3file))

    count = 0
   
    source_clips_dir = "/data/commonvoice/CV11_EN/cv-corpus-11.0-2022-09-21/en/clips"

    cy_size = int(dfSplitCY.shape[0])
    print ("Building.... will exit as soon as we have %s en rows to add to the %s split " % (cy_size, split))
    iterator = tqdm(dfSplitEN.iterrows(), total=dfSplitEN.shape[0], desc="%s: " % split)
    
    copied_mp3s = set()    
    for index, d in iterator:
        
        if d["path"] in copied_mp3s:
            continue

        if count > cy_size:
            print("Build complete")
            iterator.close()
            break
        else:
            dur = cvdb.get_duration_from_path(d["path"])
            if dur < 15.0:
                # process text - validate tokens etc.
                # word delimiter token is | not ' '                
                all_tokens = text_preprocess.cleanup(d["sentence"]).replace(" ","|")
                transcript_vocab = set(all_tokens)
                
                # determine if any are 'oov'
                oov = transcript_vocab - vocab
                if len(oov) > 0:
                    # transcript contains unsupported tokens
                    print (oov, d["sentence"])
                    continue

                #                
                dfSplitBiling = pd.concat([dfSplitBiling, d.to_frame().T])
                dfFilteredSplitEN = pd.concat([dfFilteredSplitEN, d.to_frame().T])    

                count += 1
                #print (count, cy_size)

        # copy mp3 files...
        copied_mp3s.add(d["path"])
        shutil.copyfile(os.path.join(source_clips_dir, d["path"]), 
                        os.path.join(destination_clips_dir, d["path"]))
            
    destination_file_path = os.path.join(destination_dir, trgt_corpora[split])    
    print ("Writing to %s" % destination_file_path)
    print ("Length split biling", len(dfSplitBiling))

    print ("Shuffle biling data")
    dfSplitBiling = dfSplitBiling.sample(frac=1).reset_index(drop=True)

    dfSplitBiling.to_csv(destination_file_path, sep='\t', index=None)

    if split=="test":
        # save language specific test files...
        dfSplitCY.to_csv(destination_file_path.replace(".tsv","-cy.tsv"), sep='\t', index=None)
        dfFilteredSplitEN.to_csv(destination_file_path.replace(".tsv","-en.tsv"), sep='\t', index=None)

