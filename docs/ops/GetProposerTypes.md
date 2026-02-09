## GetProposerTypes

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetProposerTypes"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
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
        "$ref": "#/$defs/ProposerTypeId"
      },
      "Title": {
        "type": "string",
        "description": "Localized proposer type name in requested language (e.g., 'Пратеник', 'Влада на Република Северна Македонија')"
      },
      "Order": {
        "type": "integer",
        "description": "Display order / sort index for the proposer type"
      }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```

### Notes
- **Operation type**: Catalog / reference data. Returns a simple flat array of all proposer types in a single response (not paginated).
- **Request format**: Method-based operation using camelCase `languageId`.
- **Language fallback behavior**: When `languageId` is set to a non-Macedonian value (e.g., 2=Albanian, 3=Turkish), the API may return `Title` values in Macedonian as fallback. Localization may not be fully applied per language; test with different language IDs to confirm expected behavior.
- **Usage**: `Id` values (1=MP, 2=Government, 4=Voter group) are used in filter parameters of other operations (e.g., `ProposerTypeId` or `InitiatorTypeId`). See global $defs for ProposerTypeId enum.
- **Example response**: `[{"Id": 1, "Title": "Пратеник", "Order": 1}, {"Id": 2, "Title": "Влада на Република Северна Македонија", "Order": 2}, {"Id": 4, "Title": "Граѓанска иницијатива", "Order": 3}, ...]`