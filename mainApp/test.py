"""The note for GET method"""


# @app.route('/api/categories', methods=['GET'])
# def get():
#     categories = []
#     cursor = connection.cursor()
# cursor.execute('SELECT lc.idListCategory, lc.RepresentName FROM list_category AS lc ORDER BY lc.idListCategory ASC')
# result_1 = [list(i) for i in cursor.fetchall()]
# for i, first_layer in enumerate(result_1, 0):
#     # print(i, first_layer)
#     categories.append({'id': first_layer[0], 'Name': first_layer[1], 'Attributes': []})
#     cursor.execute(f'SELECT lpa.idListPrivateAttribute, lpa.RepresentName, lpa.Description, lpa.idTableAttributes, lpa.ListCategoryID '
#                    f'FROM list_category AS lc '
#                    f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
#                    f'WHERE lpa.ListCategoryID={i}')
#     result_2 = [list(i) for i in cursor.fetchall()]
#     for j, second_layer in enumerate(result_2, 0):
#         # print('\t', second_layer)
#         categories[i]['Attributes'].append({'id': second_layer[0], 'Name': second_layer[1], 'Description': second_layer[2], 'AttributesContainer': []})
#         if second_layer[3] is not None:
#             cursor.execute(f'SELECT taa.idTableAttributes, taa.TableAttributesRepresentName, taa.idTypeAttributes '
#                            f'FROM list_category AS lc '
#                            f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
#                            f'LEFT JOIN table_attributes AS taa ON lpa.idTableAttributes=taa.idTableAttributes '
#                            f'WHERE lpa.ListCategoryID={i} AND taa.idTableAttributes={second_layer[3]}')
#             result_3 = [list(i) for i in cursor.fetchall()]
#             for third_layer in result_3:
#                 # print('\t\t', third_layer)
#                 cursor.execute(f'SELECT tya.TypeAttributes, tya.idTypeAttributes FROM list_category AS lc '
#                                f'LEFT JOIN list_private_attribute AS lpa ON lc.idListCategory=lpa.ListCategoryID '
#                                f'LEFT JOIN table_attributes AS taa ON lpa.idTableAttributes=taa.idTableAttributes '
#                                f'LEFT JOIN type_attributes AS tya ON taa.idTypeAttributes=tya.idTypeAttributes '
#                                f'WHERE lpa.ListCategoryID={i} AND tya.idTypeAttributes={third_layer[2]}')
#                 result_4 = [list(i) for i in cursor.fetchall()]
#                 for fourth_layer in result_4:
#                     categories[i]['Attributes'][j]['AttributesContainer'].append({'id': third_layer[0], 'Name': third_layer[1], 'Type': fourth_layer[0]})
#                     # print('\t\t\t', fourth_layer)
# return jsonify({'Categories': categories})


# def validate_pin(pin):
#     if len(pin) == 4 or len(pin) == 6:
#         return print(all(str.isdigit(s) for s in pin))
#     else:
#         return print(False)


def spin_words(sentence):
    return ' '.join(word[::-1] if len(word) >= 5 else word for word in sentence.split(' '))


if __name__ == '__main__':
    print(spin_words('Strings passed in will consist of only letters and spaces'))
