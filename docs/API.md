# Sobranie.mk API Index

> North Macedonian Parliament (Собрание) — operation index and calling conventions.

## Calling Conventions

### 1. Method-based (standard)

**URL:** `https://www.sobranie.mk/Routing/MakePostRequest`  
**Method:** POST  
**Content-Type:** application/json

Request body includes `methodName` (or `MethodName` for some operations) and operation-specific parameters. The method name selects the operation.

### 2. ASMX (non-standard)

**Base:** `https://www.sobranie.mk/Moldova/services/`  
**Format:** POST with wrapped request body (e.g. `{ "model": { ... } }`).  
**Response:** Often wrapped in `d` property.

### 3. Infrastructure (non-standard)

**Base:** `https://www.sobranie.mk/Infrastructure/`  
**Format:** POST, no methodName. Different request/response shapes.

### Parameter Casing

Some operations use `methodName`/`languageId` (camelCase); others use `MethodName`/`LanguageId` (PascalCase). See per-operation notes for each endpoint.

## Date & Language Conventions

- **Date format:** `/Date(timestamp)/` — milliseconds since Unix epoch (AspDate).
- **LanguageId:** 1 = Macedonian, 2 = Albanian, 3 = Turkish.

## Data Concepts

### StructureId

Parliamentary term/structure identifier (UUID). Obtain from `GetAllStructuresForFilter`. The structure with `IsCurrent: true` is the active parliamentary term and should be used as default StructureId in filter operations. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current term). Historical terms available back to at least 2008. When set to `null` in some operations (e.g. GetParliamentMPsNoImage, GetAllQuestions), returns empty results or cross-term results; Statistics object may still be populated with global counts.

### Institutional Authors

`Authors[].Id` = `"00000000-0000-0000-0000-000000000000"` with full name/title in `FirstName`, empty `LastName`. Used for government, committees, other institutions.

### Committee & Plenary Contexts

- `CommitteeId`/`CommitteeTitle` are `null` for plenary (`TypeId`/`SittingTypeId` = 1); populated for committee (2).
- `ResponsibleCommittee` can be empty string `""` for material types without committee assignment (appointments, resignations, certain decisions).

## Data Quality Notes

- **Placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `/`, `-`, or empty string. Filter or handle gracefully in client code.
- **Whitespace in catalog fields:** Material type titles and other catalog entries may contain leading/trailing whitespace (`\r`, `\n`, spaces). Trim for display.
- **Language fallback:** Some catalog operations (e.g. `GetAllProcedureTypes`) may return Macedonian text regardless of the requested `languageId`. Test with different language IDs to confirm behavior per endpoint.
- **Institutional author text:** Even when requesting non-Macedonian languages, `ResponsibleAuthor` for government-proposed materials may contain Cyrillic text (Macedonian). Other fields respect the requested language.

## Common Patterns

- **Pagination:** Two styles — (1) `Page` (1-based) and `Rows`; (2) `CurrentPage` and `ItemsPerPage`. When `TotalItems: 0`, `Items` may be `null` rather than `[]`. Check per-operation docs.
- **Array truncation:** Large arrays may include `"_truncated": N` indicating N additional items omitted. In detail endpoints, `_truncated` typically appears on the last item of a truncated array when present.
- **Multi-language:** Operations like GetAllMaterialsForPublicPortal and GetAllQuestions return localized text (TypeTitle, StatusGroupTitle, etc.) based on `LanguageId`.
- **Reading stages:** `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings` track material progress. Each contains sitting objects with `SittingTypeId` (1=plenary, 2=committee), `StatusGroupId`, `ObjectStatusId`.
- **Agenda tree:** GetSittingDetails agenda uses hierarchical tree with `type: "ROOT"` and `type: "LEAF"`; leaf nodes may reference materials via `objectId`/`objectTypeId`. Some fields (e.g. `afterText`) may contain XML-like language tags (`<MK>...</><AL>...</>`).
- **HTML content:** Fields like Description in GetCommitteeDetails/GetCouncilDetails contain HTML-formatted text.
- **Parliamentary group contact:** `Email` and `Phone` for parliamentary groups are typically `null`; contact is via individual members. List endpoint (GetAllParliamentaryGroups) does not include these fields; they appear in GetParliamentaryGroupDetails.

## Common Request Filters

- **StructureId:** Parliamentary term UUID; from GetAllStructuresForFilter. Often required for list/detail operations.
- **LanguageId / languageId:** 1=Macedonian, 2=Albanian, 3=Turkish. Casing varies by operation (see per-op docs).
- **Page, Rows:** 1-based pagination used by most listing operations.
- **CurrentPage, ItemsPerPage:** Alternative pagination (e.g. GetAllMaterialsForPublicPortal).
- **TypeId, StatusId, CommitteeId, SearchText, RegistrationNumber, DateFrom, DateTo:** Context-dependent; see per-operation docs.

## Common Response Keys

- **TotalItems:** Total count; when 0, `Items` may be `null`.
- **Items:** Array of results (or null when TotalItems is 0).
- **d:** ASMX responses often wrap the payload in a `d` property.
- **CompositionMembers, SecretariatMembers:** Arrays of role-based personnel (in council/committee detail responses); role membership via `CommitteeRoleId`.
- **Materials:** Array in detail responses (empty `[]` when absent, not `null`).
- **Meetings:** Array in reverse chronological order.

## $defs

```json
{
  "AspDate": {
    "type": "string",
    "pattern": "^/Date\\(\\d+\\)/$",
    "description": "Milliseconds since Unix epoch, format /Date(timestamp)/"
  },
  "UUID": {
    "type": "string",
    "format": "uuid"
  },
  "LanguageId": {
    "type": "integer",
    "enum": [1, 2, 3],
    "description": "1=Macedonian, 2=Albanian, 3=Turkish"
  },
  "GenderId": {
    "type": "integer",
    "enum": [1, 2],
    "description": "1=Male (Машки), 2=Female (Женски)"
  },
  "SittingStatusId": {
    "type": "integer",
    "enum": [1, 2, 3, 4, 5, 6],
    "description": "1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed"
  },
  "AgendaItemTypeId": {
    "type": "integer",
    "enum": [1, 2],
    "description": "1=Plenary, 2=Committee"
  },
  "SittingTypeId": {
    "type": "integer",
    "enum": [1, 2],
    "description": "1=Plenary sitting, 2=Committee sitting"
  },
  "QuestionStatusId": {
    "type": "integer",
    "enum": [17, 19, 20, 21],
    "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
  },
  "MaterialStatusId": {
    "type": "integer",
    "enum": [0, 6, 9, 10, 11, 12, 24, 64],
    "description": "0=Plenary/unknown, 6=Delivered to MPs, 9=First reading, 10=Second, 11=Third, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "StatusGroupId": {
    "type": "integer",
    "enum": [6, 9, 10, 11, 12, 24, 64],
    "description": "6=Delivered to MPs, 9=First reading, 10=Second reading, 11=Third reading, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "MaterialTypeId": {
    "type": "integer",
    "description": "Material type identifier (non-consecutive; IDs 12 and 25 absent). Common values: 1=Law proposal, 28=Report/Analysis. Full list from GetAllMaterialTypesForFilter."
  },
  "ProposerTypeId": {
    "type": "integer",
    "enum": [1, 2, 4],
    "description": "1=MP, 2=Government, 4=Voter group"
  },
  "ProcedureTypeId": {
    "type": "integer",
    "enum": [1, 2, 3],
    "description": "1=Regular, 2=Shortened, 3=Urgent"
  },
  "ApplicationTypeId": {
    "type": "integer",
    "enum": [1, 2, 3],
    "description": "1=Case report, 2=Participation in public debate, 3=Discussion"
  },
  "DocumentTypeId": {
    "type": "integer",
    "enum": [1, 7, 8, 9, 20, 26, 30, 46, 52, 65],
    "description": "1=Document, 7=Full text of material, 8=Adopted act, 9=Notification to MPs, 20=Convocation notice, 26=Question document, 30=Committee report without approval, 46=Legal-Legislative Committee report, 52=Report/Committee report, 65=Supplemented draft law"
  },
  "EventTypeId": {
    "type": "integer",
    "enum": [5],
    "description": "5=Press conference/visit/general event (other types may exist)"
  },
  "MPsClubRoleId": {
    "type": "integer",
    "enum": [78, 79, 81],
    "description": "78=President, 79=Vice-President, 81=Member"
  },
  "CommitteeRoleId": {
    "type": "integer",
    "enum": [6, 7, 10, 11, 82, 83],
    "description": "6=Committee President/Chair, 7=Committee Member, 10=Approver/Одобрувач, 11=Committee Advisor, 82=Vice President/Deputy Chair, 83=Deputy Member"
  },
  "RoleId": {
    "type": "integer",
    "enum": [1],
    "description": "1=MP (Пратеник/Пратеничка). Other role IDs may exist."
  },
  "CouncilTypeId": {
    "type": "integer",
    "enum": [1],
    "description": "1=Permanent (Постојана). Other types may exist in other structures."
  },
  "TreeItemType": {
    "type": "string",
    "enum": ["ROOT", "LEAF"],
    "description": "ROOT=root node of agenda tree, LEAF=leaf node (may contain agenda items/materials)"
  },
  "AgendaItemStatusId": {
    "type": "integer",
    "enum": [50, 69],
    "description": "50=Reviewed, 69=New"
  },
  "AgendaObjectTypeId": {
    "type": "integer",
    "enum": [0, 1, 4],
    "description": "0=None, 1=Material, 4=Questions/other"
  }
}
```

## Operations Index

### Catalogs (reference data)

| Operation | Method-based | Description |
|-----------|--------------|-------------|
| GetAllGenders | ✓ | Gender options (1=Male, 2=Female) |
| GetAllStructuresForFilter | ✓ | Parliamentary terms (StructureId) |
| GetAllCommitteesForFilter | ✓ | Committees per structure |
| GetAllMaterialStatusesForFilter | ✓ | Material status options |
| GetAllMaterialTypesForFilter | ✓ | Material type options |
| GetAllSittingStatuses | ✓ | Sitting status (1–6) |
| GetAllQuestionStatuses | ✓ | Question status (17,19,20,21) |
| GetAllInstitutionsForFilter | ✓ | Institutions (ministries, etc.). May include placeholder entries |
| GetAllProcedureTypes | ✓ | Procedure types (1,2,3) |
| GetProposerTypes | ✓ | Proposer types (Id, Title, Order) |
| GetAllApplicationTypes | ✓ | Application types |

### Listings (paginated / filterable)

| Operation | Method-based | Description |
|-----------|--------------|-------------|
| GetAllSittings | ✓ | Sittings. Filter: TypeId, CommitteeId, StatusId, dates |
| GetAllQuestions | ✓ | Parliamentary questions. Filter: SearchText, RegistrationNumber, StatusId, CommitteeId, dates. StructureId: null = cross-term |
| GetAllMaterialsForPublicPortal | ✓ | Materials. Many filters. Uses ItemsPerPage/CurrentPage |
| GetParliamentMPsNoImage | ✓ | MPs. Filter: gender, party, search, coalition, constituency. Contains UserImg despite name |
| GetMonthlyAgenda | ✓ | Agenda for month/year |
| GetAllPoliticalParties | ✓ | Parties per structure (flat array, not paginated) |
| GetAllCouncils | ✓ | Councils |
| GetAllParliamentaryGroups | ✓ | Parliamentary groups (flat array) |
| GetAllMPsClubsByStructure | ✓ | MPs clubs |

### Detail (item by ID)

| Operation | Method-based | ID source |
|-----------|--------------|----------|
| GetSittingDetails | ✓ MethodName, SittingId | GetAllSittings |
| GetMaterialDetails | ✓ MaterialId | GetAllMaterialsForPublicPortal |
| GetQuestionDetails | ✓ QuestionId | GetAllQuestions |
| GetCommitteeDetails | ✓ committeeId | GetAllCommitteesForFilter |
| GetCouncilDetails | ✓ committeeId | GetAllCouncils |
| GetPoliticalPartyDetails | ✓ politicalPartyId | GetAllPoliticalParties |
| GetParliamentaryGroupDetails | ✓ parliamentaryGroupId | GetAllParliamentaryGroups |
| GetMPsClubDetails | ✓ mpsClubId | GetAllMPsClubsByStructure |
| GetUserDetailsByStructure | ✓ userId, structureId | GetParliamentMPsNoImage |
| GetAmendmentDetails | ✓ amendmentId | GetMaterialDetails |
| GetVotingResultsForSitting | ✓ votingDefinitionId, sittingId | GetSittingDetails |
| GetVotingResultsForAgendaItem | ✓ VotingDefinitionId, AgendaItemId | GetSittingDetails agenda |
| GetVotingResultsForAgendaItemReportDocument | ✓ | Same as above |

