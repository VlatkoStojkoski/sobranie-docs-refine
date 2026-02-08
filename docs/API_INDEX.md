# Sobranie.mk API Index

> North Macedonian Parliament (Собрание) — operation index and calling conventions.

## Calling Conventions

### 1. Method-based (standard)

**URL:** `https://www.sobranie.mk/Routing/MakePostRequest`  
**Method:** POST  
**Content-Type:** application/json

Request body includes `methodName` (or `MethodName` for some operations) and operation-specific parameters. The method name selects the operation.

**Parameter casing:** Some operations use `methodName`/`languageId`; others use `MethodName`/`LanguageId`. See per-operation notes.

### 2. ASMX (non-standard)

**Base:** `https://www.sobranie.mk/Moldova/services/`  
**Format:** POST with wrapped request body (e.g. `{ "model": { ... } }`).  
**Response:** Often wrapped in `d` property.

### 3. Infrastructure (non-standard)

**Base:** `https://www.sobranie.mk/Infrastructure/`  
**Format:** POST, no methodName. Different request/response shapes.

---

## Common Conventions

- **Date format:** `/Date(timestamp)/` — milliseconds since Unix epoch
- **LanguageId:** 1 = Macedonian, 2 = Albanian, 3 = Turkish
- **StructureId:** Parliamentary term. From `GetAllStructuresForFilter`. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current)

---

## Operations

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
| GetAllInstitutionsForFilter | ✓ | Institutions (ministries, etc.). May include placeholder entries (Title: "/") |
| GetAllProcedureTypes | ✓ | Procedure types (1,2,3) |
| GetProposerTypes | ✓ | Proposer types (Id, Title, Order) |
| GetAllApplicationTypes | ✓ | Application types |

### Listings (paginated / filterable)

| Operation | Method-based | Description |
|-----------|--------------|-------------|
| GetAllSittings | ✓ | Sittings. Filter: TypeId, CommitteeId, StatusId, dates |
| GetAllQuestions | ✓ | Parliamentary questions |
| GetAllMaterialsForPublicPortal | ✓ | Materials. Uses MethodName. Many filters |
| GetParliamentMPsNoImage | ✓ | MPs. Filter: gender, party, search. Note: includes UserImg (base64) despite name |
| GetMonthlyAgenda | ✓ | Agenda for month/year |
| GetAllPoliticalParties | ✓ | Parties per structure |
| GetAllCouncils | ✓ | Councils |
| GetAllParliamentaryGroups | ✓ | Parliamentary groups |
| GetAllMPsClubsByStructure | ✓ | MPs clubs. Uses MethodName |

### Detail (item by ID)

| Operation | Method-based | ID source |
|-----------|--------------|-----------|
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

| Operation | URL | Format |
|-----------|-----|--------|
| GetCustomEventsCalendar | Moldova/services/CalendarService.asmx/GetCustomEventsCalendar | ASMX, model: {Language, Month, Year}. Response: d array with __type, Id, EventDescription, EventLink, EventLocation, EventDate, EventType |
| LoadLanguage | Infrastructure/LoadLanguage | POST, empty body. Returns Code, Items (Key/Value localization) |
| GetOfficialVisitsForUser | Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser | ASMX, model: user UUID. Response: {"d": []} (array of visit objects when data present) |
