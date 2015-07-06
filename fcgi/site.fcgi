#!/afs/cern.ch/user/a/amazurov/www/caf/venv/bin/python
import sys, os
sys.path.insert(0,'/afs/cern.ch/sw/lcg/releases/Python/2.7.9-bb158/x86_64-slc6-gcc48-opt/lib')
sys.path.insert(0, "/afs/cern.ch/user/a/amazurov/www/caf")

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
