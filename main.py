name: Monitor Ranking MuHolyShit

on:
  schedule:
    - cron: '*/15 * * * *'  # Executa a cada 15 minutos
  workflow_dispatch:        # Permite rodar manualmente para testar

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar código
        uses: actions/checkout@v3

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Instalar dependências
        run: pip install requests beautifulsoup4

      - name: Executar Robô
        run: python main.py
