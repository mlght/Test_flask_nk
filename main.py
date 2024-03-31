from flask import Flask, request, jsonify
from lxml import etree as ET
import xmlschema
import json
import xmltodict

#пути к используемым файлам
xsd_add = "./Add_Entrant_List.xsd"
xsd_get = "./Get_Entrant_List_2.xsd"
xsd_add_example = "./Add_example.xml"
fields_class = "./dict_document_type_cls.json"
xml_example = "./Get_example.xml"

#Словарь, содержащий сопоставление xml тегов с json ключами
keys_dict = {"SubdivisionCode":"passport_org_code" ,
            "IdOksm": "residence_country_id",
            "Surname": "second_name",
            "Name": "first_name",
            "Patronymic": "middle_name",
            "IdDocumentType": "passport_type_id",
            #"DocName": "",
            "DocSeries": "passport_series",
            "DocNumber": "passport_number",
            "IssueDate": "passport_begda",
            "DocOrganization": "passport_issued_by",
            "SnilsType": "snils",
            "IdGender": "dict_sex_id",
            "Birthplace": "motherland",
            "Phone": "tel_mobile",
            #"IdOksm": "citizenship_id",
            #"FullAddr": "address_txt1",
            "Guid":"user_id",
            #"IdRegion":"kladr_1"
            }

#Функция, избавляющаяся от вложенности словарей при парсинге xml
def flatten_dict(d, parent_key=''):

    items = []
    for k, i in d.items():
        new_key = k
        if isinstance(i, dict):
            items.extend(flatten_dict(i, new_key).items())
        else:
            items.append((new_key, i))
    return dict(items)


#Функция, коныертирующая xml в json
def xml_to_json(data):

    xml_dict = xmltodict.parse(data)
    #print(type(xml_dict))
    final_dict = flatten_dict(xml_dict)

    drop = []
    add = []
    for key, item in final_dict.items():
        if ("xsi" in key):
            drop.append(key)
        if (key in keys_dict):
            add.append([keys_dict[key], item])
            drop.append(key)

    for key in drop:
        final_dict.pop(key)
    for key, item in add:
        final_dict[key]=item

    json_data = json.dumps(final_dict, allow_nan=True, indent=' ')

    return json_data


#Функция для получения дерева etree из примера xml файла, из классификатора извлекает имя документа
def xml_tree(json_data):

    tree = ET.parse(xsd_add_example)
    field_id = json_data[keys_dict["IdDocumentType"]]+100000
    with open(fields_class, 'rb') as field_file:
        field = json.load(field_file)

    for item in field:
        if item["Id"] == field_id:
            doc = item["Name"]
            #print(type(item["Name"]), item["Name"])
            new_tags = []
            for item in field[0]["FieldsDescription"]["fields"]:
                new_tags.append(item["xml_name"])

    for item in tree.getiterator():
        if (item.tag == "Identification"):
            for tag in new_tags:
                buf = ET.SubElement(item, tag)
                buf.text="1"

    return tree,doc


#Функция, заполняющая etree данными из json
def filling_xml(tree, json_data,doc):

    keys=keys_dict.keys()

    for item in tree.getiterator():
        if item.tag == "IdRegion":
            item.text = json_data["kladr_1"][:2]

        if item.tag== "FullAddr":
            item.text=(json_data["address_txt1"]+(" " + json_data["address_txt2"] if json_data["address_txt2"] is not None else "")+
                        (" " + json_data["address_txt3"] if json_data["address_txt3"] is not None else "")+
                         (" " + json_data["address_txt4"] if json_data["address_txt4"] is not None else ""))


        if (item.tag in keys):
            item.text = str(json_data[keys_dict[item.tag]])
        elif (item.tag=="DocName"):
            item.text=doc

    return tree

#Функция для валидации xml файла по xsd
def validation_xml(xml_data,path):

    schema = ET.XMLSchema(file=path)
    print("val")
    try:
        schema.assertValid(ET.fromstring(xml_data))
        print("XML-схема валидна.")
    except ET.DocumentInvalid as e:
        print("XML-схема не валидна. Ошибка: ", e)

    return


app = Flask(__name__)

@app.route('/')
def main_page():
    return "work"

@app.route('/convert', methods=['POST'])
def convert_json():

    print(request.args.get('validation'))
    if request.is_json :
        data=request.get_json()
        prep,document=xml_tree(data)
        tree= filling_xml(prep, data,document)
        result = ET.tostring(tree, pretty_print=True, encoding="unicode")
        if request.args.get('validation') is not None:
            validation_xml(result,xsd_add)
    else:
        result = xml_to_json(request.data.decode(encoding='utf-8'))
        if request.args.get('validation') is not None:
            validation_xml(request.data.decode(encoding='utf-8'), xsd_get)
    return result


if __name__ == '__main__':

    app.run()



