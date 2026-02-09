## GetAllApplicationTypes

### Notes
Returns all application types available in the system.

**Usage:**
- Use to populate dropdowns or filters for application-related operations
- languageId determines the language of ApplicationTitle (1=Macedonian, 2=Albanian, 3=Turkish)

**Language fallback behavior:**
- When `languageId=3` (Turkish), the API may return English labels instead of Turkish translations, indicating fallback behavior for incomplete localizations.

**Known application types by languageId:**
- **languageId=1 (Macedonian):**
  - 1: "Пријава на случај" (Case report)
  - 2: "Учество во јавна расправа" (Participation in public discussion)
  - 3: "Дискусија" (Discussion)
- **languageId=2 (Albanian):**
  - 1: "Paraqitja e rastit" (Case report)
  - 2: "Pjesëmarrje në debatin publik" (Participation in public discussion)
  - 3: "Diskutim" (Discussion)
- **languageId=3 (Turkish - returns English fallback):**
  - 1: "Case report"
  - 2: "Participation in Public Debate"
  - 3: "Discussion"

**Response:**
- Returns array of application types with Id and localized ApplicationTitle

### Request
```json
{
  "methodName": "GetAllApplicationTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "ApplicationTitle": {
        "type": "string"
      }
    },
    "required": ["Id", "ApplicationTitle"]
  }
}
```