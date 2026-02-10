## GetAllApplicationTypes

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllApplicationTypes"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"]
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
        "$ref": "#/$defs/ApplicationTypeId"
      },
      "ApplicationTitle": {
        "type": "string",
        "description": "Localized title of the application type in the requested language"
      },
      "_truncated": {
        "type": "integer",
        "description": "Number of additional items omitted from array (present only on last item when truncation occurs)"
      }
    },
    "required": ["Id", "ApplicationTitle"]
  },
  "description": "Flat array of application types; not paginated. May be truncated; check for _truncated field on last item indicating N additional items omitted."
}
```

### Notes

- Returns a flat array (not paginated); `TotalItems` and `Items` wrapper are not used.
- `languageId` determines localization: 1=Macedonian, 2=Albanian, 3=Turkish.
- Language fallback: When `languageId=3` (Turkish), the API may return English labels (e.g. "Case report", "Participation in Public Debate") instead of Turkish translations, indicating incomplete localization for Turkish.
- `Id` values are 1, 2, 3 (see ApplicationTypeId in global $defs).
- Use these IDs in filters and request bodies for application-related operations.
- Typical use: populate dropdowns or application type filters.
- **Array truncation:** When truncation occurs, the array contains at least one complete object (Id + ApplicationTitle) before the truncation marker. Check the last item for the optional `_truncated` field indicating additional items omitted.