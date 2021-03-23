from mainApp import app

# Initialization files with business-logic
from .DBLogsMethods.GetLogsOfSession import displayLogsOfSession
from .DBLogsMethods.GetDBLogs import displayDBLogs


# This route returns logs of session
@app.route('/api/session_logs', methods=['GET'])
def getLogsOfSession():
    return displayLogsOfSession()


# This route returns DB logs
@app.route('/api/logs', methods=['GET'])
def getDBLogs():
    return displayDBLogs()
