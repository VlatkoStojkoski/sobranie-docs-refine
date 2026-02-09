## GetAllMPsClubsByStructure

Returns all MPs clubs (inter-party parliamentary groups) for a specified parliamentary structure/term. These are cross-party groups focused on specific issues such as environmental protection, Roma rights, youth issues, and anti-corruption. The response is not paginated and returns all clubs active in the structure.

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "MethodName": {
      "type": "string",
      "enum": ["GetAllMPsClubsByStructure"],
      "description": "Operation name (required, uses PascalCase casing)"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure. Obtain from GetAllStructuresForFilter. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term"
    }
  },
  "required": ["MethodName", "LanguageId", "StructureId"]
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
        "description": "Unique identifier of the MPs club"
      },
      "Name": {
        "type": "string",
        "description": "Full name/title of the MPs club in requested language. May include prefixes like Интерпартиска парламентарна група (inter-party parliamentary group) or Клуб (club) followed by topic/purpose"
      }
    },
    "required": ["Id", "Name"]
  },
  "description": "Flat array of MPs clubs for the specified structure"
}
```

### Notes

- Response is a direct array (not wrapped in Items/TotalItems pagination structure).
- All clubs for the specified structure are returned; no pagination parameters are supported.
- Club names are localized to the requested LanguageId.
- Uses PascalCase for MethodName and LanguageId (consistent with method-based calling convention).
- See global Calling Conventions § 1 (Method-based) and StructureId § Data Concepts for obtaining the structure UUID.
