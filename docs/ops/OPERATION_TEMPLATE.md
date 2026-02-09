## OperationName

### Request Schema
```json
{
  "type": "object",
  "description": "Template for per-operation request schema. Replace with actual operation details.",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "OperationName",
      "description": "Use const for the fixed method name (camelCase or PascalCase per operation); do not use single-element enum."
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
- Use $ref to global $defs for all enums and shared types (LanguageId, UUID, AspDate, etc.). Use only $ref for such properties—do not combine with "type" or duplicate description.
- Use "const" for fixed single values (e.g. methodName); do not use single-element "enum".
- Include only operation-specific details and behaviors in this section.