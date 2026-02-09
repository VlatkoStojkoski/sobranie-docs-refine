## GetAllPoliticalParties

### Request
```json
{
  "methodName": "GetAllPoliticalParties",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
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
        "format": "uuid"
      },
      "Name": {
        "type": "string",
        "description": "Political party name in the requested language"
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs affiliated with this party in the specified structure"
      },
      "Image": {
        "type": "string",
        "description": "Party logo or image identifier. May be empty string when no image is available"
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes

**Filter usage:**
- **StructureId** — Required. UUID of parliamentary term/structure from GetAllStructuresForFilter. Use `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. Determines which set of political parties and their deputy counts are returned for a specific parliamentary session.
- **languageId** — Required. Controls language of party names (1=Macedonian, 2=Albanian, 3=Turkish).

**Response structure:**
- Returns a flat array of political party objects (not wrapped in `TotalItems`/`Items` pagination structure).
- All fields (`Id`, `Name`, `NumberOfDeputies`, `Image`) are present in every party entry.

**Field meanings:**
- **Name** — Official name of the political party in the requested language.
- **NumberOfDeputies** — Current count of MPs affiliated with this party in the specified parliamentary structure/term. Reflects actual composition for that StructureId; sum across all parties (including independent MPs entry) should approximate total parliament seats.
- **Image** — Party logo or image identifier. Currently returns empty string `""` for all parties in observed data; may contain base64-encoded image data or URL in other cases.
- **Independent MPs** — Represented as a pseudo-party entry (e.g. "Независни пратеници" / Independent MPs) with its own UUID and deputy count.