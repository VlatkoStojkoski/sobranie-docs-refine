## OperationName

### Request Schema
```json
{
  "type": "object",
  "description": "Template for per-operation request schema. Replace with actual operation details.",
  "properties": {
    "methodName": {
      "type": "string",
      "description": "Operation method name (camelCase or PascalCase per operation)"
    }
  },
  "required": ["methodName"]
}
```

### Response Schema
```json
{
  "type": "object",
  "description": "Template for per-operation response schema. Replace with actual operation details.",
  "properties": {
    "Items": {
      "type": ["array", "null"],
      "description": "Result items array; may be null when TotalItems is 0"
    },
    "TotalItems": {
      "type": "integer",
      "description": "Total count of items"
    }
  }
}
```

### Notes
- This is a template placeholder. Replace with actual operation request/response schemas and operation-specific notes (parameter casing, pagination style, language fallback, data quality quirks).
- Refer to global.md for common patterns, enums ($defs), and calling conventions.
- Use $ref to global $defs for all enums and shared types (LanguageId, UUID, AspDate, etc.).
- Include only operation-specific details and behaviors in this section.