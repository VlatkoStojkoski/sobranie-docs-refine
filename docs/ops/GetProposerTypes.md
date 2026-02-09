## GetProposerTypes

### Request
```json
{
  "methodName": "GetProposerTypes",
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
        "$ref": "#/$defs/ProposerTypeId"
      },
      "Title": {
        "type": "string"
      },
      "Order": {
        "type": "integer"
      }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```

### Notes
- **Language fallback behavior**: When `languageId` is set to a non-Macedonian value (e.g., 2=Albanian, 3=Turkish), the API may return `Title` values in Macedonian as fallback. The request structure and response schema remain unchanged, but localization may not be fully applied to all catalog operations.