import javalang

import sys
sys.path.append("..")
import collections
import operator
from pathlib import Path
import git

from utils.utils import *


def parse_line(line) :
    imports = collections.defaultdict(int)
    try :
        tree = javalang.parse.parse(line)
        for lib in tree.imports :
            if not lib.wildcard :
                path = lib.path.rsplit('.',1)[0]
            else :
                path = lib.path
            imports[path] += 1
    except :
        print("ERRORE durante il PARSING della classe java.")
    return imports

def parse_code(code) :
    imports = collections.defaultdict(int)
    for line in code:
        temp = parse_line(line)
        for key in temp.keys():
            imports[key] += temp[key]
    return imports

def repo_skill_analysis(repo, name, ext = 'java'):
    print("Lavoro sulla repo: {}".format(repo.project_name))
    path = repo.path
    imports = collections.defaultdict(int)

    if ext == 'java' :
        for subdir, dirs, files in os.walk(path):
            # rimuoviamo la cartella .git per motivi di efficienza
            if '.git' in dirs :
                dirs.remove('.git')
            for filename in files:
                # evitiamo di processare files non di testo
                if not check_file_extension(filename, [ext]):
                    continue
                # creo path relativo del file
                relpath = os.path.relpath(os.path.join(subdir, filename), path)
                file_imports = []
                for entry in repo.repo.blame("HEAD", relpath):
                    commit_code = entry[0]
                    commit = repo.get_commit(commit_code)
                    for line in entry[1] :
                        if line.find("import") >= 0 :
                            if commit.author.name == name :
                                file_imports.append(line)
                temp = parse_code(file_imports)
                for key in temp.keys():
                    imports[key] += temp[key]
        return imports


def main(user, packages=['java.util','java.io']):

    name = get_name_from_user(user)
    if 'err' in name:
        return json.dumps([{ 'error' : 'Errore nome non trovato o limite utilizzo API.'}])

    repos = clone_user_repos(user)

    imports = collections.defaultdict(int)

    #user = 'gambu94'
    #repos = [clone_repo("https://github.com/gambu94/my-java-test")]
    
    for repo in repos:
        path = repo.path
        temp_imports = repo_skill_analysis(repo, name)
        for key in temp_imports.keys():
            imports[key] += temp_imports[key]
        clean_tmp_dir(path)

    # ordino il dizionario per valore
    imports_s = {k: v for k, v in sorted(imports.items(), key= lambda item: item[1], reverse=True)}

    # filtro la lista dei package
    #packages = ['java.util','java.io','com.me.giuse','alessandro']
    for p in packages :
        imports_s.pop(p,'')

    #print("Skill-Analysis user: {}.".format(user))
    for key in imports_s.keys():
        print(key, imports_s[key])

    ret = [
            {'package': key,
            'count' : imports_s[key]
            } for key in imports_s.keys()
        ]
    data = json.dumps(ret)
    save_result(data, SKILL_ANALYSIS, user)
    return ret

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
