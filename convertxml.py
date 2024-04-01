from lxml import etree as ET
import json
import xmltodict
from convertjson import xml_json_dict
import typing
from typing import List, Union

#пути к используемым файлам
xsd_add = "./sources/Add_Entrant_List.xsd"
xsd_get = "./sources/Get_Entrant_List_2.xsd"
xsd_add_example = "./sources/Add_example.xml"
fields_class = "./sources/dict_document_type_cls.json"
xml_example = "./sources/Get_example.xml"



#Функция, избавляющаяся от вложенности словарей при парсинге xml
def flatten_dict(d: dict, parent_key: str ='') -> dict:
    """ Избавляет словарь от вложений словарей в значениях, возвращает обновленный словарь

    Аргументы:
    d --  словарь
    parent_key -- ключ родительского элемента при вложении
    """
    items = []
    for k, i in d.items():
        new_key = k
        if isinstance(i, dict):
            items.extend(flatten_dict(i, new_key).items())
        else:
            items.append((new_key, i))
    return dict(items)


#Функция, конвертирующая xml в json
def xml_to_json(data: str) -> str:
    """ Конвертирует XML файл в JSON, возвращает строку, содержащую JSON файл

    Аргументы:
    data --  строка, сожержащая XML файл
    """
    xml_dict: dict = xmltodict.parse(data)
    final_dict: dict = flatten_dict(xml_dict)

    drop: List[str] = []
    add: List[list] = []
    for key, item in final_dict.items():
        if ("xsi" in key):
            drop.append(key)
        if (key in xml_json_dict):
            add.append([xml_json_dict[key], item])
            drop.append(key)

    for key in drop:
        final_dict.pop(key)
    for key, item in add:
        final_dict[key] = item

    json_data = json.dumps(final_dict, allow_nan=True, indent=' ')

    return json_data



#Функция для валидации xml файла по xsd
def validation_xml(xml_data: str, path: str) -> None:
    """ Проводит валидацию XML файла по XML-схеме

    Аргументы:
    xml_data --  строка, сожержащая XML файл
    path -- строка, содержащая путь XML-схемы
    """
    schema = ET.XMLSchema(file=path)
    print("val")
    try:
        schema.assertValid(ET.fromstring(xml_data))
        print("XML-схема валидна.")
    except ET.DocumentInvalid as e:
        print("XML-схема не валидна. Ошибка: ", e)

    return None
