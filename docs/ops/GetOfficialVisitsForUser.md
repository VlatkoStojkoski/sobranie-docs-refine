## GetOfficialVisitsForUser

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "model": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the user (MP) to retrieve official visits for"
    }
  },
  "required": ["model"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "items": {
        "type": "object",
        "description": "Official visit object. Exact schema not fully documented from available examples; typically contains visit date, location, institution, and visit type/purpose."
      },
      "nullable": true,
      "description": "Array of official visit objects. Empty array or null when user has no visits."
    }
  },
  "required": ["d"]
}
```

### Notes

- **Endpoint:** ASMX-wrapped POST to `https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser`
- **Request format:** Request body is wrapped as `{"model": "<user-uuid>"}`
- **Response format:** Results wrapped in `d` property per ASMX convention (see global Calling Conventions)
- **Empty results:** Returns `{"d": []}` when user has no official visits
- **Schema completeness:** Visit object properties (date, location, institution, type) not yet fully documented from available examples. Client implementations should handle gracefully based on actual response inspection.