### Non-standard

| Operation | Endpoint | Format |
|-----------|----------|--------|
| GetCustomEventsCalendar | Moldova/services/CalendarService.asmx/GetCustomEventsCalendar | ASMX, model: {Language, Month, Year}. Response: d array |
| LoadLanguage | Infrastructure/LoadLanguage | POST, empty body. Returns Code, Items (Key/Value localization) |
| GetOfficialVisitsForUser | Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser | ASMX, model: user UUID. Response: {"d": []} |

See per-operation .md files for detailed request/response schemas and operation-specific notes.

---

## GetAllApplicationTypes

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllApplicationTypes"]
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
        "type": "integer",
        "$ref": "#/$defs/ApplicationTypeId",
        "description": "Application type identifier (1=Case report, 2=Participation in public debate, 3=Discussion)"
      },
      "ApplicationTitle": {
        "type": "string",
        "description": "Localized title of the application type in the requested language"
      }
    },
    "required": ["Id", "ApplicationTitle"]
  },
  "description": "Flat array of application types; not paginated"
}
```

### Notes

- Returns a flat array (not paginated); `TotalItems` and `Items` wrapper are not used.
- `languageId` determines localization: 1=Macedonian, 2=Albanian, 3=Turkish.
- Language fallback: When `languageId=3` (Turkish), the API may return English labels (e.g. "Case report", "Participation in Public Debate") instead of Turkish translations, indicating incomplete localization for Turkish.
- `Id` values are 1, 2, 3 (see ApplicationTypeId in global $defs).
- Use these IDs in filters and request bodies for application-related operations.
- Typical use: populate dropdowns or application type filters.

---

## GetAllCommitteesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllCommitteesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "structureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID. Obtain from GetAllStructuresForFilter. Determines which set of committees to return (varies by parliamentary term). Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term."
    }
  },
  "required": ["methodName", "languageId", "structureId"]
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
        "description": "Committee UUID. Use as CommitteeId in other operations."
      },
      "Name": {
        "type": "string",
        "description": "Committee name in the requested language."
      }
    },
    "required": ["Id", "Name"]
  }
}
```

### Notes

- **Response format:** Direct array (not paginated; no TotalItems wrapper).
- **Language:** Committee names are returned in the language specified by `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).
- **Parameter casing:** Uses camelCase (`methodName`, `languageId`, `structureId`).
- **Usage:** Use returned `Id` as `CommitteeId` filter parameter in GetAllSittings (with `TypeId: 2` for committee sittings) or as `committeeId` in GetCommitteeDetails.
- **Typical count:** Current structure (5e00dbd6-ca3c-4d97-b748-f792b2fa3473) returns 27+ committees; count varies by parliamentary term.

---

## GetAllCouncils

### Request Schema

```json
{
  "type": "object",
  "required": ["methodName", "languageId", "StructureId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllCouncils"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure identifier. Obtain from GetAllStructuresForFilter. Current common value: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473. Filters councils to those active in the specified structure/term."
    }
  }
}
```

### Response Schema

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Name", "TypeId", "TypeTitle"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/UUID",
        "description": "Unique identifier for the council"
      },
      "Name": {
        "type": "string",
        "description": "Council name in the requested language"
      },
      "TypeId": {
        "$ref": "#/$defs/CouncilTypeId"
      },
      "TypeTitle": {
        "type": "string",
        "description": "Localized council type name (e.g. 'Постојана' for permanent)"
      }
    }
  }
}
```

### Notes

- **Response format:** Returns a flat array of councils (not wrapped in TotalItems/Items structure).
- **Council types:** Currently only type 1 (Permanent/Постојана) observed. Other types may exist in different structures or future terms.
- **Parameter casing:** Uses lowercase `methodName` and `languageId`.
- **Usage:** Council IDs returned here can be used with `GetCouncilDetails` to retrieve detailed information.
- **StructureId required:** Valid parliamentary term/structure ID is required to filter results appropriately.

---

## GetAllGenders

### Request Schema
```json
{
  "type": "object",
  "required": ["methodName", "languageId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllGenders"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  }
}
```

### Response Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/GenderId"
      },
      "Title": {
        "type": "string",
        "description": "Localized gender name in requested language"
      }
    }
  },
  "description": "Direct array of gender options (not paginated)"
}
```

### Notes
- Returns exactly 2 items: Male (Id=1) and Female (Id=2).
- Response is a direct array, not wrapped in object with `TotalItems`/`Items`.
- `Title` values are localized per the `languageId` parameter (1=Macedonian, 2=Albanian, 3=Turkish).
- Use `Id` values (1 or 2) as filter input in operations like `GetParliamentMPsNoImage`.
- Reference data: always returns the same 2 entries, no pagination required.
- Method name uses camelCase: `methodName`; language parameter uses camelCase: `languageId`.

---

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

---

## GetAllMPsClubsByStructure

Returns all MPs clubs (inter-party parliamentary groups) for a specified parliamentary structure/term. These are cross-party groups focused on specific issues such as environmental protection, Roma rights, youth issues, and anti-corruption. The response is not paginated and returns all clubs active in the structure.

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "MethodName": {
      "type": "string",
      "enum": ["GetAllMPsClubsByStructure"],
      "description": "Operation name (required, uses PascalCase casing)"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure. Obtain from GetAllStructuresForFilter. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term"
    }
  },
  "required": ["MethodName", "LanguageId", "StructureId"]
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
        "description": "Unique identifier of the MPs club"
      },
      "Name": {
        "type": "string",
        "description": "Full name/title of the MPs club in requested language. May include prefixes like Интерпартиска парламентарна група (inter-party parliamentary group) or Клуб (club) followed by topic/purpose"
      }
    },
    "required": ["Id", "Name"]
  },
  "description": "Flat array of MPs clubs for the specified structure"
}
```

### Notes

- Response is a direct array (not wrapped in Items/TotalItems pagination structure).
- All clubs for the specified structure are returned; no pagination parameters are supported.
- Club names are localized to the requested LanguageId.
- Uses PascalCase for MethodName and LanguageId (consistent with method-based calling convention).
- See global Calling Conventions § 1 (Method-based) and StructureId § Data Concepts for obtaining the structure UUID.


---

## GetAllMaterialStatusesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllMaterialStatusesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "description": "Reference data request for material processing statuses. Returns localized status labels used as filter parameters in listing operations."
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
        "$ref": "#/$defs/MaterialStatusId",
        "description": "Unique status identifier for use in filter operations"
      },
      "Title": {
        "type": "string",
        "description": "Localized status name per languageId parameter (1=Macedonian, 2=Albanian, 3=Turkish)"
      }
    },
    "required": ["Id", "Title"]
  },
  "description": "Flat array of active material statuses with localized titles"
}
```

### Notes

- **Response format:** Direct array (not paginated; no TotalItems wrapper).
- **Localization:** `Title` is localized per the `languageId` parameter. Test different language IDs to confirm behavior.
- **Returned statuses:** Only active/filterable statuses (6, 9, 10, 11, 12, 24, 64). Status 0 (Plenary/unknown) may appear in material detail records but is not returned by this endpoint.
- **Use in filters:** Pass returned `Id` values as `StatusId` or `StatusGroupId` filter parameters in operations like `GetAllMaterialsForPublicPortal` and `GetAllSittings`.
- **No additional parameters:** This is a simple reference catalog with only `methodName` and `languageId` required.
- **Parameter casing:** Uses `methodName` (camelCase).


---

## GetAllMaterialTypesForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllMaterialTypesForFilter"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
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
        "$ref": "#/$defs/MaterialTypeId",
        "description": "Material type identifier"
      },
      "Title": {
        "type": "string",
        "description": "Localized material type name in requested language. May contain leading/trailing whitespace or control characters (\\r, \\n) requiring trimming for display."
      }
    },
    "required": ["Id", "Title"]
  },
  "description": "Flat array of 37 material types covering legislative materials (laws, amendments, budget), procedural items (elections, appointments, resignations), oversight mechanisms (interpellations, reports), and constitutional procedures (amendments, interpretations)."
}
```

### Notes

- **Casing:** Uses lowercase `methodName` and `languageId` (camelCase).
- **Localization:** Response titles are localized in the requested `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).
- **Data quality:** Title values may contain leading/trailing whitespace characters (`\r`, `\n`, spaces) that should be trimmed for display. See global data quality notes.
- **Non-sequential IDs:** Material type IDs are not consecutive; IDs 12 and 25 are absent from the enumeration.
- **Usage:** Material type IDs returned here are used as `MaterialTypeId` filter values in `GetAllMaterialsForPublicPortal` and appear in material detail responses (GetMaterialDetails).
- **Returns:** Flat array of all material types (not paginated); no null check needed.

---

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

---

## GetAllParliamentaryGroups

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllParliamentaryGroups"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID. Obtain from GetAllStructuresForFilter; often 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term. Filters groups to those active in the specified term."
    }
  },
  "required": ["methodName", "languageId", "StructureId"]
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
        "description": "Parliamentary group unique identifier"
      },
      "Name": {
        "type": "string",
        "description": "Full official name of the parliamentary group. Localized in requested language."
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs belonging to this parliamentary group"
      },
      "Image": {
        "anyOf": [
          {"type": "string"},
          {"type": "null"}
        ],
        "description": "Image identifier, URL, or base64-encoded image data. May be empty string when no image is available."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  },
  "description": "Direct array of parliamentary groups (not paginated)"
}
```

### Notes

- Response is a direct flat array, not wrapped in `TotalItems`/`Items` pagination structure.
- Parameter casing: Uses `methodName` (lowercase) and `languageId` (lowercase).
- All `Image` fields in current data are empty strings, indicating parliamentary groups may not have images assigned.
- `Email` and `Phone` fields are typically `null` for parliamentary groups; contact is via individual members. See GetParliamentaryGroupDetails for additional fields.
- `NumberOfDeputies` reflects current membership. Verify with GetParliamentaryGroupDetails to confirm full member roster and roles (78=Chair, 79=Vice-President, 81=Member).

---

