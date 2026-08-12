import time
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.muholyshit.com.br/rankings"
TELEGRAM_BOT_TOKEN = "8746531275:AAEDlQeataApZoyLEpCSHWiowdDZrYbBTBs"
TELEGRAM_CHAT_ID = "948668424"

def obter_top_jogadores(limit=10):
    jogadores = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, wait_until="networkidle", timeout=30000)
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        tabela = soup.find("table")
        if tabela:
            linhas = tabela.find_all("tr")[1:]
            for linha in linhas[:limit]:
                colunas = [td.get_text(strip=True) for td in linha.find_all(["td", "th"])]
                if colunas:
                    jogadores.append(" | ".join(colunas))
    except Exception as e:
        print(f"Erro ao buscar ranking: {e}")
        
    return jogadores

def enviar_notificacao_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        print("Enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    horario_atual = time.strftime('%H:%M:%S - %d/%m/%Y')
    top = obter_top_jogadores(limit=10)

    if top:
        texto_ranking = "\n".join(top)
        mensagem = (
            f"🏆 *Ranking Top 10 - MuHolyShit*\n"
            f"🕒 `{horario_atual}`\n\n"
            f"```\n{texto_ranking}\n```"
        )
        enviar_notificacao_telegram(mensagem)
    else:
        print("Não foi possível carregar a tabela de ranking.")
