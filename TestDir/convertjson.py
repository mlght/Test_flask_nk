from lxml import etree as ET
import json
from typing import List, Tuple


#пути к используемым файлам
xsd_add: str = "./sources/Add_Entrant_List.xsd"
xsd_get: str = "./sources/Get_Entrant_List_2.xsd"
xsd_add_example: str = "./sources/Add_example.xml"
fields_class: str = "./sources/dict_document_type_cls.json"
xml_example: str = "./sources/Get_example.xml"

#Словарь, содержащий сопоставление xml тегов с json ключами
xml_json_dict: dict[str, str] = {"SubdivisionCode":"passport_org_code" ,
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
            "FullAddr": "address_txt1",
            "Guid":"user_id",
            #"IdRegion":"kladr_1"
            "City":"city"
            }


def xml_tree(json_data: dict) -> Tuple[list, str]:
    """ Возвращает шаблон дерева для создания XML файла, возвращает название типа документа

    Аргументы:
    json_data -- словарь JSON документа для конвертации
     """
    tree = ET.parse(xsd_add_example)
    field_id = json_data[xml_json_dict["IdDocumentType"]]+100000
    with open(fields_class, 'rb') as field_file:
        field = json.load(field_file)

    for item in field:
        if item["Id"] == field_id:
            doc = item["Name"]
            new_tags = []
            for i in field[0]["FieldsDescription"]["fields"]:
                new_tags.append(i["xml_name"])

    for item in tree.getiterator():
        if (item.tag == "Identification"):
            field_el = ET.SubElement(item,'Field')
            for tag in new_tags:
                buf = ET.SubElement(field_el, tag)
                buf.text = "none"

    return tree, doc


#Функция, заполняющая etree данными из json
def filling_xml(tree: list, json_data: str, doc: str) -> str:
    """ Заполняет дерево значениями из JSON файла и возвращает строку, содержащую XML файл

    Аргументы:
    tree --  шаблон дерева для создания XML файла
    json_data -- словарь JSON документа для конвертации
    doc -- название типа документа
    """
    keys = xml_json_dict.keys()

    for item in tree.getiterator():
        if item.tag == "IdRegion":
            item.text = json_data["kladr_1"][:2]

        elif item.tag == "FullAddr":
            item.text = (json_data["address_txt1"]+(" " + json_data["address_txt2"] if json_data["address_txt2"] is not None else "")+
                        (" " + json_data["address_txt3"] if json_data["address_txt3"] is not None else "")+
                         (" " + json_data["address_txt4"] if json_data["address_txt4"] is not None else ""))
        elif (item.tag == "DocName"):
            item.text = doc
        elif (item.tag in keys):
            item.text = str(json_data[xml_json_dict[item.tag]])

    result = ET.tostring(tree, pretty_print=True, encoding="unicode")
    return result
