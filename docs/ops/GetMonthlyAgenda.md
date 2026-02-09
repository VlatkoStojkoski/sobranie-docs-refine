## GetMonthlyAgenda

### Request
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "const": "GetMonthlyAgenda"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "Month": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Month (1–12) for which to retrieve agenda items"
    },
    "Year": {
      "type": "integer",
      "description": "Four-digit year (e.g. 2025, 2026) for which to retrieve agenda items"
    }
  },
  "required": ["methodName", "LanguageId", "Month", "Year"]
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
        "description": "Identifier for the agenda item/sitting"
      },
      "Title": {
        "type": "string",
        "description": "Full descriptive title including sitting number, committee/body name, and location"
      },
      "Location": {
        "type": "string",
        "description": "Physical location/room where the sitting will take place"
      },
      "Start": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date/time of the agenda item"
      },
      "Type": {
        "$ref": "#/$defs/AgendaItemTypeId",
        "description": "1=Plenary, 2=Committee"
      }
    },
    "required": ["Id", "Title", "Location", "Start", "Type"]
  }
}
```

### Notes
- **Request parameters:**
  - `methodName`: Always `"GetMonthlyAgenda"`
  - `LanguageId`: Standard language parameter (1=Macedonian, 2=Albanian, 3=Turkish). Affects language of Title and Location fields.
  - `Month`: Integer 1-12 specifying the calendar month to retrieve agenda items for. Required.
  - `Year`: Four-digit year (e.g. 2025, 2026) specifying the calendar year to retrieve agenda items for. Required.

- **Response structure:** Returns a flat array of agenda items (not wrapped in TotalItems/Items pagination structure).

- **Title format:** Typically follows pattern "Седница бр. {number} на {body name} - {location}" (in Macedonian) or equivalent localization in requested language.

- **Type values:**
  - Type 1 = Plenary sittings (main parliament sessions, typically at "Сала „Македонија"")
  - Type 2 = Committee sittings (committee meetings, typically at "Сала 4", "Сала 5", "Сала 6", etc.)

- **Empty results:** When no agenda items exist for the requested month/year, returns empty array `[]` (not null).

- **Ordering:** Results are ordered by Start date/time.

- **Usage:** Useful for calendar views, scheduling displays, and retrieving upcoming parliamentary sessions. The `Id` can be used with `GetSittingDetails` to fetch detailed sitting information.