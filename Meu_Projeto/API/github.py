import requests

TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}
with open(fr"Assets/account_github.txt", "r") as file:
    USERNAME = file.read()

def info_perfil():
    r = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HEADERS)
    dados = r.json()
    nome = dados["name"]
    bio= dados["bio"]
    url_perfil= dados["html_url"]
    url_repos = dados["repos_url"]
    seguidores = dados["followers"]
    return f"{nome} tem {seguidores} seguidores\nA bio é <{bio}>\nPerfil: {url_perfil}\nRepos: {url_repos}"

