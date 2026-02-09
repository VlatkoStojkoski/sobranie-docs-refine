## GetAllStructuresForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllStructuresForFilter",
      "description": "Operation identifier"
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
        "$ref": "#/$defs/UUID",
        "description": "UUID identifier of the parliamentary term/structure. Use as StructureId in filter operations."
      },
      "DateFrom": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date of the parliamentary term"
      },
      "DateTo": {
        "$ref": "#/$defs/AspDate",
        "description": "End date of the parliamentary term. May be set far in the future for current term."
      },
      "IsCurrent": {
        "type": "boolean",
        "description": "Boolean flag indicating whether this is the currently active parliamentary term. Only one structure has IsCurrent: true."
      }
    },
    "required": ["Id", "DateFrom", "DateTo", "IsCurrent"]
  },
  "description": "Flat array of all parliamentary terms in reverse chronological order (current/most recent first). Not paginated."
}
```

### Notes

- **Parameter casing:** Uses lowercase `methodName` and `languageId`
- **Structure selection:** Exactly one structure has `IsCurrent: true` — this is the active parliamentary term and should be used as the default `StructureId` in other operations when querying current parliamentary data (typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` as of 2024)
- **Historical data:** Returns all parliamentary terms dating back to at least June 2008; use for querying past sessions
- **Ordering:** Response is in reverse chronological order (current first)
- **DateTo placeholder:** For the current term, `DateTo` may be set to a far future placeholder date (e.g., representing 2028)
- **No localization:** The `languageId` parameter does not affect the response; no localized fields are present
- **No pagination:** Response is not paginated; returns the complete list of all structures
- **No Title field:** Unlike most catalog operations, structures are identified only by UUID and date range; no Title or Name field is present
- **Usage pattern:** Call once per session to obtain the current `StructureId` for use in subsequent filter operations
