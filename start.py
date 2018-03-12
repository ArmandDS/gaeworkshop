import logging, requests, requests_toolbelt.adapters.appengine

from flask import Flask, render_template, request, jsonify
from google.appengine.ext import ndb
from google.appengine.api import memcache, namespace_manager


application = Flask(__name__)

@application.route('/')
def dashboard():
   requests_toolbelt.adapters.appengine.monkeypatch()
   stats_1=requests.get('http://1-dot-workshop-23.appspot.com/stats/v1')
   stats_2=requests.get('http://2-dot-workshop-23.appspot.com/stats/v1')
   
   likes1=stats_1.json()['likes']
   views1=stats_1.json()['views']
   likes2=stats_2.json()['likes']
   views2=stats_2.json()['views']
   
   return render_template('dashboard.html',v=[round(likes1/views1,3),round(likes2/views2,3),views1,likes1,views2,likes2,'v1','v2'])

@application.route('/raw')
def raw():
  def_srv_versions=modules.get_versions(module='default')
  return {'versions:'+str(def_srv_versions)}
