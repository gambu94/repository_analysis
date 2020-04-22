#!/usr/bin/env python

import logging
import sys
sys.path.append("..")
import git
import collections
import os
import itertools
import networkx as nx
from utils.utils import *


def mine_repo(repo):
    commits = collections.defaultdict(set)
    path = repo.path

    for subdir, dirs, files in os.walk(path):
        # rimuoviamo la cartella .git per motivi di efficienza
        if '.git' in dirs :
            dirs.remove('.git')
        for filename in files:
            # evitiamo di processare files non di testo
            if not check_file_extension(filename):
                continue
            # creo path relativo del file
            relpath = os.path.relpath(os.path.join(subdir, filename), path)
            for entry in repo.repo.blame_incremental("HEAD", relpath):
                commits[entry.commit.hexsha].add(filename)
    return commits


def cc_graph(commits):
    G = nx.Graph()
    for commit in commits.values():
        print('commit',commit)
        # per ogni file del commit
        for file in commit :
            # se non esiste un node lo creo
            if not G.has_node(file) :
                G.add_node(file)
        # per ogni coppia di file aggiungiamo
        # il peso nel relativo arco
        for a, b in itertools.combinations(commit, 2):
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)
    return G


def main(user, repo_name):
    repo = clone_repo(user,repo_name)
    if repo is None:
        return { 'error' : 'Repo not found' }

    commits = mine_repo(repo)
    G = cc_graph(commits)

    graph = nx.readwrite.json_graph.jit_data(G)

    path = repo.path
    clean_tmp_dir(path)
    save_result(graph, CHANGE_COUPLING, user, repo_name)
    return graph


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] )