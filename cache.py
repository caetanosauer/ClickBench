import json
def stats(path,label):
    pcs={}; comp=[]; exe=[]; ela=[]
    for line in open(path):
        if "\"k\":\"query-end\"" not in line: continue
        try: e=json.loads(line)
        except: continue
        v=e["v"]
        if v.get("statement")!="SELECT": continue
        if (v.get("query-trunc","").strip().upper()=="SELECT 1"): continue
        s=v.get("plan-cache-status","?"); pcs[s]=pcs.get(s,0)+1
        comp.append(v.get("pre-execution",{}).get("compilation-time") or 0)
        exe.append(v.get("execution",{}).get("elapsed") or 0)
        ela.append(v.get("elapsed") or 0)
    n=len(comp) or 1
    print("==== %s ====" % label)
    print("  SELECT events:", len(comp))
    print("  plan-cache-status counts:", pcs)
    print("  sum elapsed=%.2f  sum exec=%.2f  sum compile=%.2f" % (sum(ela),sum(exe),sum(comp)))
    print("  compile as %% of elapsed: %.1f%%" % (100*sum(comp)/(sum(ela) or 1)))
stats("hyper/hyperd.log","NATIVE")
print()
stats("hyper-parquet/hyperd.log","PARQUET")
