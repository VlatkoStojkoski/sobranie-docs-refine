## GetAllMaterialTypesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialTypesForFilter",
  "languageId": 1
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
        "type": "integer",
        "description": "Material type identifier. See MaterialTypeId in $defs for known values (1–37, non-sequential; gaps at 12 and 25)."
      },
      "Title": {
        "type": "string",
        "description": "Localized material type name in requested language (1=Macedonian, 2=Albanian, 3=Turkish). May contain leading/trailing whitespace or control characters (\\r, \\n) requiring trimming."
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns all available material types in the system (37 types with gaps at IDs 12 and 25).
- **Data quality:** Response `Title` values may contain leading/trailing whitespace characters (`\r`, `\n`, spaces) that should be trimmed for display.
- **Language support:** Tested with `languageId: 2` (Albanian) and `languageId: 1` (Macedonian). Titles are localized in the requested language.
- **Non-sequential IDs:** Material type IDs are not consecutive. IDs 12 and 25 are absent from the enumeration.
- **Usage:** Material type IDs returned here are used as `MaterialTypeId` filter values in `GetAllMaterialsForPublicPortal` operation and appear in material detail responses.
- **Material types:** Catalog includes legislative materials (laws, amendments, budget), procedural items (elections, appointments, resignations), oversight mechanisms (interpellations, reports), and constitutional procedures (amendments, interpretations).