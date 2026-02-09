## GetAllMaterialsForPublicPortal

### Request
```json
{
  "MethodName": "GetAllMaterialsForPublicPortal",
  "LanguageId": 1,
  "ItemsPerPage": 9,
  "CurrentPage": 1,
  "SearchText": "",
  "AuthorText": "",
  "ActNumber": "",
  "StatusGroupId": null,
  "MaterialTypeId": 1,
  "ResponsibleCommitteeId": null,
  "CoReportingCommittees": null,
  "OpinionCommittees": null,
  "RegistrationNumber": null,
  "EUCompatible": null,
  "DateFrom": null,
  "DateTo": null,
  "ProcedureTypeId": null,
  "InitiatorTypeId": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

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
      "$ref": "#/$defs/LanguageId"
    },
    "ItemsPerPage": {
      "type": "integer",
      "description": "Number of items to return per page (e.g. 7, 9, 15, 31, 46). Equivalent to Rows in other operations."
    },
    "CurrentPage": {
      "type": "integer",
      "description": "Which page of results to return (1-based). Equivalent to Page in other operations."
    },
    "SearchText": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Free-text search in material titles and content. Empty string or null to omit filtering."
    },
    "AuthorText": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Filter by author name (free text). Empty string or null to omit."
    },
    "ActNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Filter by act/law number. Empty string or null to omit."
    },
    "StatusGroupId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by material status group (see MaterialStatusId/StatusGroupId). Null to include all statuses."
    },
    "MaterialTypeId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by material type. Example: 1 for law proposals, 28 for analyses/reports/information. Null to include all types."
    },
    "ResponsibleCommitteeId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of responsible committee. Null to include all committees."
    },
    "CoReportingCommittees": {
      "anyOf": [
        {"type": "array"},
        {"type": "null"}
      ],
      "description": "Filter by co-reporting committee IDs. Null to omit."
    },
    "OpinionCommittees": {
      "anyOf": [
        {"type": "array"},
        {"type": "null"}
      ],
      "description": "Filter by opinion committee IDs. Null to omit."
    },
    "RegistrationNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Filter by exact registration number (e.g. '08-750/1'). Null to omit."
    },
    "EUCompatible": {
      "anyOf": [
        {"type": "boolean"},
        {"type": "null"}
      ],
      "description": "Filter by EU compatibility flag. true=compatible only, false=non-compatible only, null=all materials."
    },
    "DateFrom": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter materials from this date. Null to omit."
    },
    "DateTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter materials up to this date. Null to omit."
    },
    "ProcedureTypeId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by procedure type (see ProcedureTypeId: 1=Regular, 2=Shortened, 3=Urgent). Null to include all."
    },
    "InitiatorTypeId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by initiator/proposer type (see ProposerTypeId). Null to include all."
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of parliamentary term/structure. Null returns materials across all structures/terms. When specified, filters to that structure only."
    }
  },
  "required": ["MethodName", "LanguageId", "ItemsPerPage", "CurrentPage"],
  "additionalProperties": false
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer"
    },
    "Items": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "type": "string",
                "format": "uuid"
              },
              "Title": {
                "type": "string"
              },
              "TypeTitle": {
                "type": "string",
                "description": "Human-readable material type name (e.g. 'Предлог закон', 'Декларација, резолуција, одлука и препорака', 'Анализи, извештаи, информации и друг материјал'). May have leading whitespace."
              },
              "Status": {
                "anyOf": [
                  {"type": "null"},
                  {"type": "string"},
                  {"type": "integer"}
                ],
                "description": "Status field. Observed as consistently null; status info provided via StatusGroupTitle."
              },
              "StatusGroupTitle": {
                "type": "string",
                "description": "Human-readable status group/phase (e.g. 'Доставен до пратеници', 'Затворен', 'Leximi i parë'). Localized per LanguageId."
              },
              "RegistrationNumber": {
                "type": "string",
                "description": "Official registration number (e.g. '08-750/1'). Format: XX-NNNN/Y."
              },
              "RegistrationDate": {
                "$ref": "#/$defs/AspDate",
                "description": "Date when material was registered."
              },
              "ResponsibleAuthor": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Primary/first author name. May be institutional (full title) or individual MP name. Can contain Cyrillic even when other language requested. Null when no designated responsible author."
              },
              "Authors": {
                "anyOf": [
                  {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "Id": {
                          "type": "string",
                          "format": "uuid",
                          "description": "UUID of author. For institutional authors: '00000000-0000-0000-0000-000000000000'. For MPs: real user UUID."
                        },
                        "FirstName": {
                          "type": "string",
                          "description": "For institutional authors: full institution name/title. For MPs: first name."
                        },
                        "LastName": {
                          "type": "string",
                          "description": "For institutional authors: empty string. For MPs: last name."
                        }
                      },
                      "required": ["Id", "FirstName", "LastName"]
                    }
                  },
                  {"type": "null"}
                ],
                "description": "Array of authors. Can be empty array [] for certain proposer types. Includes both individual MPs and institutional authors."
              },
              "ProposerTypeTitle": {
                "type": "string",
                "description": "Human-readable proposer type (e.g. 'Пратеник', 'Влада на Република Северна Македонија', 'Работно тело', 'Друга instituција'). Localized per LanguageId. May have leading whitespace."
              },
              "ResponsibleCommittee": {
                "type": "string",
                "description": "Name of responsible committee in requested language. Empty string for materials without committee assignment (appointments, resignations, decisions)."
              },
              "EUCompatible": {
                "type": "boolean",
                "description": "Whether material is EU-compatible/harmonized. Always present (not nullable)."
              },
              "TotalItems": {
                "anyOf": [
                  {"type": "null"},
                  {"type": "integer"}
                ],
                "description": "Always null at item level. Total count is in root-level TotalItems."
              }
            },
            "required": ["Id", "Title", "TypeTitle", "StatusGroupTitle", "RegistrationNumber", "RegistrationDate", "ProposerTypeTitle", "ResponsibleCommittee", "EUCompatible"]
          }
        },
        {"type": "null"}
      ],
      "description": "Array of materials, null when no results, or empty array [] when TotalItems is 0."
    }
  }
}
```

