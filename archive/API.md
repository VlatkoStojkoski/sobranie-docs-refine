## General API Format
* URL: `https://www.sobranie.mk/Routing/MakePostRequest`
* Method: `POST`
* Request body:
```
{
    "methodName": METHOD_NAME,
    "languageId": LANGUAGE_ID
}
```
* Note: Some endpoints use a different URL and request/response format (see non-standard methods below).
* **Date format**: All date fields use Microsoft JSON format `/Date(timestamp)/` where `timestamp` is milliseconds since Unix epoch.
* **LanguageId**: 1 = Macedonian (Македонски), 2 = Albanian (Shqip), 3 = Turkish (Türkçe). Used for localized content.

## Reusable Schemas

```json
{
  "$defs": {
    "AspDate": {
      "type": "string",
      "pattern": "^/Date\\(\\d+\\)/$"
    },
    "GenderId": {
      "type": "integer",
      "enum": [1, 2],
      "description": "1 = Male (Машки), 2 = Female (Женски)"
    },
    "QuestionStatusId": {
      "type": "integer",
      "enum": [17, 19, 20, 21],
      "description": "17 = Delivered (Доставено), 19 = Answered (Одговорено), 20 = Secret answer (Таен одговор), 21 = Written answer (Писмен одговор)"
    },
    "RoleId": {
      "type": "integer",
      "enum": [1],
      "description": "TBD"
    },
    "SittingStatusId": {
      "type": "integer",
      "enum": [1, 2, 3, 4, 5, 6],
      "description": "1 = Scheduled (Закажана), 2 = Started (Започната), 3 = Completed (Завршена), 4 = Incomplete (Незавршена), 5 = Closed (Затворена), 6 = Postponed (Одложена)"
    },
    "AgendaItemTypeId": {
      "type": "integer",
      "enum": [1, 2],
      "description": "1 = Plenary session (Собрание), 2 = Committee session (Комисија)"
    },
    "EventTypeId": {
      "type": "integer",
      "enum": [5],
      "description": "TBD"
    },
    "DocumentTypeId": {
      "type": "integer",
      "enum": [19, 20, 40, 42, 43, 44, 51, 52, 53, 57, 59, 64, 71, 72],
      "description": "19 = Decision to convene sitting (Решение за свикување седницa), 20 = Notice of sitting convening (Известување за свикување на седница), 40 = Notice of sitting rescheduling (Известување за презакажување на седница), 42 = Notice of sitting continuation (Известување за продолжување на седница), 43 = Notice of agenda supplement (Известување за дополнување на дневен ред), 44 = Session conclusion (Заклучок од седница), 51 = Notice of committee sitting postponement (Известување за одложување на комисиска седница), 52 = Report (Извештај), 53 = TBD, 57 = Transcript (Стенограм), 59 = Minutes (Записник), 64 = TBD, 71 = Full text of material (Целосен текст на материјалот), 72 = Document (Документ)"
    },
    "DescriptionTypeId": {
      "type": "integer",
      "enum": [1, 2],
      "description": "1 = Committee sitting (Комисиска седница), 2 = Public hearing (Јавна расправа)"
    },
    "MaterialStatusId": {
      "type": "integer",
      "enum": [0, 6, 9, 10, 11, 12, 24, 64],
      "description": "0 = Plenary/unknown (used for StatusGroupId/ObjectStatusId in plenary sittings), 6 = Delivered to MPs (Доставен до пратеници), 9 = First reading (Прво читање), 10 = Second reading (Второ читање), 11 = Third reading (Трето читање), 12 = Closed (Затворен), 24 = Rejected (Одбиен), 64 = Committee processing (Обработка кај комисија)"
    },
    "ProposerTypeId": {
      "type": "integer",
      "enum": [1, 2, 4],
      "description": "1 = MP (Пратеник), 2 = Government (Влада на Република Северна Македонија), 4 = Voter group (Група избирачи)"
    },
    "MaterialTypeId": {
      "type": "integer",
      "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
      "description": "Material type IDs; titles from GetAllMaterialTypesForFilter (e.g. 1 = Предлог закон, 2 = Интерпелација, 24 = Друго)"
    },
    "ProcedureTypeId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1 = Regular procedure (Редовна постапка), 2 = Shortened procedure (Скратена постапка), 3 = Urgent procedure (Итна постапка)"
    },
    "MaterialDocumentTypeId": {
      "type": "integer",
      "enum": [1, 7, 8, 9, 16, 17, 30, 45, 52, 65, 68],
      "description": "Material document types (different from sitting DocumentTypeId): 1 = Document (Документ), 7 = Full text (Целосен текст на материјалот), 8 = Adopted act (Донесен акт), 9 = Notice to MPs (Известување за нов материјал до пратеници), 16 = TBD, 17 = TBD, 30 = TBD, 45 = TBD, 52 = Report (Извештај), 65 = TBD, 68 = TBD"
    },
    "AgendaItemKindId": {
      "type": "integer",
      "enum": [1, 4, 8],
      "description": "Agenda item kind (Agenda.children[].agendaItemType): 1 = Material (Материјал), 4 = Parliamentary questions (Поставување на пратенички прашања), 8 = Amendment"
    },
    "AgendaItemStatusId": {
      "type": "integer",
      "enum": [0, 50, 51, 60, 61, 62, 63, 69],
      "description": "Agenda item status (Agenda.children[].status): 0 = root, 50 = Reviewed (Разгледана), 51 = Not reviewed (Неразгледана), 60/61/62 = amendment, 63 = Withdrawn (Повлечена), 69 = New (Нова)"
    },
    "ObjectTypeId": {
      "type": "integer",
      "enum": [0, 1],
      "description": "Agenda.children[].objectTypeId: 0 = root item, 1 = Material (Материјал)"
    },
    "ObjectSubTypeId": {
      "type": "integer",
      "enum": [1, 8, 22, 28],
      "description": "Material subtype; observed 1, 8, 22, 28 (28 = presidential-related)"
    },
    "VotingOverallResult": {
      "type": "string",
      "enum": ["Усвоен", "Одбиен"],
      "description": "VotingDefinitions/Votings OverallResult: Усвоен (Adopted), Одбиен (Rejected)"
    },
    "TerminationStatusTitle": {
      "type": "string",
      "enum": ["Донесен", "Прифатен", "Разгледан", "Избран", "Констатиран", "Материјалот е повлечен", "Усвоен"],
      "description": "GetMaterialDetails closed materials: Донесен (Adopted), Прифатен (Accepted), Разгледан (Reviewed), Избран (Elected), Констатиран (Noted), Материјалот е повлечен (Withdrawn), Усвоен (Approved)"
    }
  }
}
```

## Common patterns

- **Institutional authors**: `Authors[].Id` = `"00000000-0000-0000-0000-000000000000"` with full name/title in `FirstName`, empty `LastName`. Used for government, committees, other institutions.
- **Plenary vs committee**: `CommitteeId`/`CommitteeTitle` are `null` for plenary (`TypeId`/`SittingTypeId` 1); populated for committee (2).

