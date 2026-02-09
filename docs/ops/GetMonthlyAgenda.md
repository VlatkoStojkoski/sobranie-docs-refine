## GetMonthlyAgenda

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetMonthlyAgenda",
      "description": "Operation name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Controls localization of Title and Location fields (1=Macedonian, 2=Albanian, 3=Turkish)"
    },
    "Month": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Calendar month (1–12)"
    },
    "Year": {
      "type": "integer",
      "description": "Four-digit year (e.g. 2025, 2026)"
    }
  },
  "required": ["methodName", "LanguageId", "Month", "Year"]
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
        "description": "Identifier for the sitting/agenda item"
      },
      "Title": {
        "type": "string",
        "description": "Full descriptive title typically in format: Седница бр. {number} на {body name} - {location} (in requested language)"
      },
      "Location": {
        "type": "string",
        "description": "Physical room or venue (e.g. Сала \"Македонија\", Сала 4, Сала 5)"
      },
      "Start": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date/time of the sitting"
      },
      "Type": {
        "$ref": "#/$defs/AgendaItemTypeId",
        "description": "1=Plenary, 2=Committee"
      }
    },
    "required": ["Id", "Title", "Location", "Start", "Type"]
  },
  "description": "Flat array of agenda items (sittings) for the requested month, ordered by Start date/time ascending. Empty array when no agenda items exist."
}
```

### Notes

**Parameter casing:** Uses `methodName` (lowercase) and `LanguageId` (PascalCase).

**Request details:**
- `methodName`: Always `"GetMonthlyAgenda"`
- `LanguageId`: 1=Macedonian, 2=Albanian, 3=Turkish. Affects Title and Location localization.
- `Month`: Integer 1–12
- `Year`: Four-digit year

**Response format:** Returns a flat array (not paginated; no TotalItems/Items wrapper).

**Type field:** Indicates sitting context:
- `1` = Plenary sittings (main parliament sessions)
- `2` = Committee sittings (committee meetings)

**Title format:** Typically "Седница бр. {number} на {body name} - {location}" structure in Macedonian or equivalent in requested language.

**Empty results:** Returns empty array `[]` when no agenda items exist for the requested month/year.

**Ordering:** Results ordered by Start date/time ascending.

**Usage:** Pass the `Id` to `GetSittingDetails` to retrieve detailed sitting information including agenda tree, attendees, voting results, etc.