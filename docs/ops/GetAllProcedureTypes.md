## GetAllProcedureTypes

### Request
```json
{
  "methodName": "GetAllProcedureTypes",
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
        "type": "integer",
        "enum": [1, 2, 3],
        "description": "Procedure type identifier"
      },
      "Title": {
        "type": "string",
        "description": "Procedure type name in requested language (or Macedonian fallback)"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a fixed set of three procedure types regardless of language or other parameters
- **Id values:**
  - `1` = "Редовна постапка" (Regular procedure)
  - `2` = "Скратена постапка" (Shortened procedure)
  - `3` = "Итна постапка" (Urgent procedure)
- The `languageId` parameter may not affect response content; Macedonian text has been observed regardless of requested language (e.g., `languageId: 3` returning Macedonian rather than Turkish)
- No pagination is used; all three procedure types are always returned in a single response
- The returned `Id` values map directly to `ProcedureTypeId` used in filtering operations (e.g., `GetAllMaterialsForPublicPortal`)