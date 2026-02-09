## GetAllCouncils

### Request
```json
{
  "methodName": "GetAllCouncils",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

#### Request parameters
- **StructureId** (UUID, required): Parliamentary term/structure. Obtain from `GetAllStructuresForFilter`. Common current value: `5e00dbd6-ca3c-4d97-b748-f792b2fa3473`. Filters councils to those active in the specified structure/term.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Name", "TypeId", "TypeTitle"],
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "Unique identifier for the council"
      },
      "Name": {
        "type": "string",
        "description": "Council name in the requested language"
      },
      "TypeId": {
        "type": "integer",
        "enum": [1],
        "description": "Council type. See CouncilTypeId in $defs. 1=Permanent (Постојана)"
      },
      "TypeTitle": {
        "type": "string",
        "description": "Localized council type name (e.g. 'Постојана' for permanent)"
      }
    }
  }
}
```

### Notes
- **Response format**: Returns a flat array of councils (not wrapped in TotalItems/Items structure).
- **Council types**: Currently only type 1 (Permanent/Постојана) observed in sample data. Other types may exist in different structures or future parliamentary terms.
- **Usage**: Council IDs returned in this operation can be used with `GetCouncilDetails` to retrieve detailed information about a specific council.
- **StructureId required**: Operation requires a valid parliamentary term/structure ID to filter results appropriately.