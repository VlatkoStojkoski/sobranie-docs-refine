## GetAllCouncils

### Request Schema

```json
{
  "type": "object",
  "required": ["methodName", "languageId", "StructureId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllCouncils"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure identifier. Obtain from GetAllStructuresForFilter. Current common value: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473. Filters councils to those active in the specified structure/term."
    }
  }
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
        "description": "Unique identifier for the council"
      },
      "Name": {
        "type": "string",
        "description": "Council name in the requested language"
      },
      "TypeId": {
        "$ref": "#/$defs/CouncilTypeId"
      },
      "TypeTitle": {
        "type": "string",
        "description": "Localized council type name (e.g. 'Постојана' for permanent)"
      },
      "_truncated": {
        "type": "integer",
        "description": "When present (final item only), indicates number of additional councils omitted due to truncation"
      }
    },
    "required": ["Id", "Name", "TypeId", "TypeTitle"]
  }
}
```

### Notes

- **Response format:** Returns a flat array of councils (not wrapped in TotalItems/Items structure).
- **Array truncation:** When results exceed available items, the last array element is an object with only `_truncated` field (integer) indicating how many additional councils are omitted.
- **Council types:** Currently only type 1 (Permanent/Постојана) observed. Other types may exist in different structures or future terms.
- **Parameter casing:** Uses lowercase `methodName` and `languageId`.
- **Usage:** Council IDs returned here can be used with `GetCouncilDetails` to retrieve detailed information.
- **StructureId required:** Valid parliamentary term/structure ID is required to filter results appropriately.