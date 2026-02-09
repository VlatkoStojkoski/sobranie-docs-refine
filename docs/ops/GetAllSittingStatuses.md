## GetAllSittingStatuses

### Request
```json
{
  "methodName": "GetAllSittingStatuses",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "array",
  "description": "Returns all sitting status options with localized titles",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId",
        "description": "Numeric identifier for the sitting status (1–6)"
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
- Returns all six sitting status options with titles localized to the requested `LanguageId` (1=Macedonian, 2=Albanian, 3=Turkish)
- The `Id` values (1–6) map directly to the `SittingStatusId` enum in $defs
- `Title` is the human-readable label for the status in the requested language
- Use the returned `Id` values when filtering sittings via the `StatusId` parameter in `GetAllSittings`
- This is a simple array response (not wrapped in TotalItems/Items object)