## GetAllQuestions

### Request Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllQuestions",
      "description": "Operation method name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Requested language for response labels and localized content"
    },
    "Page": {
      "type": "integer",
      "minimum": 1,
      "description": "1-based page number for pagination"
    },
    "Rows": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of items per page (typical values: 6, 8, 10, 12, 14, 18)"
    },
    "CurrentPage": {
      "type": "integer",
      "minimum": 1,
      "description": "Alternative pagination parameter; may differ from Page. Both parameters accepted by API."
    },
    "SearchText": {
      "type": "string",
      "description": "Free-text search across question titles and content. Set to empty string to disable."
    },
    "RegistrationNumber": {
      "anyOf": [
        { "type": "string", "description": "Filter by question registration number (e.g. '08-750/1')" },
        { "type": "null", "description": "null to omit filter" }
      ]
    },
    "StatusId": {
      "anyOf": [
        { "$ref": "#/$defs/QuestionStatusId" },
        { "type": "null", "description": "null to include all statuses" }
      ],
      "description": "Filter by question status"
    },
    "From": {
      "type": "string",
      "description": "Filter by question author name (MP name). Set to empty string to disable."
    },
    "To": {
      "type": "string",
      "description": "Filter by recipient name (minister/official). Set to empty string to disable."
    },
    "CommitteeId": {
      "anyOf": [
        { "$ref": "#/$defs/UUID" },
        { "type": "null", "description": "null to include all committees" }
      ],
      "description": "Filter questions by committee"
    },
    "DateFrom": {
      "anyOf": [
        { "$ref": "#/$defs/AspDate" },
        { "type": "null", "description": "null to omit start date filter" }
      ],
      "description": "Filter by DateAsked start (earliest)"
    },
    "DateTo": {
      "anyOf": [
        { "$ref": "#/$defs/AspDate" },
        { "type": "null", "description": "null to omit end date filter" }
      ],
      "description": "Filter by DateAsked end (latest)"
    },
    "StructureId": {
      "anyOf": [
        { "$ref": "#/$defs/UUID" },
        { "type": "null", "description": "null to query across all parliamentary terms/structures" }
      ],
      "description": "Parliamentary term/structure UUID"
    }
  },
  "required": ["methodName", "LanguageId", "Page", "Rows"],
  "$defs": {
    "AspDate": {
      "type": "string",
      "pattern": "^/Date\\(\\d+\\)/$"
    },
    "LanguageId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
    },
    "QuestionStatusId": {
      "type": "integer",
      "enum": [17, 19, 20, 21],
      "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
    },
    "UUID": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

### Response Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer",
      "description": "Total count of questions matching filters across all pages"
    },
    "Items": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "Id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Unique question identifier"
                  },
                  "Title": {
                    "type": "string",
                    "description": "Question text/title in requested language. May be truncated in listing view with '... (N chars)' appended, where N indicates the full title character count. Full text available via GetQuestionDetails."
                  },
                  "From": {
                    "type": "string",
                    "description": "Name of the MP who submitted the question (questioner)"
                  },
                  "To": {
                    "type": "string",
                    "description": "Title/position of the recipient (minister or official)"
                  },
                  "ToInstitution": {
                    "type": "string",
                    "description": "Full name of the institution receiving the question (ministry or government body). May contain placeholder values like '/' in some datasets."
                  },
                  "StatusTitle": {
                    "type": "string",
                    "description": "Human-readable question status in requested language (e.g. 'Доставено'=Delivered, 'Одговорено'=Answered)"
                  },
                  "DateAsked": {
                    "type": "string",
                    "pattern": "^/Date\\(\\d+\\)/$",
                    "description": "Date when question was submitted or scheduled (AspDate format). May contain future dates for scheduled questions."
                  },
                  "QuestionTypeTitle": {
                    "type": "string",
                    "description": "Type of question in requested language (e.g. 'Писмено прашање'=Written question, 'Усно прашање'=Oral question)"
                  },
                  "TotalRows": {
                    "type": "integer",
                    "description": "Item-level field observed as 0 in all responses. Purpose unclear (possibly legacy)."
                  },
                  "_truncated": {
                    "type": "integer",
                    "description": "When present, indicates N additional items omitted from response due to size constraints."
                  }
                },
                "required": ["Id", "Title", "From", "To", "ToInstitution", "StatusTitle", "DateAsked", "QuestionTypeTitle", "TotalRows"]
              },
              {
                "type": "object",
                "properties": {
                  "_truncated": {
                    "type": "integer",
                    "description": "Standalone truncation marker indicating N additional items omitted"
                  }
                },
                "required": ["_truncated"],
                "additionalProperties": false
              }
            ]
          }
        },
        {
          "type": "null",
          "description": "When TotalItems=0, Items is null instead of empty array"
        }
      ]
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Notes

#### Pagination
Uses standard `Page`/`Rows` pagination pattern (1-based). Response includes `TotalItems` (full result count across all pages) and `Items` (current page subset only). When `TotalItems: 0`, the `Items` field is `null` rather than empty array `[]`.

#### Array Truncation
When results are truncated due to size constraints, the `Items` array may contain fewer complete items than requested via `Rows`. A truncation marker appears as a standalone minimal object `{"_truncated": N}` within the array, indicating N additional items omitted. This marker counts toward the array length and may not appear at the end of the array (e.g., may appear at position 2 in a 3-element array). The `_truncated` field may also appear as an optional property on the last complete item.

#### LanguageId
Response content (Title, From, To, StatusTitle, QuestionTypeTitle, ToInstitution) is returned in the requested language. Some fields may contain Cyrillic text or institutional names even for non-Macedonian language requests; see global Language Fallback section.

#### Parameter Casing
Uses PascalCase: `LanguageId`, `StructureId`, `CommitteeId`, `RegistrationNumber`, `StatusId`, `DateFrom`, `DateTo`. Method name uses camelCase: `methodName`. Other filters (SearchText, From, To, Page, Rows, CurrentPage) use mixed case.

#### CurrentPage vs Page
Both parameters present in request; API accepts them with potentially different values. Both parameters are sent in actual requests; the distinction between them remains unclear (may be legacy or redundant parameter).

#### StructureId Nullable
Unlike most listing operations that require `StructureId`, this operation accepts `null` for cross-term queries of all questions regardless of parliamentary structure. When set to a specific UUID, filters to questions in that parliamentary term only.

#### Filter Parameter Details
- **SearchText:** Free-text search. Set to empty string `""` to disable.
- **From/To:** Text-based filters (MP name, recipient name). Set to empty string `""` to disable.
- **RegistrationNumber:** Registration number filter (e.g. '08-750/1'). Use `null` to omit.
- **StatusId:** Filter by QuestionStatusId (17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Use `null` to include all statuses.
- **CommitteeId:** UUID or `null` to include all committees.
- **DateFrom/DateTo:** AspDate format or `null` to omit start/end date filtering. Filters on DateAsked field.

#### Item Field Details
- **TotalRows:** Each item includes `TotalRows: 0`. Purpose unclear (possibly legacy or reserved field); rely on top-level `TotalItems` for actual result count.
- **QuestionTypeTitle:** Observed types include "Писмено прашање" (Written question) and "Усно прашање" (Oral question). No separate type ID exposed.
- **ToInstitution:** May contain placeholder values (e.g. `/`) or inconsistent formatting ("Министерството" vs "Министерство"). Handle gracefully in client code.
- **StatusTitle:** Observed values include "Доставено" (Delivered) and "Одговорено" (Answered) in Macedonian; response localizes per LanguageId.
- **DateAsked:** May contain future timestamps for scheduled or upcoming questions, not only historical questions.
