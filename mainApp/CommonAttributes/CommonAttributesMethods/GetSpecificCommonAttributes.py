from flask import jsonify, abort

from mainApp.DataBaseConnection import con


def displaySpecificCommonAttribute(id_attribute):
    return jsonify(checkSpecificCommonAttributeId(id_attribute)), 200


def checkSpecificCommonAttributeId(id_attribute):
    with con.cursor() as cur:
        cur.execute('SELECT lca.idListCommonAttribute FROM list_common_attribute AS lca '
                    'ORDER BY lca.idListCommonAttribute ASC')
        res_id_attribute = [i[0] for i in cur.fetchall()]
        if id_attribute in filter(lambda t: t == id_attribute, res_id_attribute):
            return getCommonAttributeInfo(id_attribute)
        else:
            return abort(404, description='Resource not found')


def getCommonAttributeInfo(id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lca.idListCommonAttribute, lca.RepresentName, lca.Description, lca.idTableAttributes '
                f'FROM list_common_attribute AS lca '
                f'WHERE lca.idListCommonAttribute={id_attribute} ')
            result_1 = [list(i) for i in cur.fetchall()]
    except Exception as ex:
        print(ex)
    return getTableAttributeRepresentName(result_1, id_attribute)


def getTableAttributeRepresentName(result_1, id_attribute):
    try:
        with con.cursor() as cur:
            common_attributes = {'Id': result_1[0][0], 'Name': result_1[0][1], 'Description': result_1[0][2],
                                 'AttributesContainer': {}}
            if result_1[0][3] is not None:
                cur.execute(f'SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, taa.idTypeAttributes '
                            f'FROM list_common_attribute AS lca '
                            f'LEFT JOIN table_attributes AS taa ON lca.idTableAttributes=taa.idTableAttributes '
                            f'WHERE lca.idTableAttributes={result_1[0][3]} AND lca.idListCommonAttribute={id_attribute}')
                result_2 = [list(i) for i in cur.fetchall()]
                getTypeAttribute(common_attributes, result_2, id_attribute)
    except Exception as ex:
        print(ex)
    return common_attributes


def getTypeAttribute(common_attributes, result_2, id_attribute):
    try:
        with con.cursor() as cur:
            cur.execute(f'SELECT tya.TypeAttributes FROM list_common_attribute AS lca '
                        f'LEFT JOIN table_attributes AS taa ON lca.idTableAttributes=taa.idTableAttributes '
                        f'LEFT JOIN type_attributes AS tya ON taa.idTypeAttributes=tya.idTypeAttributes '
                        f'WHERE tya.idTypeAttributes={result_2[0][2]} AND lca.idListCommonAttribute={id_attribute}')
            result_3 = [list(i) for i in cur.fetchone()]
            sendTypeAttribute(common_attributes, result_3, result_2)
    except Exception as ex:
        print(ex)
    return common_attributes


def sendTypeAttribute(common_attributes, result_3, result_2):
    try:
        attributesContainerObject = {'Id': result_2[0][0], 'Name': result_2[0][1], 'Type': result_3[0][0]}
        common_attributes['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        print(ex)
    return common_attributes
