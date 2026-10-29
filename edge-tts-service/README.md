# Serviço intermediário Edge-TTS da Jornada de Bia

Este serviço recebe texto da aplicação web e devolve áudio MP3 gerado pelo pacote Python `edge-tts`. **Não é uma API oficial da Microsoft**: `edge-tts` utiliza uma interface de serviço online que pode mudar, impor limites ou deixar de funcionar. Não prometa uso ilimitado ou disponibilidade garantida.

## Implantação

Implante esta pasta em um serviço que aceite Docker (ou Python 3.12) e exponha HTTPS. Configure a variável `TTS_ALLOWED_ORIGINS` com a origem exata do site da Jornada, por exemplo `https://SEU-USUARIO.github.io` (substitua pela origem real; não use caminho de repositório). Durante teste controlado pode ser `*`, mas não é recomendado em produção. O serviço não armazena texto/áudio intencionalmente. O provedor de voz recebe o texto enviado para síntese; evite enviar dados pessoais sensíveis.

Depois de implantado, confira `https://SEU-SERVICO/health` e configure no app o endereço base `https://SEU-SERVICO`, sem `/api/tts`. A aplicação chama `POST /api/tts` com JSON `{"text":"Olá, Bia!","voice":"pt-BR-FranciscaNeural","rate":-8,"pitch":0}` e espera `audio/mpeg`.

## Limites de segurança

- Limite de texto: 1.200 caracteres por chamada.
- Somente vozes `pt-BR` compatíveis com o padrão `Neural`.
- Em produção, restrinja CORS a origens confiáveis e adicione rate limiting/autenticação no provedor de hospedagem.
- O CORS não é autenticação; não exponha serviço sem proteção contra abuso.
- Verifique os termos e a disponibilidade do provedor antes de uso público.
