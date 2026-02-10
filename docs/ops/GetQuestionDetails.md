## GetQuestionDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetQuestionDetails"
    },
    "QuestionId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the parliamentary question to retrieve details for. Obtained from GetAllQuestions Items[].Id."
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "QuestionId", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string",
      "description": "Full text of the parliamentary question"
    },
    "From": {
      "type": "string",
      "description": "Name of the MP who submitted the question"
    },
    "To": {
      "type": "string",
      "description": "Title/position of the official or minister the question is addressed to (e.g. 'Министерот за внатрешни работи')"
    },
    "ToInstitution": {
      "type": "string",
      "description": "Full name of the ministry or government body receiving the question (e.g. 'Министерство за внатрешни работи'). Localized according to LanguageId."
    },
    "QuestionTypeTitle": {
      "type": "string",
      "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question). Localized according to LanguageId."
    },
    "StatusTitle": {
      "type": "string",
      "description": "Current status of the question in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered). Corresponds to QuestionStatusId enum. Localized according to LanguageId."
    },
    "NumberOfDeliveryLetter": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Reference number for delivery correspondence. Often null; purpose is for tracking official delivery letters."
    },
    "Documents": {
      "type": "array",
      "description": "Array of attached documents related to the question (questions, answers, etc.). Returns empty array [] when no documents attached.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Document title"
          },
          "Url": {
            "type": "string",
            "description": "Direct URL to the document file (e.g. SharePoint path)"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Original filename; often null"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId",
            "description": "Document type identifier. 26=Question document (Прашање), 28=Answer document (Одговор)"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Human-readable document type in the requested language"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether the document has been exported/published"
          }
        },
        "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      }
    },
    "Sittings": {
      "type": "array",
      "description": "Array of parliamentary sittings where this question was discussed or answered. Returns empty array [] when question has not yet been discussed in any sitting.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "SittingTypeId": {
            "$ref": "#/$defs/SittingTypeId"
          },
          "SittingTypeTitle": {
            "type": "string",
            "description": "Human-readable sitting type in the requested language (e.g. 'Пленарна седница' for plenary, 'Комисска седница' for committee). Localized according to LanguageId."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date of sitting in AspDate format"
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Name of committee; null for plenary sittings (when SittingTypeId=1)"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential number of the sitting within its session"
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "SittingNumber"]
      }
    }
  },
  "required": ["Title", "From", "To", "ToInstitution", "QuestionTypeTitle", "StatusTitle", "Documents", "Sittings"]
}
```

### Notes

- **methodName:** Must be `"GetQuestionDetails"`.
- **QuestionId:** UUID of the parliamentary question. Obtain from `GetAllQuestions` Items[].Id.
- **LanguageId:** Requested language for response labels and localized fields (1=Macedonian, 2=Albanian, 3=Turkish).
- **Localized fields:** `ToInstitution`, `QuestionTypeTitle`, `StatusTitle`, and `SittingTypeTitle` are localized according to LanguageId request.
- **Non-localized fields:** The question `Title` and `From` field may retain their original language regardless of LanguageId.
- **Empty collections:** Both `Documents` and `Sittings` return empty arrays `[]` when no items are present (not null).
- **Document access:** Document `Url` fields point to SharePoint resources. `IsExported: true` indicates the document is publicly accessible.
- **Document types:** `DocumentTypeId` 26 identifies question documents (Прашање); 28 identifies answer documents (Одговор). See global $defs/DocumentTypeId for full enum.
- **StatusTitle mapping:** Corresponds to QuestionStatusId enum values (17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). See global for QuestionStatusId definition.
- **Sitting context:** For plenary sittings, `CommitteeTitle` is null and `SittingTypeId` is 1. For committee sittings, `CommitteeTitle` contains the committee name and `SittingTypeId` is 2.
- **NumberOfDeliveryLetter:** Often null in observed data; used for tracking official delivery correspondence when present.