from flask import jsonify

from mainApp.DataBaseConnection import con


def displayContainersOfAttributes():
    containers_of_attributes = []
    return jsonify({'AttributesContainers': getAttributesContainersInfo(containers_of_attributes)}), 200


def getAttributesContainersInfo(containers_of_attributes):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, '
                        'tya.TypeAttributes FROM table_attributes AS taa LEFT JOIN type_attributes AS tya ON '
                        'taa.idTypeAttributes=tya.idTypeAttributes ORDER BY taa.idTableAttributes ASC ')
            result_1 = [list(i) for i in cur.fetchall()]
            collectList(result_1, containers_of_attributes)
    except Exception as ex:
        print(ex)
    return containers_of_attributes


def collectList(result_1, containers_of_attributes):
    try:
        for first_layer in result_1:
            attributeObject = {'Id': first_layer[0], 'Name': first_layer[1], 'Type': first_layer[2]}
            containers_of_attributes.append(attributeObject)
    except Exception as ex:
        print(ex)
    return containers_of_attributes

