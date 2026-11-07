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

## Código Alfa (regras próprias)
- Espanhol. Oferta: VSL do "millonario secreto" (resumo em `analise/codigo-alfa/VSL.md`). Objetivo do criativo: levar a pessoa a assistir a VSL.
- O avatar que apresenta a VSL (o "millonario secreto") **nunca aparece** nos criativos.
- Avatares: usar os do HeyGen com **"depoimento"** no nome (visuais diferentes). Um deles é **homem**, mas vem com voz de mulher: sempre escolher uma **voz masculina em espanhol** para ele (conferir antes de gerar). Pode criar avatares ou imagens novas, se ajudar.
- "Depoimento" aqui é **formato UGC** (selfie, carro, conversa casual), mas o avatar **não diz que ele mesmo ganhou dinheiro** ("manifesté $8,000"). Ele conta a história/curiosidade em terceira pessoa ("vi un video de un millonario que…", "dicen que…"), reage, provoca, pergunta. Nada de prometer valor de ganho para quem assiste, nem citar universidade/estudo sem prova.
- Ângulo campeão: o gancho do "$8,000 por accidente" + "video extraño". Variar em volta disso (curiosidade, segredo escondido, "deja de rezar", parte adormecida da mente, 3 pasos), sempre sem promessa de renda garantida.

## Rotina semanal (toda quarta-feira)
Produtos: **21 Frases Secretas** (espanhol) e **Código Alfa** (**também em espanhol**; campeões numa pasta que a Aline vai separar; quando chegarem, ficam em `criativos/codigo-alfa/campeoes/`).
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

## ⚠️ VARIAÇÃO DE VERDADE (regra mais importante da Aline)
Não é para fazer só variação de gancho. Cada lote precisa variar **corpo, gancho e principalmente FORMATO**, sempre a partir do que já deu certo (ver ANALISE.md de cada produto):
- **No máximo 1/3 do lote** pode ser "mesmo corpo com gancho novo".
- **Pelo menos 5 formatos diferentes** por lote (ex.: apresentador, UGC selfie/carro, podcast a dois, entrevista de rua, tela dividida com cenas de emoção, pregador/palco, narração com imagens, conversa de WhatsApp, gancho histórico). Priorizar os formatos dos campeões e testar formatos novos próximos deles.
- **Pelo menos 5 corpos diferentes** (roteiros de miolo distintos: ângulo, mecanismo, prova, objeção, história), cada um podendo ter 2–3 ganchos.
- Registrar no `notes` do lote a tabela: criativo → formato · corpo · gancho, para provar a variação.

## Regras de criação
1. Sempre vídeo, 9:16 (fazer também 4:5 quando pedirem). Legendas grandes com palavra-chave colorida, como os campeões.
2. **Hook rate é prioridade**: muitos ganchos fortes (0–3s) por corpo. Variar formatos (podcast, entrevista de rua, apresentador, tela dividida com cenas de emoção, gancho histórico, conversa de WhatsApp) e ângulos.
3. **Economia de HeyGen**: reaproveitar áudio e imagem dos campeões para criar corpos novos; usar HeyGen só para ganchos novos e trechos curtos. Antes de gastar crédito, listar o que será gerado.
4. Copy direta, provocativa e com urgência, **mas**: nada de números/"estudos"/"cientistas" inventados, nada de avatar fingindo ser cliente real, nada de garantir resultado.
5. Entregar só os melhores: revisar cada vídeo (snapshot) antes de publicar no lote.

## Regras do Facebook (segurança da conta)
- Conta 04 (`act_1082802954199978`) para os dois produtos. Modelo de subida = só campanhas **ativas** de teste (CBO, conjuntos cjN com até 3 criativos CRn). A subida é feita pelo painel, nunca pela fábrica.
- Só a conta de anúncios do 21 Frases. Nunca mexer em campanhas ativas.
- Subir sempre **PAUSADO**, duplicando a campanha/conjunto campeão (mesmo pixel e configuração), com prefixo **[IA]** no nome.
- Nas primeiras semanas, só subir depois que a Aline aprovar no painel.

## Aviso de pronto
Avisar pela aba **Criativos** do painel (tabela de lotes/notificações no Supabase), não por Discord.
