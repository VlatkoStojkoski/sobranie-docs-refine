## GetAllGenders

### Request
```json
{
  "methodName": "GetAllGenders",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "type": "integer",
        "enum": [1, 2],
        "description": "1=Male (Машки), 2=Female (Женски)"
      },
      "Title": {
        "type": "string",
        "description": "Localized gender name"
      }
    }
  }
}
```

### Notes
- Returns exactly 2 items: Male (Id=1) and Female (Id=2)
- Response is a direct array (not wrapped in object with TotalItems/Items)
- `Title` values are localized per the `languageId` request parameter. For languageId=1 (Macedonian): "Машки" (Male), "Женски" (Female)
- Use `Id` values (1 or 2) as filter input in `GetParliamentMPsNoImage` and other operations requiring gender selection
- Reference data: always returns the same 2 entries, no pagination