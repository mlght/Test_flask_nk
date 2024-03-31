# Сервис конверации
## Flask test
### Приложение для конвертации данных, переданных в POST запросе (xml->json, json->xml)

Изменение данных в файле 'App_info.json'
| Ключ | Новое значение |
| ----------- | ----------- |
| birthday   | 2005-07-08  |
| passport_begda    | 2019-09-08   |
|  old_passport_begda|1111-11-11 |
|diploma_date|2000-10-10|
|user_id|3878111111|

### Пример выходных данных:
- json-> xml
```xml
<EntrantChoice xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="example_schema.xsd">
    <Guid>3878111111</Guid>
    <AddEntrant>
        <Identification>
            <IdDocumentType>1</IdDocumentType>
            <DocName>Паспорт гражданина Российской Федерации</DocName>
            <DocSeries>5661</DocSeries>
            <DocNumber>111111</DocNumber>
            <IssueDate>2019-09-08</IssueDate>
            <DocOrganization>МВД-АВОР.ПРДЛПАРОДАЬЕК</DocOrganization>
            <SubdivisionCode>111-111</SubdivisionCode>
            <IdOksm>185</IdOksm>
            <Surname>Яруллин</Surname>
            <Name>Максим</Name>
            <Patronymic>None</Patronymic>
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
                <City> Sample City </City>
            </Address>
        </AddressList>
    </AddEntrant>
</EntrantChoice>
```

- xml->json
``` json
{
"IdJwt": "123456",
"EntityAction": "Campaign_Add",
"IdObject": "789",
"Snils": "12345678901",
"Birthday": "2000-01-01",
"Email": "sample@example.com",
"AvailabilityEduDoc": "true",
"DateAvailabilityEduDoc": "2024-03-30T12:00:00+03:00",
"IdFreeEducationReason": "1",
"IdOksmFreeEducationReason": "1",
"IsRegistration": "true",
"FullAddr": "Sample Address",
"IdRegion": "1",
"City": "Sample City",
"Document": [
{
"Guid": "DocumentGuid123",
"FileHash": "SampleFileHash",
"IdDocumentType": "1",
"DocName": "SampleDocumentName",
"DocSeries": "ABC",
"DocNumber": "123456",
"IssueDate": "2020-01-01",
"DocOrganization": "SampleOrganization",
"IdCheckStatus": "1",
"IdAchievementCategory": "1"
},
{
"Guid": "DocumentGuid3445",
"FileHash": "SampleFileHash2",
"IdDocumentType": "2",
"DocName": "SampleDocumentName3",
"DocSeries": "12341",
"DocNumber": "123453",
"IssueDate": "2020-01-01",
"DocOrganization": "SampleOrganization4",
"IdCheckStatus": "1",
"IdAchievementCategory": "1"
}
],
"FileHash": "SamplePhotoHash",
"Fui": "SampleFui123",
"user_id": "SampleGuid123",
"dict_sex_id": "1",
"motherland": "Sample Birthplace",
"tel_mobile": "123456789",
"second_name": "SampleSurname",
"first_name": "SampleName",
"middle_name": "SamplePatronymic",
"residence_country_id": "1"
}
```


## Инструкция по запуску
```
$ python3 -m pip install -r requirements.txt
$ python3 TestFl
```

Для конвертации необходимо отправить POST запрос по адресу http://127.0.0.1:5000/convert
В теле запроса передать json/xml файл для конвертации. Направление определяется автоматически
При необходимости валидации xml, добавить в адрес параметр '?validation=1'