import logging, requests, requests_toolbelt.adapters.appengine

from flask import Flask, render_template, request, jsonify
from google.appengine.ext import ndb
from google.appengine.api import memcache, namespace_manager, modules, app_identity


application = Flask(__name__)
main_srv='default'
project_name=app_identity.app_identity.get_default_version_hostname()

@application.route('/')
def dashboard():
   #Changing to use modules API
   requests_toolbelt.adapters.appengine.monkeypatch()
   name_v1=modules.modules.get_versions('default')[0]
   name_v2=modules.modules.get_versions('default')[1]
   
   url_stats_1='http://'+name_v1+'-dot-'+main_srv+'-dot-'+project_name+'/stats/v1'
   url_stats_2='http://'+name_v2+'-dot-'+main_srv+'-dot-'+project_name+'/stats/v1'
   
   stats_1=requests.get(url_stats_1)
   stats_2=requests.get(url_stats_2)
   
   likes1=stats_1.json()['likes']
   views1=stats_1.json()['views']
   likes2=stats_2.json()['likes']
   views2=stats_2.json()['views']
   
   return render_template('dashboard.html',v=[round(likes1/views1,3),round(likes2/views2,3),views1,likes1,views2,likes2,'v1','v2'])

@application.route('/raw')
def raw():
  def_srv_versions=modules.modules.get_versions('default')
  return jsonify({"versions":def_srv_versions})
