## GetMaterialDetails

### Request
```json
{
  "methodName": "GetMaterialDetails",
  "MaterialId": "759ba4db-41e1-4fdd-9176-21cb7c260522",
  "LanguageId": 1,
  "AmendmentsPage": 1,
  "AmendmentsRows": 5
}
```

**Request parameters:**
- **methodName** — Required, string. Operation name: "GetMaterialDetails"
- **MaterialId** — Required, UUID string. Material identifier from GetAllMaterialsForPublicPortal
- **LanguageId** — Required, integer. Language for localized content (1=Macedonian, 2=Albanian, 3=Turkish)
- **AmendmentsPage** — Optional, integer. Page number for amendments pagination (1-based). Controls which page of amendments to retrieve in FirstReadingAmendments and SecondReadingAmendments arrays.
- **AmendmentsRows** — Optional, integer. Number of amendments per page (e.g. 5, 25, 47). Controls size of amendment arrays.

### Response
```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string"
    },
    "StatusGroupTitle": {
      "type": "string"
    },
    "TypeTitle": {
      "type": "string"
    },
    "ProposerTypeTitle": {
      "type": "string"
    },
    "ResponsibleAuthor": {
      "type": "string"
    },
    "Institution": {
      "type": "string"
    },
    "ProposerCommittee": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "ProcedureTypeTitle": {
      "type": "string"
    },
    "RegistrationNumber": {
      "type": "string"
    },
    "RegistrationDate": {
      "$ref": "#/$defs/AspDate"
    },
    "EUCompatible": {
      "type": "boolean"
    },
    "ParentTitle": {
      "type": "string"
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Name": {
            "type": "string"
          },
          "IsLegislative": {
            "type": "boolean"
          },
          "IsResponsible": {
            "type": "boolean"
          },
          "Documents": {
            "type": "array",
            "items": {}
          }
        }
      }
    },
    "Documents": {
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
          "Url": {
            "type": "string"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
          },
          "DocumentTypeId": {
            "type": "integer"
          },
          "DocumentTypeTitle": {
            "type": "string"
          },
          "IsExported": {
            "type": "boolean"
          }
        }
      }
    },
    "FirstReadingAmendments": {
      "type": "array",
      "items": {}
    },
    "SecondReadingAmendments": {
      "type": "array",
      "items": {}
    },
    "FirstReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string",
            "nullable": true
          },
          "StatusGroupId": {
            "type": "integer"
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
            "items": {}
          }
        }
      }
    },
    "SecondReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string",
            "nullable": true
          },
          "StatusGroupId": {
            "type": "integer"
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
            "items": {}
          }
        }
      }
    },
    "ThirdReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string",
            "nullable": true
          },
          "StatusGroupId": {
            "type": "integer"
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
            "items": {}
          }
        }
      }
    },
    "Sittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string",
            "nullable": true
          },
          "StatusGroupId": {
            "type": "integer"
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
            "items": {}
          }
        }
      }
    },
    "Authors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "FirstName": {
            "type": "string"
          },
          "LastName": {
            "type": "string"
          }
        }
      }
    },
    "IsWithdrawn": {
      "type": "boolean"
    },
    "TerminationStatusTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "TerminationNote": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "TerminationDate": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ]
    },
    "AmendmentsTotalRows": {
      "type": "integer"
    }
  }
}
```

## Response keys

- **Title** — Full title/name of the material
- **StatusGroupTitle** — Current procedural stage (e.g. "Прво читање" = First reading, "Второ читање" = Second reading, "Затворен" = Closed)
- **TypeTitle** — Material type name in requested language (e.g. "Предлог закон" = Draft law, "Анализи, извештаи, информации и друг материјал" = Analyses/reports/information/other materials). May contain leading/trailing whitespace.
- **ProposerTypeTitle** — Proposer type in natural language (e.g. "Пратеник" = MP, "Влада на Република Северна Македонија" = Government)
- **ResponsibleAuthor** — Name and title of primary responsible author/proposer. For multi-author materials, represents the lead author from the Authors list. May be empty when no responsible author designated.
- **Institution** — Institution name when material proposed by institutional entity (e.g. ministry, government body). Empty string `""` when proposer is MPs or when not applicable.
- **ProposerCommittee** — Committee name if material proposed by committee. Null for government/MP proposals or other non-committee entities.
- **ProcedureTypeTitle** — Procedure type in natural language (e.g. "Редовна постапка" = Regular procedure, "Скратена постапка" = Shortened procedure, "Итна постапка" = Urgent procedure)
- **RegistrationNumber** — Official registration number assigned by parliament (format: "XX-XXX/X", e.g. "08-676/1")
- **RegistrationDate** — Date material was officially registered with parliament (AspDate format). May include future dates (test data or planned materials).
- **EUCompatible** — Boolean indicating whether material is compatible with EU legislation/standards
- **ParentTitle** — Title of parent material if this is amendment or derivative material. Empty string `""` for standalone materials.
- **Committees** — Array of committees assigned to review the material
  - **Id** — Committee UUID
  - **Name** — Committee name
  - **IsLegislative** — Boolean; true if this is the Legislative-Legal Committee (Законодавно-правна комисија)
  - **IsResponsible** — Boolean; true if this is the lead/responsible committee for the material
  - **Documents** — Committee-specific documents array (may be empty)