### Per-operation Notes

**Pagination:** Uses `ItemsPerPage` and `CurrentPage` instead of `Rows` and `Page` pattern. Pagination example: `CurrentPage: 3` with `ItemsPerPage: 19` returns items 39-57 of the total result set.

**Parameter casing:** Uses `MethodName` (capital M) and `LanguageId` (capital L) — PascalCase unlike some other operations.

**StructureId flexibility:** When `StructureId: null`, returns materials across all parliamentary terms/structures (not limited to current term). Example: can yield 976+ total items across all terms vs. smaller subset for specific term. When specified, filters to that structure only.

**StatusGroupId usage:** When set to specific value (e.g. `12`), filters materials to that status group. Maps to MaterialStatusId enum values. Example: `StatusGroupId: 6` filters to "Delivered to MPs" materials, `StatusGroupId: 12` filters to "Closed" materials.

**MaterialTypeId values:** `1` = law proposals (законски предлози/projektligji), `28` = analyses/reports/information/other materials. Full list from GetAllMaterialTypesForFilter.

**Institutional authors pattern:** Government-proposed materials have `Authors[0].Id = "00000000-0000-0000-0000-000000000000"` with minister name/title in `FirstName`, empty `LastName`. Regulatory commissions, agencies, state audit, fiscal council, etc. follow same pattern. When `ProposerTypeTitle` is "Влада..." (Government), "Работно тело" (Working body), or "Друга институција" (Other institution), authors are institutional.

**ResponsibleAuthor behavior:** Can be `null` for materials without designated responsible author (observed with working body proposals). Individual MP materials show MP name; governmental/institutional materials show full title/position in Cyrillic even when other languages requested.

**ResponsibleCommittee empty string:** Confirmed empty string `""` (not null) for appointment/election materials, resignation materials, and certain administrative materials that bypass committee review.

**Authors array variations:** Can be empty array `[]` for certain proposer types (e.g., working body proposals after processing). Multiple co-authors listed as separate array items for MP-proposed materials.

**TypeTitle whitespace:** May have leading `\r\n` characters (e.g. `"\r\nProjektligji"`, `"\r\nAnalizat, raportet, informacionet dhe materialet e tjera"`). Trim when displaying.

**ProposerTypeTitle values observed:** "Пратеник" (MP), "Влада на Република Septembrie Македонија" (Government of RNM), "Работно тело" (Working body), "Друга instituција" (Other institution), "Dërguar" (Delivered - in Albanian). May have leading `\r\n` characters. Corresponds to ProposerTypeId enum.

**StatusGroupTitle values observed:** "Прво читање" (First reading), "Второ читање" (Second reading), "Трето читање" (Third reading), "Затворен" (Closed), "Доставен до пратеници" (Delivered to MPs), "Finalized" (English), "Mbyllur" (Albanian), "Dorëzohet deputetëve" (Albanian), "Leximi i parë" (Albanian), "Leximi i dytë" (Albanian).

**Cross-language institutional text:** Even when requesting Albanian (`LanguageId: 2`) or Turkish (`LanguageId: 3`), the `ResponsibleAuthor` field for government-proposed materials may contain Cyrillic text (Macedonian minister names/titles). Other fields respect requested language.

**Response includes null Items:** When `TotalItems: 0`, response returns `Items: []` (empty array) or `Items: null` depending on the specific result set. Both cases indicate no matching materials.

**EUCompatible filter:** Values `true`, `false`, or `null`. `false` is the common case for MP-proposed materials in typical legislative sessions.
