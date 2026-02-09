## GetAllGenders

### Request Schema
```json
{
  "type": "object",
  "required": ["methodName", "languageId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllGenders"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  }
}
```

### Response Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/GenderId"
      },
      "Title": {
        "type": "string",
        "description": "Localized gender name in requested language"
      }
    }
  },
  "description": "Direct array of gender options (not paginated)"
}
```

### Notes
- Returns exactly 2 items: Male (Id=1) and Female (Id=2).
- Response is a direct array, not wrapped in object with `TotalItems`/`Items`.
- `Title` values are localized per the `languageId` parameter (1=Macedonian, 2=Albanian, 3=Turkish).
- Use `Id` values (1 or 2) as filter input in operations like `GetParliamentMPsNoImage`.
- Reference data: always returns the same 2 entries, no pagination required.
- Method name uses camelCase: `methodName`; language parameter uses camelCase: `languageId`.