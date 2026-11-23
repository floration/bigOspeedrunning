import sys,json,gzip
P='/home/claude/w/repo/research/p104-live-relative-gain'
sys.path.insert(0,P)
from verify_split_helpers import rebuild
from verify_bidirectional import reconstruct, read, canonical
word,layout=rebuild()
word,_=reconstruct(word, read("BANK-FACTORS.json.gz"))
print(canonical(word), len(word['moves']), len(word['initial']))
json.dump(word,gzip.open('final_word.json.gz','wt'))
json.dump(layout,gzip.open('final_layout.json.gz','wt'))
