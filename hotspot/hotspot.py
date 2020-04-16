#!/usr/bin/env python
import sys
sys.path.append("..")
import git
import os
import time
import collections
from pathlib import Path

from pydriller import RepositoryMining

from utils.utils import *

def analyze_repo(repo) :

    path = repo.path
    path = path.absolute().as_posix()

    counts = collections.defaultdict(int)
    nloc = collections.defaultdict(int)
    cyclomatic = collections.defaultdict(int)

    for commit in RepositoryMining(path).traverse_commits() :
        for mod in commit.modifications :
            # nel caso in cui un file cambia path
            # sommiamo i commit precedenti e
            # rimuoviamo le entry col vecchio path
            if mod.old_path != mod.new_path :
                print(mod.old_path, mod.new_path)
                if mod.new_path == None :
                    counts.pop(mod.old_path)
                    nloc.pop(mod.old_path)
                    cyclomatic.pop(mod.old_path)
                else :
                    counts[mod.new_path] = 1
                    nloc[mod.new_path] = mod.nloc or 0
                    cyclomatic[mod.new_path] = mod.complexity or 0
                # old_path = None -> file inserito per la prima volta
                # new_path = None -> file cancellato
                #       questo crea elementi con chiave None
                #       che cancelliamo alla fine
            else :
                counts[mod.new_path] += 1
                nloc[mod.new_path] = mod.nloc or 0
                cyclomatic[mod.new_path] = mod.complexity or 0

    # print('stop repo analysis, {} sec. elapsed'.format(end-start))
    return counts, nloc, cyclomatic

def main(user,repo_name):
    start = time.time()

    repo = clone_repo(user, repo_name)
    if repo is None:
        return []

    commit_count, files_nloc_count, files_cyclomatic_count = analyze_repo(repo)

    path = repo.path
    clean_tmp_dir(path)

    #visual(commit_count, files_nloc_count, files_cyclomatic_count)

    end = time.time()
    time_elapsed = end - start

    ret = [
            {'filename': key,
            'commit_count' : commit_count[key],
            'files_nloc_count' : files_nloc_count[key],
            'files_cyclomatic_count' : files_cyclomatic_count[key]
            } for key in commit_count.keys()
        ]
    data = json.dumps(ret)
    save_result(data, HOTSPOT_ANALYSIS, user, repo_name)
    return ret

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
