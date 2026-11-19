import argparse, getpass, sys
from vault import load_vault, save_vault

p = argparse.ArgumentParser(description="Local Password Manager")
sub = p.add_subparsers(dest="cmd", required=True)
a = sub.add_parser("add");    a.add_argument("site"); a.add_argument("username")
g = sub.add_parser("get");    g.add_argument("site")
d = sub.add_parser("delete"); d.add_argument("site")
s = sub.add_parser("search"); s.add_argument("term")
args = p.parse_args()

master = getpass.getpass("Master password: ")
try:
    data = load_vault(master)
except ValueError as e:
    sys.exit(str(e))

if args.cmd == "add":
    data[args.site] = {"username": args.username,
                       "password": getpass.getpass("Password to store: ")}
    save_vault(data, master); print("Saved.")
elif args.cmd == "get":
    print(data.get(args.site, "Not found."))
elif args.cmd == "delete":
    if data.pop(args.site, None):
        save_vault(data, master); print("Deleted.")
    else:
        print("Not found.")
elif args.cmd == "search":
    hits = [k for k in data if args.term.lower() in k.lower()]
    print("\n".join(hits) if hits else "No matches.")
