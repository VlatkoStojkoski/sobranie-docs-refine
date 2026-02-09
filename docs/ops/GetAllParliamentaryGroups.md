## GetAllParliamentaryGroups

### Request
```json
{
  "methodName": "GetAllParliamentaryGroups",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Request Parameters
- **methodName** — `"GetAllParliamentaryGroups"` (required)
- **languageId** — `1` = Macedonian, `2` = Albanian, `3` = Turkish (required)
- **StructureId** — UUID of parliamentary term/structure (required). Obtain from `GetAllStructuresForFilter`. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. Determines which parliamentary groups to return based on the parliamentary term.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string",
        "description": "Full official name of the parliamentary group (e.g., \"Пратеничка група на партијата …\")"
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs belonging to this parliamentary group"
      },
      "Image": {
        "anyOf": [
          {"type": "string"},
          {"type": "null"}
        ],
        "description": "Image identifier or URL for the parliamentary group. Often empty string when no image available."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes
- Returns all parliamentary groups (factions/caucuses) for the specified structure/term. Each group represents a coalition or party with seats in parliament for that term.
- Response is a direct array, not wrapped in `TotalItems`/`Items` pagination structure.
- All `Image` fields in current data are empty strings `""`, indicating parliamentary groups may not have images assigned in the system.
- `NumberOfDeputies` reflects current membership count in each parliamentary group. Totals across all groups may not equal total MPs if there are independents or vacancies.
