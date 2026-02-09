## GetAllMaterialStatusesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialStatusesForFilter",
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
        "$ref": "#/$defs/MaterialStatusId"
      },
      "Title": {
        "type": "string"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns reference data for material processing statuses available in the legislative workflow.
- Use the returned `Id` values as the `StatusId` filter parameter in `GetAllMaterialsForPublicPortal` and similar operations.
- The `Title` value is localized according to the `languageId` parameter in the request (1=Macedonian, 2=Albanian, 3=Turkish).
- Returns only active/filterable statuses (6, 9, 10, 11, 12, 24, 64). Status `0` (Plenary/unknown) may appear in material detail records from other operations but is not returned by this catalog endpoint.
- Direct array response (not paginated; no TotalItems wrapper).
