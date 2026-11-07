# Fábrica de criativos — passo a passo da quarta-feira

Tudo roda na nuvem (ambiente "fabrica"). As chaves são injetadas sozinhas; os scripts não mandam chave.
Os vídeos ficam só em `$FABRICA_WORK` (padrão `/tmp/fabrica`) e no bucket — **nunca no git**.

1. `bash scripts/teste_nuvem.sh` — confere programas, HeyGen e Supabase.
2. Copiar `pipeline/lotes/21-frases-lote-1.json` para um lote novo (ex.: `21-frases-lote-2.json`) e trocar:
   ganchos (`criativos[].gancho.texto`), pares gancho+corpo, formatos e ângulos. Corpos = cortes dos campeões (`corpos`).
   Tipos de gancho: `avatar` (Avatar IV), `whatsapp`, `historico`, `texto` (sem HeyGen pago) e `campeao` (corte de um campeão).
3. Criar o lote no painel (`creative_batches`, status `gerando`, plano em `notes`).
4. `python3 pipeline/etapa_heygen.py audios <lote.json>` — vozes (TTS turbo-free, grátis até 30/11/2026).
5. `python3 pipeline/etapa_heygen.py orcamento <lote.json>` — lista o que vai gerar e os minutos.
   Se passar de 3 min de Avatar IV na semana: abrir `factory_requests` (kind `permissao`) e esperar.
6. `python3 pipeline/etapa_heygen.py avatar <lote.json>` — gera só o que falta (sempre Avatar IV).
7. `python3 pipeline/montar.py <lote.json>` — gancho (HyperFrames, modelos em `formatos/modelos.py`) + corpo (ffmpeg).
8. `python3 pipeline/revisar.py <lote.json>` — folhas de quadros, volume (-14 LUFS), silêncios e transcrição do gancho. Olhar tudo.
9. `python3 pipeline/publicar.py <lote.json> <batch_id> <AAAA-MM-DD> [--descartar 05,09]` — envia, cria `creatives` e fecha o lote (`pronto`).

IDs úteis (21 Frases): avatar "Daniel 21 frases secretas" = grupo `e0fdc9ef8c8b44198ce9742e28310d54` (4 visuais no JSON do lote);
voz clonada do campeão = `0e07ee5d68de482aa44d5095dfa2f900`.
Nunca subir nada no Facebook por esta rotina.
