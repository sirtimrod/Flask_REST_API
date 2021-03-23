from mainApp import app

# Initialization files with business-logic
from .ContainersOfAttributesMethods.GetContainersOfAttributes import displayContainersOfAttributes
from .ContainersOfAttributesMethods.GetContainerOfAttributesById import displayContainerOfAttributesById


# This route returns containers of attributes
@app.route('/api/attributes_containers', methods=['GET'])
def getContainersOfAttributes():
    return displayContainersOfAttributes()


# This route returns only one container of attributes by id
@app.route('/api/attributes_containers/<int:id_container>', methods=['GET'])
def getContainerOfAttributesById(id_container):
    return displayContainerOfAttributesById(id_container)
