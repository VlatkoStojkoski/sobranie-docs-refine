## GetAllParliamentaryGroups

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllParliamentaryGroups"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID. Obtain from GetAllStructuresForFilter; often 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term. Filters groups to those active in the specified term."
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
        "description": "Parliamentary group unique identifier"
      },
      "Name": {
        "type": "string",
        "description": "Full official name of the parliamentary group. Localized in requested language."
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
        "description": "Image identifier, URL, or base64-encoded image data. May be empty string when no image is available."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  },
  "description": "Direct array of parliamentary groups (not paginated)"
}
```

### Notes

- Response is a direct flat array, not wrapped in `TotalItems`/`Items` pagination structure.
- Parameter casing: Uses `methodName` (lowercase) and `languageId` (lowercase).
- All `Image` fields in current data are empty strings, indicating parliamentary groups may not have images assigned.
- `Email` and `Phone` fields are typically `null` for parliamentary groups; contact is via individual members. See GetParliamentaryGroupDetails for additional fields.
- `NumberOfDeputies` reflects current membership. Verify with GetParliamentaryGroupDetails to confirm full member roster and roles (78=Chair, 79=Vice-President, 81=Member).