#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import glob
import pandas as pd
import subprocess
import shlex

from mutagen.mp3 import MP3

from download_manager import download, extract

from pathlib import Path
from argparse import ArgumentParser, RawTextHelpFormatter

import commonvoice_database
from data_urls import DATA_URLS

DESCRIPTION = """

"""


def main(cv_root_dir, **args):

    commonvoice_database.drop()
    commonvoice_database.create()

    #for key in DATA_URLS:
    for cv_data_set in DATA_URLS:
        key = "CV" + str(cv_data_set["version"]) + "_" + cv_data_set["lang"].upper()
        downloaded_cv_root_dir = os.path.join(cv_root_dir, key)
        
        print ("Downloading and extracting CommonVoice %s to %s..." % (key, downloaded_cv_root_dir))
        downloaded, tgz_file_path = download(cv_data_set["url"], downloaded_cv_root_dir)
        if downloaded:
            extract(tgz_file_path)
            # update the downloaded_cv_root_dir
            print ("extracted cv data in: ", downloaded_cv_root_dir)

    	#
        tgz_file_name = os.path.basename(tgz_file_path)
        downloaded_cv_root_dir = os.path.join(downloaded_cv_root_dir, tgz_file_name.replace("-" + cv_data_set["lang"] + ".tar.gz",""), cv_data_set["lang"])                
        print ("{} Common Voice data extracted into {}".format(cv_data_set["version"], downloaded_cv_root_dir))

        #
        if cv_data_set["lang"].upper()=="CY":
            print("creating alternative default splits with CorporaCreator (s=3)")
            validated_tsv_file_path = os.path.join(downloaded_cv_root_dir, "validated.tsv")
            cmd = "create-corpora -f {} -d {} -s 3".format(validated_tsv_file_path, downloaded_cv_root_dir)
            print (cmd)
            subprocess.run(shlex.split(cmd), stderr=sys.stderr, stdout=sys.stdout)
            corpora_creator_output_dir = os.path.join(downloaded_cv_root_dir, cv_data_set["lang"])
            shutil.copy(os.path.join(corpora_creator_output_dir,"train.tsv"), os.path.join(downloaded_cv_root_dir,"train.tsv"))
            shutil.copy(os.path.join(corpora_creator_output_dir,"dev.tsv"), os.path.join(downloaded_cv_root_dir,"dev.tsv"))
            shutil.copy(os.path.join(corpora_creator_output_dir,"test.tsv"), os.path.join(downloaded_cv_root_dir,"test.tsv"))
            shutil.rmtree(corpora_creator_output_dir)

        #
        print ("Importing metadata into local database...")        
        # client_id     path    sentence    up_votes    down_votes	    age	    gender	    accents	    locale	    segment
        for tsvfile in Path(downloaded_cv_root_dir).glob("*.tsv"):
            h,t = os.path.split(tsvfile)
            if t=="reported.tsv": continue
            commonvoice_database.import_tsv_file(key, t, tsvfile)



if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--target_dir", dest="cv_root_dir", required=True, help="target directory for extracted archive, also root directory for training data")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

