import csv, json, os, sys, collections

def parse_results(csv_path):
    by_q = collections.defaultdict(dict)
    with open(csv_path) as f:
        for row in csv.reader(f):
            if not row or len(row) < 3:
                continue
            q, t, sec = int(row[0]), int(row[1]), float(row[2])
            by_q[q][t] = sec
    out = []
    for q in sorted(by_q):
        tries = by_q[q]
        out.append([tries[t] for t in sorted(tries)])
    return out

def build(system_dir, date_iso, machine, load_time, data_size):
    with open(os.path.join(system_dir, "template.json")) as f:
        tmpl = json.load(f)
    result = parse_results(os.path.join(system_dir, "result.csv"))
    doc = collections.OrderedDict()
    doc["system"] = tmpl["system"]
    doc["date"] = date_iso
    doc["machine"] = machine
    doc["cluster_size"] = 1
    doc["proprietary"] = tmpl["proprietary"]
    doc["hardware"] = tmpl["hardware"]
    doc["tuned"] = tmpl["tuned"]
    doc["tags"] = tmpl["tags"]
    doc["load_time"] = load_time
    doc["data_size"] = data_size
    doc["concurrent_qps"] = None
    doc["concurrent_error_ratio"] = None
    doc["result"] = result
    date_dir = date_iso.replace("-", "")
    outdir = os.path.join(system_dir, "results", date_dir)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, machine + ".json")
    # Pretty-print with result rows one-per-line to match repo style.
    head = {k: doc[k] for k in doc if k != "result"}
    lines = []
    lines.append("{")
    body = []
    for k in head:
        body.append("    " + json.dumps(k) + ": " + json.dumps(head[k]))
    rows = ",\n".join("        " + json.dumps(r) for r in result)
    body.append("    \"result\": [\n" + rows + "\n]")
    lines.append(",\n".join(body))
    lines.append("}")
    with open(outpath, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", outpath, "(%d queries)" % len(result))
    return outpath

if __name__ == "__main__":
    base = os.path.expanduser("~/repos/ClickBench_csauer")
    DATE = "2026-06-26"
    MACHINE = "c7a.metal-48xl"
    build(os.path.join(base, "hyper"), DATE, MACHINE, 466, 18959040512)
    build(os.path.join(base, "hyper-parquet"), DATE, MACHINE, 0.227, 14737666736)