## GetAllPoliticalParties

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllPoliticalParties"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure. Obtain from GetAllStructuresForFilter. Common example: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 (current term)."
    }
  },
  "required": ["methodName", "languageId", "StructureId"]
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
        "description": "Unique identifier for the political party."
      },
      "Name": {
        "type": "string",
        "description": "Official name of the political party in the requested language. If not available in requested language, Macedonian may be returned as fallback."
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs affiliated with this party in the specified parliamentary structure. May include a pseudo-entry for independent MPs (e.g., \"Независни пратеници\")."
      },
      "Image": {
        "type": "string",
        "description": "Party logo or image identifier. Currently returns empty string for all parties in observed data; may contain base64-encoded image or URL in other cases."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes

**Response structure:**
- Returns a flat array of political party objects (not wrapped in `TotalItems`/`Items` pagination structure).
- No pagination; returns all parties for the specified structure in one request.
- All fields are present in every party entry.

**Request parameters:**
- **StructureId** — Required. Determines which set of political parties and their deputy counts are returned for a specific parliamentary term. Obtain from GetAllStructuresForFilter.
- **languageId** — Controls language of party names (1=Macedonian, 2=Albanian, 3=Turkish).
- **methodName** — Must be exactly `"GetAllPoliticalParties"` (uses camelCase).

**Field meanings:**
- **Name** — Official name of the political party in the requested language.
- **NumberOfDeputies** — Current count of MPs affiliated with this party in the specified parliamentary structure/term. Sum across all parties (including independent MPs pseudo-entry) approximates total parliament seats.
- **Image** — Party logo or image identifier. Currently empty string in observed data.
- **Independent MPs** — Typically represented as a pseudo-party entry (e.g., \"Независни пратеници\" / Independent MPs) with its own UUID and deputy count.

**Parameter casing:**
- Uses camelCase: `methodName`, `languageId`. `StructureId` uses PascalCase.

---

## GetAllProcedureTypes

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllProcedureTypes"],
      "description": "Operation name"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "additionalProperties": false,
  "$defs": {
    "LanguageId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
    }
  }
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
        "$ref": "#/$defs/ProcedureTypeId"
      },
      "Title": {
        "type": "string",
        "description": "Procedure type name in requested language (or Macedonian fallback)"
      }
    },
    "required": ["Id", "Title"],
    "additionalProperties": false
  },
  "$defs": {
    "ProcedureTypeId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Regular (Редовна постапка), 2=Shortened (Скратена постапка), 3=Urgent (Итна постапка)"
    }
  }
}
```

### Notes
- Returns a fixed set of three procedure types regardless of language or other parameters.
- The `languageId` parameter may not affect response content; Macedonian text has been observed regardless of requested language (e.g., `languageId: 3` returning Macedonian rather than Turkish). See global data quality notes on language fallback.
- No pagination is used; all three procedure types are always returned in a single response.
- The returned `Id` values map directly to `ProcedureTypeId` used in filtering operations (e.g., `GetAllMaterialsForPublicPortal`).
- Uses camelCase parameter name `languageId` (not PascalCase).

---

## GetAllQuestionStatuses

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllQuestionStatuses"]
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "languageId"],
  "additionalProperties": false
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
        "$ref": "#/$defs/QuestionStatusId"
      },
      "Title": {
        "type": "string",
        "description": "Localized question status label in requested language (e.g., 'Delivered', 'Replied', 'Non disclosed reply', 'Reply in Writing')"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a direct flat array of question status objects (not wrapped in Items container or paginated).
- **Parameter casing:** Accepts both `languageId` (lowercase) and `LanguageId` (capitalized) interchangeably.
- **Localization:** `Title` is localized to the requested `LanguageId`. For example, with `languageId: 2` (Albanian), titles may appear as "Vendosur", "Përgjigj", "Përgjigj jo e zbuluar", "Përgjigj në shkrim". May return Macedonian text regardless of requested `languageId`; test per endpoint to confirm behavior.

---

## GetAllQuestions

### Request Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllQuestions",
      "description": "Operation method name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Requested language for response labels and localized content"
    },
    "Page": {
      "type": "integer",
      "minimum": 1,
      "description": "1-based page number for pagination"
    },
    "Rows": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of items per page (typical values: 6, 8, 10, 12, 14, 18)"
    },
    "CurrentPage": {
      "type": "integer",
      "minimum": 1,
      "description": "Appears alongside Page; purpose unclear (possibly legacy/redundant parameter). Recommend setting to same value as Page."
    },
    "SearchText": {
      "type": "string",
      "description": "Free-text search across question titles and content. Set to empty string to disable."
    },
    "RegistrationNumber": {
      "anyOf": [
        { "type": "string", "description": "Filter by question registration number (e.g. '08-750/1')" },
        { "type": "null", "description": "null to omit filter" }
      ]
    },
    "StatusId": {
      "anyOf": [
        { "$ref": "#/$defs/QuestionStatusId" },
        { "type": "null", "description": "null to include all statuses" }
      ],
      "description": "Filter by question status"
    },
    "From": {
      "type": "string",
      "description": "Filter by question author name (MP name). Set to empty string to disable."
    },
    "To": {
      "type": "string",
      "description": "Filter by recipient name (minister/official). Set to empty string to disable."
    },
    "CommitteeId": {
      "anyOf": [
        { "$ref": "#/$defs/UUID" },
        { "type": "null", "description": "null to include all committees" }
      ],
      "description": "Filter questions by committee"
    },
    "DateFrom": {
      "anyOf": [
        { "$ref": "#/$defs/AspDate" },
        { "type": "null", "description": "null to omit start date filter" }
      ],
      "description": "Filter by DateAsked start (earliest)"
    },
    "DateTo": {
      "anyOf": [
        { "$ref": "#/$defs/AspDate" },
        { "type": "null", "description": "null to omit end date filter" }
      ],
      "description": "Filter by DateAsked end (latest)"
    },
    "StructureId": {
      "anyOf": [
        { "$ref": "#/$defs/UUID" },
        { "type": "null", "description": "null to query across all parliamentary terms/structures" }
      ],
      "description": "Parliamentary term/structure UUID"
    }
  },
  "required": ["methodName", "LanguageId", "Page", "Rows"],
  "$defs": {
    "AspDate": {
      "type": "string",
      "pattern": "^/Date\\(\\d+\\)/$"
    },
    "LanguageId": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=Macedonian, 2=Albanian, 3=Turkish"
    },
    "QuestionStatusId": {
      "type": "integer",
      "enum": [17, 19, 20, 21],
      "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
    },
    "UUID": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

### Response Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer",
      "description": "Total count of questions matching filters across all pages"
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
                "format": "uuid",
                "description": "Unique question identifier"
              },
              "Title": {
                "type": "string",
                "description": "Question text/title in requested language"
              },
              "From": {
                "type": "string",
                "description": "Name of the MP who submitted the question (questioner)"
              },
              "To": {
                "type": "string",
                "description": "Title/position of the recipient (minister or official)"
              },
              "ToInstitution": {
                "type": "string",
                "description": "Full name of the institution receiving the question (ministry or government body). May contain placeholder values like '/' in some datasets."
              },
              "StatusTitle": {
                "type": "string",
                "description": "Human-readable question status in requested language (e.g. 'Доставено'=Delivered, 'Одговорено'=Answered)"
              },
              "DateAsked": {
                "type": "string",
                "pattern": "^/Date\\(\\d+\\)/$",
                "description": "Date when question was submitted (AspDate format)"
              },
              "QuestionTypeTitle": {
                "type": "string",
                "description": "Type of question in requested language (e.g. 'Писмено прашање'=Written question, 'Усно прашање'=Oral question)"
              },
              "TotalRows": {
                "type": "integer",
                "description": "Item-level field observed as 0 in all responses. Purpose unclear (possibly legacy)."
              }
            },
            "required": ["Id", "Title", "From", "To", "ToInstitution", "StatusTitle", "DateAsked", "QuestionTypeTitle", "TotalRows"]
          }
        },
        {
          "type": "null",
          "description": "When TotalItems=0, Items is null instead of empty array"
        }
      ]
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Notes

#### Pagination
Uses standard `Page`/`Rows` pagination pattern (1-based). Response includes `TotalItems` (full result count across all pages) and `Items` (current page subset only). When `TotalItems: 0`, the `Items` field is `null` rather than empty array `[]`.

#### LanguageId
Response content (Title, From, To, StatusTitle, QuestionTypeTitle, ToInstitution) is returned in the requested language. Some fields may contain Cyrillic text or institutional names even for non-Macedonian language requests; see global Language Fallback section.

#### Parameter Casing
Uses PascalCase: `LanguageId`, `StructureId`, `CommitteeId`, `RegistrationNumber`, `StatusId`, `DateFrom`, `DateTo`. Method name uses camelCase: `methodName`. Other filters (SearchText, From, To, Page, Rows, CurrentPage) use mixed case.

#### CurrentPage vs Page
Both parameters present in request; distinction unclear. Recommend setting both to same value. May be legacy or redundant parameter.

#### StructureId Nullable
Unlike most listing operations that require `StructureId`, this operation accepts `null` for cross-term queries of all questions regardless of parliamentary structure. When set to a specific UUID, filters to questions in that parliamentary term only.

#### Filter Parameter Details
- **SearchText:** Free-text search. Set to empty string `""` to disable.
- **From/To:** Text-based filters (MP name, recipient name). Set to empty string `""` to disable.
- **RegistrationNumber:** Registration number filter (e.g. '08-750/1'). Use `null` to omit.
- **StatusId:** Filter by QuestionStatusId (17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Use `null` to include all statuses.
- **CommitteeId:** UUID or `null` to include all committees.
- **DateFrom/DateTo:** AspDate format or `null` to omit start/end date filtering. Filters on DateAsked field.

#### Item Field Details
- **TotalRows:** Each item includes `TotalRows: 0`. Purpose unclear (possibly legacy or reserved field); rely on top-level `TotalItems` for actual result count.
- **QuestionTypeTitle:** Observed types include "Писмено прашање" (Written question) and "Усно прашање" (Oral question). No separate type ID exposed.
- **ToInstitution:** May contain placeholder values (e.g. `/`) or inconsistent formatting ("Министерството" vs "Министерство"). Handle gracefully in client code.
- **StatusTitle:** Observed values include "Доставено" (Delivered) and "Одговорено" (Answered) in Macedonian; response localizes per LanguageId.


---

## GetAllSittingStatuses

### Request Schema
```json
{
  "type": "object",
  "required": ["methodName", "LanguageId"],
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetAllSittingStatuses"],
      "description": "Operation name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  }
}
```

### Response Schema
```json
{
  "type": "array",
  "description": "Returns all sitting status options with localized titles",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId"
      },
      "Title": {
        "type": "string",
        "description": "Localized status name in the requested language (e.g., \"Закажана\" = Scheduled, \"Започната\" = Started, etc.)"
      }
    }
  }
}
```

### Notes
- Returns all six sitting status options with titles localized to the requested `LanguageId`.
- The `Id` values correspond to `SittingStatusId` enum in global $defs: 1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed.
- `Title` is the human-readable label for the status in the requested language.
- Use the returned `Id` values when filtering sittings via the `StatusId` parameter in `GetAllSittings`.
- Response is a simple flat array (not wrapped in `TotalItems`/`Items` pagination object).
- Parameter casing: Uses `LanguageId` (PascalCase).
- Calling convention: Method-based (POST to `https://www.sobranie.mk/Routing/MakePostRequest` with `methodName` in body).

---

## GetAllSittings

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllSittings",
      "description": "Operation name"
    },
    "Page": {
      "type": "integer",
      "description": "Page number (1-based)"
    },
    "Rows": {
      "type": "integer",
      "description": "Number of items per page"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "TypeId": {
      "anyOf": [
        {"$ref": "#/$defs/AgendaItemTypeId"},
        {"type": "null"}
      ],
      "description": "1=Plenary, 2=Committee. Set to null to include all types."
    },
    "CommitteeId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of committee. Use with TypeId: 2. Set to null for plenary or to include all committees."
    },
    "StatusId": {
      "anyOf": [
        {"$ref": "#/$defs/SittingStatusId"},
        {"type": "null"}
      ],
      "description": "Filter by status. Set to null to include all statuses."
    },
    "DateFrom": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter by start date. Set to null to omit."
    },
    "DateTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter by end date. Set to null to omit."
    },
    "SessionId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Filter by session UUID"
    },
    "Number": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by sitting number"
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of parliamentary term/structure. Set to null to query across all terms. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term."
    }
  },
  "required": ["methodName", "Page", "Rows", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer",
      "description": "Total sittings matching filter across all pages"
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
                "description": "Unique identifier of the sitting"
              },
              "Number": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ],
                "description": "Sitting sequence number within committee or plenary context"
              },
              "SittingDate": {
                "$ref": "#/$defs/AspDate",
                "description": "Primary sitting date/time"
              },
              "TypeId": {
                "$ref": "#/$defs/AgendaItemTypeId",
                "description": "1=Plenary, 2=Committee"
              },
              "TypeTitle": {
                "type": "string",
                "description": "Localized sitting type name (e.g. 'Пленарна седница', 'Комисионска седница')"
              },
              "StatusId": {
                "$ref": "#/$defs/SittingStatusId"
              },
              "StatusTitle": {
                "type": "string",
                "description": "Localized status name"
              },
              "Location": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Physical location/room (e.g. 'Сала 4')"
              },
              "CommitteeId": {
                "anyOf": [
                  {"$ref": "#/$defs/UUID"},
                  {"type": "null"}
                ],
                "description": "UUID of committee. Null for plenary sittings (TypeId: 1)."
              },
              "CommitteeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Localized committee name. Null for plenary (TypeId: 1)."
              },
              "SittingDescriptionTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Localized description of sitting subtype/format"
              },
              "Continuations": {
                "type": "array",
                "description": "Array of continuation sitting references. Empty in standard responses; likely populated when sitting spans multiple sessions.",
                "items": {"type": "object"}
              },
              "Structure": {
                "anyOf": [
                  {"type": "object"},
                  {"type": "null"}
                ],
                "description": "Structural metadata; typically null in list responses"
              },
              "TotalRows": {
                "type": "integer",
                "description": "Row count metadata field"
              }
            }
          }
        },
        {"type": "null"}
      ],
      "description": "Array of sittings or null when TotalItems is 0"
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Notes

