## GetAllInstitutionsForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllInstitutionsForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"]
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
        "$ref": "#/$defs/UUID",
        "description": "Unique identifier for the institution"
      },
      "Title": {
        "type": "string",
        "description": "Institution name in the requested language. May contain placeholder values '/' or '-' for invalid/legacy entries."
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes

- **Parameter casing:** Uses camelCase `methodName` and `languageId`.
- **Language fallback:** Responses for `languageId: 3` (Turkish) may return Macedonian (Cyrillic) text for institution titles, indicating incomplete Turkish localization. Confirm behavior per language before use.
- **Placeholder records:** Response includes legacy/inactive entries with `Title: "/"` or `Title: "-"`. Filter or handle client-side when building UI selectors.
- **Usage:** Common in material/question proposer selection and institutional filters. Use `Id` when filtering materials, questions, or other entities by responsible institution.
- **Typical content:** Includes current ministries (e.g., "Министерство за финансии"), Government, parliamentary committees, and historical ministries from past terms.