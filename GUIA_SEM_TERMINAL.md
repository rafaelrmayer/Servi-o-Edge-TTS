# Como publicar apenas o serviço Edge-TTS (sem terminal)

Este pacote contém SOMENTE o serviço intermediário de voz, não contém o aplicativo Jornada de Bia.

## 1. Criar repositório separado no GitHub
1. Abra https://github.com/new no navegador e entre na sua conta.
2. Nome sugerido: `jornada-bia-edge-tts`.
3. Recomendo **Private** enquanto estamos testando.
4. Clique em Create repository. Não marque para adicionar README, pois o pacote já contém arquivos.
5. Na página do repositório, escolha **Add file → Upload files**.
6. Extraia este ZIP e envie os quatro arquivos da pasta `edge-tts-service` para a raiz do repositório (README.md, Dockerfile, requirements.txt e main.py).
7. Clique em Commit changes.

## 2. Hospedar no Render
1. Abra https://render.com/ e conecte o GitHub.
2. Crie um serviço do tipo **Web Service** a partir do repositório `jornada-bia-edge-tts`.
3. Selecione o ambiente Docker; o Dockerfile está incluído.
4. Durante o teste, configure a variável `TTS_ALLOWED_ORIGINS` com a origem exata da Jornada. Não use `*` em produção.
5. Inicie o deploy e espere o status ficar Live.
6. Teste `https://SEU-SERVICO/health`; deve retornar JSON com status `ok`.

## Atenção
- Não inclua o ZIP completo da Jornada neste repositório.
- Este serviço usa `edge-tts`, uma interface não oficial; disponibilidade e limites podem mudar.
- O texto enviado para síntese é processado por um serviço de voz online; evite dados pessoais sensíveis.
- CORS não protege contra abuso. Antes de uso público, precisamos adicionar autenticação/limites e definir a origem correta.
- A aplicação não poderá usar o Edge-TTS até que o serviço seja implantado e o URL HTTPS seja configurado no app.