- **Empty results behavior:** When no sittings match filter criteria, returns `{"TotalItems": 0, "Items": null}` rather than empty array.
- **Sitting sequence number:** `Number` field represents the sitting sequence number within the specific context: for plenary (`TypeId: 1`), the Nth plenary sitting; for committee (`TypeId: 2`), the Nth committee sitting. Each context maintains its own sequence.
- **Committee metadata:** `CommitteeId` and `CommitteeTitle` are populated only for committee sittings (`TypeId: 2`); both are null for plenary (`TypeId: 1`).
- **Continuations:** `Continuations` array is empty in standard responses; likely populated when a sitting spans multiple sessions.
- **Structure field:** Metadata field typically null in list responses.
- **Cross-structure queries:** When `StructureId` is null, returns sittings from all parliamentary terms/structures; `TotalItems` reflects cross-term total.
- **Pagination:** Uses `Page` (1-based) and `Rows` pattern. When `TotalItems: 0`, `Items` is null, not an empty array.
- **Localization:** `TypeTitle`, `StatusTitle`, `CommitteeTitle`, and `SittingDescriptionTypeTitle` are localized according to `LanguageId`.


---

## GetAllStructuresForFilter

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllStructuresForFilter",
      "description": "Operation identifier"
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
        "description": "UUID identifier of the parliamentary term/structure. Use as StructureId in filter operations."
      },
      "DateFrom": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date of the parliamentary term"
      },
      "DateTo": {
        "$ref": "#/$defs/AspDate",
        "description": "End date of the parliamentary term. May be set far in the future for current term."
      },
      "IsCurrent": {
        "type": "boolean",
        "description": "Boolean flag indicating whether this is the currently active parliamentary term. Only one structure has IsCurrent: true."
      }
    },
    "required": ["Id", "DateFrom", "DateTo", "IsCurrent"]
  },
  "description": "Flat array of all parliamentary terms in reverse chronological order (current/most recent first). Not paginated."
}
```

### Notes

- **Parameter casing:** Uses lowercase `methodName` and `languageId`
- **Structure selection:** Exactly one structure has `IsCurrent: true` — this is the active parliamentary term and should be used as the default `StructureId` in other operations when querying current parliamentary data (typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` as of 2024)
- **Historical data:** Returns all parliamentary terms dating back to at least June 2008; use for querying past sessions
- **Ordering:** Response is in reverse chronological order (current first)
- **DateTo placeholder:** For the current term, `DateTo` may be set to a far future placeholder date (e.g., representing 2028)
- **No localization:** The `languageId` parameter does not affect the response; no localized fields are present
- **No pagination:** Response is not paginated; returns the complete list of all structures
- **No Title field:** Unlike most catalog operations, structures are identified only by UUID and date range; no Title or Name field is present
- **Usage pattern:** Call once per session to obtain the current `StructureId` for use in subsequent filter operations


---

## GetCommitteeDetails

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetCommitteeDetails"
    },
    "committeeId": {
      "$ref": "#/$defs/UUID",
      "description": "Committee identifier from GetAllCommitteesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "committeeId", "languageId"]
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Committee name in the requested language"
    },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID",
            "description": "Elected committee member identifier"
          },
          "FullName": {
            "type": "string",
            "description": "Full name of committee member"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Претседател/Претседателка на комисија', 'Член/Членка на комисија')"
          }
        }
      },
      "description": "Elected committee members: chair, vice-chair, members, and deputies with their roles"
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID",
            "description": "Staff member identifier"
          },
          "FullName": {
            "type": "string",
            "description": "Full name of staff member"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Советник/Советничка на комисија', 'Одобрувач/Одобрувачка')"
          }
        }
      },
      "description": "Administrative/professional staff supporting the committee (advisors, approvers). Same person may appear multiple times with different RoleIds when holding multiple roles"
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Material identifier"
          },
          "Title": {
            "type": "string",
            "description": "Material title in the requested language"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration number (e.g., '08-750/1')"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized material status (e.g., 'Доставен до пратеници')"
          }
        }
      },
      "description": "Materials assigned to this committee for review/processing. Empty array [] when no materials linked"
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Sitting/meeting identifier"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type name in the requested language (e.g., 'Комископска седница')"
          },
          "Date": {
            "$ref": "#/$defs/AspDate",
            "description": "Meeting date/time"
          },
          "Location": {
            "type": "string",
            "description": "Meeting room/venue (e.g., 'Сала 5', 'Сала 6')"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential number of the committee sitting"
          }
        }
      },
      "description": "Committee sittings/meetings, ordered by date (most recent first)"
    },
    "Description": {
      "type": "string",
      "description": "HTML-formatted committee description including mandate, responsibilities, composition requirements. May contain markup tags (<p>, <br/>, <div>). May be truncated with ellipsis in response"
    },
    "Email": {
      "type": "string",
      "description": "Committee contact email address"
    },
    "PhoneNumber": {
      "oneOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee contact phone number; may be null when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID this committee belongs to"
    }
  }
}
```

### Notes
- **CompositionMembers** contains the officially elected committee structure (chairs, members, deputies). Use with `GetUserDetailsByStructure` for full MP profile data.
- **SecretariatMembers** contains professional staff and administrative roles. Same person may appear multiple times with different RoleIds (expected behavior for staff holding multiple roles).
- **Materials** shows a subset of legislative items from `GetAllMaterialsForPublicPortal` assigned to this committee.
- **Description** contains HTML markup; parse appropriately for display in client applications.
- **Meetings** entries can be used with `GetSittingDetails` to retrieve full agenda, voting results, and documents for each sitting.
- Response examples in documentation may show `"_truncated": N` in arrays when actual arrays were truncated for documentation purposes; actual API responses include all available items.
- **languageId** casing: uses camelCase (lowercase) in this operation.
- Date/time values in `Meetings[].Date` follow AspDate format. Use parsing compatible with `/Date(timestamp)/` format.


---

## GetCouncilDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetCouncilDetails"],
      "description": "Operation method name (lowercase)"
    },
    "committeeId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the council to retrieve. Obtain from GetAllCouncils response."
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Requested language for response labels and text (1=Macedonian, 2=Albanian, 3=Turkish). Controls language for Name, RoleTitle, Description, and other text fields."
    }
  },
  "required": ["methodName", "committeeId", "languageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full name of the council in the requested language"
    },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Претседател/Претседателка', 'Член/Членка')"
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
      },
      "description": "Official council composition members (MPs with voting roles). Typically includes president (RoleId 6), vice-president (82), and members (7). Ordered by role importance."
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Одобрувач', 'Советник на комисија')"
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
      },
      "description": "Administrative and advisory staff supporting the council. RoleId typically 10 (Approver) or 11 (Advisor). Note: Same person (UserId) may appear multiple times with different RoleIds when holding multiple roles. This is expected behavior."
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Materials associated with the council (e.g., founding decisions, policy documents). Empty array [] when no materials exist."
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type label (e.g., 'Комисска седница' = Committee sitting)"
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string",
            "description": "Physical meeting location (e.g., 'Сала 4' = Room 4)"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential sitting number for the council"
          }
        },
        "required": ["Id", "TypeTitle", "Date", "Location", "SittingNumber"]
      },
      "description": "Past and scheduled council meetings/sittings, ordered by date in reverse chronological order (most recent first)."
    },
    "Description": {
      "anyOf": [
        {
          "type": "string",
          "description": "HTML-formatted description of the council's mandate and responsibilities. May contain markup including <p>, <span>, <a>, <br/> tags and inline styles. May include links to founding decisions and constitutional references."
        },
        {
          "type": "null"
        }
      ]
    },
    "Email": {
      "type": "string",
      "description": "Contact email address for the council (e.g., 'council-name@sobranie.mk')"
    },
    "PhoneNumber": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "Contact phone number. Null when not available."
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure this council belongs to. Common value: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term. Matches StructureId parameter used in other operations."
    }
  },
  "required": ["Name", "CompositionMembers", "SecretariatMembers", "Materials", "Meetings", "Email", "StructureId"]
}
```

### Notes

- **Parameter casing**: Uses lowercase `methodName` and `languageId` (standard method-based convention).
- **RoleId enum** (CommitteeRoleId): See global $defs. Composition uses 6 (President), 82 (Vice-President), 7 (Member). Secretariat uses 10 (Approver), 11 (Advisor).
- **Duplicate users in SecretariatMembers**: A single person may appear multiple times in the SecretariatMembers array with different RoleId values, reflecting their actual responsibilities. This is expected behavior.
- **Meetings ordering**: The Meetings array is ordered by Date in reverse chronological order (most recent first).
- **HTML content in Description**: Contains rich HTML markup. Parse as HTML when displaying to end users.
- **Materials**: Returns empty array `[]` when no materials exist (not `null`).


---

## GetCustomEventsCalendar

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "model": {
      "type": "object",
      "properties": {
        "Language": {
          "$ref": "#/$defs/LanguageId",
          "description": "Language for event descriptions and locations (1=Macedonian, 2=Albanian, 3=Turkish)"
        },
        "Month": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12,
          "description": "Month (1–12)"
        },
        "Year": {
          "type": "integer",
          "description": "Four-digit year (e.g., 2024, 2026)"
        }
      },
      "required": ["Language", "Month", "Year"]
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
      "description": "Array of calendar events for the requested month/year",
      "items": {
        "type": "object",
        "properties": {
          "__type": {
            "type": "string",
            "description": "ASMX type discriminator (e.g., 'moldova.controls.Models.CalendarViewModel')"
          },
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Unique event identifier"
          },
          "EventDescription": {
            "type": "string",
            "description": "Human-readable title/description of the event in the requested language"
          },
          "EventLink": {
            "type": "string",
            "description": "URL-friendly slug for event detail page"
          },
          "EventLocation": {
            "anyOf": [
              {"type": "string"},
              {"const": ""}
            ],
            "description": "Physical location/venue of event. May be empty string when location not specified or not applicable to event type"
          },
          "EventDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Scheduled date/time of the event in AspDate format"
          },
          "EventType": {
            "$ref": "#/$defs/EventTypeId",
            "description": "Type of event (currently 5=press conference/visit/working session/commemoration/public event)"
          }
        },
        "required": ["__type", "Id", "EventDescription", "EventLink", "EventLocation", "EventDate", "EventType"]
      }
    }
  },
  "required": ["d"]
}
```

### Notes
- **ASMX response format:** Endpoint uses ASMX wrapper; results are returned in the `d` property directly as an array (not wrapped in `Items`/`TotalItems` pagination).
- **Empty results:** Returns empty array `[]` if no events exist for the requested month/year.
- **Language localization:** `EventDescription` and `EventLocation` are localized based on the `Language` parameter (1=Macedonian, 2=Albanian, 3=Turkish). The same event returns different language text when queried with different `Language` values.
- **Event location handling:** `EventLocation` may be empty string when location is not specified or not applicable to the event type.
- **Event types:** All documented sample events have `EventType: 5` (press conferences, official visits, working sessions, commemorations, public events). Other EventType values may exist but are not yet documented.
- **Event links:** `EventLink` provides URL-safe slugs suitable for constructing event detail page URLs.
- **Endpoint:** Non-standard ASMX endpoint at `https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar`; POST with `model` wrapper in request body.

---

## GetMPsClubDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetMPsClubDetails"],
      "description": "Operation name. Uses lowercase 'm' in methodName."
    },
    "mpsClubId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MPs club to retrieve. Obtained from GetAllMPsClubsByStructure."
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Language for response text localization. Uses uppercase 'L' in LanguageId (PascalCase). Note: this operation mixes camelCase (methodName, mpsClubId) and PascalCase (LanguageId) naming in the same request."
    }
  },
  "required": ["methodName", "mpsClubId", "LanguageId"],
  "additionalProperties": false
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full name of the MPs club in the requested LanguageId."
    },
    "Description": {
      "type": "string",
      "description": "Description or purpose of the club. May be placeholder '-' when no description is provided."
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs belonging to this club with assigned roles. May include a {_truncated: N} object as the final element, indicating N additional members were omitted from response.",
      "items": {
        "oneOf": [
          {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "UUID of the MP."
              },
              "FirstName": {
                "type": "string",
                "description": "First name of the MP."
              },
              "LastName": {
                "type": "string",
                "description": "Last name of the MP."
              },
              "RoleId": {
                "$ref": "#/$defs/MPsClubRoleId",
                "description": "Role ID within the club (78=President, 79=Vice-President, 81=Member)."
              },
              "RoleTitle": {
                "type": "string",
                "description": "Localized role name with gender-inclusive slash notation (e.g., 'Претседател/Претседателка' = President masc./fem., 'Заменик-претседател/Заменик-претседателка' = Vice-President masc./fem., 'Член/Членка' = Member masc./fem.). Respects requested LanguageId."
              }
            },
            "required": ["Id", "FirstName", "LastName", "RoleId", "RoleTitle"],
            "additionalProperties": false
          },
          {
            "type": "object",
            "properties": {
              "_truncated": {
                "type": "integer",
                "description": "Marker object (not a member); appears as final array element when Members list is truncated. Value indicates N additional members omitted."
              }
            },
            "required": ["_truncated"],
            "additionalProperties": false
          }
        ]
      }
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID (typically current: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473). Indicates the parliamentary term to which this club belongs."
    }
  },
  "required": ["Name", "Description", "Members", "StructureId"],
  "additionalProperties": false
}
```

