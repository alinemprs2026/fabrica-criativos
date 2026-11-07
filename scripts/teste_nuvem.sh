#!/usr/bin/env bash
# Teste da nuvem: confere programas, HeyGen, Supabase e uma renderização curta.
# As chaves NÃO ficam no ambiente: o Claude Code na nuvem injeta os cabeçalhos
# (X-Api-Key no api.heygen.com; Authorization + apikey no *.supabase.co).
set -u
ok() { echo "✅ $1"; }
falha() { echo "❌ $1"; }

echo "== Programas =="
command -v ffmpeg >/dev/null && ok "ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)" || falha "ffmpeg não instalado"
command -v node >/dev/null && ok "node $(node -v)" || falha "node não instalado"
[ -x /usr/bin/google-chrome ] && ok "Chrome encontrado" || echo "⚠️ Chrome não está em /usr/bin/google-chrome"
npx -y hyperframes --version >/dev/null 2>&1 && ok "hyperframes $(npx -y hyperframes --version 2>/dev/null | tail -1)" || falha "hyperframes não roda"

echo "== HeyGen =="
code=$(curl -s -o /tmp/heygen.json -w "%{http_code}" https://api.heygen.com/v2/avatars)
if [ "$code" = "200" ]; then
  ok "HeyGen respondeu (chave funcionando)"
  python3 - <<'EOF'
import json
d = json.load(open("/tmp/heygen.json")).get("data", {})
av = d.get("avatars", []) + d.get("talking_photos", [])
achados = [a for a in av if "daniel" in json.dumps(a).lower()]
print(f"   avatares na conta: {len(av)} · com 'Daniel' no nome: {len(achados)}")
for a in achados[:5]:
    print("   -", a.get("avatar_name") or a.get("talking_photo_name"), "|", a.get("avatar_id") or a.get("talking_photo_id"))
EOF
else
  falha "HeyGen respondeu $code (confira o segredo de rede do api.heygen.com)"
fi

echo "== Supabase =="
if [ -z "${SUPABASE_URL:-}" ]; then
  falha "SUPABASE_URL não está nas variáveis de ambiente"
else
  code=$(curl -s -o /tmp/sb.json -w "%{http_code}" -X POST "$SUPABASE_URL/storage/v1/object/list/criativos" \
    -H "Content-Type: application/json" -d '{"prefix":"21-frases/campeoes/","limit":20}')
  [ "$code" = "200" ] && ok "Supabase: $(python3 -c "import json;print(len(json.load(open('/tmp/sb.json'))))") vídeos campeões encontrados" \
                      || falha "Supabase respondeu $code (confira o segredo de rede do *.supabase.co)"
fi

echo "== Renderização de teste =="
rm -rf /tmp/teste-hf && npx -y hyperframes init /tmp/teste-hf --non-interactive --skip-skills >/dev/null 2>&1
if (cd /tmp/teste-hf && timeout 300 npx -y hyperframes render --quality draft --output /tmp/teste.mp4 >/tmp/render.log 2>&1); then
  ok "Renderizou um vídeo de teste ($(du -h /tmp/teste.mp4 | cut -f1))"
else
  falha "Renderização falhou. Últimas linhas:"; tail -15 /tmp/render.log
fi
