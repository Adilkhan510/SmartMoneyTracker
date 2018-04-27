from __future__ import print_function
import os,sys,inspect
from flask import render_template, flash
from cassandra.cluster import Cluster
import pandas as pd
from app import app


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir) 

import config

cluster = Cluster(config.Config().cass_cluster_IP)
session = cluster.connect('demo1')

@app.route('/')
@app.route('/index')
def index():
    # print(app.config['cass_cluster_IP'], file=sys.stderr)
    stmt = '''SELECT event_time, ip, visits from visit_rank WHERE type = %s and event_time = \'" + previous_minute + "\''''
#     response = session.execute(stmt, parameters=[metric])
    rows = session.execute("SELECT * FROM optionflowstreaming LIMIT 10")
    total_n = session.execute("SELECT COUNT(*) FROM optionflowstreaming;")

    df = pd.DataFrame(list(session.execute("SELECT * FROM optionflowstreaming LIMIT 10")))


    display_df_html_t = df.to_html(index=True, header=False, justify='left')

    # for row in rows:
    #     flash('You were successfully logged in')
    #     print(type(row), file=sys.stderr)

    
    return render_template('demo.html', count=total_n[0], table=display_df_html_t)
