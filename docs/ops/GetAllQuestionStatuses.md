## GetAllQuestionStatuses

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllQuestionStatuses"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "additionalProperties": false
}
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
        "type": "string",
        "description": "Localized question status label in requested language (e.g., 'Delivered', 'Replied', 'Non disclosed reply', 'Reply in Writing')"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a direct flat array of question status objects (not wrapped in Items container or paginated).
- **Parameter casing:** Accepts both `languageId` (lowercase) and `LanguageId` (capitalized) interchangeably.
- **Localization:** `Title` is localized to the requested `LanguageId`. For example, with `languageId: 2` (Albanian), titles may appear as "Vendosur", "Përgjigj", "Përgjigj jo e zbuluar", "Përgjigj në shkrim". May return Macedonian text regardless of requested `languageId`; test per endpoint to confirm behavior.