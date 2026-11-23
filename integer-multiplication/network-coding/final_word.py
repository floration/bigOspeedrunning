import sys,gzip,json
sys.path.insert(0,'.')
from verify_split_helpers import rebuild, read
from verify_bidirectional import reconstruct
word,layout=rebuild(check_parents=False)
final,_=reconstruct(word, read("BANK-FACTORS.json.gz"))
json.dump(final,gzip.open('/tmp/claude-0/w/d/FINAL8027.json.gz','wt'))
json.dump(layout,open('/tmp/claude-0/w/d/LAYOUT8027.json','w'))
print(len(final['moves']),len(final['initial']),final['first_output'])
