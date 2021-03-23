from flask import request, abort, jsonify

from mainApp.DataBaseConnection import con


def checkCategoryId(id_category):
    with con.cursor() as cur:
        cur.execute('SELECT lc.IdListCategory FROM list_category AS lc ORDER BY lc.IdListCategory ASC')
        res_id_category = [i[0] for i in cur.fetchall()]
        if id_category in filter(lambda t: t == id_category, res_id_category):
            return getCategoryName(id_category)
        else:
            return abort(404, description='Resource not found')


def getCategoryName(id_category):
    try:
        with con.cursor() as cur:
            cur.execute(
                f'SELECT lc.IdListCategory, lc.RepresentName '
                f'FROM list_category AS lc WHERE lc.IdListCategory={id_category}')
            Cater_Name = cur.fetchone()[1]
    except Exception as ex:
        print(ex)
    return Cater_Name


def createPrivateAttribute(id_category):
    if not request.json:
        return abort(400, description='Your request is incorrect or missing')
    else:
        return jsonify(addAttributes(str(checkCategoryId(id_category)))), 201


def addAttributes(Cater_Name):
    try:
        Attr_Name = str(request.json['Attr_Name'])
        Description = str(request.json['Description']).replace('', 'None') \
            if str(request.json['Description']) == '' else str(request.json['Description'])
        Cont_Name = str(request.json['Cont_Name']).replace('', 'None') \
            if str(request.json['Cont_Name']) == '' else str(request.json['Cont_Name'])
        # Type must be only List, SVN, FileServer, OnlineSource
        Cont_Type = str(request.json['Cont_Type']).replace('', 'None') \
            if str(request.json['Cont_Type']) == '' else str(request.json['Cont_Type'])
        Attr_Args = [Cater_Name, Cont_Type, Cont_Name, Attr_Name, Description]
        with con.cursor() as cur:
            cur.callproc('addPrivateAttribute', Attr_Args)
            con.commit()
            new_category = {'Name': Attr_Name,
                            'Description': Description,
                            'AttributesContainer': {
                                'Name': Cont_Name,
                                'Type': Cont_Type},
                            'Category': Cater_Name}
    except Exception as ex:
        print(ex)
    return new_category
