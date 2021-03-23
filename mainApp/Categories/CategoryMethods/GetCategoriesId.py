from flask import abort, jsonify

from mainApp.DataBaseConnection import con


def displayCategoryById(Id):
    with con.cursor() as cur:
        cur.execute('SELECT lc.IdListCategory FROM list_category AS lc ORDER BY lc.IdListCategory ASC')
        res_Id = [i[0] for i in cur.fetchall()]
        if Id in filter(lambda t: t == Id, res_Id):
            return jsonify(getNameById(Id)), 200
        else:
            return abort(404, description='Resource not found')


def getNameById(Id):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lc.IdListCategory, lc.RepresentName FROM list_category AS lc WHERE lc.IdListCategory={Id}')
            result_1 = [list(i) for i in cur.fetchall()]
    except Exception as ex:
        abort(400, description=str(ex))
    return getDescriptionById(result_1, Id)


def getDescriptionById(result_1, Id):
    try:
        categories_by_Id = {'Id': result_1[0][0], 'Name': result_1[0][1], 'Attributes': []}
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lpa.IdListPrivateAttribute, lpa.RepresentName, lpa.Description, lpa.IdTableAttributes, lpa.ListCategoryId '
                f'FROM list_category AS lc '
                f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                f'WHERE lpa.ListCategoryId={Id}')
            result_2 = [list(i) for i in cur.fetchall()]
            getTableAttributesRepresentNameById(categories_by_Id, result_2, Id)
    except Exception as ex:
        abort(description=str(ex))
    return categories_by_Id


def getTableAttributesRepresentNameById(categories_by_Id, result_2, Id):
    try:
        with con.cursor() as cur:
            for j, second_layer in enumerate(result_2, 0):
                attributeObject = {'Id': second_layer[0], 'Name': second_layer[1], 'Description': second_layer[2],
                                   'AttributesContainer': {}}
                categories_by_Id['Attributes'].append(attributeObject)
                if second_layer[3] is not None:
                    cur.execute(f'SELECT taa.IdTableAttributes, taa.TableAttributesRepresentName, taa.IdTypeAttributes '
                                f'FROM list_category AS lc '
                                f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                                f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                                f'WHERE lpa.ListCategoryId={Id} AND taa.IdTableAttributes={second_layer[3]}')
                    result_3 = [list(i) for i in cur.fetchall()]
                    getTypeAttributesById(categories_by_Id, result_3, Id, j)
    except Exception as ex:
        abort(description=str(ex))
    return categories_by_Id


def getTypeAttributesById(categories_by_Id, result_3, Id, j):
    try:
        with con.cursor() as cur:
            for third_layer in result_3:
                cur.execute(f'SELECT tya.TypeAttributes, tya.IdTypeAttributes FROM list_category AS lc '
                            f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                            f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                            f'LEFT JOIN type_attributes AS tya ON taa.IdTypeAttributes=tya.IdTypeAttributes '
                            f'WHERE lpa.ListCategoryId={Id} AND tya.IdTypeAttributes={third_layer[2]}')
                result_4 = [list(i) for i in cur.fetchall()]
                sendTypeAttributes(categories_by_Id, result_4, j, third_layer)
    except Exception as ex:
        abort(description=str(ex))
    return categories_by_Id


def sendTypeAttributes(categories_by_Id, result_4, j, third_layer):
    try:
        for fourth_layer in result_4:
            attributesContainerObject = {'Id': third_layer[0], 'Name': third_layer[1], 'Type': fourth_layer[0]}
            categories_by_Id['Attributes'][j]['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        abort(description=str(ex))
    return categories_by_Id
