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

def template_analysis(repo) :

    path = repo.path
    path = path.absolute().as_posix()

    ########################
    #
    # do your analysis here
    #
    ########################

    result = []
    return results

def main(user,repo_name):
    start = time.time()

    repo = clone_repo(user, repo_name)
    if repo is None:
        return []

    ret = template_analysis(repo)

    path = repo.path
    clean_tmp_dir(path)

    end = time.time()
    time_elapsed = end - start

    data = json.dumps(ret)
    save_result(data, HOTSPOT_ANALYSIS, user, repo_name)
    return ret

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
