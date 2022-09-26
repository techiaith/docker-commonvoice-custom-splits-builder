# build o train cv9 + (validated - other)
import os
import pandas as pd
import commonvoice_database as cvdb

CV = "CV11_CY"
CV_ID = "cv-corpus-11.0-2022-09-21"

destination_dir_path = os.path.join("/data/commonvoice/", CV, CV_ID, "cy")

train = cvdb.get_split(CV, "train.tsv")
print ("Training split length", len(train))

validated = cvdb.get_split(CV, "validated.tsv")
print ("validated split length", len(validated))
unique_validated_transcripts = set(validated.sentence.tolist())

other = cvdb.get_split(CV, "other.tsv")
print ("other split length", len(other))
other_transcripts = other.sentence.tolist()
unique_other_transcripts = set(other.sentence.tolist())

new_transcripts = unique_other_transcripts - unique_validated_transcripts
print ("Unique other transcripts", len(new_transcripts))

print ("creating new training set.....")
for s in new_transcripts:
    if other_transcripts.count(s) == 1:
        train = pd.concat([train, cvdb.get_split_row(CV,"other.tsv", s)])
        
print (len(train))  
destination_file_path = os.path.join(destination_dir_path, "train_plus.tsv")
train.to_csv(destination_file_path, sep='\t', index=None)
print (destination_file_path)

# package in a tar gz file. 
cvdb.import_tsv_file(CV, "train_plus.tsv", destination_file_path)
