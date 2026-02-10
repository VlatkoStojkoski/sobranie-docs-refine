## GetMaterialDetails

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetMaterialDetails",
      "description": "Operation name"
    },
    "MaterialId": {
      "$ref": "#/$defs/UUID",
      "description": "Material identifier from GetAllMaterialsForPublicPortal"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Language for localized content (1=Macedonian, 2=Albanian, 3=Turkish)"
    },
    "AmendmentsPage": {
      "type": "integer",
      "description": "Page number for amendments pagination (1-based); optional, default 1"
    },
    "AmendmentsRows": {
      "type": "integer",
      "description": "Number of amendments per page (e.g. 5, 25); optional"
    }
  },
  "required": ["methodName", "MaterialId", "LanguageId"],
  "additionalProperties": false
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string",
      "description": "Full title/name of the material"
    },
    "StatusGroupTitle": {
      "type": "string",
      "description": "Current procedural stage in requested language (e.g. \"Прво читање\" = First reading)"
    },
    "TypeTitle": {
      "type": "string",
      "description": "Material type name in requested language. May contain leading/trailing whitespace; trim for display."
    },
    "ProposerTypeTitle": {
      "type": "string",
      "description": "Proposer type in natural language (e.g. \"Пратеник\" = MP, \"Влада на Република Северна Македонија\" = Government)"
    },
    "ResponsibleAuthor": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Name and title of primary responsible author/proposer. For multi-author materials, represents lead author. Null when no responsible author designated (e.g. committee/working body proposer) or for certain material types. May contain Cyrillic (Macedonian) even if other language requested."
    },
    "Institution": {
      "type": "string",
      "description": "Institution name when material proposed by institutional entity (e.g. government). Empty string when proposer is MPs or not applicable."
    },
    "ProposerCommittee": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee name if material proposed by committee. Null for government/MP proposals."
    },
    "ProcedureTypeTitle": {
      "type": "string",
      "description": "Procedure type in natural language (e.g. \"Редовна постапка\" = Regular, \"Скратена постапка\" = Shortened, \"Итна постапка\" = Urgent)"
    },
    "RegistrationNumber": {
      "type": "string",
      "description": "Official registration number (format: XX-XXX/X, e.g. 08-676/1)"
    },
    "RegistrationDate": {
      "$ref": "#/$defs/AspDate",
      "description": "Date material was registered"
    },
    "EUCompatible": {
      "type": "boolean",
      "description": "Indicates EU compatibility assessment"
    },
    "ParentTitle": {
      "type": "string",
      "description": "Title of parent material if this is amendment or derivative. Empty string for standalone materials."
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Committee UUID"
          },
          "Name": {
            "type": "string",
            "description": "Committee name"
          },
          "IsLegislative": {
            "type": "boolean",
            "description": "True if Legislative-Legal Committee (Законодавно-правна комисија)"
          },
          "IsResponsible": {
            "type": "boolean",
            "description": "True if lead/responsible committee"
          },
          "Documents": {
            "type": "array",
            "items": {
              "type": "object"
            },
            "description": "Committee-specific documents array (may be empty)"
          }
        },
        "required": ["Id", "Name", "IsLegislative", "IsResponsible", "Documents"]
      },
      "description": "Committees assigned to review the material"
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Document UUID"
          },
          "Title": {
            "type": "string",
            "description": "Document name"
          },
          "Url": {
            "type": "string",
            "description": "SharePoint download URL"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Original filename (often null)"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId",
            "description": "Document type (see global $defs)"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Human-readable document type. May contain leading/trailing whitespace and control characters (\\r, \\n); trim for display."
          },
          "IsExported": {
            "type": "boolean",
            "description": "True if exported/published"
          }
        },
        "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      },
      "description": "Array of attached documents. Large arrays may be truncated (indicated by _truncated marker)."
    },
    "FirstReadingAmendments": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Amendments for first reading. Empty array when no amendments."
    },
    "SecondReadingAmendments": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Amendments for second reading. Empty array when no amendments."
    },
    "FirstReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "SittingTypeId": {
            "$ref": "#/$defs/SittingTypeId"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "anyOf": [
              {"$ref": "#/$defs/UUID"},
              {"type": "null"}
            ],
            "description": "Null for plenary; populated for committee sitting"
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Null for plenary; populated for committee sitting"
          },
          "StatusGroupId": {
            "$ref": "#/$defs/StatusGroupId"
          },
          "ObjectStatusId": {
            "type": "integer"
          },
          "SittingTitle": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          },
          "VotingResults": {
            "type": "array",
            "items": {
              "type": "object"
            }
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "CommitteeId", "CommitteeTitle", "StatusGroupId", "ObjectStatusId", "SittingTitle", "SittingNumber", "VotingResults"]
      },
      "description": "Sittings discussing material at first reading. Empty when not yet scheduled."
    },
    "SecondReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "SittingTypeId": {
            "$ref": "#/$defs/SittingTypeId"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "anyOf": [
              {"$ref": "#/$defs/UUID"},
              {"type": "null"}
            ]
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
          },
          "StatusGroupId": {
            "$ref": "#/$defs/StatusGroupId"
          },
          "ObjectStatusId": {
            "type": "integer"
          },
          "SittingTitle": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          },
          "VotingResults": {
            "type": "array",
            "items": {
              "type": "object"
            }
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "CommitteeId", "CommitteeTitle", "StatusGroupId", "ObjectStatusId", "SittingTitle", "SittingNumber", "VotingResults"]
      },
      "description": "Sittings at second reading. Same structure as FirstReadingSittings."
    },
    "ThirdReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "SittingTypeId": {
            "$ref": "#/$defs/SittingTypeId"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "anyOf": [
              {"$ref": "#/$defs/UUID"},
              {"type": "null"}
            ]
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
          },
          "StatusGroupId": {
            "$ref": "#/$defs/StatusGroupId"
          },
          "ObjectStatusId": {
            "type": "integer"
          },
          "SittingTitle": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          },
          "VotingResults": {
            "type": "array",
            "items": {
              "type": "object"
            }
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "CommitteeId", "CommitteeTitle", "StatusGroupId", "ObjectStatusId", "SittingTitle", "SittingNumber", "VotingResults"]
      },
      "description": "Sittings at third reading. Same structure as FirstReadingSittings."
    },
    "Sittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "SittingTypeId": {
            "$ref": "#/$defs/SittingTypeId"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "anyOf": [
              {"$ref": "#/$defs/UUID"},
              {"type": "null"}
            ]
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
          },
          "StatusGroupId": {
            "$ref": "#/$defs/StatusGroupId"
          },
          "ObjectStatusId": {
            "type": "integer"
          },
          "SittingTitle": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          },
          "VotingResults": {
            "type": "array",
            "items": {
              "type": "object"
            }
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "CommitteeId", "CommitteeTitle", "StatusGroupId", "ObjectStatusId", "SittingTitle", "SittingNumber", "VotingResults"]
      },
      "description": "General array of all related sittings. Empty when none. Same structure as FirstReadingSittings."
    },
    "Authors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "For MPs: actual UUID. For institutional authors: all-zeros UUID (00000000-0000-0000-0000-000000000000)"
          },
          "FirstName": {
            "type": "string",
            "description": "For MPs: first name. For institutional authors: full institution name/title."
          },
          "LastName": {
            "type": "string",
            "description": "For MPs: last name. For institutional authors: empty string."
          }
        },
        "required": ["Id", "FirstName", "LastName"]
      },
      "description": "Array of co-authors/co-proposers. Can contain multiple MP co-proposers. ResponsibleAuthor typically contains first/primary author."
    },
    "IsWithdrawn": {
      "type": "boolean",
      "description": "True if withdrawn from consideration"
    },
    "TerminationStatusTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Final status when closed/terminated (e.g. \"Донесен\" = Adopted, \"Миратуар\" = Approved). Null when still active."
    },
    "TerminationNote": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Administrative note explaining termination. Null when still active."
    },
    "TerminationDate": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Timestamp when finalized. Null when still active."
    },
    "AmendmentsTotalRows": {
      "type": "integer",
      "description": "Total count of amendments for pagination. 0 when no amendments exist."
    }
  },
  "required": ["Title", "StatusGroupTitle", "TypeTitle", "ProposerTypeTitle", "ResponsibleAuthor", "Institution", "ProposerCommittee", "ProcedureTypeTitle", "RegistrationNumber", "RegistrationDate", "EUCompatible", "ParentTitle", "Committees", "Documents", "FirstReadingAmendments", "SecondReadingAmendments", "FirstReadingSittings", "SecondReadingSittings", "ThirdReadingSittings", "Sittings", "Authors", "IsWithdrawn", "TerminationStatusTitle", "TerminationNote", "TerminationDate", "AmendmentsTotalRows"]
}
```

### Notes

- **Amendments pagination:** Request parameters `AmendmentsPage` and `AmendmentsRows` control amendment array pagination (1-based). Response field `AmendmentsTotalRows` provides total count. When no amendments exist (AmendmentsTotalRows: 0), both amendment arrays return empty [].

- **Multi-author materials:** Authors array can contain multiple MP co-proposers. ResponsibleAuthor typically contains first/primary author name and title.

- **ResponsibleAuthor nullability:** ResponsibleAuthor field is null when no responsible author is designated, which occurs for certain proposer types such as committee/working body proposals (ProposerTypeId=3 or other institutional proposers) or certain material types without designated responsibility.

- **Committee processing:** Materials assigned to multiple committees with different roles. IsResponsible: true identifies lead committee. IsLegislative: true identifies legislative-legal review committee. Each committee may have associated Documents array.

- **Reading stages:** Materials progress through three reading stages. Each reading has corresponding *ReadingSittings array containing plenary (SittingTypeId: 1, CommitteeId: null) and/or committee (SittingTypeId: 2, with populated CommitteeId/CommitteeTitle) sitting records. Empty arrays indicate material not yet reached that stage. In sitting objects, StatusGroupId 9=first reading, 10=second reading, 11=third reading, 0=no specific reading stage (plenary discussion without stage context).

- **Empty arrays:** Amendment and sitting arrays return empty arrays [] when no data exists, not null.

- **Government institutional authors:** When ProposerTypeId is 2 (Government), Authors array contains entries with Id as all-zeros UUID, FirstName containing full official title/name (e.g. minister name), and LastName as empty string. ResponsibleAuthor duplicates this information and may contain Cyrillic text (Macedonian) even when other language requested. Institution field contains ministry/institution name. This pattern applies only to government proposals; other non-MP proposer types may differ.

- **Data quality - whitespace:** TypeTitle, DocumentTypeTitle, and other catalog fields may contain leading/trailing whitespace and control characters (\r, \n). Trim as needed for display.

- **Document truncation:** Large document arrays may be truncated (indicated by _truncated marker). Total document count not provided; full list may require alternative queries.

- **Registration date precision:** RegistrationDate field may include future timestamps (indicating test data, planned materials, or specific timezone handling).

- **Sittings duplicates:** Sittings array may contain multiple entries with same SittingNumber but different Id and SittingDate values. This represents multi-day sessions or continuations of the same formal sitting.

- **Language behavior:** Localized fields (StatusGroupTitle, TypeTitle, ProposerTypeTitle, ProcedureTypeTitle) return text in requested LanguageId (1=Macedonian, 2=Albanian, 3=Turkish). However, ResponsibleAuthor and Institution for government-proposed materials may contain Cyrillic regardless of requested language.