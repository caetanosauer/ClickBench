import csv, collections
def load(path):
    byq=collections.defaultdict(dict)
    for row in csv.reader(open(path)):
        if len(row)<3: continue
        byq[int(row[0])][int(row[1])]=float(row[2])
    return [[byq[q][t] for t in sorted(byq[q])] for q in sorted(byq)]
new=load("hyper-parquet/result.csv")
import json
old=json.load(open("hyper-parquet/results/20260626/c7a.metal-48xl.json"))["result"]
print("%3s %9s %9s %8s %8s" % ("Q","new_cold","old_cold","new_hot","old_hot"))
for i,(n,o) in enumerate(zip(new,old),1):
    print("%3d %9.3f %9.3f %8.3f %8.3f" % (i,n[0],o[0],min(n[1:]),min(o[1:])))
print()
print("NEW  hot-sum=%.2f  cold-sum=%.2f" % (sum(min(r[1:]) for r in new), sum(r[0] for r in new)))
print("PREV hot-sum=%.2f  cold-sum=%.2f" % (sum(min(r[1:]) for r in old), sum(r[0] for r in old)))
