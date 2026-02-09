## GetAllMPsClubsByStructure

### Description
Returns all MPs clubs (inter-party parliamentary groups) for a specified parliamentary structure/term. These are cross-party groups focused on specific issues such as environmental protection, Roma rights, youth issues, and anti-corruption. The response is not paginated and returns all clubs active in the structure.

### Request
```json
{
  "MethodName": "GetAllMPsClubsByStructure",
  "LanguageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

**Request parameters:**
- **MethodName** — Operation name (required, uses uppercase casing)
- **LanguageId** — Language for entity names (1=Macedonian, 2=Albanian, 3=Turkish). See LanguageId in global docs.
- **StructureId** — UUID of the parliamentary term/structure (required). Obtain from `GetAllStructuresForFilter`. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current term. The operation returns clubs active in this structure.

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
        "type": "string"
      }
    },
    "required": ["Id", "Name"]
  }
}
```

**Response keys:**
- **Id** — UUID identifier for the MPs club or inter-party parliamentary group
- **Name** — Full name/title of the MPs club in the requested language. May include prefixes such as "Интерпартиска парламентарна група" (inter-party parliamentary group) or "Клуб" (club) followed by the topic or purpose (e.g., "Клуб за животна средина" = Environmental Protection Club).

### Notes
- Response is a direct array, not wrapped in `Items`/`TotalItems` pagination structure
- All clubs for the specified structure are returned (no pagination parameters available)
- Club names are localized to the requested `LanguageId`