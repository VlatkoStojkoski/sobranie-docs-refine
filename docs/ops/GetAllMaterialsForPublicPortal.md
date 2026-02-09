## GetAllMaterialsForPublicPortal

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "MethodName": {
      "type": "string",
      "enum": ["GetAllMaterialsForPublicPortal"],
      "description": "Operation name (PascalCase)"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Localization: 1=Macedonian, 2=Albanian, 3=Turkish"
    },
    "ItemsPerPage": {
      "type": "integer",
      "description": "Number of items per page (e.g. 7, 9, 15, 31, 46). Equivalent to Rows in other operations."
    },
    "CurrentPage": {
      "type": "integer",
      "description": "Which page (1-based). Equivalent to Page in other operations."
    },
    "SearchText": {
      "anyOf": [{"type": "string"}, {"type": "null"}],
      "description": "Free-text search in material titles/content. Empty string or null to omit."
    },
    "AuthorText": {
      "anyOf": [{"type": "string"}, {"type": "null"}],
      "description": "Filter by author name (free text). Empty string or null to omit."
    },
    "ActNumber": {
      "anyOf": [{"type": "string"}, {"type": "null"}],
      "description": "Filter by act/law number. Empty string or null to omit."
    },
    "StatusGroupId": {
      "anyOf": [{"$ref": "#/$defs/StatusGroupId"}, {"type": "null"}],
      "description": "Filter by material status group (6=Delivered to MPs, 9=First reading, 10=Second reading, 11=Third reading, 12=Closed, 24=Rejected, 64=Committee processing). Null to include all statuses."
    },
    "MaterialTypeId": {
      "anyOf": [{"$ref": "#/$defs/MaterialTypeId"}, {"type": "null"}],
      "description": "Filter by material type. Example: 1=Law proposal, 28=Report/Analysis. Full list from GetAllMaterialTypesForFilter. Null to include all."
    },
    "ResponsibleCommitteeId": {
      "anyOf": [{"$ref": "#/$defs/UUID"}, {"type": "null"}],
      "description": "UUID of responsible committee. Null to include all."
    },
    "CoReportingCommittees": {
      "anyOf": [{"type": "array"}, {"type": "null"}],
      "description": "Filter by co-reporting committee IDs. Null to omit."
    },
    "OpinionCommittees": {
      "anyOf": [{"type": "array"}, {"type": "null"}],
      "description": "Filter by opinion committee IDs. Null to omit."
    },
    "RegistrationNumber": {
      "anyOf": [{"type": "string"}, {"type": "null"}],
      "description": "Filter by exact registration number (e.g. '08-750/1'). Null to omit."
    },
    "EUCompatible": {
      "anyOf": [{"type": "boolean"}, {"type": "null"}],
      "description": "true=EU-compatible only, false=non-compatible only, null=all."
    },
    "DateFrom": {
      "anyOf": [{"$ref": "#/$defs/AspDate"}, {"type": "null"}],
      "description": "Filter materials from this date. Null to omit."
    },
    "DateTo": {
      "anyOf": [{"$ref": "#/$defs/AspDate"}, {"type": "null"}],
      "description": "Filter materials up to this date. Null to omit."
    },
    "ProcedureTypeId": {
      "anyOf": [{"$ref": "#/$defs/ProcedureTypeId"}, {"type": "null"}],
      "description": "Filter by procedure type (1=Regular, 2=Shortened, 3=Urgent). Null to include all."
    },
    "InitiatorTypeId": {
      "anyOf": [{"$ref": "#/$defs/ProposerTypeId"}, {"type": "null"}],
      "description": "Filter by initiator/proposer type. Null to include all."
    },
    "StructureId": {
      "anyOf": [{"$ref": "#/$defs/UUID"}, {"type": "null"}],
      "description": "UUID of parliamentary term/structure. Null returns materials across all terms/structures. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term."
    }
  },
  "required": ["MethodName", "LanguageId", "ItemsPerPage", "CurrentPage"],
  "additionalProperties": false
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer",
      "description": "Total count of materials matching filter across all pages."
    },
    "Items": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "UUID of the material."
              },
              "Title": {
                "type": "string",
                "description": "Material title in requested language."
              },
              "TypeTitle": {
                "type": "string",
                "description": "Human-readable material type (e.g. 'Предлог закон', 'Декларација...'). May have leading whitespace (\\r, \\n); trim for display."
              },
              "Status": {
                "anyOf": [{"type": "null"}, {"type": "string"}, {"type": "integer"}],
                "description": "Consistently null; use StatusGroupTitle for actual status."
              },
              "StatusGroupTitle": {
                "type": "string",
                "description": "Material status group in requested language (e.g. 'Доставен до пратеници', 'Затворен', 'Leximi i parë'). Localized per LanguageId."
              },
              "RegistrationNumber": {
                "type": "string",
                "description": "Official registration number (e.g. '08-750/1'). Format: XX-NNNN/Y."
              },
              "RegistrationDate": {
                "$ref": "#/$defs/AspDate",
                "description": "Date material was registered."
              },
              "ResponsibleAuthor": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "description": "Primary/first author name. May be institutional (full title in Cyrillic) or individual MP name. Null when no designated responsible author."
              },
              "Authors": {
                "anyOf": [
                  {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "Id": {
                          "$ref": "#/$defs/UUID",
                          "description": "Author UUID. For institutions: 00000000-0000-0000-0000-000000000000. For MPs: real user UUID."
                        },
                        "FirstName": {
                          "type": "string",
                          "description": "For institutions: full name/title. For MPs: first name."
                        },
                        "LastName": {
                          "type": "string",
                          "description": "For institutions: empty string. For MPs: last name."
                        }
                      },
                      "required": ["Id", "FirstName", "LastName"]
                    },
                    "description": "Array of authors (MP or institutional). Can be empty []."
                  },
                  {"type": "null"}
                ]
              },
              "ProposerTypeTitle": {
                "type": "string",
                "description": "Human-readable proposer type in requested language (e.g. 'Пратеник', 'Влада...', 'Работно тело'). May have leading whitespace (\\r, \\n); trim for display."
              },
              "ResponsibleCommittee": {
                "type": "string",
                "description": "Name of responsible committee in requested language. Empty string \"\" for materials without committee assignment (appointments, resignations, decisions)."
              },
              "EUCompatible": {
                "type": "boolean",
                "description": "Whether material is EU-compatible/harmonized. Always present (not nullable)."
              },
              "TotalItems": {
                "anyOf": [{"type": "null"}, {"type": "integer"}],
                "description": "Always null at item level. Total count in root-level TotalItems."
              }
            },
            "required": ["Id", "Title", "TypeTitle", "StatusGroupTitle", "RegistrationNumber", "RegistrationDate", "ProposerTypeTitle", "ResponsibleCommittee", "EUCompatible"]
          }
        },
        {"type": "null"}
      ],
      "description": "Array of materials. Null when TotalItems: 0, or empty array [] depending on result set. Both indicate no matching materials."
    }
  },
  "required": ["TotalItems", "Items"],
  "additionalProperties": false
}
```

### Notes

**Pagination:** Uses `ItemsPerPage` and `CurrentPage` (alternative pagination pattern) instead of `Rows`/`Page`. Example: `CurrentPage: 3, ItemsPerPage: 19` returns items 39–57 of total.

**Parameter casing:** Uses `MethodName` (capital M) and `LanguageId` (capital L) — PascalCase. See global Calling Conventions for context.

**StructureId flexibility:** When `null`, returns materials across all parliamentary terms/structures (e.g., 976+ total). When specified, filters to that structure. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. See global StructureId section.

**Filters:** StatusGroupId, MaterialTypeId, ResponsibleCommitteeId, ProcedureTypeId, InitiatorTypeId all support null (include all). StatusGroupId maps to MaterialStatusId enum values in global $defs. MaterialTypeId full list from GetAllMaterialTypesForFilter catalog.

**Institutional authors:** Government/institution materials have `Authors[0].Id = "00000000-0000-0000-0000-000000000000"` with full title/name in `FirstName`, empty `LastName`. See global Institutional Authors section.

**ResponsibleAuthor:** Can be `null`. Government materials show full Cyrillic institutional title even when LanguageId requests Albanian/Turkish; other fields respect requested language.

**ResponsibleCommittee:** Empty string `""` (not null) for materials without committee assignment (appointments, resignations, decisions). See global Committee & Plenary Contexts.

**Authors array:** Can be empty `[]`. Multiple co-authors listed separately.

**TypeTitle/ProposerTypeTitle whitespace:** May include leading `\r`, `\n`, or spaces. Trim for display. See global Data Quality Notes.

**Response nullability:** When `TotalItems: 0`, Items may be `null` or `[]`. Both indicate no results. See global Common Patterns.

**EUCompatible:** `true` (EU-compatible only), `false` (non-compatible only), `null` (all materials).