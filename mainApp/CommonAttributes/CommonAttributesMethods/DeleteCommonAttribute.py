from flask import abort, jsonify

from mainApp.DataBaseConnection import con


def checkCommonAttributeId(id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT lca.idListCommonAttribute FROM list_common_attribute AS lca '
                        'ORDER BY lca.idListCommonAttribute ASC')
            res_id_attribute = [i[0] for i in cur.fetchall()]
            if id_attribute in filter(lambda t: t == id_attribute, res_id_attribute):
                return getAttributeInfo(id_attribute)
            else:
                return abort(404, description='Resource not found')
    except Exception as ex:
        print(ex)


def getAttributeInfo(id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute(f'SELECT lca.RepresentName, tya.TypeAttributes FROM list_common_attribute AS lca '
                        f'LEFT JOIN table_attributes AS taa ON lca.idTableAttributes=taa.idTableAttributes '
                        f'LEFT JOIN type_attributes AS tya ON taa.idTypeAttributes=tya.idTypeAttributes '
                        f'WHERE lca.idListCommonAttribute={id_attribute}')
            Attr_Args = [j for i in cur.fetchall() for j in i]
    except Exception as ex:
        print(ex)
    return Attr_Args


def deleteCommonAttribute(id_attribute):
    try:
        Attr_Args = checkCommonAttributeId(id_attribute)
        return jsonify(deleteAttributes(Attr_Args)), 204
    except Exception as ex:
        print(ex)


def deleteAttributes(Attr_Args):
    try:
        with con.cursor() as cur:
            cur.callproc('deleteCommonAttribute', Attr_Args)
            con.commit()
    except Exception as ex:
        print(ex)
