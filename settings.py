import os
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
#INTERNAL_IPS = ['127.0.0.1']
BASE_DIR = os.path.join(os.path.dirname(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR,'data','sqlite.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'app',
    'bootstrap3',
    'debug_toolbar'
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

WSGI_APPLICATION = 'wsgi.application'
SECRET_KEY = "wow"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'sh': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

TEMPLATES = [
    {
        # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates')
        ],
        'OPTIONS': {
            'trim_blocks': True
        }
    },
        {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates/html')
        ]
    }
]

# L1CALO specific
CAF_LOCAl = True
CAF_SOURCE = [
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPmtScan/{run_number}",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloEnergyScan/{run_number}",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprDacScanPars/{run_number}",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPedestalRunPars/{run_number}",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPhos4ScanPars/{run_number}",
]

#CAF_OUTPUT = os.path.join(BASE_DIR, 'output')
CAF_OUTPUT = "/afs/cern.ch/user/s/sasham/work/public/caf"
CAF_ATHENA = '20.1.5'
CAF_ASETUP = '20.1.X.Y-VAL,rel_5'

CAF_EOS_PREFIX = 'root://eosatlas'

CAF_ANALYSES = {
    'TileL1CaloRampMaker': {
        'name': 'TileL1CaloRampMaker',
        'template': 'RampMaker',
        'context' : {'doTile': 'True', 'doLAr': 'False'},
        'post_exec': 'RunPlotCalibrationGains',
        'files': [
            {
                'title': 'Gain',
                'name': 'Gains.pdf'
            },
            {
                'title': 'Ramp',
                'name': 'rampPlots.pdf'
            },
            {
                'title': 'FT',
                'name': 'CalibrationTimingPlots.pdf'
            },
            {
                'title': 'Bad',
                'name': 'bad_gains.txt'
            },
            {
                'title': 'Drift',
                'name': 'drifted_towers.txt'
            }
        ]
    },
    'LArRampMaker': {
        'name': 'LArRampMaker',
        'template': 'RampMaker',
        'context' : {'doTile': 'False', 'doLAr': 'True'},
        'post_exec': 'RunPlotCalibrationGains'
    }
    
}
CAF_SCANS = {
    "coolpath": "/TDAQ/RunCtrl",
    "cooltlbpath": "/TRIGGER/LUMI",
    "cooll1calopath": "/TRIGGER/L1Calo/V1/Conditions",
    "coolstrategypath": "/TRIGGER/Receivers/Conditions",
    "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
    "trigdbname": "COOLONL_TRIGGER/CONDBR2",
    "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
    "scans":
        [
          {
            "name": "LArEnergyScan",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "LarCalibL1Calo",
            "tag": "",
            "detstatus": "",
            "detstatustag": "HEAD",
            "daqpartition": [
            "L1CaloCombined",
            "LArgL1CaloCombined"
            ],
            "tierzerotag": "L1CaloEnergyScan",
            "NOTtierzerotag": [],
            "gainstrategy": [
              "GainOneOvEmecFcalLowEta",
              "GainOneOvEmbFcalHighEta"
            ],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": False,
            "minevents": 1700,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          },
          {
            "name": "LArEnergyScanHV",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "LarCalibL1Calo",
            "tag": "",
            "detstatus": "",
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloCombined",
              "LArgL1CaloCombined"
            ],
            "tierzerotag": "",
            "NOTtierzerotag": [],
            "gainstrategy": [
              "CalibGainsEt"
            ],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": False,
            "minevents": 1700,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          },
          {
            "name": "TileEnergyScan",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "cismono",
            "tag": "",
            "detstatus": 2,
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloCombined",
              "TileL1CaloCombined"
            ],
            "tierzerotag": "L1CaloEnergyScan",
            "NOTtierzerotag": [],
            "gainstrategy": [],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": True,
            "minevents": 1700,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          },
          {
            "name": "L1CaloPhos4Scan",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "",
            "tag": "",
            "detstatus": 2,
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloCombined",
              "LArgL1CaloCombined",
              "TileL1CaloCombined"
            ],
            "tierzerotag": "L1CaloPprPhos4ScanPars",
            "NOTtierzerotag": [],
            "gainstrategy": [],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": True,
            "minevents": 0,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          },
          {
            "name": "LArCailbL1Calo",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "LarCalibL1Calo",
            "tag": "",
            "detstatus": 2,
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloCombined",
              "LArgL1CaloCombined"
            ],
            "tierzerotag": "",
            "NOTtierzerotag": [
              "L1CaloEnergyScan",
              "L1CaloPprPhos4ScanPars"
            ],
            "gainstrategy": [],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": False,
            "minevents": 0,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          },
          {
            "name": "TileCalibL1Calo",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "cismono",
            "tag": "",
            "detstatus": 2,
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloCombined",
              "TileL1CaloCombined"
            ],
            "tierzerotag": "",
            "NOTtierzerotag": [],
            "gainstrategy": [],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": True,
            "minevents": 0,
            "initialrun": 266242,
            "fileslocations": [
              "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPmtScan/{run_number}",
              "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloEnergyScan/{run_number}"
            ],
            "analyses": ["TileL1CaloRampMaker"]
          },
          {
            "name": "L1CaloStandalone",
            "tdaqdbname": "COOLONL_TDAQ/CONDBR2",
            "trigdbname": "COOLONL_TRIGGER/CONDBR2",
            "statusdbname": "COOLOFL_GLOBAL/CONDBR2",
            "loglevel": 0,
            "oracle": False,
            "reconly": True,
            "detmask": 0,
            "runtype": "Physics",
            "tag": "",
            "detstatus": 2,
            "detstatustag": "HEAD",
            "daqpartition": [
              "L1CaloStandalone",
              "L1CaloCalibration"
            ],
            "tierzerotag": "",
            "NOTtierzerotag": [],
            "gainstrategy": [],
            "format": "acertd",
            "reverse": False,
            "stoptimestamp": True,
            "cleanstop": True,
            "hasevents": True,
            "minevents": 0,
            "initialrun": 266242,
            "fileslocations": [
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#",
              "/castor/cern.ch/grid/atlas/DAQ/l1calo"
            ]
          }
        ]
}
