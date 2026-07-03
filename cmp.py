import json, sys
sysdir = sys.argv[1]
new = json.load(open(sysdir+"/results/20260626/c7a.metal-48xl.json"))["result"]
old = json.load(open(sysdir+"/results/20260511/c7a.metal-48xl.json"))["result"]
hdr = "%3s %9s %9s %8s %8s  flag" % ("Q","new_cold","old_cold","new_hot","old_hot")
print(hdr)
for i,(n,o) in enumerate(zip(new,old),1):
    nh=min(n[1:]); oh=min(o[1:])
    flag=""
    if nh>oh*1.3 and nh-oh>0.05: flag+="HOT_SLOWER "
    if oh>nh*1.3 and oh-nh>0.05: flag+="hot_faster "
    if n[0]>o[0]*1.5 and n[0]-o[0]>0.5: flag+="COLD_SLOWER"
    print("%3d %9.3f %9.3f %8.3f %8.3f  %s" % (i,n[0],o[0],nh,oh,flag))
print()
print("sum new hot-min: %.3f   sum old hot-min: %.3f" % (sum(min(r[1:]) for r in new), sum(min(r[1:]) for r in old)))
print("sum new cold   : %.3f   sum old cold   : %.3f" % (sum(r[0] for r in new), sum(r[0] for r in old)))
