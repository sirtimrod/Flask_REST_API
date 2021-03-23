from flask import jsonify

from mainApp.DataBaseConnection import con


def displayCategories():
    categories = []
    return jsonify({'Categories': getName(categories)}), 200


def getName(categories):
    try:
        with con.cursor() as cur:
            cur.execute('SELECT lc.idListCategory, lc.RepresentName '
                        'FROM list_category AS lc ORDER BY lc.idListCategory ASC')
            result_1 = [list(i) for i in cur.fetchall()]
            getDescription(categories, result_1)
    except Exception as ex:
        print(ex)
    return categories


def getDescription(categories, result_1):
    try:
        with con.cursor() as cur:
            for i, first_layer in enumerate(result_1, 0):
                categories.append({'Id': first_layer[0], 'Name': first_layer[1], 'Attributes': []})
                cur.execute(
                    f'SELECT lpa.idListPrivateAttribute, lpa.RepresentName, lpa.Description, lpa.idTableAttributes, lpa.ListCategoryID '
                    f'FROM list_category AS lc '
                    f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
                    f'WHERE lpa.ListCategoryID={first_layer[0]}')
                result_2 = [list(i) for i in cur.fetchall()]
                getTableAttributesRepresentName(categories, result_2, i, first_layer[0])
    except Exception as ex:
        print(ex)
    return categories


def getTableAttributesRepresentName(categories, result_2, i, first_layer):
    try:
        with con.cursor() as cur:
            for j, second_layer in enumerate(result_2, 0):
                attributeObject = {'Id': second_layer[0], 'Name': second_layer[1], 'Description': second_layer[2], 'AttributesContainer': {}}
                categories[i]['Attributes'].append(attributeObject)
                if second_layer[3] is not None:
                    cur.execute(f'SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, taa.idTypeAttributes '
                                f'FROM list_category AS lc '
                                f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
                                f'LEFT JOIN table_attributes AS taa ON lpa.idTableAttributes=taa.idTableAttributes '
                                f'WHERE lpa.ListCategoryID={first_layer} AND taa.idTableAttributes={second_layer[3]}')
                    result_3 = [list(i) for i in cur.fetchall()]
                    getTypeAttributes(categories, result_3, i, j, first_layer)
    except Exception as ex:
        print(ex)
    return categories


def getTypeAttributes(categories, result_3, i, j, first_layer):
    try:
        with con.cursor() as cur:
            for third_layer in result_3:
                cur.execute(f'SELECT tya.TypeAttributes, tya.idTypeAttributes FROM list_category AS lc '
                            f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
                            f'LEFT JOIN table_attributes AS taa ON lpa.idTableAttributes=taa.idTableAttributes '
                            f'LEFT JOIN type_attributes AS tya ON taa.idTypeAttributes=tya.idTypeAttributes '
                            f'WHERE lpa.ListCategoryID={first_layer} AND tya.idTypeAttributes={third_layer[2]}')
                result_4 = [list(i) for i in cur.fetchall()]
                sendTypeAttributes(categories, result_4, i, j, third_layer)
    except Exception as ex:
        print(ex)
    return categories


def sendTypeAttributes(categories, result_4, i, j, third_layer):
    try:
        for fourth_layer in result_4:
            attributesContainerObject = {'Id': third_layer[0], 'Name': third_layer[1], 'Type': fourth_layer[0]}
            categories[i]['Attributes'][j]['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        print(ex)
    return categories
