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

## Formatos novos (Lote 2 em diante): criativo inteiro por roteiro de cenas
- Plano: `pipeline/lotes/21-frases-lote-2.json` (cenas com voz grátis, clipes de Avatar IV já pagos, cenas dos campeões e visuais em HTML).
- Visuais prontos em `formatos/cenas.py`: avatar (com zoom & movimento), broll, zap, split (antes/depois), busca, stories, notícia URGENTE,
  notícia absurda + plot twist, CCTV, tela bloqueada, quiz A/B/C, texto + música (mini VSL), cartão de CTA, comentário.
- `python3 pipeline/roteiro.py <lote.json> --vozes` (vozes) → `python3 pipeline/roteiro.py <lote.json> [ids]` (render) → revisar → `publicar.py`.
- Cenas dos campeões: conferir os cortes (o campeão alterna cena em cima/embaixo e tem trocas rápidas; olhar a folha de quadros antes).

## Reeditar um lote já publicado (sem HeyGen novo) — usado no Lote 2 em 08/11/2026
- Plano: `pipeline/lotes/21-frases-lote-2-v2.json` (`corte` = fim do gancho no vídeo atual; `blocos` = corpo novo).
  Cada bloco `partes` = frase + imagem do banco (`b:<n>` = item n de `criativos/banco/indice.json`); a imagem entra na 1ª palavra da frase.
- `python3 pipeline/reeditar.py <plano> --vozes` (vozes grátis + durações e ritmo de cada troca) → `python3 pipeline/reeditar.py <plano> [ids]`.
  Mantém o começo original intacto, monta o corpo (HyperFrames), música baixa (abaixa sob a voz), efeitos nas trocas, -14 LUFS,
  e gera `revisao/<id>.jpg` (um quadro a cada 2 s). Recusa clipe repetido no mesmo vídeo e evita trechos já usados em outro vídeo.
- `python3 pipeline/republicar.py <plano> <batch_id> 21-frases/lotes/<data>-L2v2` atualiza as linhas existentes (não cria lote novo; pula < 60 s).
