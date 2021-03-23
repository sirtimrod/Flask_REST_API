from flask import jsonify, abort

from mainApp.DataBaseConnection import con


def displayContainerOfAttributesById(id_container):
    with con.cursor() as cur:
        cur.execute('SELECT taa.idTableAttributes FROM table_attributes AS taa ORDER BY taa.idTableAttributes ASC')
        res_id_container = [i[0] for i in cur.fetchall()]
        if id_container in filter(lambda t: t == id_container, res_id_container):
            return jsonify(getAttributeContainersInfoById(id_container)), 200
        else:
            return abort(404, description='Resource not found')


def getAttributeContainersInfoById(id_container):
    try:
        with con.cursor() as cur:
            cur.execute(f'SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, '
                        f'tya.TypeAttributes FROM table_attributes AS taa LEFT JOIN type_attributes AS tya ON '
                        f'taa.idTypeAttributes=tya.idTypeAttributes WHERE taa.idTableAttributes={id_container}')
            result_1 = [list(i) for i in cur.fetchall()]
    except Exception as ex:
        print(ex)
    return collectDict(result_1)


def collectDict(result_1):
    try:
        container_of_attributes_by_id = {'Id': result_1[0][0], 'Name': result_1[0][1], 'Type': result_1[0][2]}
    except Exception as ex:
        print(ex)
    return container_of_attributes_by_id
