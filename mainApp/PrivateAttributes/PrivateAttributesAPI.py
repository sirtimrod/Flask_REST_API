from mainApp import app

# Initialization files with business-logic
from .PrivateAttributesMethods.GetPrivateAttributes import displayPrivateAttributes
from .PrivateAttributesMethods.GetCurrentPrivateAttribute import displayCurrentPrivateAttribute
from .PrivateAttributesMethods.AddNewPrivateAttribute import createPrivateAttribute
from .PrivateAttributesMethods.DeletePrivateAttribute import deleteOnePrivateAttribute


# This route returns only private attributes of one category
@app.route('/api/categories/<int:id_category>/attributes', methods=['GET'])
def getPrivateAttributes(id_category):
    return displayPrivateAttributes(id_category)


# This route returns current private attribute
@app.route('/api/categories/<int:id_category>/attributes/<int:id_attribute>', methods=['GET'])
def getCurrentPrivateAttribute(id_category, id_attribute):
    return displayCurrentPrivateAttribute(id_category, id_attribute)


# This route adds new private attribute to a certain category
@app.route('/api/categories/<int:id_category>/attributes', methods=['POST'])
def addPrivateAttribute(id_category):
    return createPrivateAttribute(id_category)


# This route deletes private attribute
@app.route('/api/categories/<int:id_category>/attributes/<int:id_attribute>', methods=['DELETE'])
def deletePrivateAttribute(id_category, id_attribute):
    return deleteOnePrivateAttribute(id_category, id_attribute)
