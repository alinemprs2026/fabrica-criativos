# Fábrica de criativos — instruções para o Claude

A dona (Aline) não programa. Responda sempre em português do Brasil, simples e passo a passo.
Os **criativos** (anúncios em vídeo) são em **espanhol** para o produto 21 Frases Secretas. Depois virá o Código Alfa.

## Objetivo
Toda semana: olhar quais anúncios mais vendem, entender por que funcionam e entregar **variações em vídeo** prontas para revisão, com qualidade alta e custo baixo de HeyGen.

## Onde estão as coisas
- Supabase (o mesmo do painel `deash-track`): `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` no ambiente.
  - Bucket privado `criativos`: `21-frases/campeoes/*.mp4` são os vídeos campeões. Saídas vão em `21-frases/lotes/<AAAA-MM-DD>/`.
- Análise dos campeões: `analise/21-frases/ANALISE.md` e `transcricoes.json`.
- Modelos de formato (layouts do Canva recriados em vídeo): `formatos/`.
- HeyGen: `HEYGEN_API_KEY` no ambiente (créditos de API — economizar).
  - Avatar do 21 Frases: **"Daniel 21 frases secretas"**.
  - Usar **sempre o Avatar IV** (o intermediário). Não usar o Avatar III (qualidade ruim) nem o V ou superiores (caros demais). Se a API não deixar escolher o IV para esse avatar, parar e avisar a Aline antes de gerar.

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
