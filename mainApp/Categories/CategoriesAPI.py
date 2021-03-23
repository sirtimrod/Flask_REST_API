from mainApp import app

# Initialization files with business-logic
from .CategoryMethods.GetCategories import displayCategories
from .CategoryMethods.GetCategoriesId import displayCategoryById
from .CategoryMethods.addCategory import createCategory


# Home route
@app.route("/api/")
def hello():
    return "<h1> Hello World! </h1>"


# That route allows display all categories with their characteristics
@app.route('/api/categories', methods=['GET'])
def getCategories():
    return displayCategories()


# That route displays only one category with characteristics
@app.route('/api/categories/<int:Id>', methods=['GET'])
def getIdCategories(Id):
    return displayCategoryById(Id)


# That route adds new category with characteristics
@app.route('/api/categories', methods=['POST'])
def addCategories():
    return createCategory()
