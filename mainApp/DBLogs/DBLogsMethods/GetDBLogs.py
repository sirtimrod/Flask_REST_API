from flask import jsonify

from mainApp.DataBaseConnection import con


def displayDBLogs():
    db_logs = []
    return jsonify({'Logs': getLogsInfo(db_logs)}), 200


def getLogsInfo(db_logs):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT l.DateTime, tyq.TypeQuery, l.Element, lc.RepresentName, l.Description, u.Login '
                        'FROM logs AS l LEFT JOIN type_query AS tyq ON l.idTypeQuery=tyq.idTypeQuery '
                        'LEFT JOIN list_category AS lc ON l.idListCategory=lc.idListCategory '
                        'LEFT JOIN users AS u ON l.idUser=u.idUser ORDER BY l.idLog ASC ')
            result_1 = [list(i) for i in cur.fetchall()]
            collectList(result_1, db_logs)
    except Exception as ex:
        print(ex)
    return db_logs


def collectList(result_1, db_logs):
    try:
        for first_layer in result_1:
            attributeObject = {'DateTime': str(first_layer[0]), 'TypeQuery': first_layer[1],
                               'Element': first_layer[2], 'Category': first_layer[3],
                               'Description': first_layer[4], 'User': {'Login': first_layer[5]}}
            db_logs.append(attributeObject)
    except Exception as ex:
        print(ex)
    return db_logs

