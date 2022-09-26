import commonvoice_database as cvdb

from get_transcripts import get_transcript


from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""


def main(transcript_file_paths, **args):

    # ignore and hardcode splits we're interested in.
    transcript_file_paths="/data/commonvoice/CV9_CY/other.tsv,/data/commonvoice/CV9_CY/validated.tsv"

    transcript_sets = list()
    transcript_collection = list()
    transcript_file_paths_list = transcript_file_paths.split(",")
        
    for transcript_file_path in transcript_file_paths_list:
        transcripts = get_transcript(transcript_file_path)
        transcript_sets.append(set(transcripts))
        transcript_collection.append(transcripts)

    #
    for idx, ts in enumerate(transcript_sets):
        print("\n\n#unique transcripts in set %s : %s" % (str(idx), len(ts)))
        if idx<len(transcript_sets)-1:
            # because of hardcoded file paths.
            # idx 0 = other.tsv
            # idx 1 = validated.tsv 
            new_sentences = ts - transcript_sets[idx+1]
            unique_new_sentences = list()
            
            for sentence in new_sentences:
                if transcript_collection[idx].count(sentence) == 1:
                    unique_new_sentences.append(sentence)

            total_duration = 0.0
            cx = 0
            for us in unique_new_sentences:
                total_duration = total_duration + cvdb.get_duration("CV9_CY", "other.tsv", us)
                cx += 1
                print (cx, total_duration)

            print (idx, len(new_sentences))
            print (total_duration)



if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--transcript_file_paths", dest="transcript_file_paths", required=True, help="comma seperated transcript_file_path")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

