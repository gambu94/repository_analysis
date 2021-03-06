import os
import requests
import json
from pathlib import Path
from git import Repo, RemoteProgress
from pydriller import GitRepository
from github import Github


# path file temporanei e risultati
tmp_dir = Path('../tmp/')
results_dir = Path('../results/')

# credenziali account gitHub dedicato
credential = {
    'user': 'gastige',
    'password': 'Sistemi.Distribuiti.2'}

CHANGE_COUPLING = 'change-coupling'
HOTSPOT_ANALYSIS = 'hotspot-analysis'
SKILL_ANALYSIS = 'skill-analysis'

# set di linguaggi di programmazione
ENDINGS = ['4th', 'forth', 'fr', 'frt', 'fth', 'f83', 'fb', 'fpm', 'e4', 'rx', 'ft', 'ada', 'adb', 'ads', 'pad', 'agda',
           'as', 'awk', 'bat', 'btm', 'cmd', 'c', 'ec', 'pgc', 'cc', 'cpp', 'cxx', 'c++', 'pcc', 'cfc', 'coffee', 'cs',
           'csh', 'css', 'cu', 'cuh', 'd', 'dart', 'dts', 'dtsi', 'el', 'lisp', 'lsp', 'scm', 'ss', 'rkt', 'erl', 'hrl',
           'fs', 'fsx', 'vert', 'tesc', 'tese', 'geom', 'frag', 'comp', 'go', 'h', 'hh', 'hpp', 'hxx', 'hbs',
           'handlebars', 'hs', 'html', 'idr', 'lidr', 'ini', 'jai', 'java', 'jl', 'js', 'jsx', 'kt', 'kts', 'lds',
           'lean', 'hlean', 'less', 'lua', 'm', 'ml', 'mli', 'nb', 'wl', 'sh', 'asa', 'asp', 'asax', 'ascx', 'asmx',
           'aspx', 'master', 'sitemap', 'webinfo', 'in', 'clj', 'cljs', 'cljc', 'f', 'for', 'ftn', 'f77', 'pfo', 'f03',
           'f08', 'f90', 'f95', 'makefile', 'mk', 'mm', 'nim', 'php', 'pl', 'qcl', 'qml', 'cshtml', 'mustache', 'oz',
           'p', 'pro', 'pas', 'hex', 'ihex', 'json', 'markdown', 'rst', 'text', 'txt', 'polly', 'proto', 'arr',
           'py', 'r', 'rake', 'rb', 'rhtml', 'rs', 's', 'asm', 'sass', 'scss', 'sc', 'scala', 'sls', 'sml', 'sql',
           'styl', 'swift', 'tcl', 'tex', 'sty', 'toml', 'ts', 'tsx', 'thy', 'uc', 'uci', 'upkg', 'v', 'vim', 'xml',
           'yaml', 'yml', 'y', 'zsh']


def get_repo_name_from_url(url: str) -> str:
    # restituisce il nome del repository tramite l'url in input
    # rfind(str) restituisce l'indice di partenza dell'utlima occorrenza di str)
    last_slash_index = url.rfind("/")
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        return ""
    return url[last_slash_index + 1:last_suffix_index]


def clean_tmp_dir(path=None):
    # elimina tutti i file all'interno del path passato in input (default = tmp )
    import shutil
    if path == None:
        path = tmp_dir
    shutil.rmtree(path, ignore_errors=True)


def read_code(path):
    # ritorna l'intero contenuto del file in cui è presente il codice sorgente
    try:
        with open(path) as f:
            return f.read()
    except:
        return ""


class Progress(RemoteProgress):
    # viene stampato l'avanzamento del download dei risultati
    def update(self, op_code, cur_count, max_count=None, message=''):
        percentage = cur_count * 100 / max_count
        print("Downloading: (==== {:03.2f} % ====)".format(
            percentage), end='\r')


