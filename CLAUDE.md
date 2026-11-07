# Fábrica de criativos — instruções para o Claude

A dona (Aline) não programa. Responda sempre em português do Brasil, simples e passo a passo.
Os **criativos** (anúncios em vídeo) são em **espanhol** para o produto 21 Frases Secretas. Depois virá o Código Alfa.

## Objetivo
Toda semana: olhar quais anúncios mais vendem, entender por que funcionam e entregar **variações em vídeo** prontas para revisão, com qualidade alta e custo baixo de HeyGen.

## Chaves (importante)
Na nuvem, as chaves NÃO estão em variáveis de ambiente: o ambiente "fabrica" injeta sozinho os cabeçalhos
(`X-Api-Key` em api.heygen.com; `Authorization: Bearer` e `apikey` em *.supabase.co). Nos scripts, chame essas
APIs **sem** mandar cabeçalho de autenticação. Só `SUPABASE_URL` vem como variável. Teste geral: `bash scripts/teste_nuvem.sh`.

## Onde estão as coisas
- Supabase (o mesmo do painel `deash-track`): `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` no ambiente.
  - Bucket privado `criativos`: `21-frases/campeoes/*.mp4` são os vídeos campeões. Saídas vão em `21-frases/lotes/<AAAA-MM-DD>/`.
- Análise dos campeões: `analise/21-frases/ANALISE.md` e `transcricoes.json`.
- Modelos de formato (layouts do Canva recriados em vídeo): `formatos/`.
- HeyGen: `HEYGEN_API_KEY` no ambiente (créditos de API — economizar).
  - Avatar do 21 Frases: **"Daniel 21 frases secretas"**.
  - Usar **sempre o Avatar IV** (o intermediário). Não usar o Avatar III (qualidade ruim) nem o V ou superiores (caros demais). Se a API não deixar escolher o IV para esse avatar, parar e avisar a Aline antes de gerar.

## Rotina semanal (toda quarta-feira)
Produtos: **21 Frases Secretas** (espanhol) e **Código Alfa** (campeões numa pasta que a Aline vai separar; quando chegarem, ficam em `criativos/codigo-alfa/campeoes/`).
Para cada produto, por semana: **mínimo 15, até 25 criativos**, bem diferentes entre si: **corpos diferentes**, ganchos diferentes e formatos variados. **Qualidade vem antes da quantidade**: se não der 25 bons, entregar menos (nunca menos de 15 sem avisar o motivo).

## Como falar com a Aline (pelo painel, nunca só no chat)
Tabelas no Supabase (REST em `$SUPABASE_URL/rest/v1/...`, cabeçalhos de autenticação são injetados sozinhos):
- `creative_batches` (workspace_id, title, notes, status 'gerando' → 'pronto'): um lote por produto por semana.
- `creatives` (batch_id, workspace_id, title, format, angle, hook, primary_text opcional, storage_path, thumb_path, duration_s): um por vídeo, status 'pendente'. Vídeos em `criativos/<produto>/lotes/<AAAA-MM-DD>/`.
- `factory_requests` (workspace_id, kind 'permissao' ou 'mensagem', title, body): pedir autorização (ex.: gasto extra no HeyGen) ou **avisar qualquer erro** que ela possa resolver. Ler as respostas em `status`/`answer`.
- Áreas: 21 Frases = `2171e39a-2760-4d8e-868e-060cbdf0f8c1`, Código Alfa = `57fbb528-40ce-47ef-8cc3-9c0be86b4ec5`.
- Ao terminar o lote, mudar para `status='pronto'` (o painel mostra e avisa).

## Controle de gastos no HeyGen
- Por produto e por semana, sem pedir: até **3 minutos de Avatar IV** no total (ganchos e trechos curtos).
- Passou disso: abrir um `factory_requests` 'permissao' com a lista do que quer gerar e a estimativa, e esperar.
- Anotar em `notes` do lote quantos minutos de HeyGen foram usados.

## Regras de criação
1. Sempre vídeo, 9:16 (fazer também 4:5 quando pedirem). Legendas grandes com palavra-chave colorida, como os campeões.
2. **Hook rate é prioridade**: muitos ganchos fortes (0–3s) por corpo. Variar formatos (podcast, entrevista de rua, apresentador, tela dividida com cenas de emoção, gancho histórico, conversa de WhatsApp) e ângulos.
3. **Economia de HeyGen**: reaproveitar áudio e imagem dos campeões para criar corpos novos; usar HeyGen só para ganchos novos e trechos curtos. Antes de gastar crédito, listar o que será gerado.
4. Copy direta, provocativa e com urgência, **mas**: nada de números/"estudos"/"cientistas" inventados, nada de avatar fingindo ser cliente real, nada de garantir resultado.
5. Entregar só os melhores: revisar cada vídeo (snapshot) antes de publicar no lote.

## Regras do Facebook (segurança da conta)
- Só a conta de anúncios do 21 Frases. Nunca mexer em campanhas ativas.
- Subir sempre **PAUSADO**, duplicando a campanha/conjunto campeão (mesmo pixel e configuração), com prefixo **[IA]** no nome.
- Nas primeiras semanas, só subir depois que a Aline aprovar no painel.

## Aviso de pronto
Avisar pela aba **Criativos** do painel (tabela de lotes/notificações no Supabase), não por Discord.
