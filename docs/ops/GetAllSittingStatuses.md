## GetAllSittingStatuses

### Request Schema
```json
{
  "type": "object",
  "required": ["methodName", "LanguageId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllSittingStatuses"],
      "description": "Operation name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  }
}
```

### Response Schema
```json
{
  "type": "array",
  "description": "Returns all sitting status options with localized titles",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId"
      },
      "Title": {
        "type": "string",
        "description": "Localized status name in the requested language (e.g., \"Закажана\" = Scheduled, \"Започната\" = Started, etc.)"
      }
    }
  }
}
```

### Notes
- Returns all six sitting status options with titles localized to the requested `LanguageId`.
- The `Id` values correspond to `SittingStatusId` enum in global $defs: 1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed.
- `Title` is the human-readable label for the status in the requested language.
- Use the returned `Id` values when filtering sittings via the `StatusId` parameter in `GetAllSittings`.
- Response is a simple flat array (not wrapped in `TotalItems`/`Items` pagination object).
- Parameter casing: Uses `LanguageId` (PascalCase).
- Calling convention: Method-based (POST to `https://www.sobranie.mk/Routing/MakePostRequest` with `methodName` in body).