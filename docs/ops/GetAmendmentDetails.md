## GetAmendmentDetails

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "description": "Operation name (e.g. GetAmendmentDetails or /GetAmendmentDetails); casing may vary"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "amendmentId": {
      "$ref": "#/$defs/UUID",
      "description": "Amendment identifier from GetMaterialDetails"
    }
  },
  "required": ["methodName", "languageId", "amendmentId"]
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "Title": { "type": "string" },
    "ParentMaterialId": { "$ref": "#/$defs/UUID" },
    "ParentMaterialTitle": { "type": "string" },
    "TypeTitle": { "type": "string" },
    "StatusTitle": { "type": "string" },
    "ProposerTypeTitle": { "type": "string" },
    "ResponsibleProposer": { "type": "string" },
    "RegistrationNumber": { "type": "string" },
    "ResponsibleInstitution": { "type": ["string", "null"] },
    "Sittings": { "type": "array", "items": { "type": "object" } },
    "Documents": { "type": "array", "items": { "type": "object" } },
    "Authors": { "type": "array", "items": { "type": "object" } }
  }
}
```

### Notes
- Method-based (MakePostRequest). Amendment details for a given amendmentId; parent material and documents included.
- Refine from collected pairs to complete request/response schema and notes.
