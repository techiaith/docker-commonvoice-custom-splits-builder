# @todo.

# select frequency, count(*) from 
#   (
#       select sentence, count(*) as frequency 
#       from commonvoice 
#       where version like 'CV10_CY' 
#       and split like 'validated.tsv' 
#       group by sentence
#   ) 
#   group by frequency 
#   order by frequency desc;
#
