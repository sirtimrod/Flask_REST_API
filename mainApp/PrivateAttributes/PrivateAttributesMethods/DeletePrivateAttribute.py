from flask import abort, jsonify

from mainApp.DataBaseConnection import con


def checkCategoryId(id_category, id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT lc.IdListCategory FROM list_category AS lc ORDER BY lc.IdListCategory ASC')
            res_id_category = [i[0] for i in cur.fetchall()]
            if id_category in filter(lambda t: t == id_category, res_id_category):
                return checkAttributeId(id_category, id_attribute)
            else:
                return abort(404, description='Requested category do not found')
    except Exception as ex:
        print(ex)


def checkAttributeId(id_category, id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute(f'SELECT lpa.IdListPrivateAttribute, lpa.ListCategoryId '
                        f'FROM list_category AS lc '
                        f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                        f'WHERE lpa.ListCategoryId={id_category} AND lpa.idListPrivateAttribute={id_attribute}')
            res_id_attribute = [i[0] for i in cur.fetchall()]
            if id_attribute in filter(lambda t: t == id_attribute, res_id_attribute):
                return getData(id_category, id_attribute)
            else:
                return abort(404, description='Requested attribute do not found')
    except Exception as ex:
        print(ex)


def getData(id_category, id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lpa.RepresentName, tya.TypeAttributes, lc.RepresentName FROM list_category AS lc LEFT '
                f'JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId LEFT JOIN '
                f'table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes LEFT JOIN '
                f'type_attributes AS tya ON taa.IdTypeAttributes=tya.IdTypeAttributes WHERE '
                f'lc.idListCategory={id_category} AND lpa.idListPrivateAttribute={id_attribute}')
            data_list = [j for i in cur.fetchall() for j in i]
    except Exception as ex:
        print(ex)
    return data_list


def deleteOnePrivateAttribute(id_category, id_attribute):
    try:
        Attr_Args = checkCategoryId(id_category, id_attribute)
        return jsonify(addAttributes(Attr_Args)), 204
    except Exception as ex:
        print(ex)


def addAttributes(Attr_Args):
    try:
        with con.cursor() as cur:
            cur.callproc('deletePrivateAttribute', Attr_Args)
            con.commit()
    except Exception as ex:
        print(ex)
