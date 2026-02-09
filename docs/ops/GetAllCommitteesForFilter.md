## GetAllCommitteesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllCommitteesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "structureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID. Obtain from GetAllStructuresForFilter. Determines which set of committees to return (varies by parliamentary term). Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term."
    }
  },
  "required": ["methodName", "languageId", "structureId"]
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
        "description": "Committee UUID. Use as CommitteeId in other operations."
      },
      "Name": {
        "type": "string",
        "description": "Committee name in the requested language."
      }
    },
    "required": ["Id", "Name"]
  }
}
```

### Notes

- **Response format:** Direct array (not paginated; no TotalItems wrapper).
- **Language:** Committee names are returned in the language specified by `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).
- **Parameter casing:** Uses camelCase (`methodName`, `languageId`, `structureId`).
- **Usage:** Use returned `Id` as `CommitteeId` filter parameter in GetAllSittings (with `TypeId: 2` for committee sittings) or as `committeeId` in GetCommitteeDetails.
- **Typical count:** Current structure (5e00dbd6-ca3c-4d97-b748-f792b2fa3473) returns 27+ committees; count varies by parliamentary term.