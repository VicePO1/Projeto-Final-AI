import requests

TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}

def info_perfil():
    with open(fr"Assets/account_github.txt", "r") as file:
        USERNAME = file.read()

    r = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HEADERS)
    if r.status_code==200:
        dados = r.json()
        nome = dados["name"]
        bio = dados["bio"]
        url_perfil = dados["html_url"]
        url_repos = dados["repos_url"]
        seguidores = dados["followers"]
        return f"{nome} tem {seguidores} seguidores\nA bio é <{bio}>\nPerfil: {url_perfil}\nRepos: {url_repos}"
    elif r.status_code == 404:
        return "User not found"
    else:
        return "Erro desconhecido"