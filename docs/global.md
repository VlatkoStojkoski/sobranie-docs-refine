# Sobranie.mk API Index

> Macedonian Parliament (Собрание) — operation index and calling conventions.

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