- **Documents** — Array of attached documents for the material
  - **Id** — Document UUID
  - **Title** — Document name
  - **Url** — SharePoint download URL
  - **FileName** — Original filename (often null)
  - **DocumentTypeId** — Document type identifier (see $defs: 1=Document, 7=Full text of material, 8=Adopted act, 9=Notification to MPs, 30=Committee report without approval, 46=Legal-Legislative Committee report, 52=Report, 65=Supplemented draft law)
  - **DocumentTypeTitle** — Human-readable document type. May contain control characters like `\r\n`.
  - **IsExported** — Boolean; true if document has been exported/published
- **FirstReadingAmendments** — Array of amendments proposed during first reading. Empty array `[]` when no amendments submitted for first reading.
- **SecondReadingAmendments** — Array of amendments proposed during second reading. Empty array `[]` when no amendments submitted for second reading.
- **FirstReadingSittings** — Array of sittings where material was discussed at first reading stage. Empty array when material not yet scheduled for first reading discussion. Each sitting includes: Id, SittingTypeId (1=plenary, 2=committee), SittingTypeTitle, SittingDate (AspDate), CommitteeId (null for plenary), CommitteeTitle, StatusGroupId, ObjectStatusId, SittingTitle, SittingNumber, VotingResults.
- **SecondReadingSittings** — Array of sittings where material was discussed at second reading stage. Empty array when material not yet scheduled for second reading discussion. Same structure as FirstReadingSittings.
- **ThirdReadingSittings** — Array of sittings where material was discussed at third reading stage. Empty array when material not yet scheduled for third reading discussion. Same structure as FirstReadingSittings.
- **Sittings** — General array of all related sittings (usage purpose may overlap with reading-specific arrays). Empty when no sittings associated. Same structure as FirstReadingSittings.
- **Authors** — Array of co-authors/co-proposers
  - **Id** — UUID identifier. For MPs: actual UUID. For institutional authors: all-zeros UUID `"00000000-0000-0000-0000-000000000000"`
  - **FirstName** — For MPs: first name. For institutional authors: full institution name/title.
  - **LastName** — For MPs: last name. For institutional authors: empty string.
- **IsWithdrawn** — Boolean; true if material has been withdrawn from consideration by proposer(s)
- **TerminationStatusTitle** — Final status when material is closed/terminated (e.g. "Донесен" = Adopted, "Миратуар" = Approved). Null when material still active.
- **TerminationNote** — Administrative note explaining termination reason/outcome (e.g. "СОБРАНИЕТО ГО ДОНЕСЕ ЗАКОНОТ" = Parliament adopted the law). Null when material still active.
- **TerminationDate** — AspDate timestamp when material was finalized/closed. Null when material still active.
- **AmendmentsTotalRows** — Total count of amendments across all reading stages for pagination purposes. Value 0 when no amendments exist.

## Per-operation notes

- **Amendments pagination**: The `AmendmentsPage` and `AmendmentsRows` request parameters control pagination of the amendment arrays (`FirstReadingAmendments`, `SecondReadingAmendments`). The `AmendmentsTotalRows` response field provides the total amendment count across all pages. When no amendments exist (`AmendmentsTotalRows: 0`), both amendment arrays return empty `[]` rather than null.

- **Multi-author materials**: The `Authors` array can contain multiple MP authors for co-proposed materials. The `ResponsibleAuthor` field typically contains the first/primary author's name from this list.

- **Committee processing**: Materials are assigned to multiple committees with different roles. The `IsResponsible: true` flag identifies the lead committee. The `IsLegislative: true` flag identifies the legislative-legal review committee (standard for all legislative materials). Each committee may have associated `Documents` array (may be empty).

- **Reading stages**: Materials progress through three reading stages (first, second, third). Each reading has a corresponding `*ReadingSittings` array containing plenary (`SittingTypeId: 1`, `CommitteeId: null`) and/or committee (`SittingTypeId: 2`, with populated `CommitteeId`/`CommitteeTitle`) sitting records. Empty arrays indicate the material has not yet reached that stage.

- **Status tracking**: In sitting objects, `StatusGroupId` and `ObjectStatusId` both equal 9 indicates completed first reading; values 10 and 11 indicate second and third readings respectively.

- **Empty arrays**: Amendment and sitting arrays (`FirstReadingAmendments`, `SecondReadingAmendments`, FirstReadingSittings, SecondReadingSittings, ThirdReadingSittings, Sittings`) return empty arrays `[]` when no data exists, not `null` (contrast with paginated list operations where `TotalItems: 0` causes `Items: null`).

- **Institutional authors**: When `ProposerTypeId` is 2 (Government), the `Authors` array contains entries with `Id: "00000000-0000-0000-0000-000000000000"`, `FirstName` containing the full official title/name (e.g. minister name), and `LastName` as empty string. The `ResponsibleAuthor` field duplicates this information. The `Institution` field contains the ministry/institution name.

- **Data quality - whitespace**: The `TypeTitle` and `DocumentTypeTitle` fields may contain leading/trailing whitespace and control characters (`\r`, `\n`). Trim as needed for display.

- **Document truncation**: Large document arrays may be truncated (indicated by `"_truncated": 1` marker in final element). Total document count not provided; full document list may require multiple calls or alternative queries.

- **Registration date precision**: The `RegistrationDate` field uses AspDate format and may include future timestamps (indicating test data, planned materials, or specific timezone handling).

- **Sittings duplicates**: The `Sittings` array may contain multiple entries with the same `SittingNumber` but different `Id` and `SittingDate` values. This likely represents multi-day sessions or continuations of the same formal sitting.