### Notes

**Parameter casing:** This operation uses mixed casing in the request: `methodName` and `mpsClubId` (camelCase) combined with `LanguageId` (PascalCase). This is intentional and differs from some other operations; follow the exact casing shown in the Request Schema.

**Member roles and RoleId values:**
- **RoleId 78** (Претседател/Претседателка) — President/Chairperson; typically one per club
- **RoleId 79** (Заменик-претседател/Заменик-претседателка) — Vice-President; zero or more
- **RoleId 81** (Член/Членка) — Member; regular members

**Gender-inclusive role titles:** RoleTitle uses Macedonian notation with `/` separator showing masculine and feminine forms. All roles include this dual-form notation. Other languages may use different conventions; test with LanguageId 2 (Albanian) or 3 (Turkish) if needed.

**Description placeholder:** When no description exists, the field returns the placeholder string `"-"` (not `null` or empty string). Client code should recognize and filter this placeholder for display.

**Array truncation:** Large clubs may have their Members array truncated in the response. The final element will be `{"_truncated": N}` (not a regular member object), indicating N additional members were omitted. Client should handle this marker gracefully and may fetch additional context from GetAllMPsClubsByStructure if a complete roster is needed.

**Localization:** Name, Description, and RoleTitle are localized to the requested LanguageId. Test with different language IDs (1=Macedonian, 2=Albanian, 3=Turkish) to verify localization behavior and any fallback patterns.

**StructureId in response:** The returned StructureId reflects the parliamentary term to which the club belongs and typically matches the structure ID used in the GetAllMPsClubsByStructure call that provided the mpsClubId.

**Data ID source:** Obtain mpsClubId from GetAllMPsClubsByStructure listing.

---

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
      "type": "string",
      "description": "Name and title of primary responsible author/proposer. For multi-author materials, represents lead author. May be empty when no responsible author designated. May contain Cyrillic (Macedonian) even if other language requested."
    },
    "Institution": {
      "type": "string",
      "description": "Institution name when material proposed by institutional entity. Empty string when proposer is MPs or not applicable."
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

- **Committee processing:** Materials assigned to multiple committees with different roles. IsResponsible: true identifies lead committee. IsLegislative: true identifies legislative-legal review committee. Each committee may have associated Documents array.

- **Reading stages:** Materials progress through three reading stages. Each reading has corresponding *ReadingSittings array containing plenary (SittingTypeId: 1, CommitteeId: null) and/or committee (SittingTypeId: 2, with populated CommitteeId/CommitteeTitle) sitting records. Empty arrays indicate material not yet reached that stage. In sitting objects, StatusGroupId 9=first reading, 10=second reading, 11=third reading.

- **Empty arrays:** Amendment and sitting arrays return empty arrays [] when no data exists, not null.

- **Institutional authors:** When ProposerTypeId is 2 (Government), Authors array contains entries with Id as all-zeros UUID, FirstName containing full official title/name (e.g. minister name), and LastName as empty string. ResponsibleAuthor duplicates this information and may contain Cyrillic text (Macedonian) even when other language requested. Institution field contains ministry/institution name.

- **Data quality - whitespace:** TypeTitle, DocumentTypeTitle, and other catalog fields may contain leading/trailing whitespace and control characters (\r, \n). Trim as needed for display.

- **Document truncation:** Large document arrays may be truncated (indicated by _truncated marker). Total document count not provided; full list may require alternative queries.

- **Registration date precision:** RegistrationDate field may include future timestamps (indicating test data, planned materials, or specific timezone handling).

- **Sittings duplicates:** Sittings array may contain multiple entries with same SittingNumber but different Id and SittingDate values. This represents multi-day sessions or continuations of the same formal sitting.

- **Language behavior:** Localized fields (StatusGroupTitle, TypeTitle, ProposerTypeTitle, ProcedureTypeTitle) return text in requested LanguageId (1=Macedonian, 2=Albanian, 3=Turkish). However, ResponsibleAuthor and Institution for government-proposed materials may contain Cyrillic regardless of requested language.


---

## GetMonthlyAgenda

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetMonthlyAgenda",
      "description": "Operation name"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Controls localization of Title and Location fields (1=Macedonian, 2=Albanian, 3=Turkish)"
    },
    "Month": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Calendar month (1–12)"
    },
    "Year": {
      "type": "integer",
      "description": "Four-digit year (e.g. 2025, 2026)"
    }
  },
  "required": ["methodName", "LanguageId", "Month", "Year"]
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
        "description": "Identifier for the sitting/agenda item"
      },
      "Title": {
        "type": "string",
        "description": "Full descriptive title typically in format: Седница бр. {number} на {body name} - {location} (in requested language)"
      },
      "Location": {
        "type": "string",
        "description": "Physical room or venue (e.g. Сала \"Македонија\", Сала 4, Сала 5)"
      },
      "Start": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date/time of the sitting"
      },
      "Type": {
        "$ref": "#/$defs/AgendaItemTypeId",
        "description": "1=Plenary, 2=Committee"
      }
    },
    "required": ["Id", "Title", "Location", "Start", "Type"]
  },
  "description": "Flat array of agenda items (sittings) for the requested month, ordered by Start date/time ascending. Empty array when no agenda items exist."
}
```

### Notes

**Parameter casing:** Uses `methodName` (lowercase) and `LanguageId` (PascalCase).

**Request details:**
- `methodName`: Always `"GetMonthlyAgenda"`
- `LanguageId`: 1=Macedonian, 2=Albanian, 3=Turkish. Affects Title and Location localization.
- `Month`: Integer 1–12
- `Year`: Four-digit year

**Response format:** Returns a flat array (not paginated; no TotalItems/Items wrapper).

**Type field:** Indicates sitting context:
- `1` = Plenary sittings (main parliament sessions)
- `2` = Committee sittings (committee meetings)

**Title format:** Typically "Седница бр. {number} на {body name} - {location}" structure in Macedonian or equivalent in requested language.

**Empty results:** Returns empty array `[]` when no agenda items exist for the requested month/year.

**Ordering:** Results ordered by Start date/time ascending.

**Usage:** Pass the `Id` to `GetSittingDetails` to retrieve detailed sitting information including agenda tree, attendees, voting results, etc.

---

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

---

## GetParliamentMPsNoImage

Retrieve active and expired-mandate members of parliament from a specified parliamentary term, with optional filtering by gender, age, party, and search text.

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetParliamentMPsNoImage"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "genderId": {
      "anyOf": [
        {"$ref": "#/$defs/GenderId"},
        {"type": "null"}
      ],
      "description": "Filter by gender; null includes all genders"
    },
    "ageFrom": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Minimum age for filtering; null = no lower bound"
    },
    "ageTo": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Maximum age for filtering; null = no upper bound"
    },
    "politicalPartyId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Filter by political party; null includes all parties"
    },
    "searchText": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Filter MPs by name substring; null applies no text filtering"
    },
    "page": {
      "type": "integer",
      "minimum": 1,
      "description": "1-based page number for pagination of active MPs"
    },
    "rows": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of results per page"
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Parliamentary term UUID from GetAllStructuresForFilter. null returns empty MP arrays but populates Statistics with global counts"
    },
    "coalition": {
      "type": "string",
      "description": "Coalition filter (empty string when not filtering)"
    },
    "constituency": {
      "type": "string",
      "description": "Constituency filter (empty string when not filtering)"
    }
  },
  "required": ["methodName", "page", "rows"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "MembersOfParliament": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "UserId": {
                "$ref": "#/$defs/UUID",
                "description": "Unique identifier for the MP"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for MP's photograph"
              },
              "FullName": {
                "type": "string",
                "description": "MP's full name in requested language"
              },
              "RoleId": {
                "type": "integer",
                "description": "Internal role identifier"
              },
              "PoliticalPartyTitle": {
                "type": "string",
                "description": "Name of the political party"
              },
              "PoliticalPartyId": {
                "$ref": "#/$defs/UUID",
                "description": "UUID of the political party"
              }
            },
            "required": ["UserId", "FullName"]
          },
          "description": "Active-mandate MPs for the current page"
        },
        {"type": "null"}
      ],
      "description": "Array of active MPs matching filters, paginated; empty array [] when no results, null in some edge cases"
    },
    "ExpiredMandateMembers": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "UserId": {
                "$ref": "#/$defs/UUID"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for expired-mandate MP's photograph"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "type": "integer"
              },
              "PoliticalPartyTitle": {
                "type": "string"
              },
              "PoliticalPartyId": {
                "$ref": "#/$defs/UUID"
              }
            },
            "required": ["UserId", "FullName"]
          },
          "description": "MPs whose mandates have expired"
        },
        {"type": "null"}
      ]
    },
    "TotalItems": {
      "type": "integer",
      "description": "Total count of active-mandate MPs matching the filter criteria (across all pages)"
    },
    "TotalItemsExpiredMandate": {
      "type": "integer",
      "description": "Total count of expired-mandate MPs matching the filter criteria"
    },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": {
          "type": "integer",
          "description": "Global count of materials (non-zero even when filter results are empty)"
        },
        "NumberOfQuestions": {
          "type": "integer",
          "description": "Count of parliamentary questions"
        },
        "TotalNumberOfMPs": {
          "type": "integer",
          "description": "Total active MPs in the structure"
        },
        "TotalNumberOfExpiredMandateMPs": {
          "type": "integer",
          "description": "Total expired-mandate MPs in the structure"
        },
        "MPsInPoliticalParties": {
          "type": "integer",
          "description": "Number of active MPs in political parties"
        },
        "MPsInParliamentaryGroups": {
          "type": "integer",
          "description": "Number of active MPs in parliamentary groups"
        },
        "NumberOfMaterialsInStructure": {
          "type": "integer",
          "description": "Materials count for the specified structure"
        }
      },
      "description": "Aggregate statistics; always present and populated even when filter results are empty"
    }
  },
  "required": ["MembersOfParliament", "ExpiredMandateMembers", "TotalItems", "TotalItemsExpiredMandate", "Statistics"]
}
```

### Notes

#### Operation Name vs. Response Content
Despite the operation name "GetParliamentMPsNoImage", the response **includes** the `UserImg` field containing base64-encoded photograph data for each MP in both `MembersOfParliament` and `ExpiredMandateMembers` arrays. Do not assume images are absent.

#### StructureId Behavior
When `StructureId` is `null`, the operation returns empty MP arrays (`MembersOfParliament: []`, `ExpiredMandateMembers: []`) with `TotalItems: 0` and `TotalItemsExpiredMandate: 0`. However, the `Statistics` object is still populated with aggregate counts that may be global. **Always provide a valid StructureId UUID (e.g., current term from GetAllStructuresForFilter) to retrieve MP data.** The active parliamentary term is marked with `IsCurrent: true`.

#### Pagination
The `page` (1-based) and `rows` parameters control pagination of the `MembersOfParliament` results only. `TotalItems` reflects the full count of active MPs across all pages; the returned array contains only the subset for the requested page. Pagination behavior for `ExpiredMandateMembers` (whether separate pagination or all expired members regardless of page parameters) is not fully documented.

#### Empty Results
When no MPs match the filter criteria, both `MembersOfParliament` and `ExpiredMandateMembers` return empty arrays `[]` (not `null`), unlike some other operations. Requesting a page beyond the result set returns empty arrays without error.

