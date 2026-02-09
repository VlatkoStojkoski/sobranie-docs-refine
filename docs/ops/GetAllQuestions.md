## GetAllQuestions

### Request
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

### Response
```json
{
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
            "type": "object",
            "properties": {
              "Id": {
                "type": "string",
                "format": "uuid",
                "description": "Unique identifier for the question"
              },
              "Title": {
                "type": "string",
                "description": "Question text/title"
              },
              "From": {
                "type": "string",
                "description": "Name of the MP who asked the question (questioner)"
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
                "description": "Human-readable status of the question in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered). Maps to QuestionStatusId enum values."
              },
              "DateAsked": {
                "$ref": "#/$defs/AspDate",
                "description": "Date when the question was submitted"
              },
              "QuestionTypeTitle": {
                "type": "string",
                "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question)"
              },
              "TotalRows": {
                "type": "integer",
                "description": "Per-item metadata field. Observed as 0 in all responses; purpose unclear (possibly legacy or unused field)."
              }
            },
            "required": ["Id", "Title", "From", "To", "ToInstitution", "StatusTitle", "DateAsked", "QuestionTypeTitle", "TotalRows"]
          }
        },
        {
          "type": "null",
          "description": "When TotalItems is 0, Items becomes null instead of empty array"
        }
      ]
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Request Schema Details

**Core parameters:**
- **methodName** — Required; must be `"GetAllQuestions"`
- **LanguageId** — Language for response labels (1=Macedonian, 2=Albanian, 3=Turkish)
- **Page** — 1-based page number for pagination
- **Rows** — Number of items per page (typical values: 6, 8, 10, 12, 14, 18)
- **CurrentPage** — Appears alongside `Page`; purpose unclear (possibly legacy/redundant parameter). Typically set to same value as `Page`.

**Optional filters** (all can be empty string or null to omit):
- **SearchText** — Free-text search across question titles and content. Set to `""` (empty string) to omit text filtering.
- **RegistrationNumber** — Filter by question registration number. Set to `""` to omit.
- **From** — Filter by question author name (MP name). Set to `""` to omit.
- **To** — Filter by recipient name (minister/official). Set to `""` to omit.
- **StatusId** — Filter by question status (see QuestionStatusId enum: 17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Set to `null` to include all statuses. Example: `19` returns only answered questions.
- **CommitteeId** — Filter questions by committee. UUID or `null` to include all committees.
- **DateFrom / DateTo** — Filter by DateAsked range. AspDate format or `null` to omit date filtering.
- **StructureId** — Parliamentary term UUID. Can be specific UUID (e.g., `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term) or `null` to query across all parliamentary terms/structures.

### Per-operation Notes

- **Pagination behavior**: Uses standard `Page`/`Rows` pagination. Response includes `TotalItems` (full result count) and page subset of `Items`.

- **StatusId filter example**: Setting `StatusId: 19` filters to answered questions only. Setting `StatusId: null` includes questions with all statuses.

- **CurrentPage vs Page**: Both parameters present in actual requests; their distinction is unclear. Recommend setting both to same value until behavior diverges. May be legacy/redundant parameter.

- **StructureId nullable behavior**: Unlike most operations that require `StructureId`, GetAllQuestions accepts `null` for cross-term queries of all questions regardless of parliamentary structure.

- **Empty string filters**: Multiple text filters (`SearchText`, `RegistrationNumber`, `From`, `To`) accept empty string `""` to disable filtering on that dimension.

- **TotalRows in items**: Each item includes `TotalRows: 0` in the response. Purpose is unclear (possibly legacy or reserved field); total count provided via top-level `TotalItems` instead.

- **Question types observed**: "Писмено прашање" (Written question), "Усно прашање" (Oral question). No separate question-type ID exposed; use `QuestionTypeTitle` for filtering/display.

- **Status values observed**: "Доставено" (Delivered, StatusId 17), "Одговорено" (Answered, StatusId 19).

- **Language localization**: Response content (Title, From, To, StatusTitle, QuestionTypeTitle, ToInstitution) is returned in the requested `LanguageId` language.

- **ToInstitution data quality**: May contain placeholder values (e.g., `"/"`) similar to `GetAllInstitutionsForFilter`; handle gracefully in client code. Note: inconsistent formatting in API responses (e.g., "Министерството" vs "Министерство" for ministry names).
