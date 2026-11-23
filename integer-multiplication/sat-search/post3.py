import sys
sys.argv=['x']
exec(open('checkhit.py').read().split("if __name__")[0])
hits=json.load(open('bypass3_hits.json'))
good=[]
for h in hits:
    ok=check(*h[1:])
    if ok: good.append(h)
print('SURVIVE',len(good)); json.dump(good,open('bypass3_good.json','w'))
for g in sorted(good,reverse=True)[:30]: print(g)
