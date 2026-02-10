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
    "Sittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID" },
          "SittingTypeId": { "$ref": "#/$defs/SittingTypeId" },
          "SittingTypeTitle": { "type": "string" },
          "SittingDate": { "$ref": "#/$defs/AspDate" },
          "CommitteeTitle": { "type": "string" },
          "VotingResults": { "type": "array" }
        }
      }
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID" },
          "Title": { "type": "string" },
          "Url": { "type": "string" },
          "FileName": { "type": ["string", "null"] },
          "DocumentTypeId": { "type": "integer" },
          "DocumentTypeTitle": { "type": ["string", "null"] },
          "IsExported": { "type": "boolean" }
        }
      }
    },
    "Authors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID" },
          "FirstName": { "type": "string" },
          "LastName": { "type": "string" }
        }
      }
    }
  }
}
```

### Notes
- Method-based (MakePostRequest). Amendment details for a given amendmentId; parent material, sittings, documents, and authors included.
- Documents.DocumentTypeId may be 0 (no type/unknown) or reference the DocumentTypeId enum values.
- Documents.DocumentTypeTitle and FileName may be null.
- Sittings array includes sitting metadata (Id, date, type, committee context) and associated voting results.
- Authors array includes amendment proposers and co-signatories with full name components.