#### Filtering Details
- **genderId:** When set, filters both active and expired MPs by gender (1=Male, 2=Female). When `null`, all genders are included.
- **politicalPartyId:** When set, returns only MPs from that party in both arrays. When `null`, all parties are included.
- **searchText:** Filters MPs by name substring match. When `null`, no text filtering is applied.
- **ageFrom / ageTo:** When set, filters by age range (inclusive). Both are nullable; null means no bound on that end.
- **coalition / constituency:** String filters that can be empty string `""` (no filtering) or set to a value. Exact matching behavior requires testing with actual data.

#### Language Support
MP names (`FullName`), party titles (`PoliticalPartyTitle`), and other localized fields are returned in the language specified by `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).

#### Statistics Object
Always present in the response and provides aggregate counts across the structure. Some fields (e.g., `TotalNumberOfMaterials`) reflect global data and remain non-zero even when all MP filter results are empty. Other fields (e.g., `NumberOfMaterialsInStructure`) reflect the specified structure. These statistics do not change based on MP-specific filters (gender, party, search, age, coalition, constituency).

#### Casing
The operation uses camelCase for most parameters (`methodName`, `languageId`, `genderId`, `politicalPartyId`, `searchText`, `page`, `rows`, `coalition`, `constituency`) but PascalCase for `StructureId`. See per-operation details for parameter casing.


---

## GetParliamentaryGroupDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetParliamentaryGroupDetails"
    },
    "parliamentaryGroupId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the parliamentary group (from GetAllParliamentaryGroups)"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "parliamentaryGroupId", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full official name of the parliamentary group (localized per LanguageId)"
    },
    "Description": {
      "type": "string",
      "description": "Group description; may be minimal placeholder like '-' when not set"
    },
    "NumberOfDeputies": {
      "type": "integer",
      "description": "Count of MPs in the parliamentary group"
    },
    "Materials": {
      "type": "array",
      "description": "Array of materials proposed by the parliamentary group, may be truncated with _truncated property",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Material registration number (e.g. '08-750/1')"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status label"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present (only on last array item), indicates N additional items exist but are not shown"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      }
    },
    "Amendments": {
      "type": "array",
      "description": "Array of amendments proposed by the parliamentary group, may be truncated",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          },
          "_truncated": {
            "type": "integer"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      }
    },
    "Questions": {
      "type": "array",
      "description": "Array of parliamentary questions submitted by members of the parliamentary group",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "DateAsked": {
            "$ref": "#/$defs/AspDate"
          },
          "DateAnswered": {
            "anyOf": [
              {"$ref": "#/$defs/AspDate"},
              {"type": "null"}
            ],
            "description": "null for unanswered questions (StatusId=17), AspDate timestamp for answered questions"
          },
          "StatusId": {
            "$ref": "#/$defs/QuestionStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized question status label"
          }
        },
        "required": ["Id", "Title", "DateAsked", "DateAnswered", "StatusId", "StatusTitle"]
      }
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs in the parliamentary group with role and activity counts, may be truncated",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer",
            "description": "Role within parliamentary group (e.g. 26=Coordinator of political party, 72=Deputy coordinator)"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role label"
          },
          "MaterialsCount": {
            "type": "integer",
            "description": "Count of materials proposed by this member"
          },
          "AmendmentsCount": {
            "type": "integer",
            "description": "Count of amendments proposed by this member"
          },
          "QuestionsCount": {
            "type": "integer",
            "description": "Count of questions submitted by this member"
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle", "MaterialsCount", "AmendmentsCount", "QuestionsCount"]
      }
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Contact email for the parliamentary group, typically null (contact directed through individual members)"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Contact phone for the parliamentary group, typically null"
    },
    "Image": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Image identifier, URL, or base64 data for parliamentary group logo/emblem, null when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure to which this group belongs"
    }
  },
  "required": ["Name", "Description", "NumberOfDeputies", "Materials", "Amendments", "Questions", "Members", "Email", "Phone", "Image", "StructureId"]
}
```

### Notes

**Parameter Casing:** This operation uses mixed PascalCase: lowercase `methodName` and uppercase `LanguageId`.

**Array Truncation:** The `Materials`, `Amendments`, and `Questions` arrays may be truncated due to API display limitations. When truncated, the last item in the array contains an `_truncated` property with an integer value indicating how many additional items exist beyond those shown. The `Members` array may also be truncated for large parliamentary groups. See global "Array truncation" pattern.

**Contact Fields:** `Email`, `Phone`, and `Image` fields are frequently `null` for parliamentary groups. Contact is typically directed through individual members rather than through the group entity itself. See global "Parliamentary group contact" note.

**Response Language:** All localized text fields (Name, StatusTitle, RoleTitle, etc.) are returned in the language specified by the `LanguageId` request parameter.

**Member Roles:** Members include role information via `RoleId`. Observed role IDs in parliamentary group context:
- `26` = Coordinator of political party (Координатор/Координаторка на политичка партија)
- `72` = Deputy coordinator of political party (Заменик координатор/координаторка на политичка партија)

Each member object includes aggregated activity counts (`MaterialsCount`, `AmendmentsCount`, `QuestionsCount`) showing their legislative contributions within this parliamentary group context.

**Questions Field:** The `DateAnswered` field is `null` for questions that have not yet been answered (when `StatusId=17`, Delivered). For answered questions, this field contains an AspDate timestamp.

**StructureId:** Identifies the parliamentary term to which this parliamentary group belongs. Typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current parliamentary term. See global "StructureId" concept.


---

## GetPoliticalPartyDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetPoliticalPartyDetails"
    },
    "politicalPartyId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the political party obtained from GetAllPoliticalParties"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "politicalPartyId", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Official name of the political party in the requested language"
    },
    "Description": {
      "type": "string",
      "description": "Party description; may be placeholder like '-' when not provided"
    },
    "NumberOfDeputies": {
      "type": "integer",
      "description": "Count of MPs/deputies currently affiliated with this political party"
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Material title/name"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration identifier (format: NN-NNN/N)"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier; see MaterialStatusId in global $defs"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Human-readable status label in requested language"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      },
      "description": "Materials (legislative proposals, amendments) submitted by this political party. Empty array when party has no materials."
    },
    "Amendments": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Amendments proposed by the party. Empty array when party has no amendments."
    },
    "Questions": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Parliamentary questions submitted by the party. Empty array when party has no questions."
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string",
            "description": "Complete name of the party member"
          },
          "RoleId": {
            "type": "integer",
            "const": 27,
            "description": "Member role within party (27=Member of political party)"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized human-readable role name (e.g., 'Член/Членка на политичка партија')"
          },
          "MaterialsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
          },
          "AmendmentsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
          },
          "QuestionsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
      },
      "description": "All MPs currently affiliated with this political party"
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact email; typically null"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact phone number; typically null"
    },
    "Image": {
      "type": "string",
      "description": "Party logo/image; may be base64-encoded data or empty string when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure ID this party data belongs to"
    }
  },
  "required": ["Name", "NumberOfDeputies", "Materials", "Amendments", "Questions", "Members", "StructureId"]
}
```

### Notes

- **Parameter casing**: Uses lowercase `methodName` and PascalCase `LanguageId`.
- **politicalPartyId source**: Obtain from GetAllPoliticalParties response.
- **LanguageId**: Controls language of all text fields (Name, StatusTitle, RoleTitle, etc.). See global LanguageId enum (1=Macedonian, 2=Albanian, 3=Turkish).
- **Response structure**: Comprehensive party details including name, member count, associated legislative materials/amendments/questions, and full member roster.
- **Materials array**: All legislative materials (proposals) submitted by the party, with registration dates and current status. Empty when party has no submissions. StatusId references MaterialStatusId enum in global $defs.
- **Amendments and Questions arrays**: Separate from Materials; may be empty depending on party activity.
- **Members array**: Lists all MPs currently affiliated with the party. All members have RoleId `27` (member of political party). The *Count fields (MaterialsCount, AmendmentsCount, QuestionsCount) are always `null` in this endpoint response; they are not populated. Use dedicated per-MP endpoints if per-member activity counts are needed.
- **Description field**: May contain placeholder value like `"-"` if party has no biography text set.
- **Image field**: May be empty string `""` when party has no logo; when present contains base64-encoded image data.
- **Email/Phone**: Typically `null` for political parties; contact information is directed through individual members rather than the party entity.
- **Not paginated**: Returns complete party details in a single response (no page/rows parameters).
- **StructureId**: Implicitly matches the parliamentary term from which politicalPartyId was obtained. Identifies which parliamentary term the party data belongs to.


---

## GetProposerTypes

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetProposerTypes"]
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
        "$ref": "#/$defs/ProposerTypeId"
      },
      "Title": {
        "type": "string",
        "description": "Localized proposer type name in requested language (e.g., 'Пратеник', 'Влада на Република Северна Македонија')"
      },
      "Order": {
        "type": "integer",
        "description": "Display order / sort index for the proposer type"
      }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```

### Notes
- **Operation type**: Catalog / reference data. Returns a simple flat array of all proposer types in a single response (not paginated).
- **Request format**: Method-based operation using camelCase `languageId`.
- **Language fallback behavior**: When `languageId` is set to a non-Macedonian value (e.g., 2=Albanian, 3=Turkish), the API may return `Title` values in Macedonian as fallback. Localization may not be fully applied per language; test with different language IDs to confirm expected behavior.
- **Usage**: `Id` values (1=MP, 2=Government, 4=Voter group) are used in filter parameters of other operations (e.g., `ProposerTypeId` or `InitiatorTypeId`). See global $defs for ProposerTypeId enum.
- **Example response**: `[{"Id": 1, "Title": "Пратеник", "Order": 1}, {"Id": 2, "Title": "Влада на Република Северна Македонија", "Order": 2}, {"Id": 4, "Title": "Граѓанска иницијатива", "Order": 3}, ...]`

---

## GetQuestionDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetQuestionDetails"
    },
    "QuestionId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the parliamentary question to retrieve details for. Obtained from GetAllQuestions Items[].Id."
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "QuestionId", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string",
      "description": "Full text of the parliamentary question"
    },
    "From": {
      "type": "string",
      "description": "Name of the MP who submitted the question"
    },
    "To": {
      "type": "string",
      "description": "Title/position of the official or minister the question is addressed to (e.g. 'Министерот за внатрешни работи')"
    },
    "ToInstitution": {
      "type": "string",
      "description": "Full name of the ministry or government body receiving the question (e.g. 'Министерство за внатрешни работи'). Localized according to LanguageId."
    },
    "QuestionTypeTitle": {
      "type": "string",
      "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question). Localized according to LanguageId."
    },
    "StatusTitle": {
      "type": "string",
      "description": "Current status of the question in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered). Corresponds to QuestionStatusId enum. Localized according to LanguageId."
    },
    "NumberOfDeliveryLetter": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Reference number for delivery correspondence. Often null; purpose is for tracking official delivery letters."
    },
    "Documents": {
      "type": "array",
      "description": "Array of attached documents related to the question (questions, answers, etc.). Returns empty array [] when no documents attached.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Document title"
          },
          "Url": {
            "type": "string",
            "description": "Direct URL to the document file (e.g. SharePoint path)"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Original filename; often null"
          },
          "DocumentTypeId": {
            "type": "integer",
            "const": 26,
            "description": "26=Question document (Прашање)"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Human-readable document type in the requested language"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether the document has been exported/published"
          }
        },
        "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      }
    },
    "Sittings": {
      "type": "array",
      "description": "Array of parliamentary sittings where this question was discussed or answered. Returns empty array [] when question has not yet been discussed in any sitting.",
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
            "type": "string",
            "description": "Human-readable sitting type in the requested language (e.g. 'Пленарна седница' for plenary, 'Комисска седница' for committee). Localized according to LanguageId."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date of sitting in AspDate format"
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Name of committee; null for plenary sittings (when SittingTypeId=1)"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential number of the sitting within its session"
          }
        },
        "required": ["Id", "SittingTypeId", "SittingTypeTitle", "SittingDate", "SittingNumber"]
      }
    }
  },
  "required": ["Title", "From", "To", "ToInstitution", "QuestionTypeTitle", "StatusTitle", "Documents", "Sittings"]
}
```

### Notes

- **methodName:** Must be `"GetQuestionDetails"`.
- **QuestionId:** UUID of the parliamentary question. Obtain from `GetAllQuestions` Items[].Id.
- **LanguageId:** Requested language for response labels and localized fields (1=Macedonian, 2=Albanian, 3=Turkish).
- **Localized fields:** `ToInstitution`, `QuestionTypeTitle`, `StatusTitle`, and `SittingTypeTitle` are localized according to LanguageId request.
- **Non-localized fields:** The question `Title` and `From` field may retain their original language regardless of LanguageId.
- **Empty collections:** Both `Documents` and `Sittings` return empty arrays `[]` when no items are present (not null).
- **Document access:** Document `Url` fields point to SharePoint resources. `IsExported: true` indicates the document is publicly accessible.
- **StatusTitle mapping:** Corresponds to QuestionStatusId enum values (17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). See global for QuestionStatusId definition.
- **Sitting context:** For plenary sittings, `CommitteeTitle` is null and `SittingTypeId` is 1. For committee sittings, `CommitteeTitle` contains the committee name and `SittingTypeId` is 2.
- **NumberOfDeliveryLetter:** Often null in observed data; used for tracking official delivery correspondence when present.


---

## GetSittingDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "MethodName": {
      "type": "string",
      "const": "GetSittingDetails"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "SittingId": {
      "$ref": "#/$defs/UUID",
      "description": "Sitting identifier from GetAllSittings Items[].Id"
    }
  },
  "required": ["MethodName", "LanguageId", "SittingId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "StatusId": {
      "$ref": "#/$defs/SittingStatusId"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Localized sitting status label (e.g. 'Затворена' for closed, 'Почната' for started). Trim whitespace for display."
    },
    "Location": {
      "type": "string",
      "description": "Physical location/room (e.g. 'Сала 6'). Empty string when not specified."
    },
    "Number": {
      "type": "integer",
      "description": "Sequential sitting number within the committee (TypeId: 2) or plenary (TypeId: 1)"
    },
    "SittingDate": {
      "$ref": "#/$defs/AspDate",
      "description": "Primary date/time of the sitting event"
    },
    "TypeTitle": {
      "type": "string",
      "description": "Localized sitting type (e.g. 'Комисіska седница' for committee, 'Пленарна седница' for plenary). Trim whitespace for display."
    },
    "TypeId": {
      "$ref": "#/$defs/SittingTypeId"
    },
    "CommitteeId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Committee UUID when TypeId: 2 (committee sitting). Null for plenary sittings (TypeId: 1)"
    },
    "CommitteeTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee name in requested language. Null for plenary sittings. Trim whitespace for display."
    },
    "DescriptionTypeId": {
      "type": "integer",
      "description": "Sitting description type; e.g. 1 for committee sitting"
    },
    "DescriptionTypeTitle": {
      "type": "string",
      "description": "Localized description type label (e.g. 'Комисiska седница', 'Јавна расправа' for public discussion). Trim whitespace for display."
    },
    "Structure": {
      "type": "string",
      "description": "Parliamentary term period as string (e.g. '2024-2028')"
    },
    "SittingDuration": {
      "anyOf": [
        {"type": "number"},
        {"type": "null"}
      ],
      "description": "Duration in hours. Null for scheduled/incomplete sittings; populated after sitting completes"
    },
    "MediaLinks": {
      "type": "array",
      "items": {},
      "description": "Media/video links for the sitting. Empty array when none available"
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Document title/name"
          },
          "Url": {
            "type": "string",
            "description": "URL to download or view document"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "File name. Often null in practice"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Localized document type label"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether document has been exported/published"
          }
        },
        "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      },
      "description": "Sitting-level documents (e.g. convocation notices). Empty array when none. Multiple documents may share same DocumentTypeId."
    },
    "Continuations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Number": {
            "type": "integer",
            "description": "May be 0 for continuation sessions"
          },
          "StatusId": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Continuation sitting status"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized continuation sitting status. Trim whitespace for display."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date/time of continuation sitting"
          },
          "Location": {
            "type": "string",
            "description": "Physical location of continuation sitting"
          }
        },
        "required": ["Id", "StatusTitle", "SittingDate", "Location"]
      },
      "description": "Continuation sittings when sitting spans multiple sessions. Empty array when no continuations."
    },
    "Absents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "MP identifier"
          },
          "Fullname": {
            "type": "string",
            "description": "Full name of absent MP"
          },
          "PoliticalParty": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Political party name, or null for independents. Large lists may be truncated with _truncated object as final item."
          }
        },
        "required": ["Id", "Fullname"]
      },
      "description": "MPs absent from the sitting. Available for scheduled sittings. May be truncated in response with _truncated indicator on last item."
    },
    "Attendances": {
      "type": "array",
      "items": {},
      "description": "Attendance records. Empty array for scheduled/future sittings; populated after sitting occurs"
    },
    "Votings": {
      "type": "array",
      "items": {},
      "description": "Voting records at sitting level. Empty array for scheduled sittings or when no top-level votes occur"
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {
          "$ref": "#/$defs/UUID"
        },
        "type": {
          "$ref": "#/$defs/TreeItemType",
          "description": "ROOT for root agenda container, LEAF for individual agenda items"
        },
        "text": {
          "type": "string",
          "description": "Root agenda text/title"
        },
        "beforeText": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
        },
        "afterText": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "May contain XML-like multilingual markup: <MK>...</MK><AL>...</AL><EN>...</EN><FR>...</FR> regardless of requested LanguageId"
        },
        "status": {
          "type": "integer",
          "description": "0 for ROOT node. For LEAF items: see AgendaItemStatusId (50=reviewed, 69=new)"
        },
        "statusTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
        },
        "treeItemTypeId": {
          "anyOf": [
            {"type": "integer"},
            {"type": "null"}
          ]
        },
        "agendaItemType": {
          "anyOf": [
            {"type": "integer"},
            {"type": "null"}
          ],
          "description": "See AgendaItemTypeId (1=Plenary, 2=Committee). Null for ROOT nodes."
        },
        "isActive": {
          "type": "boolean"
        },
        "order": {
          "type": "integer",
          "description": "Display order"
        },
        "euCompatible": {
          "type": "boolean",
          "description": "EU compatibility flag"
        },
        "data": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "HTML-formatted material type and proposer info. Null for ROOT. Parse HTML appropriately for display."
        },
        "objectId": {
          "anyOf": [
            {"$ref": "#/$defs/UUID"},
            {"type": "null"}
          ],
          "description": "UUID of linked material when objectTypeId: 1. Null for ROOT or non-material items. Pass to GetMaterialDetails."
        },
        "objectTypeId": {
          "$ref": "#/$defs/AgendaObjectTypeId",
          "description": "0 for ROOT. 1=Material, 4=Questions/other items."
        },
        "objectTypeTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "e.g. 'Материјал' for material items. Null for ROOT"
        },
        "objectStatusId": {
          "type": "integer",
          "description": "Material status when objectTypeId: 1. See MaterialStatusId. 0 for ROOT"
        },
        "objectSubTypeId": {
          "type": "integer",
          "description": "Material subtype (e.g. 1=law proposal, 28=reports). 0 for ROOT"
        },
        "manyAmendments": {
          "type": "boolean",
          "description": "Indicates multiple amendments to material"
        },
        "mediaItems": {
          "type": "array",
          "items": {},
          "description": "Media items associated with agenda item or ROOT"
        },
        "VotingDefinitions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "Use as VotingDefinitionId parameter in GetVotingResultsForAgendaItem"
              },
              "Title": {
                "type": "string",
                "description": "Voting definition title"
              },
              "Description": {
                "type": "string",
                "description": "Voting description"
              },
              "VotingType": {
                "type": "string",
                "description": "Type of voting (e.g. 'Јавно' for public voting)"
              },
              "OverallResult": {
                "type": "string",
                "description": "Overall voting result (e.g. 'Усвоен' for adopted/passed)"
              }
            },
            "required": ["Id", "Title", "VotingType", "OverallResult"]
          },
          "description": "Voting events for agenda item. Empty array when no votes."
        },
        "Documents": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID"
              },
              "Title": {
                "type": "string"
              },
              "Url": {
                "type": "string"
              },
              "FileName": {
                "type": "null"
              },
              "DocumentTypeId": {
                "$ref": "#/$defs/DocumentTypeId"
              },
              "DocumentTypeTitle": {
                "type": "string"
              },
              "IsExported": {
                "type": "boolean"
              }
            },
            "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
          },
          "description": "Documents associated with agenda item. Empty array when none."
        },
        "children": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/$defs/UUID"
              },
              "type": {
                "$ref": "#/$defs/TreeItemType",
                "description": "Should be LEAF for child items"
              },
              "text": {
                "type": "string"
              },
              "beforeText": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "afterText": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "status": {
                "type": "integer",
                "description": "See AgendaItemStatusId (50=reviewed, 69=new)"
              },
              "statusTitle": {
                "type": "string"
              },
              "treeItemTypeId": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ]
              },
              "agendaItemType": {
                "type": "integer",
                "description": "See AgendaItemTypeId (1=Plenary, 2=Committee)"
              },
              "isActive": {
                "type": "boolean"
              },
              "order": {
                "type": "integer"
              },
              "euCompatible": {
                "type": "boolean"
              },
              "data": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "HTML-formatted material/item details. Parse HTML appropriately for display."
              },
              "objectId": {
                "anyOf": [
                  {"$ref": "#/$defs/UUID"},
                  {"type": "null"}
                ],
                "description": "UUID of linked material (when objectTypeId: 1)"
              },
              "objectTypeId": {
                "$ref": "#/$defs/AgendaObjectTypeId"
              },
              "objectTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "objectStatusId": {
                "type": "integer",
                "description": "Material status"
              },
              "objectSubTypeId": {
                "type": "integer",
                "description": "Material subtype"
              },
              "manyAmendments": {
                "type": "boolean"
              },
              "mediaItems": {
                "type": "array",
                "items": {}
              },
              "VotingDefinitions": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {"$ref": "#/$defs/UUID"},
                    "Title": {"type": "string"},
                    "Description": {"type": "string"},
                    "VotingType": {"type": "string"},
                    "OverallResult": {"type": "string"}
                  },
                  "required": ["Id", "Title", "VotingType", "OverallResult"]
                },
                "description": "Voting events for this leaf item"
              },
              "Documents": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {"$ref": "#/$defs/UUID"},
                    "Title": {"type": "string"},
                    "Url": {"type": "string"},
                    "FileName": {"type": "null"},
                    "DocumentTypeId": {"$ref": "#/$defs/DocumentTypeId"},
                    "DocumentTypeTitle": {"type": "string"},
                    "IsExported": {"type": "boolean"}
                  },
                  "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
                }
              },
              "children": {
                "type": "array",
                "items": {},
                "description": "Nested children; typically empty for LEAF items"
              }
            },
            "required": ["id", "type", "text", "status", "agendaItemType", "isActive", "order", "euCompatible", "objectTypeId", "objectStatusId", "objectSubTypeId", "manyAmendments", "mediaItems", "VotingDefinitions", "Documents", "children"]
          },
          "description": "Agenda items (LEAF nodes) within the sitting. Root node (type: ROOT) contains this children array."
        }
      },
      "required": ["id", "type", "text", "status", "isActive", "order", "euCompatible", "objectTypeId", "objectStatusId", "objectSubTypeId", "manyAmendments", "mediaItems", "VotingDefinitions", "Documents", "children"],
      "description": "Hierarchical tree structure of sitting agenda. Root node has type: ROOT with children array of agenda items (type: LEAF)."
    }
  },
  "required": ["StatusId", "StatusTitle", "Location", "Number", "SittingDate", "TypeTitle", "TypeId", "DescriptionTypeId", "DescriptionTypeTitle", "Structure", "MediaLinks", "Documents", "Continuations", "Absents", "Attendances", "Votings", "Agenda"]
}
```

### Notes

**Parameter casing:**
- Request uses `MethodName`, `LanguageId`, `SittingId` (all PascalCase)
- Do not use lowercase variants (`methodName`, `languageId`, `sittingId`)

**Sitting types:**
- **Plenary sitting** (`TypeId: 1`): `CommitteeId` and `CommitteeTitle` are null. `DescriptionTypeTitle` typically 'Пленарна седница'
- **Committee sitting** (`TypeId: 2`): `CommitteeId` and `CommitteeTitle` are populated. `DescriptionTypeTitle` may be 'Комисiska седница' or other committee-specific type
- **Public hearing**: May appear as `TypeId: 2` with `DescriptionTypeTitle: 'Јавна расправа'`

**Status and timing:**
- **Scheduled sitting** (`StatusId: 1`): `Absents` is pre-populated; `Attendances`, `Votings`, `SittingDuration` are empty/null
- **Started/completed sitting** (`StatusId: 2, 3`): All fields populated; `SittingDuration` contains hours
- **Closed sitting** (`StatusId: 5`): Similar to completed

