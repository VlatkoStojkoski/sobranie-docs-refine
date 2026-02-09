## GetAllPoliticalParties

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllPoliticalParties"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure. Obtain from GetAllStructuresForFilter. Common example: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 (current term)."
    }
  },
  "required": ["methodName", "languageId", "StructureId"]
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
        "description": "Unique identifier for the political party."
      },
      "Name": {
        "type": "string",
        "description": "Official name of the political party in the requested language. If not available in requested language, Macedonian may be returned as fallback."
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs affiliated with this party in the specified parliamentary structure. May include a pseudo-entry for independent MPs (e.g., \"Независни пратеници\")."
      },
      "Image": {
        "type": "string",
        "description": "Party logo or image identifier. Currently returns empty string for all parties in observed data; may contain base64-encoded image or URL in other cases."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes

**Response structure:**
- Returns a flat array of political party objects (not wrapped in `TotalItems`/`Items` pagination structure).
- No pagination; returns all parties for the specified structure in one request.
- All fields are present in every party entry.

**Request parameters:**
- **StructureId** — Required. Determines which set of political parties and their deputy counts are returned for a specific parliamentary term. Obtain from GetAllStructuresForFilter.
- **languageId** — Controls language of party names (1=Macedonian, 2=Albanian, 3=Turkish).
- **methodName** — Must be exactly `"GetAllPoliticalParties"` (uses camelCase).

**Field meanings:**
- **Name** — Official name of the political party in the requested language.
- **NumberOfDeputies** — Current count of MPs affiliated with this party in the specified parliamentary structure/term. Sum across all parties (including independent MPs pseudo-entry) approximates total parliament seats.
- **Image** — Party logo or image identifier. Currently empty string in observed data.
- **Independent MPs** — Typically represented as a pseudo-party entry (e.g., \"Независни пратеници\" / Independent MPs) with its own UUID and deputy count.

**Parameter casing:**
- Uses camelCase: `methodName`, `languageId`. `StructureId` uses PascalCase.