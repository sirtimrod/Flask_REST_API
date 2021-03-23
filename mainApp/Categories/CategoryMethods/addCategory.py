from flask import request, abort, jsonify

from mainApp.DataBaseConnection import con


def createCategory():
    new_category = {}
    if not request.json:
        return abort(400, description='Your request is incorrect or missing')
    else:
        addCategory()
    return jsonify(new_category), 201


def addCategory():
    try:
        Cater_Name = str(request.json['Categ_Name'])
        Cater_Args = [Cater_Name]
        with con.cursor() as cur:
            cur.callproc('createCategory', Cater_Args)
            con.commit()
            new_category = {'Name': Cater_Name, 'Attributes': []}
            if 'Attr_Name' in request.json:
                addAttributes(new_category, Cater_Name)
    except Exception as ex:
        print(ex)
    return new_category


def addAttributes(new_category, Cater_Name):
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
            new_category['Attributes'].append({'Name': Attr_Name,
                                               'Description': Description,
                                               'AttributesContainer': {
                                                   'Name': Cont_Name,
                                                   'Type': Cont_Type}})
    except Exception as ex:
        print(ex)
    return new_category