## Methods

### `GetCustomEventsCalendar` *(non-standard)*
* **Differs from standard format:** Different URL, request body structure, and response wrapper.
* URL: `https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar`
* Request body example:
```json
{
    "model": {
        "Language": 1,
        "Month": 1,
        "Year": 2026
    }
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "__type": { "type": "string" },
          "Id": { "type": "string", "format": "uuid" },
          "EventDescription": { "type": "string" },
          "EventLink": { "type": "string" },
          "EventLocation": { "type": "string" },
          "EventDate": { "$ref": "#/$defs/AspDate" },
          "EventType": { "$ref": "#/$defs/EventTypeId" }
        },
        "required": ["__type", "Id", "EventDescription", "EventLink", "EventLocation", "EventDate", "EventType"]
      }
    }
  },
  "required": ["d"]
}
```
* Response example:
```json
{
    "d": [
        {"__type": "moldova.controls.Models.CalendarViewModel", "Id": "c46c450b-c40f-433e-b733-042cedfb3140", "EventDescription": "Прес-конференција за медиуми", "EventLink": "pres-konferencija-za-mediumi-2312026", "EventLocation": "Прес-центар ", "EventDate": "/Date(1769174100000)/", "EventType": 5}
    ]
}
```
* Notes:
  - **Response wrapper**: Items are in `d` property, not at root.
  - **__type**: Often `"moldova.controls.Models.CalendarViewModel"` (legacy/shared code).
  - **EventLink**: URL slug format; may include date suffixes (e.g. `-2312026`).
  - **EventType**: Only value 5 observed; other values possible.

