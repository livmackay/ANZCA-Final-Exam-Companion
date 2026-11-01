#!/usr/bin/env python3
"""Validate every content/set-N.json, recompute its counts, and rebuild content/index.json.
Run after adding or changing a set:  python3 tools/build_index.py"""
import json,glob,os,re,sys,datetime
root=os.path.join(os.path.dirname(__file__),'..','content')
TYPES={'learn','retrieve','speak','saq','viva','los','trials','refs','docs'}
sets=[];bad=0
for f in sorted(glob.glob(root+'/set-*.json'),key=lambda p:int(re.search(r'set-(\d+)',p).group(1))):
    d=json.load(open(f,encoding='utf-8'));n=int(re.search(r'set-(\d+)',f).group(1))
    errs=[]
    if d.get('num')!=n:errs.append(f"num should be {n}")
    ids=set()
    for it in d.get('items',[]):
        i=it.get('id')
        if not i or i in ids:errs.append(f"missing or duplicate id {i}")
        ids.add(i)
        t=it.get('type')
        if t not in TYPES:errs.append(f"{i}: unknown type {t}")
        if t in('retrieve','speak') and not(it.get('q') and it.get('a')):errs.append(f"{i}: needs q and a")
        if t in('learn','trials','refs','docs') and not it.get('body'):errs.append(f"{i}: needs body")
        if t=='los' and not it.get('groups'):errs.append(f"{i}: needs groups")
    c={}
    for it in d.get('items',[]):c[it['type']]=c.get(it['type'],0)+1
    los=sum(len(g.get('items',[])) for it in d['items'] if it['type']=='los' for g in it.get('groups',[]))
    d['counts']={k:c.get(k,0) for k in('learn','speak','retrieve','saq','viva')}
    d['counts']['los']=d.get('counts_los_override',los)
    d['counts'].update({'trials':c.get('trials',0),'refs':c.get('refs',0),'docs':c.get('docs',0)})
    d['updated']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    if errs:
        bad+=1;print(f"set-{n}: PROBLEMS");[print('  -',e) for e in errs];continue
    json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False)
    sets.append({'num':n,'file':os.path.basename(f),'updated':d['updated']});print(f"set-{n}: ok {d['counts']}")
json.dump({'sets':sets},open(root+'/index.json','w'))
print(f"{len(sets)} sets in index; {bad} with problems");sys.exit(1 if bad else 0)
