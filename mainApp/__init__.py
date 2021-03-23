from flask import Flask

# Initialization the app application
app = Flask(__name__)

# That setting don't allows JSON displaying by the alphabet
app.config['JSON_SORT_KEYS'] = False

# Initialization main files of project
from .Categories.CategoriesAPI import *
from .PrivateAttributes.PrivateAttributesAPI import *
from .CommonAttributes.CommonAttributesAPI import *
from .ContainersOfAttributes.ContainersOfAttributesAPI import *
from .DBLogs.DBLogsAPI import *

from .Errors import *
