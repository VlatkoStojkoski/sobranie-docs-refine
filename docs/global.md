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
- **Spelling variations in TypeTitle:** Fields like `TypeTitle` in detail endpoints (e.g., GetCouncilDetails Meetings array, GetCommitteeDetails, GetSittingDetails) may contain spelling variations, typos, or inconsistencies. Normalize for display if needed.

## Common Patterns

- **Pagination:** Two styles — (1) `Page` (1-based) and `Rows`; (2) `CurrentPage` and `ItemsPerPage`. When `TotalItems: 0`, `Items` may be `null` rather than `[]`. Check per-operation docs.
- **Array truncation:** Large arrays in listing endpoints may include a truncation marker. In listing endpoints (e.g., GetAllSittings, GetAllQuestions), `_truncated` appears as a standalone minimal object `{"_truncated": N}` within the array at any position, counting toward array length and indicating N additional items omitted. In detail endpoints (e.g., GetSittingDetails, GetCouncilDetails, GetCommitteeDetails), `_truncated` may appear as a standalone object within member/item arrays (CompositionMembers, SecretariatMembers, Documents, Absents, Attendances, Votings, Agenda.children, etc.), also counting toward array length. In ASMX endpoints (e.g., GetCustomEventsCalendar), `_truncated` may appear as a standalone object within the response array, counting toward array length. Detail endpoints such as GetPoliticalPartyDetails and GetUserDetailsByStructure may also include `_truncated` within related arrays (Materials, Amendments, Acts, Committees, Delegations, FriendshipGroups, etc.), appearing as standalone objects counting toward array length. Check per-operation docs for endpoint-specific truncation behavior.
- **Multi-language:** Operations like GetAllMaterialsForPublicPortal and GetAllQuestions return localized text (TypeTitle, StatusGroupTitle, etc.) based on `LanguageId`.
- **Reading stages:** `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings` track material progress. Each contains sitting objects with `SittingTypeId` (1=plenary, 2=committee), `StatusGroupId`, `ObjectStatusId`.
- **Agenda tree:** GetSittingDetails agenda uses hierarchical tree with `type: "ROOT"` and `type: "LEAF"`; leaf nodes may reference materials via `objectId`/`objectTypeId`. Some fields (e.g. `afterText`) may contain XML-like language tags (`<MK>...</><AL>...</>`). Nested children may include amendments with `agendaItemType: 8`.
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
- **Materials:** Array in detail responses (empty `[]` when absent, not `null`). May include truncation marker.
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
    "enum": [1, 2, 8],
    "description": "1=Plenary, 2=Committee, 8=Amendment, other values may exist"
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
    "enum": [0, 6, 9, 10, 11, 12, 24, 64],
    "description": "0=No specific reading stage, 6=Delivered to MPs, 9=First reading, 10=Second reading, 11=Third reading, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "MaterialTypeId": {
    "type": "integer",
    "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "description": "1=Law proposal (Предлог закон), 2=Interpellation, 3=Government election, 4=Authentic interpretation of law, 5=Consolidated law text, 6=Budget, 7=Rules of procedure (Деловник), 8=Declaration/resolution/decision/recommendation, 9=Consent to statutes and other general acts, 10=Ratification of international treaties, 11=Citizens' initiative, 13=Proposal to establish responsibility of President, 14=Confidence in Government, 15=Government resignation, 16=Dismissal of government member, 17=Termination and revocation of MP mandate, 18=Strategy proposal, 19=Spatial plan proposal, 20=Resignation of public/other office holder, 21=Election of working bodies/permanent delegations/friendship groups, 22=Elections/appointments/dismissals of public/other functions, 23=Question of confidence in Government, 24=Other, 26=Corrections, 27=Amendment proposal, 28=Analysis/report/information/other material, 29=Proposal for constitutional amendment, 30=Determination of draft constitutional amendments, 31=Decision on establishment of permanent working bodies, 32=Budget final account, 33=Proposed constitutional law for implementing amendments, 34=Determination of proposed constitutional amendments, 35=Adoption of constitutional amendments, 36=Proclamation of constitutional amendments, 37=Appointment of government member. IDs 12 and 25 are absent."
  },
  "ProposerTypeId": {
    "type": "integer",
    "enum": [1, 2, 4, 5],
    "description": "1=MP, 2=Government, 4=Voter group, 5=Друга институција (Other institution)"
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
    "enum": [0, 1, 7, 8, 9, 19, 20, 26, 28, 30, 40, 42, 43, 46, 52, 57, 59, 65],
    "description": "0=No type/Unknown, 1=Document, 7=Full text of material, 8=Adopted act, 9=Notification to MPs, 19=Решение за свикување седница (Decision to convene), 20=Convocation notice, 26=Question document, 28=Answer document, 30=Committee report without approval, 40=Notice of sitting rescheduling, 42=Notice of sitting continuation, 43=Notice of agenda supplement, 46=Legal-Legislative Committee report, 52=Report/Committee report, 57=Стенограм (Stenographic notes/transcript), 59=Записник (Minutes/record of proceedings), 65=Supplemented draft law"
  },
  "EventTypeId": {
    "type": "integer",
    "enum": [5],
    "description": "5=Press conference/visit/working session/commemoration/public event (other types may exist)"
  },
  "MPsClubRoleId": {
    "type": "integer",
    "enum": [77, 78, 79, 81],
    "description": "77=Член/Членка (Member of friendship group), 78=President, 79=Vice-President, 81=Member"
  },
  "CommitteeRoleId": {
    "type": "integer",
    "enum": [6, 7, 10, 11, 82, 83],
    "description": "6=Committee President/Chair, 7=Committee Member, 10=Approver/Одобрувач, 11=Committee Advisor, 82=Vice President/Deputy Chair, 83=Deputy Member"
  },
  "RoleId": {
    "type": "integer",
    "enum": [1, 27, 72],
    "description": "1=MP (Пратеник/Пратеничка), 27=Member of political party (Член/Членка на политичка партија), 72=Deputy coordinator of political party (Заменик координатор/координаторка на политичка партија). Other role IDs may exist."
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
    "enum": [50, 51, 60, 62, 63, 69],
    "description": "50=Reviewed, 51=Status variant, 60=Other status, 62=Status variant, 63=Withdrawn (Повлечена), 69=New"
  },
  "AgendaObjectTypeId": {
    "type": "integer",
    "enum": [0, 1, 4],
    "description": "0=None, 1=Material, 4=Questions/other"
  },
  "VotingOptionId": {
    "type": "string",
    "format": "uuid",
    "description": "Voting option identifier"
  },
  "VotingTypeId": {
    "type": "string",
    "description": "Voting type (e.g. 'Јавно'=Public voting; localized text; other types may exist)"
  },
  "VotingOutcomeId": {
    "type": "string",
    "enum": ["Усвоен"],
    "description": "Voting outcome/result: Усвоен=Adopted. Other values may exist."
  }
}
```

## Operations Index

### Catalogs (reference data)

| Operation | Method-based | Description |
|-----------|--------------|----------|
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
|-----------|--------------|----------|
| GetAllSittings | ✓ | Sittings. Filter: TypeId, CommitteeId, StatusId, dates. May include truncation marker in Items array. |
| GetAllQuestions | ✓ | Parliamentary questions. Filter: SearchText, RegistrationNumber, StatusId, CommitteeId, dates. StructureId: null = cross-term. May include truncation marker in Items array. |
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
|-----------|----------|----------|
| GetCustomEventsCalendar | Moldova/services/CalendarService.asmx/GetCustomEventsCalendar | ASMX, model: {Language, Month, Year}. Response: d array |
| LoadLanguage | Infrastructure/LoadLanguage | POST, empty body. Returns Code, Items (Key/Value localization) |
| GetOfficialVisitsForUser | Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser | ASMX, model: user UUID. Response: {"d": []} |

See per-operation .md files for detailed request/response schemas and operation-specific notes.