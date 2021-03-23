from flask import jsonify

from mainApp.DataBaseConnection import con


def displayCommonAttributes():
    common_attributes = []
    return jsonify({'CommonAttributes': getAttributesInfo(common_attributes)}), 200


def getAttributesInfo(common_attributes):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lca.idListCommonAttribute, lca.RepresentName, lca.Description, lca.idTableAttributes '
                f'FROM list_common_attribute AS lca '
                f'ORDER BY lca.idListCommonAttribute ASC ')
            result_1 = [list(i) for i in cur.fetchall()]
            getTableAttributesRepresentName(result_1, common_attributes)
    except Exception as ex:
        print(ex)
    return common_attributes


def getTableAttributesRepresentName(result_1, common_attributes):
    try:
        with con.cursor() as cur:
            for i, first_layer in enumerate(result_1, 0):
                attributeObject = {'Id': first_layer[0], 'Name': first_layer[1], 'Description': first_layer[2], 'AttributesContainer': {}}
                common_attributes.append(attributeObject)
                if first_layer[3] is not None:
                    cur.execute(f'SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, taa.idTypeAttributes '
                                f'FROM list_common_attribute AS lca '
                                f'LEFT JOIN table_attributes AS taa ON lca.idTableAttributes=taa.idTableAttributes '
                                f'WHERE lca.idTableAttributes={first_layer[3]}')
                    result_2 = [list(i) for i in cur.fetchall()]
                    getTypeAttributes(common_attributes, result_2, i)
    except Exception as ex:
        print(ex)
    return common_attributes


def getTypeAttributes(common_attributes, result_2, i):
    try:
        with con.cursor() as cur:
            for second_layer in result_2:
                cur.execute(f'SELECT tya.TypeAttributes FROM list_common_attribute AS lca '
                            f'LEFT JOIN table_attributes AS taa ON lca.idTableAttributes=taa.idTableAttributes '
                            f'LEFT JOIN type_attributes AS tya ON taa.idTypeAttributes=tya.idTypeAttributes '
                            f'WHERE tya.idTypeAttributes={second_layer[2]}')
                result_3 = [list(i) for i in cur.fetchall()]
                sendTypeAttributes(common_attributes, result_3, second_layer, i)
    except Exception as ex:
        print(ex)
    return common_attributes


def sendTypeAttributes(common_attributes, result_3, second_layer, i):
    try:
        for third_attributes in result_3:
            attributesContainerObject = {'Id': second_layer[0], 'Name': second_layer[1], 'Type': third_attributes[0]}
            common_attributes[i]['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        print(ex)
    return common_attributes
