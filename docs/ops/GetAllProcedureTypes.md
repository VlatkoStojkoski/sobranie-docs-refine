## GetAllProcedureTypes

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllProcedureTypes"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "additionalProperties": false,
  "$defs": {
    "LanguageId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
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
    "properties": {
      "Id": {
        "$ref": "#/$defs/ProcedureTypeId"
      },
      "Title": {
        "type": "string",
        "description": "Procedure type name in requested language (or Macedonian fallback)"
      }
    },
    "required": ["Id", "Title"],
    "additionalProperties": false
  },
  "$defs": {
    "ProcedureTypeId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Regular (Редовна постапка), 2=Shortened (Скратена постапка), 3=Urgent (Итна постапка)"
    }
  }
}
```

### Notes
- Returns a fixed set of three procedure types regardless of language or other parameters.
- The `languageId` parameter may not affect response content; Macedonian text has been observed regardless of requested language (e.g., `languageId: 3` returning Macedonian rather than Turkish). See global data quality notes on language fallback.
- No pagination is used; all three procedure types are always returned in a single response.
- The returned `Id` values map directly to `ProcedureTypeId` used in filtering operations (e.g., `GetAllMaterialsForPublicPortal`).
- Uses camelCase parameter name `languageId` (not PascalCase).