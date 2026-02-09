## GetAllCommitteesForFilter

### Request
```json
{
  "methodName": "GetAllCommitteesForFilter",
  "languageId": 1,
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

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
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure UUID. Determine which set of committees to return (committees vary by parliamentary term/structure). Obtain from GetAllStructuresForFilter."
    }
  },
  "required": ["methodName", "languageId", "structureId"]
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
        "description": "Committee name in requested language"
      }
    },
    "required": ["Id", "Name"]
  }
}
```

### Per-operation Notes
- **Purpose**: Returns all committees active within the specified parliamentary structure/term
- **Response format**: Direct array (not paginated, no TotalItems wrapper)
- **Language**: Committee names are returned in the language specified by `languageId`
- **Usage**: Use the returned `Id` values as `CommitteeId` filter in GetAllSittings (with `TypeId: 2` for committee sittings) or as `committeeId` parameter in GetCommitteeDetails
- **Typical count**: Current structure (5e00dbd6-ca3c-4d97-b748-f792b2fa3473) returns 27+ committees; count varies by parliamentary term