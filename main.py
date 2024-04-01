from flask import Flask, request, jsonify
from lxml import etree as ET
from convertxml import xml_to_json, validation_xml
from convertjson import  xml_tree, filling_xml, xsd_add, xsd_get


app = Flask(__name__)

@app.route('/')
def main_page():

    return "work"

@app.route('/convert_json', methods=['POST'])
def convert_json():
    """ Конвертирует JSON файл из POST запроса в XML. Если передан параметр 'validation', проводит валидацию по XSD """
    try:
        data = request.get_json()
    except:
        return "Load JSON file"
    prep, document = xml_tree(data)
    result = filling_xml(prep, data, document)

    if request.args.get('validation') is not None:
        validation_xml(result, xsd_add)

    return result


@app.route('/convert_xml', methods=['POST'])
def convert_xml():
    """ Конвертирует XML файл из POST запроса в JSON. Если передан параметр 'validation', проводит валидацию по XSD """
    result = xml_to_json(request.data.decode(encoding='utf-8'))
    if request.args.get('validation') is not None:
        validation_xml(request.data.decode(encoding='utf-8'), xsd_get)
    return result


if __name__ == '__main__':
    app.run()



