from lxml import etree as ET
import json
import xmltodict
from typing import List

#пути к используемым файлам
xsd_add = "./sources/Add_Entrant_List.xsd"
xsd_get = "./sources/Get_Entrant_List_2.xsd"
xsd_add_example = "./sources/Add_example.xml"
fields_class = "./sources/dict_document_type_cls.json"
xml_example = "./sources/Get_example.xml"

xml_json_dict: dict[str, str] = {"SubdivisionCode": "passport_org_code",
            "IdOksm": "residence_country_id",
            "Surname": "second_name",
            "Name": "first_name",
            "Patronymic": "middle_name",
            "IdDocumentType": "passport_type_id",
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
            #"City":"city",
            "IdJwt": "id",
            "Fui": "photo_id",
          }




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
    flat_dict: dict = flatten_dict(xmltodict.parse(data))
    for key, item in flat_dict.items():
        print(key,':',item)

    final_dict: dict = {}

    for key, item in flat_dict.items():
        if (key in xml_json_dict):
            final_dict[xml_json_dict[key]] = item

    if "Address" in flat_dict.keys():
        num = "1"
        for adr in flat_dict["Address"]:
            if adr["IsRegistration"] == "true":
                final_dict["address_txt1"] = adr["FullAddr"]
                final_dict["city"] = adr["City"]
            else:
                final_dict["has_another_living_address"] = "true"
                final_dict["address_txt" + str(int(num) + 1)] = adr["FullAddr"]
                num = str(int(num) + 1)
    elif "FullAddr" in flat_dict.keys():
        final_dict["address_txt1"] = flat_dict["FullAddr"]
        final_dict["city"] = flat_dict["City"]
        final_dict["has_another_living_address"] = "false"



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
