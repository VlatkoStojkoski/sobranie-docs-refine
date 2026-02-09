## GetAllQuestionStatuses

### Request
```json
{
  "methodName": "GetAllQuestionStatuses",
  "languageId": 1
}
```

**Note:** This operation accepts both `languageId` (lowercase) and `LanguageId` (capitalized) parameter names interchangeably. Either casing is accepted.

### Response
```json
[
  {
    "Id": 17,
    "Title": "Delivered"
  },
  {
    "Id": 19,
    "Title": "Replied"
  },
  {
    "Id": 20,
    "Title": "Non disclosed reply"
  },
  {
    "Id": 21,
    "Title": "Reply in Writing"
  }
]
```

### Response Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/QuestionStatusId"
      },
      "Title": {
        "type": "string"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a direct array of question status objects (not wrapped in an Items container or paginated).
- Parameter casing: accepts both `languageId` and `LanguageId`.
- `Title` is localized to the requested `LanguageId`. For example, with `LanguageId: 2` (Albanian), titles may appear as "Vendosur", "Përgjigj", "Përgjigj jo e zbuluar", "Përgjigj në shkrim".