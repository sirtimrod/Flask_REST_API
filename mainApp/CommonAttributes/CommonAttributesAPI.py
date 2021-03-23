from mainApp import app

# Initialization files with business-logic
from .CommonAttributesMethods.GetCommonAttributes import displayCommonAttributes
from .CommonAttributesMethods.GetSpecificCommonAttributes import displaySpecificCommonAttribute
from .CommonAttributesMethods.AddCommonAttribute import addNewCommonAttribute
from .CommonAttributesMethods.DeleteCommonAttribute import deleteCommonAttribute


# This route returns common attributes
@app.route('/api/common_attributes', methods=['GET'])
def getCommonAttributes():
    return displayCommonAttributes()


# This route returns specific common attribute by id
@app.route('/api/common_attributes/<int:id_attribute>', methods=['GET'])
def getSpecificCommonAttribute(id_attribute):
    return displaySpecificCommonAttribute(id_attribute)


# This route adds new common attribute
@app.route('/api/common_attributes', methods=['POST'])
def addCommonAttribute():
    return addNewCommonAttribute()


# This route deletes common attribute by id
@app.route('/api/common_attributes/<int:id_attribute>', methods=['DELETE'])
def deleteCertainCommonAttribute(id_attribute):
    return deleteCommonAttribute(id_attribute)
