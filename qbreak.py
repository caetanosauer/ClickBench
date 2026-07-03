import json, sys
# Parse query-end events from the parquet run; show per-query execution vs compile
# and whether parquet restriction pushdown / page-skipping shows up.
path = "hyper-parquet/hyperd.log"
ends=[]
for line in open(path):
    line=line.strip()
    if not line or "\"k\":\"query-end\"" not in line: continue
    try: e=json.loads(line)
    except: continue
    v=e["v"]
    if v.get("statement")!="SELECT": continue
    qt=v.get("query-trunc","")
    if qt.strip().upper()=="SELECT 1": continue
    ex=v.get("execution",{}); pre=v.get("pre-execution",{})
    ends.append({
      "elapsed":v.get("elapsed"),
      "compile":pre.get("compilation-time"),
      "exec":ex.get("elapsed"),
      "rows":ex.get("processed-rows",{}).get("total"),
      "native":ex.get("processed-rows",{}).get("native"),
      "thread_time":ex.get("threads",{}).get("thread-time"),
      "cpu_time":ex.get("threads",{}).get("cpu-time"),
      "q":qt[:55],
    })
print("total SELECT query-end events:", len(ends))
print("%-57s %8s %8s %8s %10s %10s" % ("query","elapsed","exec","compile","threadT","cpuT"))
for e in ends[-43:]:   # last sweep = hot try presumably; just show distribution
    print("%-57s %8.3f %8.3f %8.4f %10.2f %10.2f" % (
      e["q"], e["elapsed"] or 0, e["exec"] or 0, e["compile"] or 0, e["thread_time"] or 0, e["cpu_time"] or 0))
