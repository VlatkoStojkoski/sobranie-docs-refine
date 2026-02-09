## GetAllMaterialTypesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllMaterialTypesForFilter"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
    }
  },
  "required": ["methodName", "languageId"]
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
        "$ref": "#/$defs/MaterialTypeId",
        "description": "Material type identifier"
      },
      "Title": {
        "type": "string",
        "description": "Localized material type name in requested language. May contain leading/trailing whitespace or control characters (\\r, \\n) requiring trimming for display."
      }
    },
    "required": ["Id", "Title"]
  },
  "description": "Flat array of 37 material types covering legislative materials (laws, amendments, budget), procedural items (elections, appointments, resignations), oversight mechanisms (interpellations, reports), and constitutional procedures (amendments, interpretations)."
}
```

### Notes

- **Casing:** Uses lowercase `methodName` and `languageId` (camelCase).
- **Localization:** Response titles are localized in the requested `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).
- **Data quality:** Title values may contain leading/trailing whitespace characters (`\r`, `\n`, spaces) that should be trimmed for display. See global data quality notes.
- **Non-sequential IDs:** Material type IDs are not consecutive; IDs 12 and 25 are absent from the enumeration.
- **Usage:** Material type IDs returned here are used as `MaterialTypeId` filter values in `GetAllMaterialsForPublicPortal` and appear in material detail responses (GetMaterialDetails).
- **Returns:** Flat array of all material types (not paginated); no null check needed.