**Agenda structure:**
- Root node always has `type: 'ROOT'`, `objectTypeId: 0`, `status: 0`, `objectId: null`
- `children` array contains LEAF nodes representing actual agenda items
- Each LEAF node has `objectTypeId` indicating linked item type (1=Material, 4=Questions, 0=None)
- Leaf nodes with `objectTypeId: 1` have `objectId` = material UUID; pass to `GetMaterialDetails`
- Tree may be nested to arbitrary depth

**Voting definitions:**
- Each agenda item can have zero or more voting definitions
- Use `VotingDefinitions[].Id` as `VotingDefinitionId` parameter in `GetVotingResultsForAgendaItem` to retrieve detailed voting tallies
- `OverallResult` shows high-level outcome (e.g. 'Усвоен' = passed)

**Document types:**
- `DocumentTypeId: 20` = Convocation notice (Известување за свикување)
- `DocumentTypeId: 7` = Full text of material
- `DocumentTypeId: 46` = Legislative committee report
- `DocumentTypeId: 52` = Committee report
- Multiple documents may have the same type

**Continuations:**
- Empty array when sitting completes in single session
- Multiple continuation objects when sitting spans multiple days/sessions
- Each continuation has its own date, location, status

**Absents array:**
- Lists MPs who did not attend
- `PoliticalParty` may be null for independents or when affiliation not recorded
- Large lists may be truncated with `_truncated` object as final item indicating number of additional records omitted
- Empty array if all expected members attended

**Language support:**
- `LanguageId: 1` = Macedonian (default)
- `LanguageId: 2` = Albanian
- `LanguageId: 3` = Turkish
- Affects `StatusTitle`, `TypeTitle`, `CommitteeTitle`, `DescriptionTypeTitle`, `statusTitle` in agenda, and other localized fields
- `afterText` may contain XML-like multilingual markup (`<MK>...</MK><AL>...</AL>`) even when specific language requested

**Data quality:**
- Localized titles may contain leading/trailing whitespace; trim for display
- HTML in `data` fields should be parsed appropriately for client display
- Handle `null` and empty array values consistently in client code"


---

## GetUserDetailsByStructure

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetUserDetailsByStructure"
    },
    "userId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MP. Obtain from GetParliamentMPsNoImage Items[].Id"
    },
    "structureId": {
      "anyOf": [
        {
          "$ref": "#/$defs/UUID"
        },
        {
          "type": "null"
        }
      ],
      "description": "UUID of parliamentary term. Obtain from GetAllStructuresForFilter. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current. Required for valid MP data."
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "1=Macedonian, 2=Albanian, 3=Turkish. Affects localized response fields."
    }
  },
  "required": [
    "methodName",
    "userId",
    "structureId",
    "languageId"
  ]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "FullName": {
      "type": "string",
      "description": "Full name of the MP (FirstName LastName)"
    },
    "Email": {
      "type": "string",
      "description": "Official parliamentary email in format FirstInitial.LastName@sobranie.mk"
    },
    "Image": {
      "type": "string",
      "description": "Base64-encoded profile image (JPEG or PNG). Can be very long string (tens of kilobytes)."
    },
    "MobileNumber": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "Mobile phone number or null if not provided"
    },
    "PhoneNumber": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "Office phone number or null if not provided"
    },
    "Biography": {
      "type": "string",
      "description": "HTML-formatted biographical text with inline <p> and <span> tags"
    },
    "RoleId": {
      "$ref": "#/$defs/RoleId",
      "description": "Primary role in parliament. Example: 1=MP (Пратеник/Пратеничка)"
    },
    "RoleTitle": {
      "type": "string",
      "description": "Localized role title in requested language (e.g., 'Пратеник/Пратеничка' for MP)"
    },
    "ElectedFrom": {
      "$ref": "#/$defs/AspDate",
      "description": "Start date of mandate (AspDate format)"
    },
    "ElectedTo": {
      "anyOf": [
        {
          "$ref": "#/$defs/AspDate"
        },
        {
          "type": "null"
        }
      ],
      "description": "End date of mandate (AspDate format). null for current/active mandates."
    },
    "PoliticalPartyId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MP's political party"
    },
    "PoliticalPartyTitle": {
      "type": "string",
      "description": "Name of the MP's political party in requested language"
    },
    "Gender": {
      "type": "string",
      "description": "Localized gender string in requested language. Examples: 'Машки' (Male), 'Женски' (Female)"
    },
    "DateOfBirth": {
      "type": "string",
      "pattern": "^\\d{2}\\.\\d{2}\\.\\d{4}$",
      "description": "Date of birth in DD.MM.YYYY format (not AspDate). Example: '02.03.1974'"
    },
    "Constituency": {
      "type": "string",
      "description": "Electoral constituency number as string. Example: '6'"
    },
    "Coalition": {
      "type": "string",
      "description": "Electoral coalition name MP was elected under. Example: 'Коалиција Твоја Македонија'"
    },
    "StructureDate": {
      "type": "string",
      "description": "Human-readable parliamentary term date range. Example: '2024 - 2028'"
    },
    "CabinetMembers": {
      "type": "array",
      "items": {},
      "description": "Cabinet/ministerial positions held by the MP. Empty array [] when no data."
    },
    "Materials": {
      "type": "array",
      "items": {},
      "description": "Materials (bills/acts) associated with the MP. Empty array [] when no data."
    },
    "Questions": {
      "type": "array",
      "items": {},
      "description": "Parliamentary questions submitted by the MP. Empty array [] when no data."
    },
    "Delegations": {
      "type": "array",
      "items": {},
      "description": "Delegation memberships. Empty array [] when no data."
    },
    "FriendshipGroups": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Name of friendship group in requested language"
          },
          "Description": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "description": "Description or null if not set"
          }
        },
        "required": [
          "Id",
          "Title"
        ]
      },
      "description": "Friendship group memberships. Empty array [] when no groups."
    },
    "Amendments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Registration number in format XX-XXX/X (e.g., '08-750/1')"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status text in requested language"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present on last item, indicates N additional items not shown"
          }
        },
        "required": [
          "Id",
          "Title",
          "RegistrationDate",
          "RegistrationNumber",
          "StatusId",
          "StatusTitle"
        ]
      },
      "description": "Amendment proposals submitted by the MP. May be truncated by API. Empty array [] when no amendments."
    },
    "Acts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Registration number in format XX-XXX/X"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status text in requested language"
          }
        },
        "required": [
          "Id",
          "Title",
          "RegistrationDate",
          "RegistrationNumber",
          "StatusId",
          "StatusTitle"
        ]
      },
      "description": "Legislative acts/proposals authored or co-sponsored by the MP. Empty array [] when no acts."
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "CommitteeId": {
            "$ref": "#/$defs/UUID"
          },
          "CommitteeTitle": {
            "type": "string",
            "description": "Committee name in requested language"
          },
          "Roles": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "$ref": "#/$defs/CommitteeRoleId"
                },
                "Title": {
                  "type": "string",
                  "description": "Localized role title in requested language (e.g., 'Претседател/Претседателка на комисија')"
                }
              },
              "required": [
                "Id",
                "Title"
              ]
            },
            "description": "Roles within the committee. MP can have multiple roles in one committee."
          }
        },
        "required": [
          "CommitteeId",
          "CommitteeTitle",
          "Roles"
        ]
      },
      "description": "Committee memberships with roles. Empty array [] when MP has no committee roles."
    },
    "CommitteeMemberships": {
      "type": "array",
      "items": {},
      "description": "Additional committee membership details. Empty array [] when no data."
    },
    "DelegationMemberships": {
      "type": "array",
      "items": {},
      "description": "Delegation membership details. Empty array [] when no data."
    },
    "DepartmentMemberships": {
      "type": "array",
      "items": {},
      "description": "Department membership details. Empty array [] when no data."
    },
    "FriendshipGroupMemberships": {
      "type": "array",
      "items": {},
      "description": "Friendship group membership details. Empty array [] when no data."
    },
    "MediaItems": {
      "type": "array",
      "items": {},
      "description": "Media items associated with the MP. Empty array [] when no data."
    }
  },
  "required": [
    "FullName",
    "Email",
    "Image",
    "Biography",
    "RoleId",
    "RoleTitle",
    "ElectedFrom",
    "PoliticalPartyId",
    "PoliticalPartyTitle",
    "Gender",
    "DateOfBirth",
    "Constituency",
    "Coalition",
    "StructureDate"
  ]
}
```

### Notes

**Calling convention:**  
Method-based POST to `https://www.sobranie.mk/Routing/MakePostRequest` with lowercase `methodName` and `languageId` in request body.

**Response structure:**  
Returns comprehensive MP profile including biographical data, political affiliations, committee roles, and legislative activity.

**Array behavior:**  
All relationship arrays (CabinetMembers, Materials, Questions, Delegations, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems) return empty arrays `[]` when no data, never `null`.

**Notable field behaviors:**
- **Biography** — HTML-formatted text with inline `<p>` and `<span>` tags containing biographical details.
- **Image** — Base64-encoded JPEG or PNG image data. Field populated with actual image despite operation name implying "NoImage". Can be tens of kilobytes; clients should handle large string payloads.
- **Gender** — Localized text string in requested language (e.g., "Машки" for male, "Женски" for female), not a numeric GenderId.
- **DateOfBirth** — String format DD.MM.YYYY (distinct from AspDate format). Example: "02.03.1974"
- **Constituency** — String value representing electoral constituency number (e.g., "6").
- **ElectedTo** — `null` for current/active parliamentary term. Contains AspDate when term has ended.
- **MobileNumber / PhoneNumber** — Often `null` when not provided.
- **PoliticalPartyTitle** — Party name in requested language.
- **RoleTitle** — Localized role title (e.g., "Пратеник/Пратеничка" for MP); corresponds to RoleId enum value.

**Array field details:**
- **CabinetMembers, Materials, Questions, Delegations, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems** — Documented with minimal item schemas from available samples; full structure may be expanded when more response data available. All return empty `[]` when MP has no entries.
- **Amendments** — Array may be truncated by API with `{"_truncated": N}` object appended, indicating N additional items exist. Uses MaterialStatusId enum (e.g., 6=Delivered to MPs, 12=Closed). Empty `[]` when no amendments.
- **Acts** — Array of legislative proposals/laws the MP authored or co-sponsored. Uses same structure as Amendments. Empty `[]` when no acts.
- **Committees** — Shows all committee memberships. Roles array can have multiple entries per committee when MP holds multiple roles. Roles use CommitteeRoleId enum (6=Chair, 7=Member, 10=Approver, 11=Advisor, 82=Deputy Chair, 83=Deputy Member). Empty `[]` when MP has no committee roles.
- **FriendshipGroups** — Descriptions can be empty strings or null. Empty `[]` when MP is not part of any friendship groups.

**Date formats:**
- **ElectedFrom / ElectedTo** — AspDate format (`/Date(timestamp)/`)
- **DateOfBirth** — DD.MM.YYYY string format (not AspDate)
- **RegistrationDate** (in Amendments/Acts) — AspDate format

**Localization:**  
Response fields such as RoleTitle, PoliticalPartyTitle, CommitteeTitle, StatusTitle, and Gender are localized based on the requested `languageId`.

**StructureId behavior:**  
When `structureId` is null, results may be empty or cross-term; use current structure UUID from GetAllStructuresForFilter for standard MP profile retrieval.


---

## OperationName

### Request Schema
```json
{
  "type": "object",
  "description": "Template for per-operation request schema. Replace with actual operation details.",
  "properties": {
    "methodName": {
      "type": "string",
      "description": "Operation method name (camelCase or PascalCase per operation)"
    }
  },
  "required": ["methodName"]
}
```

### Response Schema
```json
{
  "type": "object",
  "description": "Template for per-operation response schema. Replace with actual operation details.",
  "properties": {
    "Items": {
      "type": ["array", "null"],
      "description": "Result items array; may be null when TotalItems is 0"
    },
    "TotalItems": {
      "type": "integer",
      "description": "Total count of items"
    }
  }
}
```

### Notes
- This is a template placeholder. Replace with actual operation request/response schemas and operation-specific notes (parameter casing, pagination style, language fallback, data quality quirks).
- Refer to global.md for common patterns, enums ($defs), and calling conventions.
- Use $ref to global $defs for all enums and shared types (LanguageId, UUID, AspDate, etc.).
- Include only operation-specific details and behaviors in this section.