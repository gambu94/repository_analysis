import os
import sys
sys.path.append('../')
import json
from pathlib import Path

from utils.utils import *

from flask import Flask, render_template, request, jsonify

from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__,None,'../results')

def get_time():
    return 'time.time()'

def read_code(path):
    try :
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except :
        return "File not Found"

def parse_results():
    ret = []
    for user in os.listdir(results_dir) :
        if ( user[0] == '.' ) : continue
        t_user = { 'username' : user, 'repos' : [] }
        user_path = results_dir/user
        repos = []
        for repo in os.listdir(user_path) :
            if ( repo[0] == '.' ) : continue
            if repo == 'skill-analysis' :
                t_user['skill-analysis'] = {}
                p = user_path/'skill-analysis'/'skill-analysis.json'
                relative_path = os.path.relpath(p, '../results/')
                t_user['skill-analysis']['path'] = relative_path
            else:
                t_user['repos'].append(repo)
                t_user[repo] = {}
                for analysis in os.listdir(user_path/repo):
                    if analysis == 'change-coupling' :
                        t_user[repo]['change-coupling'] = {}
                        p = user_path/repo/'change-coupling'/'change-coupling.json'
                        relative_path = os.path.relpath(p, '../results/')
                        t_user[repo]['change-coupling']['path'] = relative_path
                    if analysis == 'hotspot-analysis' :
                        t_user[repo]['hotspot-analysis'] = {}
                        p = user_path/repo/'hotspot-analysis'/'hotspot-analysis.json'
                        relative_path = os.path.relpath(p, '../results/')
                        t_user[repo]['hotspot-analysis']['path'] = relative_path
        ret.append(t_user)
    return ret

@app.route('/')
def hello_world():
    results = parse_results()
    return render_template('index.html', results = results, len=len)

@app.route("/show/<user>/skill")
#@use_args({'path':Arg(type_= str, required=True)})
def show_skill(user):
    result = results_dir/user/SKILL_ANALYSIS/'skill-analysis.json';
    res = read_code(result)
    return render_template('show-skill-analysis.html', res=res)

@app.route("/show/<user>/<repo>/hotspot")
def show_hotspot(user,repo):
    result = results_dir/user/repo/HOTSPOT_ANALYSIS/'hotspot-analysis.json';
    res = read_code(result)
    return render_template('show-hotspot-analysis.html', res=res)

@app.route("/show/<user>/<repo>/change-coupling")
def show_change(user,repo):
    result = results_dir/user/repo/CHANGE_COUPLING/'change-coupling.json';
    res = read_code(result)
    return render_template('show-change-coupling.html', res=res)
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)