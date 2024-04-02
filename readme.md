# Сервис конверации
## Flask test
### Приложение для конвертации данных, переданных в POST запросе (xml->json, json->xml)

Изменение данных в файле 'App_info.json'
| Ключ | Новое значение |
| ----------- | ----------- |
| birthday   | 2005-07-08  |
| passport_begda    | 2019-09-08   |
|  old_passport_begda|1111-11-11 |
|city(добавление ключа)| "Астана""|
|diploma_date|2000-10-10|
|user_id|3878111111|
|passport_type_id| 100001|

### Пример выходных данных:
- json-> xml
```xml
<EntrantChoice xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="example_schema.xsd">
    <Guid>3878</Guid>
    <AddEntrant>
        <Identification>
            <IdDocumentType>100001</IdDocumentType>
            <DocName>Паспорт гражданина Российской Федерации</DocName>
            <DocSeries>5661</DocSeries>
            <DocNumber>111111</DocNumber>
            <IssueDate>2019-09-08</IssueDate>
            <DocOrganization>МВД-АВОР.ПРДЛПАРОДАЬЕК</DocOrganization>
            <Field>
                <SubdivisionCode>111-111</SubdivisionCode>
                <IdOksm>185</IdOksm>
                <Surname>Яруллин</Surname>
                <Name>Максим</Name>
                <Patronymic>None</Patronymic>
            </Field>
        </Identification>
        <Snils> 12345678901 </Snils>
        <IdGender>1</IdGender>
        <Birthday> 2000-01-01 </Birthday>
        <Birthplace>Россия Г.Астана</Birthplace>
        <Phone>+7 (888) 888-88-88</Phone>
        <Email> sample@example.com </Email>
        <IdOksm>185</IdOksm>
        <AddressList>
            <Address>
                <IsRegistration> true </IsRegistration>
                <FullAddr>Могилевская область тестовый дом</FullAddr>
                <IdRegion>22</IdRegion>
                <City>Астана</City>
            </Address>
        </AddressList>
    </AddEntrant>
</EntrantChoice>
```

- xml->json
``` json
{
"id": "123456",
"user_id": "DocumentGuid123",
"dict_sex_id": "1",
"motherland": "Sample Birthplace",
"tel_mobile": "123456789",
"second_name": "SampleSurname",
"first_name": "SampleName",
"middle_name": "SamplePatronymic",
"residence_country_id": "1",
"passport_type_id": "1",
"passport_series": "ABC",
"passport_number": "123456",
"passport_begda": "2020-01-01",
"passport_issued_by": "SampleOrganization",
"photo_id": "SampleFui123",
"address_txt1": "Sample Address",
"city": "Sample City",
"has_another_living_address": "true",
"address_txt2": "Sample Address 2"
}
```


## Инструкция по запуску
```
$ python3 -m pip install -r requirements.txt
$ python3 TestFl
```

Для конвертации необходимо отправить POST запрос по адресу http://127.0.0.1:5000/convert_json_to_xml или http://127.0.0.1:5000/convert_xml_to_json.

В теле запроса передать json/xml файл для конвертации. 

При необходимости валидации xml, добавить в адрес параметр "?validation=1".