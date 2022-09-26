import pandas as pd

from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

"""

def get_transcript(transcript_file_path):
    df = pd.read_csv(transcript_file_path, sep='\t', engine='python', quotechar='"', error_bad_lines=False)
    return df["sentence"].tolist()



def main(transcript_file_path, **args):
    transcripts = get_transcript(transcript_file_path)
    unique_transcripts = set()
    duplicate_transcripts = set()

    print ("Transcripts length = %s" % len(transcripts))

    for s in transcripts:
        if s not in unique_transcripts:
            unique_transcripts.add(s)
        else:
            duplicate_transcripts.add(s)

    print ("Unique transcripts = %s" % len(unique_transcripts))
    print ("Duplicate transcripts = %s" % len(duplicate_transcripts))
    #print (duplicate_transcripts)


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--transcript_file_path", dest="transcript_file_path", required=True, help="transcript_file_path")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

