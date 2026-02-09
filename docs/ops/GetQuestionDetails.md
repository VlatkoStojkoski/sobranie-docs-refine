## GetQuestionDetails

### Request
```json
{
  "methodName": "GetQuestionDetails",
  "QuestionId": "0e2039bb-7a4b-462b-9489-6bce448eeb2a",
  "LanguageId": 1
}
```

### Response
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
      "description": "Title/position of the official or minister the question is addressed to"
    },
    "ToInstitution": {
      "type": "string",
      "description": "Full name of the ministry or government body receiving the question"
    },
    "QuestionTypeTitle": {
      "type": "string",
      "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question)"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Human-readable status in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered)"
    },
    "NumberOfDeliveryLetter": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Delivery letter reference number; null when not assigned"
    },
    "Documents": {
      "type": "array",
      "description": "Array of attached documents. May be empty array [] when no documents attached.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Title": {
            "type": "string"
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
            "type": "integer",
            "enum": [26],
            "description": "26=Question document (Прашање)"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Human-readable document type in the requested language"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether the document has been exported/published"
          }
        }
      }
    },
    "Sittings": {
      "type": "array",
      "description": "Array of sittings where the question was discussed. Empty array [] when question has not been discussed in any sitting yet.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer",
            "enum": [1, 2],
            "description": "1=Plenary (Пленарна седница), 2=Committee"
          },
          "SittingTypeTitle": {
            "type": "string",
            "description": "Human-readable sitting type in the requested language"
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
        }
      }
    }
  }
}
```

## Operation Notes

### Parameter Notes
- **QuestionId** — UUID of the parliamentary question to retrieve details for. Obtain from `GetAllQuestions` Items[].Id.
- **LanguageId** — Requested language for response labels (1=Macedonian, 2=Albanian, 3=Turkish).

### Response Field Meanings
- **Title** — Full text of the parliamentary question.
- **From** — Name of the MP who submitted the question.
- **To** — Title/position of the official or minister to whom the question is directed (e.g. "Министерот за внатрешни работи").
- **ToInstitution** — Full name of the ministry or government body receiving the question (e.g. "Министерство за внатрешни работи"). Localized according to LanguageId.
- **QuestionTypeTitle** — Type of question in the requested language (e.g. "Писмено прашање" = Written question, "Усно прашање" = Oral question). Localized according to LanguageId.
- **StatusTitle** — Current status of the question in the requested language (e.g. "Доставено" = Delivered, "Одговорено" = Answered). Corresponds to QuestionStatusId enum values from GetAllQuestionStatuses. Localized according to LanguageId.
- **NumberOfDeliveryLetter** — Reference number for delivery correspondence. Often null in observed data; purpose may be for tracking official delivery letters.
- **Documents** — Array of attached documents related to the question (questions, answers, etc.). Each document has a direct `Url` for download. The `DocumentTypeId` value 26 indicates a question document. Returns empty array `[]` when no documents are attached (not `null`).
- **Sittings** — Array of parliamentary sittings where this question was discussed or answered. For plenary sittings, `CommitteeTitle` is `null` and `SittingTypeId` is 1. For committee sittings, `CommitteeTitle` contains the committee name and `SittingTypeId` is 2. Returns empty array `[]` when the question has not yet been discussed in any sitting (not `null`).

### Schema Notes
- **Empty collections**: Unlike some other endpoints where empty `Items` becomes `null`, both `Documents` and `Sittings` return empty arrays `[]` when no items are present.
- **Localization**: `ToInstitution`, `QuestionTypeTitle`, `StatusTitle`, and `SittingTypeTitle` are localized according to the `LanguageId` parameter. The question `Title` and `From` field may retain their original language regardless of `LanguageId`.
- **Document access**: Document URLs point to SharePoint resources; `IsExported: true` indicates the document is publicly accessible.
