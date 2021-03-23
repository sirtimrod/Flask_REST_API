from flask import jsonify

from mainApp.DataBaseConnection import con


def displayLogsOfSession():
    session_logs = []
    return jsonify({'SessionLogs': getLogsInfo(session_logs)}), 200


def getLogsInfo(session_logs):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT ls.DateTime, u.Login FROM logs_session AS ls LEFT JOIN users AS u ON '
                        'ls.idUser=u.idUser ORDER BY ls.idLogSession ASC ')
            result_1 = [list(i) for i in cur.fetchall()]
            collectList(result_1, session_logs)
    except Exception as ex:
        print(ex)
    return session_logs


def collectList(result_1, session_logs):
    try:
        for first_layer in result_1:
            attributeObject = {'DateTime': str(first_layer[0]), 'User': {'Login': first_layer[1]}}
            session_logs.append(attributeObject)
    except Exception as ex:
        print(ex)
    return session_logs

