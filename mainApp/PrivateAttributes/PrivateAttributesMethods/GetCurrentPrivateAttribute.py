from flask import abort, jsonify

from mainApp.DataBaseConnection import con


def displayCurrentPrivateAttribute(id_category, id_attribute):
    with con.cursor() as cur:
        cur.execute('SELECT lc.IdListCategory FROM list_category AS lc ORDER BY lc.IdListCategory ASC')
        res_id_category = [i[0] for i in cur.fetchall()]
        if id_category in filter(lambda t: t == id_category, res_id_category):
            return jsonify(getDescriptionById(id_category, id_attribute)), 200
        else:
            return abort(404, description='Resource not found')


def getDescriptionById(id_category, id_attribute):
    with con.cursor() as cur:
        cur.execute(
            f'SELECT lpa.IdListPrivateAttribute, lpa.RepresentName, lpa.Description, lpa.IdTableAttributes, '
            f'lpa.ListCategoryId, lc.RepresentName '
            f'FROM list_category AS lc '
            f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
            f'WHERE lpa.ListCategoryId={id_category} AND lpa.idListPrivateAttribute={id_attribute}')
        db_output = cur.fetchall()
        result_1 = [list(i) for i in db_output]
        res_id_attribute = [i[0] for i in db_output]
        if id_attribute in filter(lambda t: t == id_attribute, res_id_attribute):
            return getTableAttributesRepresentNameById(result_1, id_category, id_attribute)
        else:
            return abort(404, description='Resource not found')


def getTableAttributesRepresentNameById(result_1, id_category, id_attribute):
    try:
        with con.cursor() as cur:
            attributes_by_Id = {'Id': result_1[0][0], 'Name': result_1[0][1], 'Description': result_1[0][2],
                                'AttributesContainer': {}, 'Category': result_1[0][5]}
            if result_1[0][3] is not None:
                cur.execute(f'SELECT taa.IdTableAttributes, taa.TableAttributesRepresentName, taa.IdTypeAttributes, lpa.idListPrivateAttribute '
                            f'FROM list_category AS lc '
                            f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                            f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                            f'WHERE lpa.ListCategoryId={id_category} AND lpa.idListPrivateAttribute={id_attribute} '
                            f'AND taa.IdTableAttributes={result_1[0][3]}')
                result_2 = [list(i) for i in cur.fetchall()]
                getTypeAttributesById(attributes_by_Id, result_2, id_category, id_attribute)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id


def getTypeAttributesById(attributes_by_Id, result_2, id_category, id_attribute):
    try:
        with con.cursor() as cur:
            for third_layer in result_2:
                cur.execute(f'SELECT tya.TypeAttributes, tya.IdTypeAttributes, lpa.idListPrivateAttribute FROM list_category AS lc '
                            f'LEFT JOIN list_private_attribute AS lpa ON lc.IdListCategory=lpa.ListCategoryId '
                            f'LEFT JOIN table_attributes AS taa ON lpa.IdTableAttributes=taa.IdTableAttributes '
                            f'LEFT JOIN type_attributes AS tya ON taa.IdTypeAttributes=tya.IdTypeAttributes '
                            f'WHERE lpa.ListCategoryId={id_category} AND lpa.idListPrivateAttribute={id_attribute} '
                            f'AND tya.IdTypeAttributes={third_layer[2]}')
                result_3 = [list(i) for i in cur.fetchall()]
                sendTypeAttributes(attributes_by_Id, result_3, third_layer)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id


def sendTypeAttributes(attributes_by_Id, result_3, third_layer):
    try:
        for fourth_layer in result_3:
            attributesContainerObject = {'Id': third_layer[0], 'Name': third_layer[1], 'Type': fourth_layer[0]}
            attributes_by_Id['AttributesContainer'].update(attributesContainerObject)
    except Exception as ex:
        abort(description=str(ex))
    return attributes_by_Id
