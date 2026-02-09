## GetAllMaterialStatusesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllMaterialStatusesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "description": "Reference data request for material processing statuses. Returns localized status labels used as filter parameters in listing operations."
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
        "$ref": "#/$defs/MaterialStatusId",
        "description": "Unique status identifier for use in filter operations"
      },
      "Title": {
        "type": "string",
        "description": "Localized status name per languageId parameter (1=Macedonian, 2=Albanian, 3=Turkish)"
      }
    },
    "required": ["Id", "Title"]
  },
  "description": "Flat array of active material statuses with localized titles"
}
```

### Notes

- **Response format:** Direct array (not paginated; no TotalItems wrapper).
- **Localization:** `Title` is localized per the `languageId` parameter. Test different language IDs to confirm behavior.
- **Returned statuses:** Only active/filterable statuses (6, 9, 10, 11, 12, 24, 64). Status 0 (Plenary/unknown) may appear in material detail records but is not returned by this endpoint.
- **Use in filters:** Pass returned `Id` values as `StatusId` or `StatusGroupId` filter parameters in operations like `GetAllMaterialsForPublicPortal` and `GetAllSittings`.
- **No additional parameters:** This is a simple reference catalog with only `methodName` and `languageId` required.
- **Parameter casing:** Uses `methodName` (camelCase).
