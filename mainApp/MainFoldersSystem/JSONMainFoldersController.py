from mainApp.DataBaseConnection import con
import pymysql


def Reqursion(list, rowParent, row):
    for itemList in list:
        if itemList['name'] == rowParent:
            itemList['child'].append({'id': row[0], 'name': row[1], 'child': []})
        else:
            Reqursion(itemList['child'], rowParent, row)


def getFolders():
    local_con = pymysql.connect(host='127.0.0.1',
                          port=3306,
                          user='george_mihal',
                          password='treaw221',
                          database='ciris_lib')
    cur = local_con.cursor()
    cur.execute("SELECT * FROM folderscomponent ORDER BY idFoldersComponent")

    rows = cur.fetchall()
    cur.execute("SELECT * FROM folderscomponent ORDER BY idFoldersComponent")
    rowsParent = cur.fetchall()
    mainList = []
    for row in rows:
        if row[2] is None:
            mainList.append({'id': row[0], 'name': row[1], 'child': []})
        else:
            for rowParent in rowsParent:
                if row[2] == rowParent[0]:
                    for itemList in mainList:
                        if itemList['name'] == rowParent[1]:
                            itemList['child'].append({'id': row[0], 'name': row[1], 'child': []})
                        else:
                            Reqursion(itemList['child'], rowParent[1], row)
    return mainList


def addFolder(id, object):
    cur = con.cursor()
    if id == '0':
        request = "INSERT INTO folderscomponent SET FolderName = '{folderName}'"
        request = request.format(folderName=object['Name'])
        cur.execute(request)
    else:
        request = "INSERT INTO folderscomponent SET FolderName = '{folderName}', FolderID = {idParent}"
        request = request.format(folderName=object['Name'], idParent=id)
        cur.execute(request)
