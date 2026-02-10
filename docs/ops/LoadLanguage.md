## LoadLanguage

### Request Schema
```json
{
  "type": "object",
  "properties": {},
  "description": "Empty body or no body"
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "Code": { "type": "string", "description": "Language code (e.g. mk-MK)" },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Key": { "type": "string" },
          "Value": { "type": "string" }
        }
      },
      "description": "Key-value localization strings"
    }
  }
}
```

### Notes
- Infrastructure endpoint (Infrastructure/LoadLanguage). POST, often empty body. Returns localization strings for a language.
- Refine from collected pairs to complete request/response schema and notes.