def clone_repo(user, repo_name):
    # viene copiato il repository nel path locale tmp_dir/repo_name e viene restituita in output
    try:
        url = "https://{}:{}@github.com/{}/{}".format(
            'gastige', 'Sistemi.Distribuiti.2', user, repo_name)
        print("git clone {}".format(url))
        repo_name = get_repo_name_from_url(url)
        path = tmp_dir/repo_name
        if os.path.exists(path):
            clean_tmp_dir(path)
        Repo.clone_from(url, path, progress=Progress())
        print("\nRepository {} clonata.".format(repo_name))
        return GitRepository(path)
    except:
        return None


def clone_user_repos(user):
    # clona tutte le repositories di un utente
    names = get_user_repos_name(user)
    ret = []
    for name in names:
        repo = clone_repo(user, name)
        ret.append(repo)
    return ret


def check_file_extension(filename, endings=ENDINGS):
    # restituisce true se l'estensione del file è presente nella lista ENDINGS sopra definita, false altrimenti
    ext = os.path.splitext(filename)[1][1:]
    return True if (ext in endings) else False


def check_repo_languages(url, languages=['java']):
    # con requests.get(url) viene inviata una richiesta http all url,le API di github restituiranno i dati dei
    # linguaggi utilizzati in formato json, verrà restituita una lista di linguaggi utilizzati
    req = requests.get(url)
    data = req.json()
    ret = []
    for f in data:
        ret.append(f)
    return ret


def get_user_repos_name(user):
    # Utilizzando le api di gitHub riusciamo ad ottenere informazioni come nome e cognome
    # del proprietario del repository, il linguaggio utilizzato etc.
    url = "https://api.github.com/users/{}/repos".format(user)
    req = requests.get(url)
    data = req.json()
    ret = []
    if 'message' in data:
        if data['message'].find('Not Found') >= 0:
            print("Utente non trovato")
        elif data['message'].find('rate limit') >= 0:
            print("Hai raggiunto il limite di utilizzo delle API github.com")
        return ret
    else:
        for f in data:
            if 'name' in f:
                name = f['name']
                print("Repository: {}...".format(name))
            if 'languages_url' in f:
                lang_url = f['languages_url']
                languages = check_repo_languages(lang_url)
                if 'Java' not in languages:
                    print('Non è presente codice java in questa repo: {}.'.format(name))
                elif 'html_url' in f:
                    ret.append(f['name'])
        return ret


def get_name_from_user(user):
    # In particolare il nome e cognome servirà ad individuare gli import inseriti dal proprietrario
    # per effetuare la skill analysis 
    url = "https://api.github.com/users/{}".format(user)
    req = requests.get(url)
    data = req.json()
    ret = None
    if 'message' in data:
        if data['message'].find('Not Found') >= 0:
            print("Utente non trovato")
            ret['err'] = "Utente non trovato"
        elif data['message'].find('rate limit') >= 0:
            print("Hai raggiunto il limite di utilizzo delle API github.com")
            ret['err'] = "Github API limit."
        return ret
    else:
        if 'name' in data:
            name = data['name']
        if 'login' in data:
            username = data['login']
        return name


def save_result(data, service, user, repo=None):
    # Salviamo i risultati nella cartella locale secondo il seguente path in base al servizio
    # result_dir/user/SKILL_ANALYSIS,
    # result_dir/user/CHANGE_COUPLING,
    # result_dir/user/HOTSPOT_ANALYSIS
    path = results_dir/user
    if repo is not None:
        path = path/repo
    path = path/service
    filename = service+".json"
    path = path/filename
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as outfile:
        outfile.write(data)
    return





if __name__ == "__main__":
    # check_repo_languages('https://api.github.com/repos/gambu94/giuse-py/languages')
    m = "org.openide.util.NbBundle"
    # get_name_from_user("andrea993")
    #print( m.rsplit('.',1)[0] )
    # clone_repo('https://github.com/giuse/ciao')
