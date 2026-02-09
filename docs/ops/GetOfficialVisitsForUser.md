## GetOfficialVisitsForUser

### Request
```json
{
  "model": "914bff80-4c19-4675-ace4-cb0c7a08f688"
}
```

### Response
```json
{
  "d": []
}
```

### Notes
- **Endpoint format:** ASMX-wrapped POST request
- **Request body:** `model` field contains a UUID string representing the user ID
- **Response format:** `d` property contains array of visit objects (empty array when user has no official visits)
- **Visit object schema:** When visits exist, items in `d` array contain official visit details. Exact schema not yet documented from available examples.