### `GetAllGenders`
* Request body example:
```
{
    "methodName": "GetAllGenders",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/GenderId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Response example:
```
[
    {"Id": 1, "Title":"Машки" },
    {"Id": 2, "Title":"Женски" }
]
```

### `GetAllSittings`
* Request body example:
```json
{
    "methodName": "GetAllSittings",
    "Page": 1,
    "Rows": 10,
    "LanguageId": 1,
    "TypeId": null,
    "CommitteeId": null,
    "StatusId": null,
    "DateFrom": null,
    "DateTo": null,
    "SessionId": null,
    "Number": null,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "TotalItems": { "type": "integer" },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Number": { "type": "integer" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "TypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
          "TypeTitle": { "type": "string" },
          "StatusId": { "$ref": "#/$defs/SittingStatusId" },
          "StatusTitle": { "type": "string" },
          "Location": { "type": "string" },
          "CommitteeTitle": { "type": ["string", "null"] },
          "SittingDescriptionTypeTitle": { "type": ["string", "null"] },
          "Continuations": { "type": "array", "items": {} },
          "Structure": { "type": ["object", "null"] },
          "TotalRows": { "type": "integer" }
        },
        "required": ["Id", "Number", "SittingDate", "TypeId", "TypeTitle", "StatusId", "StatusTitle", "Location", "CommitteeTitle", "SittingDescriptionTypeTitle", "Continuations", "Structure", "TotalRows"]
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```
* Response example:
```json
{
    "TotalItems": 677,
    "Items": [
        {"Id": "8811dffb-8d40-4e16-9a72-a51f4eac33e7", "Number": 85, "SittingDate": "/Date(1771408800000)/", "TypeId": 1, "TypeTitle": "Пленарна седница", "StatusId": 1, "StatusTitle": "Закажана", "Location": "Сала „Македонија“", "CommitteeTitle": null, "SittingDescriptionTypeTitle": null, "Continuations": [], "Structure": null, "TotalRows": 0},
        {"Id": "05ca599c-b1ab-4671-8cf8-538d1c16b565", "Number": 143, "SittingDate": "/Date(1770717600000)/", "TypeId": 2, "TypeTitle": "Комисиска седница", "StatusId": 1, "StatusTitle": "Закажана", "Location": "Сала 6", "CommitteeTitle": "Законодавно-правна комисија", "SittingDescriptionTypeTitle": "Комисиска седница", "Continuations": [], "Structure": null, "TotalRows": 0}
    ]
}
```
* Notes:
  - **TypeId**: See `AgendaItemTypeId`. Use null for mixed.
  - **CommitteeId**: Filter by committee (UUID from `GetAllCommitteesForFilter`). Use null for all.
  - **StatusId**, **DateFrom**, **DateTo**, **SessionId**, **Number**: Optional filters.
  - **CommitteeTitle**: Populated for committee sittings; null for plenary (see Common patterns).
  - **Structure**: Consistently `null` in list items; populated in `GetSittingDetails` with parliamentary term (e.g. "2024-2028").
  - **TotalRows**: Always `0`; purpose unclear.
  - **Continuations**: Often empty `[]`; populated when sitting has continuations.

### `GetSittingDetails`
* Request body example (uses `MethodName` and `SittingId`, not `methodName`):
```json
{
    "MethodName": "GetSittingDetails",
    "SittingId": "8811dffb-8d40-4e16-9a72-a51f4eac33e7",
    "LanguageId": 1
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "StatusId": { "$ref": "#/$defs/SittingStatusId" },
    "StatusTitle": { "type": "string" },
    "Location": { "type": "string" },
    "Number": { "type": "integer" },
    "SittingDate": { "$ref": "#/$defs/AspDate" },
    "TypeTitle": { "type": "string" },
    "TypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
    "CommitteeId": { "type": ["string", "null"] },
    "CommitteeTitle": { "type": ["string", "null"] },
    "MediaLinks": { "type": "array", "items": {} },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "Url": { "type": "string" },
          "FileName": { "type": ["string", "null"] },
          "DocumentTypeId": { "$ref": "#/$defs/DocumentTypeId" },
          "DocumentTypeTitle": { "type": "string" },
          "IsExported": { "type": "boolean" }
        },
        "required": ["Id", "Title", "Url", "FileName", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      }
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "beforeText": { "type": ["string", "null"] },
        "afterText": { "type": ["string", "null"] },
        "text": { "type": "string" },
        "type": { "type": "string" },
        "treeItemTypeId": { "type": ["integer", "null"] },
        "agendaItemType": { "type": ["integer", "null"] },
        "status": { "type": "integer" },
        "statusTitle": { "type": ["string", "null"] },
        "isActive": { "type": "boolean" },
        "order": { "type": "integer" },
        "euCompatible": { "type": "boolean" },
        "data": { "type": ["string", "null"] },
        "children": { "type": "array", "items": {} },
        "objectId": { "type": ["string", "null"] },
        "objectTypeId": { "type": ["integer", "null"] },
        "objectTypeTitle": { "type": ["string", "null"] },
        "objectStatusId": { "type": ["integer", "null"] },
        "objectSubTypeId": { "type": ["integer", "null"] },
        "manyAmendments": { "type": "boolean" },
        "mediaItems": { "type": "array" },
        "VotingDefinitions": { "type": "array" },
        "Documents": { "type": "array" }
      }
    },
    "Continuations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Number": { "type": "integer" },
          "StatusId": { "type": ["integer", "null"] },
          "StatusTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "Location": { "type": "string" }
        }
      }
    },
    "SittingDuration": { "type": ["string", "number", "null"] },
    "Absents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Fullname": { "type": "string" },
          "PoliticalParty": { "type": ["string", "null"] }
        },
        "required": ["Id", "Fullname"]
      }
    },
    "Attendances": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Fullname": { "type": "string" },
          "PoliticalParty": { "type": ["string", "null"] }
        }
      }
    },
    "DescriptionTypeTitle": { "type": ["string", "null"] },
    "DescriptionTypeId": { "oneOf": [{ "type": "null" }, { "$ref": "#/$defs/DescriptionTypeId" }] },
    "Votings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "Description": { "type": "string" },
          "VotingType": { "type": "string" },
          "OverallResult": { "type": "string" }
        }
      }
    },
    "Structure": { "type": ["string", "null"] }
  },
  "required": ["StatusId", "StatusTitle", "Location", "Number", "SittingDate", "TypeTitle", "TypeId", "CommitteeId", "CommitteeTitle", "MediaLinks", "Documents", "Agenda", "Continuations", "SittingDuration", "Absents", "Attendances", "DescriptionTypeTitle", "DescriptionTypeId", "Votings", "Structure"]
}
```
* Response example:
```json
{
    "StatusId": 1,
    "StatusTitle": "Закажана",
    "Location": "Сала „Македонија“",
    "Number": 85,
    "SittingDate": "/Date(1771408800000)/",
    "TypeId": 1,
    "TypeTitle": "Пленарна седница",
    "CommitteeId": null,
    "CommitteeTitle": null,
    "Documents": [{"Id": "eb4a551b-7d59-4248-82a8-1bc0f050ad6d", "Title": "Решение за свикување седницa", "Url": "https://sp.sobranie.mk/...", "FileName": null, "DocumentTypeId": 19, "DocumentTypeTitle": "Решение за свикување седницa", "IsExported": true}],
    "Absents": [{"Id": "85048fa9-e61b-4eb1-be26-8d537cb1d7c4", "Fullname": "Аднан Азизи", "PoliticalParty": "Движење БЕСА"}],
    "Structure": "2024-2028"
}
```

#### Extra notes and patterns

- **TypeTitle vs TypeId**: `TypeTitle` can differ for the same `TypeId` (e.g. `TypeId` 2 may be "Комисиска седница" or "Јавна расправа"). `DescriptionTypeId` reflects the more specific subtype.
- **Attendances vs Absents**: Committee sittings often have empty `Attendances` and populated `Absents`; plenary sittings typically have both.
- **Continuations**: `StatusId` can be null even when `StatusTitle` is present. `Number` can be 0.
- **Structure**: Indicates parliamentary term (e.g. `"2024-2028"`).
- **Document titles**: May include carriage returns (`\r\n`).
- **Agenda structure**: Root is `type: "ROOT"`; children are `type: "LEAF"`. `children` is recursive.
- **Agenda multilingual text**: `afterText` uses tags like `<MK>…</MK><AL>…</AL><EN>…</EN><FR>…</FR>` for Macedonian, Albanian, English, French.
- **Agenda data**: The `data` field often contains HTML (e.g. `<div>…</div>`).
- **Agenda children IDs**: `agendaItemType` → `AgendaItemKindId`; `status` → `AgendaItemStatusId`; `objectTypeId` → `ObjectTypeId`; `objectSubTypeId` → `ObjectSubTypeId`.
- **DocumentTypeId location**: Values like 71, 44, 52, 53, 64 appear in `Agenda.children[].Documents`, not in top-level `Documents`.
- **Agenda `euCompatible`**, **`manyAmendments`**: Boolean flags. `euCompatible` = EU legislation compatibility; `manyAmendments` threshold undefined.
- **VotingDefinitions vs Votings**: `Agenda.children[].VotingDefinitions` mirrors top-level `Votings`. `VotingType`: "Јавно" (Public). `OverallResult`: See `VotingOverallResult`.
- **FileName**: Consistently `null`; use `Title` and `Url`.
- **SittingDuration**: Often `null`.
- **Agenda children schema**: Some items may omit fields (objectId, VotingDefinitions, Documents, etc.); treat as optional.

### `GetAllStructuresForFilter`
* Request body example:
```json
{
    "methodName": "GetAllStructuresForFilter",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "DateFrom": { "$ref": "#/$defs/AspDate" },
      "DateTo": { "$ref": "#/$defs/AspDate" },
      "IsCurrent": { "type": "boolean" }
    },
    "required": ["Id", "DateFrom", "DateTo", "IsCurrent"]
  }
}
```
* Response example:
```json
[
    {"Id": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473", "DateFrom": "/Date(1725141600000)/", "DateTo": "/Date(1851372000000)/", "IsCurrent": true},
    {"Id": "09f340db-6cfa-4b40-8439-48ebe97d46ec", "DateFrom": "/Date(1596232800000)/", "DateTo": "/Date(1725055200000)/", "IsCurrent": false},
    {"Id": "f824d503-ebdb-412f-a231-40c390060f0f", "DateFrom": "/Date(1467324000000)/", "DateTo": "/Date(1596146400000)/", "IsCurrent": false},
    {"Id": "f60fa001-b769-4e7e-93bd-debbaef43fd2", "DateFrom": "/Date(1399413600000)/", "DateTo": "/Date(1462572000000)/", "IsCurrent": false},
    {"Id": "37be4494-20cc-4007-8dc4-fa36a1ea82cb", "DateFrom": "/Date(1307311200000)/", "DateTo": "/Date(1399327200000)/", "IsCurrent": false},
    {"Id": "f4903d12-f855-4d37-8842-5b702c28aae7", "DateFrom": "/Date(1220220000000)/", "DateTo": "/Date(1307224800000)/", "IsCurrent": false}
]
```
* Notes:
  - **No Title/Name**: Unlike other catalogs; DateFrom/DateTo represent parliamentary term period.

### `GetAllCommitteesForFilter`
* Request body example:
```json
{
    "methodName": "GetAllCommitteesForFilter",
    "languageId": 1,
    "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Name": { "type": "string" }
    },
    "required": ["Id", "Name"]
  }
}
```
* Response example:
```json
[
    {"Id": "19594193-2911-4164-9073-4de1f1673049", "Name": "Комисија за прашања на изборите и именувањата"},
    {"Id": "5c5c22fc-eeb5-4bb6-8a0a-638c25fe3223", "Name": "Комисија за финансирање и буџет"},
    {"Id": "bb8e23a1-c959-4818-8e6e-ebe450847fd8", "Name": "Законодавно-правна комисија"}
]
```
* Notes:
  - **structureId**: From `GetAllStructuresForFilter`. Committees are per assembly term.

### `GetAllMaterialStatusesForFilter`
* Request body example:
```json
{
    "methodName": "GetAllMaterialStatusesForFilter",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/MaterialStatusId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Response example:
```json
[
    {"Id": 6, "Title": "Доставен до пратеници"},
    {"Id": 9, "Title": "Прво читање"},
    {"Id": 10, "Title": "Второ читање"},
    {"Id": 11, "Title": "Трето читање"},
    {"Id": 12, "Title": "Затворен"},
    {"Id": 24, "Title": "Одбиен"},
    {"Id": 64, "Title": "Обработка кај комисија"}
]
```

### `GetAllMaterialTypesForFilter`
* Request body example:
```json
{
    "methodName": "GetAllMaterialTypesForFilter",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/MaterialTypeId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Response example:
```json
[
    {"Id": 1, "Title": "Предлог закон"},
    {"Id": 2, "Title": "Интерпелација"},
    {"Id": 3, "Title": "Избор на Влада"},
    {"Id": 4, "Title": "Автентично толкување на закон"},
    {"Id": 5, "Title": "Пречистен текст на закон"},
    {"Id": 6, "Title": "Буџет"},
    {"Id": 7, "Title": "Деловник"},
    {"Id": 8, "Title": "Декларација, резолуција, одлука и препорака"},
    {"Id": 9, "Title": "Согласност на статути и други општи акти"},
    {"Id": 10, "Title": "Ратификација на меѓународни договори"},
    {"Id": 11, "Title": "Граѓанска иницијатива"},
    {"Id": 13, "Title": "Предлог за утврдување на одговорност на Претседател на Република"},
    {"Id": 14, "Title": "Доверба на Влада"},
    {"Id": 15, "Title": "Оставка на Влада"},
    {"Id": 24, "Title": "Друго"},
    {"Id": 28, "Title": "Анализи, извештаи, информации и друг материјал"}
]
```
* Notes:
  - IDs 12 and 25 are not present in the API response.

### `GetAllMaterialsForPublicPortal`
* Request body example (uses `MethodName` and `LanguageId`, not `methodName` and `languageId`):
```json
{
    "MethodName": "GetAllMaterialsForPublicPortal",
    "LanguageId": 1,
    "ItemsPerPage": 15,
    "CurrentPage": 1,
    "SearchText": "",
    "AuthorText": "",
    "ActNumber": "",
    "StatusGroupId": null,
    "MaterialTypeId": null,
    "ResponsibleCommitteeId": null,
    "CoReportingCommittees": null,
    "OpinionCommittees": null,
    "RegistrationNumber": null,
    "EUCompatible": null,
    "DateFrom": null,
    "DateTo": null,
    "ProcedureTypeId": null,
    "InitiatorTypeId": null,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "TotalItems": { "type": "integer" },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "TypeTitle": { "type": "string" },
          "Status": { "type": ["string", "null"] },
          "StatusGroupTitle": { "type": "string" },
          "RegistrationNumber": { "type": "string" },
          "RegistrationDate": { "$ref": "#/$defs/AspDate" },
          "ResponsibleAuthor": { "type": ["string", "null"] },
          "Authors": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": { "type": "string", "format": "uuid" },
                "FirstName": { "type": "string" },
                "LastName": { "type": "string" }
              },
              "required": ["Id", "FirstName", "LastName"]
            }
          },
          "ProposerTypeTitle": { "type": "string" },
          "ResponsibleCommittee": { "type": "string" },
          "EUCompatible": { "type": "boolean" },
          "TotalItems": { "type": ["integer", "null"] }
        },
        "required": ["Id", "Title", "TypeTitle", "Status", "StatusGroupTitle", "RegistrationNumber", "RegistrationDate", "ResponsibleAuthor", "Authors", "ProposerTypeTitle", "ResponsibleCommittee", "EUCompatible", "TotalItems"]
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```
* Response example:
```json
{
    "TotalItems": 976,
    "Items": [
        {
            "Id": "c09a44ca-f2bb-4298-8672-0bbe3b62322f",
            "Title": "Предлог за именување на (непрофесионално ангажиран) член на Советот на експерти на Агенцијата за супервизија на осигурување",
            "TypeTitle": "Избори, именување и разрешување на јавни и други функции",
            "Status": null,
            "StatusGroupTitle": "Доставен до пратеници",
            "RegistrationNumber": "08-750/1",
            "RegistrationDate": "/Date(1770024442000)/",
            "ResponsibleAuthor": "д-р Христијан Мицкоски",
            "Authors": [{"Id": "00000000-0000-0000-0000-000000000000", "FirstName": "д-р Христијан Мицкоски", "LastName": ""}],
            "ProposerTypeTitle": "Влада на Република Северна Македонија",
            "ResponsibleCommittee": "",
            "EUCompatible": false,
            "TotalItems": null
        },
        {
            "Id": "7b876eb2-2eef-4584-8953-8ab1f9fb2dce",
            "Title": "Предлог на закон за дополнување на Законот за здравствената заштита, по скратена постапка",
            "TypeTitle": "Предлог закон",
            "Status": null,
            "StatusGroupTitle": "Второ читање",
            "RegistrationNumber": "08-674/1",
            "RegistrationDate": "/Date(1769691810000)/",
            "ResponsibleAuthor": "Димитар Апасиев",
            "Authors": [{"Id": "4eeadcc4-4b7b-4708-ae9b-1ebf1c0a25f9", "FirstName": "Димитар", "LastName": "Апасиев"}],
            "ProposerTypeTitle": "Пратеник",
            "ResponsibleCommittee": "Комисија за здравство",
            "EUCompatible": false,
            "TotalItems": null
        }
    ]
}
```
* Notes:
  - **StructureId**: From `GetAllStructuresForFilter`. Required.
  - **StatusGroupId**: Filter by material status group (from `GetAllMaterialStatusesForFilter`).
  - **MaterialTypeId**: Filter by material type (from `GetAllMaterialTypesForFilter`).
  - **ResponsibleCommitteeId**: Filter by committee (UUID from `GetAllCommitteesForFilter`).
  - **ProcedureTypeId**: Filter by procedure type (from `GetAllProcedureTypes`).
  - **InitiatorTypeId**: Filter by proposer type (from `GetProposerTypes`).
  - **ProposerTypeTitle**: May include values beyond `GetProposerTypes` (e.g. "Работно тело", "Друга институција").
  - **Filter coverage**: StatusGroupId=64, 24, 11 may return 0 results depending on current data.
  - **Status**: Consistently `null`; `StatusGroupTitle` holds the status text.
  - **TotalItems** (at item level): Always `null`; root-level `TotalItems` is used for pagination.
  - **Authors**: See Common patterns (institutional authors).

### `GetMaterialDetails`
* Request body example:
```json
{
    "methodName": "GetMaterialDetails",
    "MaterialId": "1b2114f3-72ff-43b5-887e-17316e501592",
    "LanguageId": 1,
    "AmendmentsPage": 1,
    "AmendmentsRows": 5
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "Title": { "type": "string" },
    "StatusGroupTitle": { "type": "string" },
    "TypeTitle": { "type": "string" },
    "ProposerTypeTitle": { "type": "string" },
    "ResponsibleAuthor": { "type": ["string", "null"] },
    "Institution": { "type": "string" },
    "ProposerCommittee": { "type": ["string", "object", "null"] },
    "ProcedureTypeTitle": { "type": "string" },
    "RegistrationNumber": { "type": "string" },
    "RegistrationDate": { "$ref": "#/$defs/AspDate" },
    "EUCompatible": { "type": "boolean" },
    "ParentTitle": { "type": "string" },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Name": { "type": "string" },
          "IsLegislative": { "type": "boolean" },
          "IsResponsible": { "type": "boolean" },
          "Documents": { "type": "array", "items": {} }
        },
        "required": ["Id", "Name", "IsLegislative", "IsResponsible", "Documents"]
      }
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "Url": { "type": "string" },
          "FileName": { "type": ["string", "null"] },
          "DocumentTypeId": { "$ref": "#/$defs/MaterialDocumentTypeId" },
          "DocumentTypeTitle": { "type": "string" },
          "IsExported": { "type": "boolean" }
        },
        "required": ["Id", "Title", "Url", "FileName", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      }
    },
    "FirstReadingAmendments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "ProposerTypeTitle": { "type": "string" },
          "ResponsibleAuthor": { "type": ["string", "null"] },
          "StatusId": { "type": "integer" },
          "StatusTitle": { "type": "string" },
          "ParentStatusId": { "type": "integer" },
          "Authors": { "type": "array", "items": {} }
        }
      }
    },
    "SecondReadingAmendments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "ProposerTypeTitle": { "type": "string" },
          "ResponsibleAuthor": { "type": ["string", "null"] },
          "StatusId": { "type": "integer" },
          "StatusTitle": { "type": "string" },
          "ParentStatusId": { "type": "integer" },
          "Authors": { "type": "array", "items": {} }
        }
      }
    },
    "FirstReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "SittingTypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
          "SittingTypeTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "CommitteeId": { "type": ["string", "null"] },
          "CommitteeTitle": { "type": ["string", "null"] },
          "StatusGroupId": { "type": "integer" },
          "ObjectStatusId": { "type": "integer" },
          "SittingTitle": { "type": "string" },
          "SittingNumber": { "type": "integer" },
          "VotingResults": { "type": "array" }
        }
      }
    },
    "SecondReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "SittingTypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
          "SittingTypeTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "CommitteeId": { "type": ["string", "null"] },
          "CommitteeTitle": { "type": ["string", "null"] },
          "StatusGroupId": { "type": "integer" },
          "ObjectStatusId": { "type": "integer" },
          "SittingTitle": { "type": "string" },
          "SittingNumber": { "type": "integer" },
          "VotingResults": { "type": "array" }
        }
      }
    },
    "ThirdReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "SittingTypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
          "SittingTypeTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "CommitteeId": { "type": ["string", "null"] },
          "CommitteeTitle": { "type": ["string", "null"] },
          "StatusGroupId": { "type": "integer" },
          "ObjectStatusId": { "type": "integer" },
          "SittingTitle": { "type": "string" },
          "SittingNumber": { "type": "integer" },
          "VotingResults": { "type": "array" }
        }
      }
    },
    "Sittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "SittingTypeId": { "$ref": "#/$defs/AgendaItemTypeId" },
          "SittingTypeTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "CommitteeId": { "type": ["string", "null"] },
          "CommitteeTitle": { "type": ["string", "null"] },
          "StatusGroupId": { "type": "integer" },
          "ObjectStatusId": { "type": "integer" },
          "SittingTitle": { "type": "string" },
          "SittingNumber": { "type": "integer" },
          "VotingResults": { "type": "array" }
        }
      }
    },
    "Authors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "FirstName": { "type": "string" },
          "LastName": { "type": "string" }
        },
        "required": ["Id", "FirstName", "LastName"]
      }
    },
    "IsWithdrawn": { "type": "boolean" },
    "TerminationStatusTitle": { "type": ["string", "null"] },
    "TerminationNote": { "type": ["string", "null"] },
    "TerminationDate": { "type": ["string", "null"] },
    "AmendmentsTotalRows": { "type": "integer" }
  }
}
```
* Response example:
```json
{
    "Title": "Извештај за работата на Регулаторна комисија за домување од 01.07.2025  до 31.12.2025 година",
    "StatusGroupTitle": "Доставен до пратеници",
    "TypeTitle": "Анализи, извештаи, информации и друг материјал",
    "ProposerTypeTitle": "Друга институција",
    "ResponsibleAuthor": "Регулаторна комисија за домување",
    "Institution": "",
    "ProposerCommittee": null,
    "ProcedureTypeTitle": "Редовна постапка",
    "RegistrationNumber": "08-535/1",
    "RegistrationDate": "/Date(1769161701000)/",
    "EUCompatible": false,
    "ParentTitle": "",
    "Committees": [{"Id": "bd4ee825-8799-406c-bb19-73a2ea198c7b", "Name": "Комисија за транспорт, дигитална трансформација, животна средина и просторно планирање", "IsLegislative": false, "IsResponsible": true, "Documents": []}],
    "Documents": [{"Id": "e60a2f7e-258c-489b-92d3-6fe41d6d7559", "Title": "Целосен текст на материјалот...", "Url": "https://sp.sobranie.mk/sites/2023/materials/...", "FileName": null, "DocumentTypeId": 7, "DocumentTypeTitle": "Целосен текст на материјалот", "IsExported": true}],
    "FirstReadingAmendments": [],
    "SecondReadingAmendments": [],
    "FirstReadingSittings": [],
    "SecondReadingSittings": [],
    "ThirdReadingSittings": [],
    "Sittings": [{"Id": "e1d82671-dc29-4c3b-9ff9-aa7c58fe96d6", "SittingTypeId": 2, "SittingTypeTitle": "Комисиска седница", "SittingDate": "/Date(1770120000000)/", "CommitteeId": "bd4ee825-8799-406c-bb19-73a2ea198c7b", "CommitteeTitle": "Комисија за транспорт, дигитална трансформација, животна средина и просторно планирање", "StatusGroupId": 6, "ObjectStatusId": 6, "SittingTitle": "52. седница на Комисија за транспорт...", "SittingNumber": 52, "VotingResults": []}],
    "Authors": [{"Id": "00000000-0000-0000-0000-000000000000", "FirstName": "Регулаторна комисија за домување", "LastName": ""}],
    "IsWithdrawn": false,
    "TerminationStatusTitle": null,
    "TerminationNote": null,
    "TerminationDate": null,
    "AmendmentsTotalRows": 0
}
```
* Notes:
  - **MaterialId**: UUID from `GetAllMaterialsForPublicPortal` items.
  - **AmendmentsPage**, **AmendmentsRows**: Pagination for amendments.
  - **Documents.DocumentTypeId**: See `MaterialDocumentTypeId`.
  - **Sittings CommitteeId/CommitteeTitle**: See Common patterns (plenary vs committee). Same for `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings`.
  - **ResponsibleAuthor**: Can be `null` for materials proposed by "Работно тело" (working body).
  - **Authors**: Can be empty for institutional proposers. See Common patterns.
  - **Institution**: May be empty string or "/"; `ResponsibleAuthor` often contains the actual institution name.
  - **Committees**: Can be empty when `ProposerCommittee` is populated (e.g. "Работно тело" proposers). `ProposerCommittee` is a string (committee name) when `ProposerTypeTitle` is "Работно тело".
  - **Reading-specific arrays**: `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings` may contain data while `Sittings` is empty; reading-specific arrays take precedence.
  - **StatusGroupId/ObjectStatusId**: Can be `0` for plenary sittings (see `MaterialStatusId` 0).
  - **TerminationStatusTitle**: See `TerminationStatusTitle` schema.
  - **Title**: May contain literal newline characters.
  - **Committees[].Documents**: Often empty `[]`; main `Documents` array holds material documents.
  - **IsLegislative vs IsResponsible**: Typically mutually exclusive per committee; responsible committee handles the material, legislative committee does legal review.

### `GetMonthlyAgenda`
* Request body example:
```json
{
    "methodName": "GetMonthlyAgenda",
    "LanguageId": 1,
    "Month": 1,
    "Year": 2026
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Title": { "type": "string" },
      "Location": { "type": "string" },
      "Start": { "$ref": "#/$defs/AspDate" },
      "Type": { "$ref": "#/$defs/AgendaItemTypeId" }
    },
    "required": ["Id", "Title", "Location", "Start", "Type"]
  }
}
```
* Response example:
```json
[
    {"Id": "03141907-bd27-4ef2-a4a3-bbee47835a5d", "Title": "Седница бр. 80 на Собрание на Р. Северна Македонија - Сала „Македонија“", "Location": "Сала „Македонија“", "Start": "/Date(1768212000000)/", "Type": 1},
    {"Id": "1e124fa3-ed9a-4ab9-8661-50ae85944306", "Title": "Седница бр. 17 на Комисија за социјална политика, демографија и млади - Сала 5", "Location": "Сала 5", "Start": "/Date(1768208400000)/", "Type": 2}
]
```
* Notes:
  - **Response format**: Returns array directly (no TotalItems/Items wrapper).
  - **Type**: See `AgendaItemTypeId`.

### `GetAllSittingStatuses`
* Request body example:
```json
{
    "methodName": "GetAllSittingStatuses",
    "LanguageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/SittingStatusId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Response example:
```json
[
    {"Id": 1, "Title": "Закажана"},
    {"Id": 2, "Title": "Започната"},
    {"Id": 3, "Title": "Завршена"},
    {"Id": 4, "Title": "Незавршена"},
    {"Id": 5, "Title": "Затворена"},
    {"Id": 6, "Title": "Одложена"}
]
```

### `GetAllPoliticalParties`
* Request body example:
```json
{
    "methodName": "GetAllPoliticalParties",
    "languageId": 1,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Name": { "type": "string" },
      "NumberOfDeputies": { "type": "integer" },
      "Image": { "type": "string" }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```
* Response example:
```json
[
    {"Id": "e693cd9f-5893-49ab-9ede-0abd6e820664", "Name": "Левица", "NumberOfDeputies": 6, "Image": ""},
    {"Id": "4c57e5ab-2bc1-4943-8ecd-bde1166cf829", "Name": "ВМРО-ДПМНЕ", "NumberOfDeputies": 55, "Image": ""},
    {"Id": "8ab9ecb5-c53a-44ef-a468-ed94dd459fbe", "Name": "Движење БЕСА", "NumberOfDeputies": 10, "Image": ""}
]
```
* Notes:
  - **StructureId**: From `GetAllStructuresForFilter`. Parties are per assembly term.
  - **Image**: Often empty string `""` for all entries.

### `GetAllProcedureTypes`
* Request body example:
```json
{
    "methodName": "GetAllProcedureTypes",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/ProcedureTypeId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Response example:
```json
[
    {"Id": 1, "Title": "Редовна постапка"},
    {"Id": 2, "Title": "Скратена постапка"},
    {"Id": 3, "Title": "Итна постапка"}
]
```

### `GetParliamentMPsNoImage`
* Request body example:
```json
{
    "methodName": "GetParliamentMPsNoImage",
    "languageId": 1,
    "genderId": null,
    "ageFrom": null,
    "ageTo": null,
    "politicalPartyId": null,
    "searchText": null,
    "page": 1,
    "rows": 12,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
    "coalition": "",
    "constituency": ""
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "MembersOfParliament": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "type": "string", "format": "uuid" },
          "UserImg": { "type": "string", "contentEncoding": "base64" },
          "FullName": { "type": "string" },
          "RoleId": { "$ref": "#/$defs/RoleId" },
          "PoliticalPartyTitle": { "type": "string" },
          "PoliticalPartyId": { "type": "string", "format": "uuid" }
        },
        "required": ["UserId", "UserImg", "FullName", "RoleId", "PoliticalPartyTitle", "PoliticalPartyId"]
      }
    },
    "ExpiredMandateMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "type": "string", "format": "uuid" },
          "UserImg": { "type": "string", "contentEncoding": "base64" },
          "FullName": { "type": "string" },
          "RoleId": { "$ref": "#/$defs/RoleId" },
          "PoliticalPartyTitle": { "type": "string" },
          "PoliticalPartyId": { "type": "string", "format": "uuid" }
        },
        "required": ["UserId", "UserImg", "FullName", "RoleId", "PoliticalPartyTitle", "PoliticalPartyId"]
      }
    },
    "TotalItems": { "type": "integer" },
    "TotalItemsExpiredMandate": { "type": "integer" },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": { "type": "integer" },
        "NumberOfQuestions": { "type": "integer" },
        "TotalNumberOfMPs": { "type": "integer" },
        "TotalNumberOfExpiredMandateMPs": { "type": "integer" },
        "MPsInPoliticalParties": { "type": "integer" },
        "MPsInParliamentaryGroups": { "type": "integer" },
        "NumberOfMaterialsInStructure": { "type": "integer" }
      }
    }
  },
  "required": ["MembersOfParliament", "ExpiredMandateMembers", "TotalItems", "TotalItemsExpiredMandate", "Statistics"]
}
```
* Response example:
```json
{
    "MembersOfParliament": [
        {"UserId": "85048fa9-e61b-4eb1-be26-8d537cb1d7c4", "UserImg": "iVBORw0KGgoAAAANSUhEUgAAAMgAAAEs...", "FullName": "Аднан Азизи", "RoleId": 1, "PoliticalPartyTitle": "Движење БЕСА", "PoliticalPartyId": "8ab9ecb5-c53a-44ef-a468-ed94dd459fbe"}
    ],
    "ExpiredMandateMembers": [],
    "TotalItems": 120,
    "TotalItemsExpiredMandate": 13,
    "Statistics": {
        "TotalNumberOfMaterials": 10959,
        "NumberOfQuestions": 517,
        "TotalNumberOfMPs": 120,
        "TotalNumberOfExpiredMandateMPs": 13,
        "MPsInPoliticalParties": 120,
        "MPsInParliamentaryGroups": 110,
        "NumberOfMaterialsInStructure": 976
    }
}
```
* Notes:
  - **genderId**: Filter by `GenderId` (from `GetAllGenders`).
  - **politicalPartyId**: Filter by party (UUID from `GetAllPoliticalParties`).
  - **searchText**, **ageFrom**, **ageTo**, **coalition**, **constituency**: Optional filters.
  - **UserImg**: Despite endpoint name "NoImage", response includes base64-encoded images in `UserImg` (~100–130k chars). Empty string `""` when no image.
  - **Pagination**: `MembersOfParliament` and `ExpiredMandateMembers` are separately paginated. Use `TotalItems` and `TotalItemsExpiredMandate` respectively.
  - **Expired mandate**: `PoliticalPartyTitle` may be `""` and `PoliticalPartyId` may be `null` for expired MPs.
  - **Statistics**: Contains `TotalNumberOfMaterials`, `NumberOfQuestions`, `NumberOfMaterialsInStructure`, `MPsInPoliticalParties`, `MPsInParliamentaryGroups`, `TotalNumberOfExpiredMandateMPs`. Counts may differ from `TotalItems` when filters apply.

### `GetProposerTypes`
* Request body example:
```json
{
    "methodName": "GetProposerTypes",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/ProposerTypeId" },
      "Title": { "type": "string" },
      "Order": { "type": "integer" }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```
* Response example:
```json
[
    {"Id": 1, "Title": "Пратеник", "Order": 1},
    {"Id": 2, "Title": "Влада на Република Северна Македонија", "Order": 2},
    {"Id": 4, "Title": "Група избирачи", "Order": 4}
]
```
* Notes:
  - **Order**: Display order; ID 3 is not present in the API response.

### `GetAllQuestionStatuses`
* Request body example:
```json
{
    "methodName": "GetAllQuestionStatuses",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "$ref": "#/$defs/QuestionStatusId" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Notes:
  - **Id**: See `QuestionStatusId`. Used for filtering in `GetAllQuestions`.

### `GetAllInstitutionsForFilter`
* Request body example:
```json
{
    "methodName": "GetAllInstitutionsForFilter",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Title": { "type": "string" }
    },
    "required": ["Id", "Title"]
  }
}
```
* Notes:
  - Institutions (ministries, government bodies) for filtering parliamentary questions. Used with `To`/`ToInstitution` filters in `GetAllQuestions`.

### `GetAllQuestions`
* Request body example:
```json
{
    "methodName": "GetAllQuestions",
    "LanguageId": 1,
    "CurrentPage": 1,
    "Page": 1,
    "Rows": 10,
    "SearchText": "",
    "RegistrationNumber": "",
    "StatusId": null,
    "From": "",
    "To": "",
    "CommitteeId": null,
    "DateFrom": null,
    "DateTo": null,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "TotalItems": { "type": "integer" },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "From": { "type": "string" },
          "To": { "type": "string" },
          "ToInstitution": { "type": "string" },
          "StatusTitle": { "type": "string" },
          "DateAsked": { "$ref": "#/$defs/AspDate" },
          "QuestionTypeTitle": { "type": "string" },
          "TotalRows": { "type": "integer" }
        },
        "required": ["Id", "Title", "From", "To", "ToInstitution", "StatusTitle", "DateAsked", "QuestionTypeTitle", "TotalRows"]
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```
* Notes:
  - **StructureId**: From `GetAllStructuresForFilter`. Required.
  - **StatusId**: From `GetAllQuestionStatuses`.
  - **QuestionTypeTitle**: e.g. "Писмено прашање" (Written question), "Усно прашање" (Oral question).

### `GetQuestionDetails`
* Request body example:
```json
{
    "methodName": "GetQuestionDetails",
    "QuestionId": "0e2039bb-7a4b-462b-9489-6bce448eeb2a",
    "LanguageId": 1
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "Title": { "type": "string" },
    "From": { "type": "string" },
    "To": { "type": "string" },
    "ToInstitution": { "type": "string" },
    "QuestionTypeTitle": { "type": "string" },
    "StatusTitle": { "type": "string" },
    "NumberOfDeliveryLetter": { "type": ["string", "null"] },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "Url": { "type": "string" },
          "FileName": { "type": ["string", "null"] },
          "DocumentTypeId": { "type": "integer" },
          "DocumentTypeTitle": { "type": "string" },
          "IsExported": { "type": "boolean" }
        }
      }
    },
    "Sittings": { "type": "array", "items": {} }
  }
}
```

### `GetAllApplicationTypes`
* Request body example:
```json
{
    "methodName": "GetAllApplicationTypes",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "integer" },
      "ApplicationTitle": { "type": "string" }
    },
    "required": ["Id", "ApplicationTitle"]
  }
}
```
* Notes:
  - Application types for parliamentary submissions (e.g. "Пријава на случај", "Учество во јавна расправа").

### `GetAllCouncils`
* Request body example:
```json
{
    "methodName": "GetAllCouncils",
    "languageId": 1,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Name": { "type": "string" },
      "TypeId": { "type": "integer" },
      "TypeTitle": { "type": "string" }
    },
    "required": ["Id", "Name", "TypeId", "TypeTitle"]
  }
}
```
* Notes:
  - **StructureId**: From `GetAllStructuresForFilter`. Councils (e.g. Budget Council) are distinct from committees.

### `GetCouncilDetails`
* Request body example:
```json
{
    "methodName": "GetCouncilDetails",
    "committeeId": "d596538c-f3d4-4440-8ae7-6e25ea094c6a",
    "languageId": 1
}
```
* Response schema: Same structure as `GetCommitteeDetails` (Name, CompositionMembers, SecretariatMembers, Materials, Meetings, Description, Email, PhoneNumber, StructureId).

### `GetAllParliamentaryGroups`
* Request body example:
```json
{
    "methodName": "GetAllParliamentaryGroups",
    "languageId": 1,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Name": { "type": "string" },
      "NumberOfDeputies": { "type": "integer" },
      "Image": { "type": "string" }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```
* Notes:
  - Parliamentary groups (coalitions/parties). Image often empty.

### `GetParliamentaryGroupDetails`
* Request body example:
```json
{
    "methodName": "GetParliamentaryGroupDetails",
    "parliamentaryGroupId": "6f83cbd1-af39-44e5-bfd0-0cde68932844",
    "LanguageId": 1
}
```
* Response schema: Object with Name, Materials, Members (Id, FirstName, LastName, RoleId, RoleTitle), StructureId.

### `GetPoliticalPartyDetails`
* Request body example:
```json
{
    "methodName": "GetPoliticalPartyDetails",
    "politicalPartyId": "e693cd9f-5893-49ab-9ede-0abd6e820664",
    "LanguageId": 1
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "Name": { "type": "string" },
    "Description": { "type": "string" },
    "NumberOfDeputies": { "type": "integer" },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "RegistrationDate": { "$ref": "#/$defs/AspDate" },
          "RegistrationNumber": { "type": "string" },
          "StatusId": { "type": "integer" },
          "StatusTitle": { "type": "string" }
        }
      }
    }
  }
}
```

### `GetCommitteeDetails`
* Request body example:
```json
{
    "methodName": "GetCommitteeDetails",
    "committeeId": "bb8e23a1-c959-4818-8e6e-ebe450847fd8",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "Name": { "type": "string" },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "type": "string", "format": "uuid" },
          "FullName": { "type": "string" },
          "RoleId": { "type": "integer" },
          "RoleTitle": { "type": "string" }
        }
      }
    },
    "SecretariatMembers": { "type": "array", "items": {} },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "RegistrationDate": { "$ref": "#/$defs/AspDate" },
          "RegistrationNumber": { "type": "string" },
          "StatusId": { "type": "integer" },
          "StatusTitle": { "type": "string" }
        }
      }
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "TypeTitle": { "type": "string" },
          "Date": { "$ref": "#/$defs/AspDate" },
          "Location": { "type": "string" },
          "SittingNumber": { "type": "integer" }
        }
      }
    },
    "Description": { "type": "string" },
    "Email": { "type": ["string", "null"] },
    "PhoneNumber": { "type": ["string", "null"] },
    "StructureId": { "type": "string", "format": "uuid" }
  }
}
```
* Notes:
  - **committeeId**: From `GetAllCommitteesForFilter`.

### `GetAllMPsClubsByStructure`
* Request body example (uses `MethodName`, not `methodName`):
```json
{
    "MethodName": "GetAllMPsClubsByStructure",
    "LanguageId": 1,
    "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```
* Response schema:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": { "type": "string", "format": "uuid" },
      "Name": { "type": "string" }
    },
    "required": ["Id", "Name"]
  }
}
```
* Notes:
  - MPs clubs (inter-party groups, caucuses) – distinct from parliamentary groups (political parties).

### `GetMPsClubDetails`
* Request body example:
```json
{
    "methodName": "GetMPsClubDetails",
    "mpsClubId": "22ded665-2466-4d7e-a04b-03f8a150fc8c",
    "LanguageId": 1
}
```
* Response schema: Object with Name, Members (Id, FirstName, LastName, RoleId, RoleTitle), StructureId.

### `GetVotingResultsForSitting`
* Request body example:
```json
{
    "methodName": "GetVotingResultsForSitting",
    "votingDefinitionId": "076a2ea4-5477-467f-8217-4c3b8b6b5e92",
    "sittingId": "f06b995b-c5c7-42cd-8605-ec2d9ab7aac1",
    "languageId": 1
}
```
* Response schema:
```json
{
  "type": "object",
  "properties": {
    "votingOptions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "VotingDefinitionId": { "type": "string" },
          "Title": { "type": "string" },
          "Order": { "type": "integer" }
        }
      }
    },
    "sittingItem": {
      "type": "object",
      "properties": {
        "Id": { "type": "string", "format": "uuid" },
        "Number": { "type": "integer" },
        "Continuation": { "type": "integer" },
        "Title": { "type": "string" },
        "SittingDate": { "$ref": "#/$defs/AspDate" },
        "AgendaItemType": { "type": "string" }
      }
    },
    "summaryResult": {
      "type": "object",
      "properties": {
        "Present": { "type": "integer" },
        "Yes": { "type": "integer" },
        "No": { "type": "integer" },
        "NotVoted": { "type": "integer" },
        "VotingType": { "type": "string" },
        "VotingOutcome": { "type": "string" }
      }
    },
    "votingResultsByUser": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "FirstName": { "type": "string" },
          "LastName": { "type": "string" },
          "PoliticalParty": { "type": "string" },
          "PoliticalPartyId": { "type": ["string", "null"] },
          "Registered": { "type": "boolean" },
          "Present": { "type": "boolean" },
          "Yes": { "type": "boolean" },
          "No": { "type": "boolean" },
          "NotVoted": { "type": "boolean" }
        }
      }
    }
  }
}
```
* Notes:
  - **votingDefinitionId**, **sittingId**: From `GetSittingDetails` agenda item `VotingDefinitions`.
  - **VotingOutcome**: "Усвоен" (Adopted), "Одбиен" (Rejected).

### `GetVotingResultsForAgendaItem`
* Request body example:
```json
{
    "methodName": "GetVotingResultsForAgendaItem",
    "VotingDefinitionId": "9d80de02-11fb-4f79-80ee-181c0f92629d",
    "AgendaItemId": "98BBFA75-F432-4BBB-9A10-202EFE7E2569",
    "LanguageId": 1
}
```
* Notes:
  - Similar to `GetVotingResultsForSitting` but for a specific agenda item. May return 500 in some cases; IDs from `GetSittingDetails` agenda `VotingDefinitions`.

### `GetVotingResultsForAgendaItemReportDocument`
* Request body example:
```json
{
    "methodName": "GetVotingResultsForAgendaItemReportDocument",
    "VotingDefinitionId": "9d80de02-11fb-4f79-80ee-181c0f92629d",
    "AgendaItemId": "98BBFA75-F432-4BBB-9A10-202EFE7E2569",
    "LanguageId": 1
}
```
* Notes:
  - May return voting results as report document (JSON or file download). Check `Content-Disposition` header for file responses.

### `GetAmendmentDetails`
* Request body example:
```json
{
    "methodName": "GetAmendmentDetails",
    "amendmentId": "9a130205-3d0a-4394-a0b1-a0ac4b15a047",
    "languageId": 1
}
```
* Notes:
  - **amendmentId**: From `GetMaterialDetails` → `Amendments.Items[].Id`. Response schema not yet documented.

### `LoadLanguage` *(non-standard)*
* **Differs from standard format:** Different URL, no methodName.
* URL: `https://www.sobranie.mk/Infrastructure/LoadLanguage`
* Method: `POST`
* Request body: Empty `{}` or no body.
* Response: JSON object with `Code` (e.g. "mk-MK") and `Items` array of `{Key, Value}` localization strings.
* Notes: Sets/loads language preferences for session. Called on page load or language switch.

### `GetOfficialVisitsForUser` *(non-standard)*
* **Differs from standard format:** ASMX service, different URL and request format.
* URL: `https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser`
* Request body:
```json
{
    "model": "914bff80-4c19-4675-ace4-cb0c7a08f688"
}
```
* Response: Wrapper with `d` array (same pattern as `GetCustomEventsCalendar`). Returns `{"d": []}` when no visits.
* Notes: **model**: User/session UUID. May require authentication. Returns official visit records for the user.

### `GetUserDetailsByStructure`
* Request body example:
```json
{
    "methodName": "GetUserDetailsByStructure",
    "userId": "00000000-0000-0000-0000-000000000000",
    "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
    "languageId": 1
}
```
* Notes:
  - **userId**: From `GetParliamentMPsNoImage` or similar. **structureId**: From `GetAllStructuresForFilter`. Returns user profile, parliamentary membership, committee assignments within the structure. Response schema not fully documented.
