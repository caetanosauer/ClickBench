import json, re
src = open("data.generated.js").read()
src = src[src.index("["): src.rindex("]")+1]
data = json.loads(src)
MACH = "c7a.metal-48xl"
rows = []
for d in data:
    if d.get("machine") != MACH: continue
    res = d.get("result") or []
    # hot = min of tries[1:], cold = tries[0]; skip nulls
    hot=cold=0.0; nq=0; bad=False
    for r in res:
        if not r or r[0] is None: continue
        cold += r[0]
        tail=[x for x in r[1:] if x is not None]
        hot += (min(tail) if tail else r[0]); nq+=1
    if nq < 40: continue
    rows.append((d["system"], d.get("date"), nq, round(cold,1), round(hot,2), d.get("load_time"), d.get("data_size")))
rows.sort(key=lambda x: x[4])
print("%-38s %-11s %3s %9s %9s %8s" % ("system","date","nq","cold_sum","HOT_sum","load_s"))
for s,dt,nq,c,h,lt,ds in rows:
    star = "  <<<" if "Salesforce Hyper" in s else ""
    print("%-38s %-11s %3d %9.1f %9.2f %8s%s" % (s,dt,nq,c,h,lt,star))
