import os, sys, json, glob, urllib.request
env = {}
for l in open(sys.argv[1], encoding="utf-8"):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
URL, KEY = env["SUPABASE_URL"].rstrip("/"), env["SUPABASE_SERVICE_ROLE_KEY"]
H = {"Authorization": f"Bearer {KEY}", "apikey": KEY}
def req(metodo, caminho, dados=None, tipo="application/json"):
    r = urllib.request.Request(URL + caminho, data=dados, method=metodo, headers={**H, "Content-Type": tipo})
    try:
        with urllib.request.urlopen(r) as resp: return resp.status, resp.read()[:200]
    except urllib.error.HTTPError as e: return e.code, e.read()[:200]
print("bucket:", req("POST", "/storage/v1/bucket", json.dumps({"id": "criativos", "name": "criativos", "public": False}).encode()))
pasta = sys.argv[2]
for f in sorted(glob.glob(os.path.join(pasta, "*.mp4"))):
    nome = os.path.basename(f)
    if "1794084887525" in nome: continue
    destino = "21-frases/campeoes/" + nome.replace(" ", "-").lower()
    st, _ = req("POST", f"/storage/v1/object/criativos/{destino}", open(f, "rb").read(), "video/mp4")
    if st == 400 or st == 409:
        st, _ = req("PUT", f"/storage/v1/object/criativos/{destino}", open(f, "rb").read(), "video/mp4")
    print(st, destino)
