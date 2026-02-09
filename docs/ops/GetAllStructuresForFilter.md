## GetAllStructuresForFilter

### Request
```json
{
  "methodName": "GetAllStructuresForFilter",
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
        "type": "string",
        "format": "uuid",
        "description": "UUID identifier of the parliamentary term/structure. Use this as StructureId in filter operations."
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
        "description": "Boolean flag indicating whether this is the currently active parliamentary term. Only one structure should have IsCurrent: true."
      }
    },
    "required": ["Id", "DateFrom", "DateTo", "IsCurrent"]
  }
}
```

### Notes
- Returns all parliamentary terms/structures in reverse chronological order (current/most recent first, oldest last)
- Exactly one structure has `IsCurrent: true` — this is the active parliamentary term
- The `Id` of the structure with `IsCurrent: true` should be used as the default `StructureId` parameter in other operations when querying current parliamentary data (typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` as of 2024)
- Historical structures are available, dating back to at least June 2008
- `DateTo` for the current term may be set to a far future placeholder date (e.g., `/Date(1851372000000)/` representing 2028)
- Unlike most catalog operations, structures do not include a `Title` or `Name` field; they are identified only by UUID and date range
- The `languageId` parameter does not affect the response structure (no localized fields are present)
- Response is not paginated; returns the complete list of all structures
- Use this operation once per session to obtain the current `StructureId` for use in other filtering operations