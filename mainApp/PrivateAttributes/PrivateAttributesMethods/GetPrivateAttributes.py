from flask import abort, jsonify

from mainApp.DataBaseConnection import con


def displayPrivateAttributes(id_category):
    with con.cursor() as cur:
        cur.execute('SELECT lc.IdListCategory FROM list_category AS lc ORDER BY lc.IdListCategory ASC')
        res_id_category = [i[0] for i in cur.fetchall()]
        if id_category in filter(lambda t: t == id_category, res_id_category):
            return jsonify(getDescriptionById(id_category)), 200
        else:
            return abort(404, description='Resource not found')


def getDescriptionById(id_category):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lpa.IdListPrivateAttribute, lpa.RepresentName, lpa.Description, lpa.IdTableAttributes, '
                f'lpa.ListCategoryId, lc.RepresentName '
                f'FROM list_category AS lc '
                f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                f'WHERE lpa.ListCategoryId={id_category}')
            result_1 = [list(i) for i in cur.fetchall()]
    except Exception as ex:
        abort(description=str(ex))
    return getTableAttributesRepresentNameById(result_1, id_category)


def getTableAttributesRepresentNameById(result_1, id_category):
    try:
        with con.cursor() as cur:
            attributes_by_Id = {'Attributes': []}
            for j, second_layer in enumerate(result_1, 0):
                attributeObject = {'Id': second_layer[0], 'Name': second_layer[1], 'Description': second_layer[2],
                                   'AttributesContainer': {}, 'Category': second_layer[5]}
                attributes_by_Id['Attributes'].append(attributeObject)
                if second_layer[3] is not None:
                    cur.execute(f'SELECT taa.IdTableAttributes, taa.TableAttributesRepresentName, taa.IdTypeAttributes '
                                f'FROM list_category AS lc '
                                f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                                f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                                f'WHERE lpa.ListCategoryId={id_category} AND taa.IdTableAttributes={second_layer[3]}')
                    result_2 = [list(i) for i in cur.fetchall()]
                    getTypeAttributesById(attributes_by_Id, result_2, id_category, j)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id


def getTypeAttributesById(attributes_by_Id, result_2, id_category, j):
    try:
        with con.cursor() as cur:
            for third_layer in result_2:
                cur.execute(f'SELECT tya.TypeAttributes, tya.IdTypeAttributes FROM list_category AS lc '
                            f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                            f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                            f'LEFT JOIN type_attributes AS tya ON taa.IdTypeAttributes=tya.IdTypeAttributes '
                            f'WHERE lpa.ListCategoryId={id_category} AND tya.IdTypeAttributes={third_layer[2]}')
                result_3 = [list(i) for i in cur.fetchall()]
                sendTypeAttributes(attributes_by_Id, result_3, j, third_layer)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id


def sendTypeAttributes(attributes_by_Id, result_3, j, third_layer):
    try:
        for fourth_layer in result_3:
            attributesContainerObject = {'Id': third_layer[0], 'Name': third_layer[1], 'Type': fourth_layer[0]}
            attributes_by_Id['Attributes'][j]['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id
