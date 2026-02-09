## GetAllInstitutionsForFilter

### Description
Returns list of institutions (ministries, government bodies). Includes historical and current entities. Contains placeholder records with Title `"/"` or `"-"` that should be filtered. Turkish localization (`languageId: 3`) returns Macedonian text, indicating incomplete translation coverage.

### Request
```json
{
  "methodName": "GetAllInstitutionsForFilter",
  "languageId": 1
}
```

### Request notes
- **languageId** accepts values 1 (Macedonian), 2 (Albanian), or 3 (Turkish). However, responses for `languageId: 3` (Turkish) currently return Macedonian text for institution titles, suggesting incomplete Turkish localization.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "Unique identifier for the institution (UUID)"
      },
      "Title": {
        "type": "string",
        "description": "Institution name (e.g., ministry) in the requested language. May contain placeholder values '/' or '-' for invalid/legacy entries."
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- **Data quality**: Response includes placeholder entries with `Title: "/"` or `Title: "-"` (examples: UUIDs `eb0e5bfd-ee7e-40f2-8cab-322cefd440fd`, `6ebe4c24-98ac-4d4b-99d7-b6d8b10dd1db`, `e48be100-961e-45fa-a53c-c3a73bc6181a`, `4027bbeb-ad05-47b6-a345-f25fdda12e09`, `f7d211f2-6b4b-4ff4-80fa-3a7c8ae97123`, `b9521d21-cb7e-4129-9f15-4bcdf983ce2c`). These are legacy or inactive records. Filter client-side when building UI selectors.
- **Language consistency**: While `languageId` parameter controls the language requested, some institution entries may return text in Macedonian regardless of the requested language due to incomplete translations in the underlying dataset.
- **Usage**: Returns all institutions (ministries, government bodies, state institutions) for use in filters and dropdowns. Common in material/question proposer selection. Use the `Id` value when filtering materials, questions, or other entities by responsible institution.
- **Common institutions**: Response includes entities such as "Министерство за финансии" (Ministry of Finance), "Министерство за образование и наука" (Ministry of Education and Science), "Влада на Република Северна Македонија" (Government of North Macedonia), and both current and historical ministries (e.g., "Министерство за информатичко општество" appears to be historical).
