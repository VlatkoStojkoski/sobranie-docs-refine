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
**Parameter casing:** Some operations use `methodName`/`languageId`; others use `MethodName`/`LanguageId`. Some operations accept both casings interchangeably (e.g., GetAllQuestionStatuses accepts both `languageId` and `LanguageId`). See per-operation notes.

## Common Conventions
- **Date format:** `/Date(timestamp)/` — milliseconds since Unix epoch
- **LanguageId:** 1 = Macedonian, 2 = Albanian, 3 = Turkish
- **StructureId:** Parliamentary term. From `GetAllStructuresForFilter`. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current). Historical terms available back to at least 2008. The structure with `IsCurrent: true` is the active parliamentary term and should be used as default StructureId in filter operations.
---
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/". These should be filtered or handled gracefully in client code.
- **Data quality / whitespace:** Material type titles (from `GetAllMaterialTypesForFilter`) and other catalog entries may contain leading/trailing whitespace characters (`\r`, `\n`, spaces) that should be trimmed for display.
- **Language fallback:** Some endpoints (e.g. `GetAllProcedureTypes`, catalog operations) may return Macedonian text regardless of the requested `languageId` parameter, indicating incomplete localization or API-level fallback behavior. Test with different language IDs to confirm actual behavior for each endpoint.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/"`
- **StructureId:** Parliamentary term. From `GetAllStructuresForFilter`. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current). Historical terms available back to at least 2008. The structure with `IsCurrent: true` is the active parliamentary term and should be used as default StructureId in filter operations. When set to `null` in some operations (e.g., GetParliamentMPsNoImage), returns empty results but Statistics object may still be populated with global counts.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/ "` or `"-"`. These should be filtered or handled gracefully in client code.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `/` or `-`. These should be filtered or handled gracefully in client code.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"slash"` or `"-"`. These should be filtered or handled gracefully in client code.
- **StructureId:** Parliamentary term. From `GetAllStructuresForFilter`. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current)
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/"` or `"-"`. These should be filtered or handled gracefully in client code.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `/`, `-`, or `/`. These should be filtered or handled gracefully in client code.
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/"
- **Data quality / placeholder records:** Some endpoints (e.g. `GetAllInstitutionsForFilter`) may return placeholder entries with non-descriptive titles like `"/

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
| Operation | URL | Format |
|-----------|-----|--------|
| GetCustomEventsCalendar | Moldova/services/CalendarService.asmx/GetCustomEventsCalendar | ASMX, model: {Language, Month, Year}. Response: d array with __type, Id, EventDescription, EventLink, EventLocation, EventDate, EventType |
| LoadLanguage | Infrastructure/LoadLanguage | POST, empty body. Returns Code, Items (Key/Value localization) |
| GetOfficialVisitsForUser | Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser | ASMX, model: user UUID. Response: {"d": []} (array of visit objects when data present) |
---
# Schemas and per-operation reference
| GetAllInstitutionsForFilter | ✓ | Institutions (ministries, etc.). Includes placeholder entries with Title "/" or "-" that should be filtered. May return translations in Macedonian even when other languages are requested. |
| GetAllQuestions | ✓ | Parliamentary questions. Filter: SearchText, RegistrationNumber, StatusId, From, To, CommitteeId, dates |
| GetCustomEventsCalendar | ✓ | Calendar events (ASMX wrapper). Returns events for month/year |
**Parameter casing:** Some operations use `methodName`/`languageId`; others use `MethodName`/`LanguageId`. Some operations accept both casings interchangeably (e.g., GetAllQuestionStatuses accepts both `languageId` and `LanguageId`). See per-operation notes.
| GetParliamentMPsNoImage | ✓ | MPs. Filter: gender, party, search, coalition, constituency. Returns active and expired mandate MPs. Note: includes UserImg (base64) despite name |

## $defs
```json
{
  "AspDate": {
    "type": "string",
    "pattern": "^/Date\\(\\d+\\)/$"
  },
  "LanguageId": {
    "type": "integer",
    "description": "1=Macedonian, 2=Albanian, 3=Turkish"
  },
  "GenderId": {
    "enum": [1, 2],
    "description": "1=Male (Машки), 2=Female (Женски)"
  },
  "SittingStatusId": {
    "enum": [1, 2, 3, 4, 5, 6],
    "description": "1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed"
  },
  "AgendaItemTypeId": {
    "description": "1=Plenary, 2=Committee"
  },
  "QuestionStatusId": {
    "enum": [17, 19, 20, 21],
    "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
  },
  "MaterialStatusId": {
    "enum": [0, 6, 9, 10, 11, 12, 24, 64],
    "description": "0=Plenary/unknown, 6=Delivered to MPs, 9=First reading, 10=Second, 11=Third, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "ProposerTypeId": {
    "enum": [1, 2, 4, 5, 6],
    "description": "1=MP (Пратеник), 2=Government (Влада на Република Северна Македонија), 4=Voter group, 5=Working body (Работно тело), 6=Other institution (Друга институција)"
  },
  "ProcedureTypeId": {
    "enum": [1, 2, 3],
    "description": "1=Regular (Редовна постапка), 2=Shortened (Скратена постапка), 3=Urgent (Итна постапка)"
  },
  "ApplicationTypeId": {
    "description": "1=Case report (Пријава на случај / Paraqitja e rastit), 2=Participation in public debate (Учество во јавна расправа / Pjesëmarrje në debatin publik), 3=Discussion (Дискусија / Diskutim)"
  },
  "UUID": {
    "format": "uuid"
  },
  "CouncilTypeId": {
    "enum": [1],
    "description": "1=Permanent (Постојана)"
  },
  "MaterialTypeId": {
    "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "description": "1=Draft law (Предлог закон), 2=Interpellation (Интерпелација), 3=Government election (Избор на Влада), 4=Authentic interpretation (Автентично толкување на закон), 5=Consolidated text (Пречистен текст на закон), 6=Budget (Буџет), 7=Rules of procedure (Деловник), 8=Declaration/resolution/decision/recommendation (Декларација, резолуција, одлука и препорака), 9=Consent to statutes (Согласност на статути и други општи акти), 10=Ratification of international treaties (Ратификација на меѓународни договори), 11=Citizen initiative (Граѓанска иницијатива), 13=President responsibility proposal (Предлог за одговорност на Президент), 14=Government confidence (Доверба во Влада), 15=Government resignation (Оставка на Влада), 16=Government member dismissal (Отказ на член на Влада), 17=MP mandate termination (Прекин на мандат на пратеник), 18=Draft strategy (Предлог на стратегија), 19=Spatial plan proposal (Предлог на просторен план), 20=Public office holder resignation (Оставка на јавен функционер), 21=Election of working bodies (Избор на работни тела), 22=Public function appointments (Избор/назначување јавни функции), 23=Government confidence question (Прашање за доверба во Влада), 24=Other (Останато), 26=Corrections (Исправки), 27=Amendment proposal (Предлог за амандман), 28=Analyses/reports/information (Анализи/извештаи/информации), 29=Constitution amendment proposal (Предлог за измена на Устав), 30=Constitutional bill adoption (Усвојување на уставен предлог), 31=Permanent working bodies (Формирање трајни работни тела), 32=Budget final account (Завршен налог на буџетот), 33=Constitutional bill for amendments (Уставен предлог за спроведување амандмани), 34=Constitutional amendments proposal (Предлог за измена на Устав), 35=Constitutional amendments adoption (Усвојување на измени на Устав), 36=Constitutional amendments proclamation (Прокламирање на измени на Устав), 37=Government member appointment (Назначување член на Влада). Note: IDs 12 and 25 are not present in enumeration (gap in sequence)."
  },
  "StatusGroupId": {
    "enum": [6, 9, 10, 11, 12, 24, 64],
    "description": "6=Delivered to MPs (Доставен до пратеници), 9=First reading (Прво читање), 10=Second reading (Второ читање), 11=Third reading (Трето читање), 12=Finalized (Финализирано), 24=Rejected (Одбиен), 64=Committee processing (Обработка кај комисија)"
  },
  "EventTypeId": {
    "enum": [5],
    "description": "Event type classification. 5=Press conference/visit/general event (observed values; other types may exist)"
  },
  "RoleId": {
    "enum": [1, 6, 7, 10, 11, 26, 27, 72, 82, 83],
    "description": "1=MP (Пратеник/Пратеничка), 6=Committee President, 7=Committee Member, 10=Approver, 11=Committee Advisor, 26=Coordinator/Coordinator of political party, 27=Political party member (Член/Членка на политичка партија), 72=Deputy Coordinator/Deputy coordinator of political party, 82=Committee Vice President, 83=Deputy Member (Заменик-член/Заменик-членка)"
  },
  "CommitteeRoleId": {
    "enum": [6, 7, 10, 11, 82],
    "description": "6=Committee chair, 7=Committee member, 10=Approver, 11=Committee advisor, 82=Deputy chair"
  },
  "MPsClubRoleId": {
    "enum": [78, 79, 81],
    "description": "78=President/Chairperson (Претседател/Претседателка), 79=Vice-President (Заменик-претседател/Заменик-претседателка), 81=Member (Член/Членка)"
  },
  "SittingTypeId": {
    "description": "1=Plenary sitting (Пленарна седница), 2=Committee sitting (Комsissка седница)"
  },
  "DocumentTypeId": {
    "enum": [1, 7, 8, 9, 30, 46, 52, 65],
    "description": "1=Document, 7=Full text of material (Целосен текст на материјалот), 8=Adopted act (Донесен акт), 9=Notification to MPs about new material (Известување за нов материјал до пратеници), 30=Committee report without approval, 46=Legal-Legislative Committee report (Извештај од Законодавно-правна комисија), 52=Report/Committee report (Извештај), 65=Supplemented draft law (Дополнет предлог закон)"
  },
  "AgendaObjectTypeId": {
    "enum": [0, 1, 4],
    "description": "0=No object, 1=Material, 4=Parliamentary questions/other agenda item"
  },
  "AgendaItemStatusId": {
    "enum": [0, 50, 69],
    "description": "0=Unknown/not started, 50=Reviewed (Разгледана), 69=New (Нова)"
  },
  "TreeItemType": {
    "enum": ["ROOT", "LEAF"],
    "description": "ROOT=Agenda container node, LEAF=Individual agenda item"
  }
}
```

## Common patterns
- **Institutional authors**: `Authors[].Id` = `"00000000-0000-0000-0000-000000000000"` with full name/title in `FirstName`, empty `LastName`. Used for government, committees, other institutions.
- **Plenary vs committee**: `CommitteeId`/`CommitteeTitle` are `null` for plenary (`TypeId`/`SittingTypeId` 1); populated for committee (2).
- **ResponsibleCommittee**: Can be empty string `""` for some material types (e.g. appointments, resignations, certain decisions). For materials without committee assignment, is empty string rather than null.
- **Multi-language support in filter operations**: Operations like GetAllMaterialsForPublicPortal return localized text (TypeTitle, StatusGroupTitle, ProposerTypeTitle, ResponsibleCommittee, Author names) based on `LanguageId`. Same material IDs return different language content.
- **Institutional authors in Cyrillic**: Even when `LanguageId=2` (Albanian) or other non-Macedonian language, institutional `ResponsibleAuthor` field may contain Cyrillic text (e.g. "д-р Христијан Мицкоски", "м-р Гордана Димитриеска - Кочоска, министер за финансии"), while other fields use the requested language.
- **Empty ResponsibleCommittee for certain material types**: Materials like government proposals for appointments, resignations, and certain decisions may have `ResponsibleCommittee: ""` (empty string) even when processed/delivered.
- **Multi-language support in filter operations**: Operations like GetAllMaterialsForPublicPortal return localized text (TypeTitle, StatusGroupTitle, ProposerTypeTitle, ResponsibleCommittee, Author names) based on `LanguageId`. Same material IDs return different language content. Similarly, GetAllQuestions returns localized field values (StatusTitle, QuestionTypeTitle, From, To, ToInstitution) in the requested language.
- **Question types**: Parliamentary questions can be written (Писмено прашање) or oral (Усно прашање), indicated by QuestionTypeTitle in response.
- **Questions across parliamentary terms**: GetAllQuestions accepts `StructureId: null` to query questions across all parliamentary terms/structures, not limited to current term.
---
- **Multiple committee review**: Materials may be reviewed by multiple committees. `IsResponsible: true` indicates the responsible committee; `IsLegislative: true` indicates legislative review committee (typically "Законодавно-правна комисија").
- **Reading stages**: `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings` track material progress. Each contains sitting objects with `SittingTypeId` (1=plenary, 2=committee), `StatusGroupId`, and `ObjectStatusId` (both 9 = completed).
- **Document truncation**: API may truncate large arrays (indicated by `"_truncated": 1` in response). Full document list may require separate calls or pagination.
- **Agenda tree structure**: Agenda uses hierarchical tree with `type: "ROOT"` at root level and `type: "LEAF"` for actual agenda items in `children[]`. Leaf nodes may reference materials via `objectId`/`objectTypeId`.
- **Multilingual agenda text**: Some fields like `afterText` in agenda items may contain XML-like language tags (e.g. `<MK>...</><AL>...</><EN>...</><FR>...</>`) for multilingual content.
- **Absents array truncation**: The Absents array may be truncated by the API with an object containing `_truncated` property indicating number of omitted entries.
- **Empty arrays vs null**: Most collections return empty array `[]` (MediaLinks, Attendances, Votings, Continuations, Documents) when empty. Some operations return `null` for Items when `TotalItems: 0`.
- **PoliticalParty nullable**: In Absents array, `PoliticalParty` can be `null` for independent MPs or those without current party affiliation.

## Common request filters
- **Page / Rows** — Pagination: `Page` is which page of results to return (1-based), `Rows` is number of items per page (e.g. 7, 15)
- **TypeId** — In GetAllSittings context: `1` = Plenary sittings, `2` = Committee sittings
- **StatusId** — In GetAllSittings context: `2` = Started sittings (from SittingStatusId enum). Filter sittings by status (see SittingStatusId enum). Set to `null` to include all statuses.
- **CommitteeId** — UUID of committee to filter by. Use with `TypeId: 2` for committee sittings. Set to `null` for plenary sittings or to include all committees.
- **StructureId** — UUID of parliamentary term/structure. Required in most operations. Obtain from GetAllStructuresForFilter. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. In GetAllCouncils context: filters councils to those active in the specified parliamentary structure/term. In GetAllParliamentaryGroups context: filters parliamentary groups by parliamentary term/structure; required parameter.
- **DateFrom / DateTo** — Filter sittings by date range. Both nullable. Set to `null` to omit date filtering.
- **SessionId / Number** — Filter by specific session ID or sitting number. Both nullable. Set to `null` to omit these filters.
- **languageId** — Requested language for labels and names (1=Macedonian, 2=Albanian, 3=Turkish). Note: In `GetAllInstitutionsForFilter`, some entries may return text in Macedonian regardless of the requested language, indicating incomplete localization. Some catalog operations (e.g. `GetAllProcedureTypes`) may also ignore this parameter and return Macedonian text regardless of the requested language.
- **ItemsPerPage / CurrentPage** — Pagination variant used by GetAllMaterialsForPublicPortal: `ItemsPerPage` is number of items per page (e.g. 5, 9, 15, 31, 46), `CurrentPage` is which page to return (1-based). Functionally equivalent to `Rows` and `Page` but naming varies by operation.
- **SearchText** — Free-text search filter for material title/content. Set to empty string `""` to omit. In GetAllMaterialsForPublicPortal context: searches in material titles and content.
- **AuthorText** — Filter materials by author name (free text). Set to empty string `""` to omit.
- **ActNumber** — Filter by act/law number. Set to empty string `""` to omit.
- **StatusGroupId** — Filter materials by status group (corresponds to MaterialStatusId enum). Set to `null` to include all status groups. Related to MaterialStatusId but represents aggregated status categories. In GetAllMaterialsForPublicPortal context: filters materials by processing stage/phase.
- **MaterialTypeId** — Filter by material type (from GetAllMaterialTypesForFilter). Set to `null` to include all material types. Common types include: `1` = standard legislative material/laws, `28` = analyses/reports/information/other materials, and various types for elections/appointments, reports, resignations. In GetAllMaterialsForPublicPortal context: `1` corresponds to law proposals (законски предлози/projektligji).
- **ResponsibleCommitteeId** — UUID of responsible committee. Set to `null` to include all committees.
- **CoReportingCommittees** — Filter by co-reporting committees. Set to `null` to omit.
- **OpinionCommittees** — Filter by opinion committees. Set to `null` to omit.
- **RegistrationNumber** — Filter by exact registration number (e.g. "08-750/1"). Set to `null` to omit.
- **EUCompatible** — Filter by EU compatibility flag. Set to `null` to include both compatible and non-compatible materials. `true` = EU-compatible only, `false` = non-compatible only.
- **ProcedureTypeId** — Filter by procedure type (see ProcedureTypeId enum: 1=Regular, 2=Shortened, 3=Urgent). Set to `null` to include all procedure types.
- **InitiatorTypeId** — Filter by initiator/proposer type (see ProposerTypeId enum). Set to `null` to include all initiator types.
- **Month** — Integer (1–12) specifying the month for which to retrieve agenda items. Used in GetMonthlyAgenda.
- **Year** — Four-digit integer specifying the year for which to retrieve agenda items. Used in GetMonthlyAgenda.
- **TypeId** — In GetAllSittings context: `1` = Plenary sittings, `2` = Committee sittings. Set to `null` to include both types or omit type filtering.
- **StatusId** — In GetAllSittings context: `2` = Started sittings (from SittingStatusId enum). Filter sittings by status (see SittingStatusId enum). Set to `null` to include all statuses. In GetAllQuestions context: filter by question status (see QuestionStatusId enum: 17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Set to `null` to include all statuses.
- **CommitteeId** — UUID of committee to filter by. Use with `TypeId: 2` for committee sittings. Set to `null` for plenary sittings or to include all committees. In GetAllQuestions context: filter questions by committee. Set to `null` to include all committees.
- **StructureId** — UUID of parliamentary term/structure. Can be set to `null` to query across all parliamentary terms/structures (returns broader historical dataset). When specified, obtain from GetAllStructuresForFilter. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. In GetAllCouncils context: filters councils to those active in the specified parliamentary structure/term. In GetAllParliamentaryGroups context: filters parliamentary groups by parliamentary term/structure. In GetAllQuestions context: can be `null` to query across all parliamentary terms/structures.
- **DateFrom / DateTo** — Filter sittings or questions by date range. Both nullable. Set to `null` to omit date filtering. In GetAllQuestions context: filters by DateAsked.
- **languageId** — Requested language for labels and names (1=Macedonian, 2=Albanian, 3=Turkish). Note: In `GetAllInstitutionsForFilter`, some entries may return text in Macedonian regardless of the requested language, indicating incomplete localization. Some catalog operations (e.g. `GetAllProcedureTypes`) may also ignore this parameter and return Macedonian text regardless of the requested language. Some operations accept both `languageId` (lowercase) and `LanguageId` (capitalized); check per-operation notes.
- **SearchText** — Free-text search filter for material or question content. Set to empty string `""` to disable text filtering. In GetAllMaterialsForPublicPortal context: searches in material titles and content. In GetAllQuestions context: searches question titles and content.
- **RegistrationNumber** — Filter by exact registration number (e.g. "08-750/1") or by registration number (varies by operation context). Set to `null` or empty string `""` to omit. In GetAllMaterialsForPublicPortal context: filters by material registration number. In GetAllQuestions context: filters by question registration number.
- **From / To** — Text filters for author/recipient names. Set to empty string `""` to omit. In GetAllMaterialsForPublicPortal context: `AuthorText` filters by author name. In GetAllQuestions context: `From` filters by question author name, `To` filters by recipient name (distinct from DateFrom/DateTo).
- **CurrentPage** — Appears alongside `Page` in some operations (e.g., GetAllQuestions). Purpose may be redundant or legacy; typically set to same value as `Page`.
- **Language** — Used in ASMX endpoints (e.g., GetCustomEventsCalendar). LanguageId (1=Macedonian, 2=Albanian, 3=Turkish). Affects language of localized response fields (EventDescription, EventLocation, etc.).
- **Month** — Calendar month (1-12) to retrieve events for (in GetCustomEventsCalendar context).
- **Year** — Four-digit calendar year to retrieve events for (in GetCustomEventsCalendar context).
- **StructureId** — UUID of parliamentary term/structure. Required in most operations. Obtain from GetAllStructuresForFilter. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. In GetAllCouncils context: filters councils to those active in the specified parliamentary structure/term. In GetAllParliamentaryGroups context: filters parliamentary groups by parliamentary term/structure; required parameter. In GetAllQuestions context: can be `null` to query across all parliamentary terms/structures. In GetParliamentMPsNoImage context: when `null`, returns empty MP lists but Statistics object may still be populated with global counts; provide valid StructureId to retrieve MP data.
- **SearchText** — Free-text search filter for material title/content. Set to empty string `""` to omit. In GetAllMaterialsForPublicPortal context: searches in material titles and content. In GetParliamentMPsNoImage context: text search for MP names. Set to `null` for no text filtering.
- **RegistrationNumber** — Filter by exact registration number (e.g. "08-750/1"). Set to `null` to omit. In GetAllMaterialsForPublicPortal context: filters by material registration number. In GetAllQuestions context: filters by question registration number.
- **genderId** — Filter MPs by gender (see GenderId enum: 1=Male, 2=Female). Set to `null` to include all genders. In GetParliamentMPsNoImage context: filters the returned MP lists by gender.
- **ageFrom / ageTo** — Filter MPs by age range. Both nullable. Set to `null` to omit age filtering. In GetParliamentMPsNoImage context: filters MPs by age.
- **politicalPartyId** — UUID of political party to filter MPs. Set to `null` to include all parties. In GetParliamentMPsNoImage context: returns only MPs belonging to the specified party when provided.
- **coalition** — Filter by coalition affiliation. String filter. Can be empty string `""` when not filtering. In GetParliamentMPsNoImage context: usage unclear from available samples.
- **constituency** — Filter by electoral constituency. String filter. Can be empty string `""` when not filtering. In GetParliamentMPsNoImage context: usage unclear from available samples.
- **languageId** — Requested language for labels and names (1=Macedonian, 2=Albanian, 3=Turkish). Note: In `GetAllInstitutionsForFilter`, some entries may return text in Macedonian regardless of the requested language, indicating incomplete localization.
- **languageId** — Requested language for labels and names (1=Macedonian, 2=Albanian, 3=Turkish). Note: In `GetAllInstitutionsForFilter`, some entries may return text in Macedonian regardless of the requested language, indicating incomplete localization. Some operations accept both `languageId` (lowercase) and `LanguageId` (capitalized); check per-operation notes.
- **Page / Rows** — Pagination: `Page` is which page of results to return (1-based), `Rows` is number of items per page (e.g. 6, 7, 10, 12, 14, 18, 15)
- **StructureId** — UUID of parliamentary term/structure. Required in most operations. Obtain from GetAllStructuresForFilter. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. In GetAllCouncils context: filters councils to those active in the specified parliamentary structure/term. In GetAllParliamentaryGroups context: filters parliamentary groups by parliamentary term/structure; required parameter. In GetAllQuestions context: can be `null` to query across all parliamentary terms/structures.
- **RegistrationNumber** — Filter by registration number. Set to empty string `""` to omit. In GetAllMaterialsForPublicPortal context: filters by material registration number. In GetAllQuestions context: filters by question registration number.
- **Page / Rows** — Pagination: `Page` is which page of results to return (1-based), `Rows` is number of items per page (e.g. 6, 7, 10, 12, 14, 15, 18).
- **TypeId** — In GetAllSittings context: `1` = Plenary sittings, `2` = Committee sittings.
- **StatusId** — In GetAllSittings context: Filter sittings by status (see SittingStatusId enum: 1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed). Set to `null` to include all statuses. In GetAllQuestions context: filter by question status (see QuestionStatusId enum: 17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Set to `null` to include all statuses.
- **SearchText** — Free-text search filter for material title/content. Set to empty string `""` to omit. In GetAllMaterialsForPublicPortal context: searches in material titles and content. In GetAllQuestions context: searches question titles and content.
- **RegistrationNumber** — Filter by exact registration number (e.g. "08-750/1"). Set to `null` to omit. In GetAllQuestions context: filters by question registration number.
- **AmendmentsPage / AmendmentsRows** — Pagination for amendments. When omitted or when AmendmentsTotalRows is 0, amendment arrays (FirstReadingAmendments, SecondReadingAmendments) return empty arrays.
- **QuestionId** — UUID of the parliamentary question to retrieve details for. Obtained from `GetAllQuestions` Items[].Id.
- **SittingId** — UUID of the sitting to retrieve. Obtained from `GetAllSittings` response (`Items[].Id`). Required for `GetSittingDetails`.

## Common response keys
- **TotalItems** — Total count of items matching filter. When `TotalItems: 0`, the `Items` array becomes `null` rather than an empty array `[]`. For paginated results, represents the full total across all pages, not just the current page.
- **Items** — Array of result items, or `null` when no results match. When paginated, contains only the subset for the requested page.
- **d** — ASMX-wrapped responses contain results in this property
- **_truncated** — When present in array items, indicates N additional items were omitted from the array but exist in full data. Appears as an integer value indicating the count of truncated items.
- **Id** — Identifier; context-dependent meaning. In `GetAllGenders`: numeric gender identifier (1=Male, 2=Female). In `GetAllApplicationTypes`: numeric identifier for the application type. In `GetAllProcedureTypes`: numeric identifier for the procedure type (1=Regular, 2=Shortened, 3=Urgent). In other catalog endpoints: UUID or numeric identifier for the catalog item. Use this value in filter parameters of other operations. In `GetAllInstitutionsForFilter`: UUID of the institution (ministry, government body, etc.). In GetAllMaterialsForPublicPortal materials: UUID of the material. In `GetAllStructuresForFilter`: UUID identifying the parliamentary term/structure. The structure with `IsCurrent: true` is typically used as the default StructureId in other operations. In GetMonthlyAgenda: UUID of the agenda item/sitting.
- **Title** — Human-readable label. In catalog endpoints like `GetAllGenders`: localized label in the requested language (controlled by `languageId`). In `GetAllProcedureTypes`: procedure type name (may return Macedonian regardless of requested language). In `GetAllMaterialTypesForFilter`: human-readable name of the material type in the requested language; may contain leading/trailing whitespace characters (`\r`, `\n`) requiring trimming. In `GetAllMaterialStatusesForFilter`: human-readable status name (e.g., "Доставен до пратеници", "Прво читање"). In `GetAllInstitutionsForFilter`: official name of the institution (ministry, government body, etc.) in the requested language; may be incomplete translations returning Macedonian despite other language requests. In GetMonthlyAgenda: full descriptive title of the scheduled event, includes sitting number, committee/body name, and location. In other contexts, provides descriptive text for the item.
- **ApplicationTitle** — Human-readable name of the application type in the requested language (from `GetAllApplicationTypes`)
- **Name** — Human-readable name or title. Context-specific: in `GetAllParliamentaryGroups`, the full official name of the parliamentary group (e.g., "Пратеничка група на партијата „Движење ЗНАМ - За наша Македонија""); in `GetAllMPsClubsByStructure`, the full name of the MPs club or inter-party parliamentary group in the requested language; in GetParliamentaryGroupDetails context: the official name of the parliamentary group in the requested language; in other endpoints may represent party name, material title, committee name, or other entity names.
- **NumberOfDeputies** — Count of MPs/deputies in a parliamentary group (from `GetAllParliamentaryGroups`). Reflects current composition; totals across all groups may not equal total MPs if there are independents or vacancies.
- **Image** — Image identifier, URL, path, or base64-encoded image data. May be empty string `""` when no image is available. Context-specific: in `GetAllParliamentaryGroups`, image/logo for the parliamentary group; in `GetUserDetailsByStructure`, base64-encoded profile image.
- **TypeId / TypeTitle** — Numeric identifier and localized label for entity type. In council contexts, TypeId indicates council permanence type (see CouncilTypeId), TypeTitle provides the human-readable label (e.g. "Постојана" = Permanent).
- **RegistrationNumber** — Official registration number in format "XX-XXX/X" (e.g. "08-676/1"). Unique identifier for tracking materials through the legislative process. In GetAllMaterialsForPublicPortal context: material registration identifier in format like "08-750/1", "08-722/1".
- **RegistrationDate** — Date when material was registered, in AspDate format. In GetAllMaterialsForPublicPortal context: date material was registered.
- **ResponsibleAuthor** — Primary author name(s). For institutional authors (government ministers), contains full title. For MP authors, contains first and last name. In GetAllMaterialsForPublicPortal context: primary/first author name as display string; may be institutional (government minister title in Cyrillic) or individual MP name. Can be `null` when no responsible author designated.
- **TypeTitle** — Human-readable title of the material type in the requested language (e.g. "Предлог закон" for proposed law, "Анализи, извештаи, информации и друг материјал" for analyses/reports/information/other materials). In GetAllMaterialsForPublicPortal context: material type name as displayed string; may have leading whitespace (e.g. `\r\n`).
- **StatusGroupTitle** — Human-readable status of the material (e.g. "Прво читање" = First reading, "Второ читање" = Second reading, "Затворен" = Closed). In GetAllMaterialsForPublicPortal context: material status group/phase in the requested language (e.g. "Доставен до пратеници" = Delivered to MPs, "Leximi i parë" in Albanian).
- **ProposerTypeTitle** — Human-readable proposer type (e.g. "Влада на Република België Македонија" = Government, "Пратеник" = MP). In GetAllMaterialsForPublicPortal context: human-readable proposer type in requested language (e.g. "Qeveria e Republikës së Maqedonisë Veriore" in Albanian, "Trupi punues" for working body).
- **ResponsibleCommittee** — Name of the committee responsible for processing the material. In GetAllMaterialsForPublicPortal context: name of responsible parliamentary committee in requested language; can be empty string `""` for material types without committee assignment (appointments, resignations, certain decisions).
- **EUCompatible** — Boolean indicating EU compatibility status. Always present (not nullable) in GetAllMaterialsForPublicPortal context.
- **Authors** — Array of author objects. In GetAllMaterialsForPublicPortal context: contains mix of individual MPs (with real UUIDs, FirstName, LastName) and institutional authors (zero UUID `"00000000-0000-0000-0000-000000000000"` with full institution name in FirstName, empty LastName). Array can be empty `[]` for certain proposer types. Each author has `Id` (UUID), `FirstName` (string), `LastName` (string) properties.
- **DateFrom / DateTo** — Start and end dates of an item's period or validity. In `GetAllStructuresForFilter` context: AspDate format timestamps marking the start and end dates of a parliamentary term/structure. Current term's DateTo may be set far in the future.
- **IsCurrent** — Boolean flag indicating whether this is the current/active item. In `GetAllStructuresForFilter`: marks the active parliamentary term (`IsCurrent: true`). Only one structure should have this flag set to `true` at any given time.
- **Location** — Physical location/room where the sitting or meeting will take place (e.g. "Сала 4", "Сала „Македонија""). In GetMonthlyAgenda context: the physical location/hall where the sitting will occur.
- **Start** — Start date/time of an agenda item, sitting, or event. In GetMonthlyAgenda context: AspDate format timestamp indicating when the agenda item begins. In other contexts, may represent start date/time of the associated entity.
- **Type** — Context-dependent type identifier. In GetMonthlyAgenda context: AgendaItemTypeId (1=Plenary, 2=Committee) indicating the type of sitting.
- **From** — Author/originator name. In GetAllQuestions Items: name of the MP who submitted the question. In GetUserDetailsByStructure: name of the MP who submitted the question.
- **To** — Recipient name/title. In GetAllQuestions Items: title/position of the official or minister to whom the question is directed (e.g., "Министерот за внатрешни работи"). In GetUserDetailsByStructure: title/position of the official or minister to whom the question is directed.
- **ToInstitution** — Institution name of the recipient. In GetAllQuestions Items: full name of the ministry or government body receiving the question (e.g., "Министерство за внатрешни работи"). May contain placeholder values like `"/"` in some datasets (data quality issue).
- **StatusTitle** — Human-readable status label in the requested language. In GetAllMaterialsForPublicPortal context: material status name (e.g., "Доставен до пратеници", "Прво читање"). In GetAllQuestions context: question status (e.g., "Доставено" = Delivered, "Одговорено" = Answered). In GetUserDetailsByStructure context: question status in requested language.
- **DateAsked** — AspDate format timestamp. In GetAllQuestions context: date when question was submitted.
- **DateAnswered** — AspDate format timestamp when a question was answered, or `null` when question has not yet been answered. In GetParliamentaryGroupDetails context: date question was answered.
- **QuestionTypeTitle** — Type of question in the requested language (e.g., "Писмено прашање" = Written question, "Усно прашање" = Oral question). From GetAllQuestions Items. In GetUserDetailsByStructure: type of question in requested language.
- **TotalRows** — Item-level row count field. In GetAllQuestions Items: observed as `0` (purpose unclear; may be legacy or item-specific field).
- **EventDescription** — Human-readable description/title of the calendar event in the requested language (from GetCustomEventsCalendar). Examples: "Прес-конференција за медиуми", "Посета на...", "Давање свечена изјава".
- **EventLink** — URL-friendly slug/path component for the event (from GetCustomEventsCalendar). Suitable for constructing event detail page URLs. Example: "pres-konferencija-za-mediumi-10-12-2024".
- **EventLocation** — Physical location or venue where the event takes place (from GetCustomEventsCalendar). Examples: "Прес-центар", "Охридска сала", "Стар кабинет". May be empty string `""` when location is not specified or not applicable.
- **EventDate** — Timestamp in AspDate format (`/Date(milliseconds)/`) representing the scheduled date/time of the calendar event (from GetCustomEventsCalendar).
- **EventType** — Numeric identifier for the type/category of calendar event (see EventTypeId enum). In GetCustomEventsCalendar context: observed value `5` appears to cover press conferences, official visits, working sessions, commemorations, and public events. Other values may exist but are not yet documented.
- **__type** — Type discriminator in ASMX responses. Contains fully-qualified .NET type name (e.g., "moldova.controls.Models.CalendarViewModel"). Indicates the response object type in ASMX-wrapped endpoints.
- **Number** — Context-dependent sequence number. In GetAllSittings: sitting sequence number within the committee (for `TypeId: 2`) or plenary (for `TypeId: 1`). Each committee maintains its own sequence. When `TypeId: 1` (plenary), represents plenary sitting sequence number.
- **CommitteeTitle** — Localized name of the committee. Present for committee sittings (`TypeId: 2`); typically null for plenary sittings (`TypeId: 1`).
- **Continuations** — Array of continuation sitting references. Empty array when sitting has no continuations. Used when a sitting spans multiple sessions.
- **SittingDate** — Primary date/time of the sitting event (AspDate format).
- **Structure** — Structural metadata field in response items. Typically `null` in list responses. In GetSittingDetails context: human-readable parliamentary term/period name (e.g., "2024-2028").
- **CompositionMembers** — Array of council composition members (official MPs and their roles within the council). See GetCouncilDetails for usage.
- **SecretariatMembers** — Array of secretariat/administrative staff supporting the council/committee, with their roles (e.g., Approvers, Advisors). May contain duplicate UserId entries with different RoleId values (same person holding multiple roles).
- **Materials** — Array of materials associated with council/committee or user/MP. May be empty array `[]` when no materials exist.
- **Meetings** — Array of council/committee meeting/sitting records with date, location, and sitting number.
- **Description** — HTML-formatted description or detailed text. Context-specific: in GetCouncilDetails, describes the council's mandate and responsibilities; may contain HTML markup including paragraphs, links, and styling. In GetUserDetailsByStructure, HTML-formatted biography text with inline `<span>` tags. In other contexts, may contain empty `<p><br/></p>` tags.
- **Email** — Contact email address. Context-specific: in GetCouncilDetails, official email for the council. In GetUserDetailsByStructure, official parliamentary email in format FirstInitial.LastName@sobranie.mk.
- **PhoneNumber** — Contact phone number. Nullable (can be `null` when not provided).
- **SittingNumber** — Sequential number of the sitting/meeting within the council/committee.
- **RoleId** — Committee/council member role identifier. See RoleId enum for values (1=MP, 6=President, 7=Member, 10=Approver, 11=Advisor, 26=Coordinator of political party, 27=Political party member, 72=Deputy coordinator of political party, 82=Vice President, 83=Deputy Member). In GetUserDetailsByStructure context: MP's primary role in parliament (e.g., 1 = MP).
- **RoleTitle** — Localized human-readable role name corresponding to RoleId (e.g., "Претседател/Претседателка на комисија" for President, "Член/Членка на комисија" for Member, "Одобрувач/Одобрувачка" for Approver, "Советник/Советничка на комисија" for Advisor, "Заменик-претседател/Заменик-претседателка на комисија" for Vice President). In GetUserDetailsByStructure context: localized role title (e.g., "Пратеник/Пратеничка" for MP).
- **FullName** — Full name of a person (format: "FirstName LastName"). In GetCouncilDetails context: name of council/committee member or secretariat staff. In GetUserDetailsByStructure context: name of the MP.
- **UserId** — UUID identifier for a user/person in the system. In GetCouncilDetails context: identifier for council member or secretariat staff. Can appear multiple times in the same array with different RoleId values when a person holds multiple roles. In GetUserDetailsByStructure context: identifier for the MP.
- **_truncated** — When present in documentation examples, indicates N additional items were omitted from the example but exist in the full API response.
- **Items** — Array of result items, or `null` when no results match. When paginated, contains only the subset for the requested page. Can also be empty array `[]` when `TotalItems: 0` depending on operation.
- **d** — In ASMX-wrapped responses (e.g., GetCustomEventsCalendar, GetOfficialVisitsForUser), contains the full response array/object. Unlike paginated responses that wrap results in `Items`/`TotalItems`, ASMX responses place results directly in `d` as an array of items. May be empty array `[]` when no results exist.
- **MembersOfParliament** — Array of MPs with active mandate in the specified structure. Returns empty array `[]` when no results (from GetParliamentMPsNoImage).
- **ExpiredMandateMembers** — Array of MPs whose mandate has expired in the specified structure. Returns empty array `[]` when no results (from GetParliamentMPsNoImage).
- **TotalItemsExpiredMandate** — Total count of MPs with expired mandates. Returns `0` when no expired mandate MPs exist or when StructureId is null.
- **Statistics** — Object containing aggregate counts across the system or filtered dataset. May include `TotalNumberOfMaterials`, `NumberOfQuestions`, `TotalNumberOfMPs`, `TotalNumberOfExpiredMandateMPs`, `MPsInPoliticalParties`, `MPsInParliamentaryGroups`, `NumberOfMaterialsInStructure`. From GetParliamentMPsNoImage context: some statistics are global (e.g., `TotalNumberOfMaterials`) and may be populated even when other results are empty; others reflect the filtered result set.
- **PoliticalPartyTitle** — Human-readable name of a political party. In GetParliamentMPsNoImage context: name of the MP's political party. In GetUserDetailsByStructure context: name of the MP's political party.
- **PoliticalPartyId** — UUID of a political party. In GetParliamentMPsNoImage context: party identifier for the MP's affiliated party. In GetUserDetailsByStructure context: party identifier for the MP's affiliated party.
- **UserImg** — Base64-encoded image data for the user/MP's photo. In GetParliamentMPsNoImage context: despite the operation name "NoImage", this field contains base64-encoded image data for each MP. Field is populated with actual image data, not null or empty.
- **Gender** — Gender as text representation. In GetUserDetailsByStructure context: "Машки" (Male) or "Женски" (Female) in the requested language, corresponding to GenderId enum (1=Male, 2=Female).
- **DateOfBirth** — Date of birth as string in DD.MM.YYYY format (not AspDate format).
- **Constituency** — Electoral constituency number as string (e.g., "6").
- **Coalition** — Electoral coalition name the MP was elected under (e.g., "Коалиција Твоја Македонија").
- **StructureDate** — Human-readable parliamentary term date range as string (e.g., "2024 - 2028").
- **ElectedFrom** — Start date of the MP's current mandate in AspDate format.
- **ElectedTo** — End date of the MP's mandate in AspDate format, or `null` for current/active mandates.
- **Biography** — HTML-formatted biographical text. May contain inline `<p>` and `<span>` tags with biographical details.
- **Acts** — Array of legislative acts (proposals, laws) associated with the MP. Each item: `{Id, Title, RegistrationDate, RegistrationNumber, StatusId, StatusTitle}`. Empty array `[]` when no acts.
- **Committees** — Array of committee memberships. Each item: `{CommitteeId, CommitteeTitle, Roles[]}` where Roles is array of `{Id, Title}` (e.g., role within committee). Empty array `[]` when no committee memberships.
- **CommitteeMemberships** — Array for committee membership details. Empty array `[]` when no data.
- **DelegationMemberships** — Array for delegation membership details. Empty array `[]` when no data.
- **DepartmentMemberships** — Array for department membership details. Empty array `[]` when no data.
- **FriendshipGroupMemberships** — Array for friendship group membership details. Empty array `[]` when no data.
- **MediaItems** — Array for media items. Empty array `[]` when no data.
- **FriendshipGroups** — Array of friendship group memberships. Each item: `{Id, Title, Description}`. Empty array `[]` when no friendship groups.
- **Amendments** — Array of amendments proposed by the MP. Each item: `{Id, Title, RegistrationDate, RegistrationNumber, StatusId, StatusTitle}`. May be truncated with `"_truncated": N` indicating N additional items. Empty array `[]` when no amendments.
- **Questions** — Array of parliamentary questions submitted by the MP. Each item: `{Id, Title, DateAsked, DateAnswered, StatusId, StatusTitle}`. Empty array `[]` when no questions.
- **CabinetMembers** — Array of cabinet/ministerial positions held by the MP. Empty array `[]` when no cabinet positions.
- **Delegations** — Array of delegation memberships. Empty array `[]` when no delegations.

## See per-operation .md files for detailed request/response schemas and operation-specific notes.


## Common usage notes
- **Pagination style variants**: Some operations use `Page`/`Rows`; others use `ItemsPerPage`/`CurrentPage`. Check per-operation documentation for which pattern applies.
- **Parameter casing**: Some operations use `MethodName`/`LanguageId` (PascalCase); others use `methodName`/`languageId` (camelCase). Some operations accept both casings interchangeably. Check per-operation documentation.
- **Whitespace in type fields**: In GetAllMaterialsForPublicPortal, `TypeTitle` and `ProposerTypeTitle` may include leading `\r\n` characters. Trim appropriately in client code.
- **Cross-language institutional text**: For GetAllMaterialsForPublicPortal: even when requesting Albanian (`LanguageId=2`) or Turkish (`LanguageId=3`), the `ResponsibleAuthor` field for government-proposed materials may contain Cyrillic text (Macedonian minister names/titles). Other fields respect the requested language.
- **Catalog operations language behavior**: Some catalog operations (e.g. `GetAllProcedureTypes`) may return Macedonian labels regardless of the `languageId` parameter. Test with different language IDs to confirm expected localization for critical operations in your application.
- **Catalog operations**: Operations like `GetAllSittingStatuses`, `GetAllGenders`, `GetAllMaterialStatusesForFilter`, etc. return simple arrays of `{Id, Title}` objects where `Id` is the enum value used in filter parameters and `Title` is the human-readable label in the requested language.
- **Language handling in GetAllQuestions**: Response content (Title, From, To, StatusTitle, QuestionTypeTitle, ToInstitution) is returned in the requested `LanguageId` language.
- **Committee member roles**: In GetCommitteeDetails, CompositionMembers contain elected MPs with political roles (chair, vice-chair, members). SecretariatMembers contain administrative/professional staff (advisors, approvers). Same person may appear multiple times in SecretariatMembers with different RoleIds when holding multiple roles.
- **HTML content in descriptions**: Fields like Description in GetCommitteeDetails contain HTML-formatted text with markup. Parse appropriately for display in client applications.
- **Calendar event language handling**: GetCustomEventsCalendar returns localized EventDescription and EventLocation based on the `Language` parameter (1=Macedonian, 2=Albanian, 3=Turkish).
- **HTML content in descriptions**: Fields like Description in GetCommitteeDetails and GetCouncilDetails contain HTML-formatted text with markup. Parse appropriately for display in client applications.
- **Parameter casing**: Some operations use `MethodName`/`LanguageId` (PascalCase); others use `methodName`/`languageId` (camelCase). Check per-operation documentation.
- **Empty arrays vs null for zero results**: Most operations return `null` for `Items` when `TotalItems: 0`. However, some operations (e.g., GetParliamentMPsNoImage) return empty arrays `[]` instead. Check per-operation behavior.
- **Language handling in GetAllQuestions**: Response content (Title, From, To, StatusTitle, QuestionTypeTitle) is returned in the requested `LanguageId` language.
---
- **MPs club member roles**: In GetMPsClubDetails, Members array contains MPs with their roles within the club (78=President/Chair, 79=Vice-President, 81=Member). RoleTitle uses gendered forms separated by slash (e.g., "Претседател/Претседателка" for male/female President). Large member lists may be truncated in response with `_truncated` placeholder.
- **Array truncation in detail endpoints**: Detail endpoints like GetParliamentaryGroupDetails may truncate large arrays (Materials, Amendments, Questions, Members) in their responses. When truncated, these arrays are truncated due to API display limitations, not pagination. The `_truncated` property in array items indicates how many additional items exist beyond those shown.
- **Parliamentary group contact fields**: The `Email` and `Phone` fields for parliamentary groups are typically `null`, as contact is typically directed through individual members rather than the group entity itself.
- **Empty collections in GetQuestionDetails**: Both `Documents` and `Sittings` return empty arrays `[]` rather than `null` when no items are present.
- **Political party details**: GetPoliticalPartyDetails returns array of materials proposed by the party, members list with role information, and summary counts. Amendments and Questions arrays may be empty when party has no associated items. Description may contain placeholder value like "-" when not set.
- **Agenda structure in sittings**: GetSittingDetails returns hierarchical agenda tree with root node containing child items. Use `objectId`/`objectTypeId` in agenda items to reference linked materials.
- **User profile structure**: GetUserDetailsByStructure returns comprehensive MP biographical data, political affiliations, committee memberships, and legislative activities. Arrays (CabinetMembers, Materials, Questions, Delegations, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems) return empty `[]` when no data rather than `null`. Amendments and Acts arrays may be truncated with `_truncated` indicator.

## \$defs
```json
{
  "AspDate": {
    "type": "string",
    "pattern": "^/Date\\(\\d+\\)/$"
  },
  "LanguageId": {
    "type": "integer",
    "description": "1=Macedonian, 2=Albanian, 3=Turkish"
  },
  "GenderId": {
    "enum": [1, 2],
    "description": "1=Male (Машки), 2=Female (Женски)"
  },
  "SittingStatusId": {
    "enum": [1, 2, 3, 4, 5, 6],
    "description": "1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed"
  },
  "AgendaItemTypeId": {
    "description": "1=Plenary, 2=Committee"
  },
  "QuestionStatusId": {
    "enum": [17, 19, 20, 21],
    "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
  },
  "MaterialStatusId": {
    "enum": [0, 6, 9, 10, 11, 12, 24, 64],
    "description": "0=Plenary/unknown, 6=Delivered to MPs, 9=First reading, 10=Second, 11=Third, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "ProposerTypeId": {
    "enum": [1, 2, 4, 5, 6],
    "description": "1=MP (Пратеник), 2=Government (Влада на Република Северна Македонија), 4=Voter group, 5=Working body (Работно тело), 6=Other institution (Друга институција)"
  },
  "ProcedureTypeId": {
    "enum": [1, 2, 3],
    "description": "1=Regular (Редовна постапка), 2=Shortened (Скратена постапка), 3=Urgent (Итна постапка)"
  },
  "ApplicationTypeId": {
    "description": "1=Case report (Пријава на случај / Paraqitja e rastit), 2=Participation in public debate (Учество во јавна расправа / Pjesëmarrje në debatin publik), 3=Discussion (Дискусија / Diskutim)"
  },
  "UUID": {
    "format": "uuid"
  },
  "CouncilTypeId": {
    "enum": [1],
    "description": "1=Permanent (Постојана)"
  },
  "MaterialTypeId": {
    "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "description": "1=Draft law (Предлог закон), 2=Interpellation (Интерпелација), 3=Government election (Избор на Влада), 4=Authentic interpretation (Автентично толкување на закон), 5=Consolidated text (Пречистен текст на закон), 6=Budget (Буџет), 7=Rules of procedure (Деловник), 8=Declaration/resolution/decision/recommendation (Декларација, резолуција, одлука и препорака), 9=Consent to statutes (Согласност на статути и други општи акти), 10=Ratification of international treaties (Ратификација на меѓународни договори), 11=Citizen initiative (Граѓанска иницијатива), 13=President responsibility proposal (Предлог за одговорност на Президент), 14=Government confidence (Доверба во Влада), 15=Government resignation (Оставка на Влада), 16=Government member dismissal (Отказ на член на Влада), 17=MP mandate termination (Прекин на мандат на пратеник), 18=Draft strategy (Предлог на стратегија), 19=Spatial plan proposal (Предлог на просторен план), 20=Public office holder resignation (Оставка на јавен функционер), 21=Election of working bodies (Избор на работни тела), 22=Public function appointments (Избор/назначување јавни функции), 23=Government confidence question (Прашање за доверба во Влада), 24=Other (Останато), 26=Corrections (Исправки), 27=Amendment proposal (Предлог за амандман), 28=Analyses/reports/information (Анализи/извештаи/информации), 29=Constitution amendment proposal (Предлог за измена на Устав), 30=Constitutional bill adoption (Усвојување на уставен предлог), 31=Permanent working bodies (Формирање трајни работни тела), 32=Budget final account (Завршен налог на буџетот), 33=Constitutional bill for amendments (Уставен предлог за спроведување амандмани), 34=Constitutional amendments proposal (Предлог за измена на Устав), 35=Constitutional amendments adoption (Усвојување на измени на Устав), 36=Constitutional amendments proclamation (Прокламирање на измени на Устав), 37=Government member appointment (Назначување член на Влада). Note: IDs 12 and 25 are not present in enumeration (gap in sequence)."
  },
  "StatusGroupId": {
    "enum": [6, 9, 10, 11, 12, 24, 64],
    "description": "6=Delivered to MPs (Доставен до пратеници), 9=First reading (Прво читање), 10=Second reading (Второ читање), 11=Third reading (Трето читање), 12=Finalized (Финализирано), 24=Rejected (Одбиен), 64=Committee processing (Обработка кај комисија)"
  },
  "EventTypeId": {
    "enum": [5],
    "description": "Event type classification. 5=Press conference/visit/general event (observed values; other types may exist)"
  },
  "RoleId": {
    "enum": [1, 6, 7, 10, 11, 26, 27, 72, 82, 83],
    "description": "1=MP (Пратеник/Пратеничка), 6=Committee President, 7=Committee Member, 10=Approver, 11=Committee Advisor, 26=Coordinator/Coordinator of political party, 27=Political party member (Член/Членка на политичка партија), 72=Deputy Coordinator/Deputy coordinator of political party, 82=Committee Vice President, 83=Deputy Member (Заменик-член/Заменик-членка)"
  },
  "CommitteeRoleId": {
    "enum": [6, 7, 10, 11, 82],
    "description": "6=Committee chair, 7=Committee member, 10=Approver, 11=Committee advisor, 82=Deputy chair"
  },
  "MPsClubRoleId": {
    "enum": [78, 79, 81],
    "description": "78=President/Chairperson (Претседател/Претседателка), 79=Vice-President (Заменик-претседател/Заменик-претседателка), 81=Member (Член/Членка)"
  },
  "SittingTypeId": {
    "description": "1=Plenary sitting (Пленарна седница), 2=Committee sitting (Комsissка седница)"
  },
  "DocumentTypeId": {
    "enum": [1, 7, 8, 9, 30, 46, 52, 65],
    "description": "1=Document, 7=Full text of material (Целосен текст на материјалот), 8=Adopted act (Донесен акт), 9=Notification to MPs about new material (Известување за нов материјал до пратеници), 30=Committee report without approval, 46=Legal-Legislative Committee report (Извештај од Законодавно-правна комисија), 52=Report/Committee report (Извештај), 65=Supplemented draft law (Дополнет предлог закон)"
  },
  "AgendaObjectTypeId": {
    "enum": [0, 1, 4],
    "description": "0=No object, 1=Material, 4=Parliamentary questions/other agenda item"
  },
  "AgendaItemStatusId": {
    "enum": [0, 50, 69],
    "description": "0=Unknown/not started, 50=Reviewed (Разгледана), 69=New (Нова)"
  },
  "TreeItemType": {
    "enum": ["ROOT", "LEAF"],
    "description": "ROOT=Agenda container node, LEAF=Individual agenda item"
  }
}
```

## Per-operation reference
See per-operation .md files for detailed request/response schemas and operation-specific notes.

---

## GetAllApplicationTypes

### Notes
Returns all application types available in the system.

**Usage:**
- Use to populate dropdowns or filters for application-related operations
- languageId determines the language of ApplicationTitle (1=Macedonian, 2=Albanian, 3=Turkish)

**Language fallback behavior:**
- When `languageId=3` (Turkish), the API may return English labels instead of Turkish translations, indicating fallback behavior for incomplete localizations.

**Known application types by languageId:**
- **languageId=1 (Macedonian):**
  - 1: "Пријава на случај" (Case report)
  - 2: "Учество во јавна расправа" (Participation in public discussion)
  - 3: "Дискусија" (Discussion)
- **languageId=2 (Albanian):**
  - 1: "Paraqitja e rastit" (Case report)
  - 2: "Pjesëmarrje në debatin publik" (Participation in public discussion)
  - 3: "Diskutim" (Discussion)
- **languageId=3 (Turkish - returns English fallback):**
  - 1: "Case report"
  - 2: "Participation in Public Debate"
  - 3: "Discussion"

**Response:**
- Returns array of application types with Id and localized ApplicationTitle

### Request
```json
{
  "methodName": "GetAllApplicationTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "ApplicationTitle": {
        "type": "string"
      }
    },
    "required": ["Id", "ApplicationTitle"]
  }
}
```

---

## GetAllCommitteesForFilter

### Request
```json
{
  "methodName": "GetAllCommitteesForFilter",
  "languageId": 1,
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

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
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure UUID. Determine which set of committees to return (committees vary by parliamentary term/structure). Obtain from GetAllStructuresForFilter."
    }
  },
  "required": ["methodName", "languageId", "structureId"]
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string",
        "description": "Committee name in requested language"
      }
    },
    "required": ["Id", "Name"]
  }
}
```

### Per-operation Notes
- **Purpose**: Returns all committees active within the specified parliamentary structure/term
- **Response format**: Direct array (not paginated, no TotalItems wrapper)
- **Language**: Committee names are returned in the language specified by `languageId`
- **Usage**: Use the returned `Id` values as `CommitteeId` filter in GetAllSittings (with `TypeId: 2` for committee sittings) or as `committeeId` parameter in GetCommitteeDetails
- **Typical count**: Current structure (5e00dbd6-ca3c-4d97-b748-f792b2fa3473) returns 27+ committees; count varies by parliamentary term

---

## GetAllCouncils

### Request
```json
{
  "methodName": "GetAllCouncils",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

#### Request parameters
- **StructureId** (UUID, required): Parliamentary term/structure. Obtain from `GetAllStructuresForFilter`. Common current value: `5e00dbd6-ca3c-4d97-b748-f792b2fa3473`. Filters councils to those active in the specified structure/term.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Name", "TypeId", "TypeTitle"],
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "Unique identifier for the council"
      },
      "Name": {
        "type": "string",
        "description": "Council name in the requested language"
      },
      "TypeId": {
        "type": "integer",
        "enum": [1],
        "description": "Council type. See CouncilTypeId in $defs. 1=Permanent (Постојана)"
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
- **Response format**: Returns a flat array of councils (not wrapped in TotalItems/Items structure).
- **Council types**: Currently only type 1 (Permanent/Постојана) observed in sample data. Other types may exist in different structures or future parliamentary terms.
- **Usage**: Council IDs returned in this operation can be used with `GetCouncilDetails` to retrieve detailed information about a specific council.
- **StructureId required**: Operation requires a valid parliamentary term/structure ID to filter results appropriately.

---

## GetAllGenders

### Request
```json
{
  "methodName": "GetAllGenders",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "type": "integer",
        "enum": [1, 2],
        "description": "1=Male (Машки), 2=Female (Женски)"
      },
      "Title": {
        "type": "string",
        "description": "Localized gender name"
      }
    }
  }
}
```

### Notes
- Returns exactly 2 items: Male (Id=1) and Female (Id=2)
- Response is a direct array (not wrapped in object with TotalItems/Items)
- `Title` values are localized per the `languageId` request parameter. For languageId=1 (Macedonian): "Машки" (Male), "Женски" (Female)
- Use `Id` values (1 or 2) as filter input in `GetParliamentMPsNoImage` and other operations requiring gender selection
- Reference data: always returns the same 2 entries, no pagination

---

## GetAllInstitutionsForFilter

### Description
Returns list of institutions (ministries, government bodies). Includes historical and current entities. Contains placeholder records with Title `"/"` or `"-"` that should be filtered. Turkish localization (`languageId: 3`) returns Macedonian text, indicating incomplete translation coverage.

### Request
```json
{
  "methodName": "GetAllInstitutionsForFilter",
  "languageId": 1
}
```

### Request notes
- **languageId** accepts values 1 (Macedonian), 2 (Albanian), or 3 (Turkish). However, responses for `languageId: 3` (Turkish) currently return Macedonian text for institution titles, suggesting incomplete Turkish localization.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "Unique identifier for the institution (UUID)"
      },
      "Title": {
        "type": "string",
        "description": "Institution name (e.g., ministry) in the requested language. May contain placeholder values '/' or '-' for invalid/legacy entries."
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- **Data quality**: Response includes placeholder entries with `Title: "/"` or `Title: "-"` (examples: UUIDs `eb0e5bfd-ee7e-40f2-8cab-322cefd440fd`, `6ebe4c24-98ac-4d4b-99d7-b6d8b10dd1db`, `e48be100-961e-45fa-a53c-c3a73bc6181a`, `4027bbeb-ad05-47b6-a345-f25fdda12e09`, `f7d211f2-6b4b-4ff4-80fa-3a7c8ae97123`, `b9521d21-cb7e-4129-9f15-4bcdf983ce2c`). These are legacy or inactive records. Filter client-side when building UI selectors.
- **Language consistency**: While `languageId` parameter controls the language requested, some institution entries may return text in Macedonian regardless of the requested language due to incomplete translations in the underlying dataset.
- **Usage**: Returns all institutions (ministries, government bodies, state institutions) for use in filters and dropdowns. Common in material/question proposer selection. Use the `Id` value when filtering materials, questions, or other entities by responsible institution.
- **Common institutions**: Response includes entities such as "Министерство за финансии" (Ministry of Finance), "Министерство за образование и наука" (Ministry of Education and Science), "Влада на Република Северна Македонија" (Government of North Macedonia), and both current and historical ministries (e.g., "Министерство за информатичко општество" appears to be historical).


---

## GetAllMPsClubsByStructure

### Description
Returns all MPs clubs (inter-party parliamentary groups) for a specified parliamentary structure/term. These are cross-party groups focused on specific issues such as environmental protection, Roma rights, youth issues, and anti-corruption. The response is not paginated and returns all clubs active in the structure.

### Request
```json
{
  "MethodName": "GetAllMPsClubsByStructure",
  "LanguageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

**Request parameters:**
- **MethodName** — Operation name (required, uses uppercase casing)
- **LanguageId** — Language for entity names (1=Macedonian, 2=Albanian, 3=Turkish). See LanguageId in global docs.
- **StructureId** — UUID of the parliamentary term/structure (required). Obtain from `GetAllStructuresForFilter`. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current term. The operation returns clubs active in this structure.

### Response
```json
{
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
      }
    },
    "required": ["Id", "Name"]
  }
}
```

**Response keys:**
- **Id** — UUID identifier for the MPs club or inter-party parliamentary group
- **Name** — Full name/title of the MPs club in the requested language. May include prefixes such as "Интерпартиска парламентарна група" (inter-party parliamentary group) or "Клуб" (club) followed by the topic or purpose (e.g., "Клуб за животна средина" = Environmental Protection Club).

### Notes
- Response is a direct array, not wrapped in `Items`/`TotalItems` pagination structure
- All clubs for the specified structure are returned (no pagination parameters available)
- Club names are localized to the requested `LanguageId`

---

## GetAllMaterialStatusesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialStatusesForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/MaterialStatusId"
      },
      "Title": {
        "type": "string"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns reference data for material processing statuses available in the legislative workflow.
- Use the returned `Id` values as the `StatusId` filter parameter in `GetAllMaterialsForPublicPortal` and similar operations.
- The `Title` value is localized according to the `languageId` parameter in the request (1=Macedonian, 2=Albanian, 3=Turkish).
- Returns only active/filterable statuses (6, 9, 10, 11, 12, 24, 64). Status `0` (Plenary/unknown) may appear in material detail records from other operations but is not returned by this catalog endpoint.
- Direct array response (not paginated; no TotalItems wrapper).


---

## GetAllMaterialTypesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialTypesForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer",
        "description": "Material type identifier. See MaterialTypeId in $defs for known values (1–37, non-sequential; gaps at 12 and 25)."
      },
      "Title": {
        "type": "string",
        "description": "Localized material type name in requested language (1=Macedonian, 2=Albanian, 3=Turkish). May contain leading/trailing whitespace or control characters (\\r, \\n) requiring trimming."
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns all available material types in the system (37 types with gaps at IDs 12 and 25).
- **Data quality:** Response `Title` values may contain leading/trailing whitespace characters (`\r`, `\n`, spaces) that should be trimmed for display.
- **Language support:** Tested with `languageId: 2` (Albanian) and `languageId: 1` (Macedonian). Titles are localized in the requested language.
- **Non-sequential IDs:** Material type IDs are not consecutive. IDs 12 and 25 are absent from the enumeration.
- **Usage:** Material type IDs returned here are used as `MaterialTypeId` filter values in `GetAllMaterialsForPublicPortal` operation and appear in material detail responses.
- **Material types:** Catalog includes legislative materials (laws, amendments, budget), procedural items (elections, appointments, resignations), oversight mechanisms (interpellations, reports), and constitutional procedures (amendments, interpretations).

---

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


---

## GetAllParliamentaryGroups

### Request
```json
{
  "methodName": "GetAllParliamentaryGroups",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Request Parameters
- **methodName** — `"GetAllParliamentaryGroups"` (required)
- **languageId** — `1` = Macedonian, `2` = Albanian, `3` = Turkish (required)
- **StructureId** — UUID of parliamentary term/structure (required). Obtain from `GetAllStructuresForFilter`. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. Determines which parliamentary groups to return based on the parliamentary term.

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string",
        "description": "Full official name of the parliamentary group (e.g., \"Пратеничка група на партијата …\")"
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
        "description": "Image identifier or URL for the parliamentary group. Often empty string when no image available."
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes
- Returns all parliamentary groups (factions/caucuses) for the specified structure/term. Each group represents a coalition or party with seats in parliament for that term.
- Response is a direct array, not wrapped in `TotalItems`/`Items` pagination structure.
- All `Image` fields in current data are empty strings `""`, indicating parliamentary groups may not have images assigned in the system.
- `NumberOfDeputies` reflects current membership count in each parliamentary group. Totals across all groups may not equal total MPs if there are independents or vacancies.


---

## GetAllPoliticalParties

### Request
```json
{
  "methodName": "GetAllPoliticalParties",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string",
        "description": "Political party name in the requested language"
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0,
        "description": "Count of MPs affiliated with this party in the specified structure"
      },
      "Image": {
        "type": "string",
        "description": "Party logo or image identifier. May be empty string when no image is available"
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

### Notes

**Filter usage:**
- **StructureId** — Required. UUID of parliamentary term/structure from GetAllStructuresForFilter. Use `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term. Determines which set of political parties and their deputy counts are returned for a specific parliamentary session.
- **languageId** — Required. Controls language of party names (1=Macedonian, 2=Albanian, 3=Turkish).

**Response structure:**
- Returns a flat array of political party objects (not wrapped in `TotalItems`/`Items` pagination structure).
- All fields (`Id`, `Name`, `NumberOfDeputies`, `Image`) are present in every party entry.

**Field meanings:**
- **Name** — Official name of the political party in the requested language.
- **NumberOfDeputies** — Current count of MPs affiliated with this party in the specified parliamentary structure/term. Reflects actual composition for that StructureId; sum across all parties (including independent MPs entry) should approximate total parliament seats.
- **Image** — Party logo or image identifier. Currently returns empty string `""` for all parties in observed data; may contain base64-encoded image data or URL in other cases.
- **Independent MPs** — Represented as a pseudo-party entry (e.g. "Независни пратеници" / Independent MPs) with its own UUID and deputy count.

---

## GetAllProcedureTypes

### Request
```json
{
  "methodName": "GetAllProcedureTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer",
        "enum": [1, 2, 3],
        "description": "Procedure type identifier"
      },
      "Title": {
        "type": "string",
        "description": "Procedure type name in requested language (or Macedonian fallback)"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a fixed set of three procedure types regardless of language or other parameters
- **Id values:**
  - `1` = "Редовна постапка" (Regular procedure)
  - `2` = "Скратена постапка" (Shortened procedure)
  - `3` = "Итна постапка" (Urgent procedure)
- The `languageId` parameter may not affect response content; Macedonian text has been observed regardless of requested language (e.g., `languageId: 3` returning Macedonian rather than Turkish)
- No pagination is used; all three procedure types are always returned in a single response
- The returned `Id` values map directly to `ProcedureTypeId` used in filtering operations (e.g., `GetAllMaterialsForPublicPortal`)

---

## GetAllQuestionStatuses

### Request
```json
{
  "methodName": "GetAllQuestionStatuses",
  "languageId": 1
}
```

**Note:** This operation accepts both `languageId` (lowercase) and `LanguageId` (capitalized) parameter names interchangeably. Either casing is accepted.

### Response
```json
[
  {
    "Id": 17,
    "Title": "Delivered"
  },
  {
    "Id": 19,
    "Title": "Replied"
  },
  {
    "Id": 20,
    "Title": "Non disclosed reply"
  },
  {
    "Id": 21,
    "Title": "Reply in Writing"
  }
]
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
        "type": "string"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

### Notes
- Returns a direct array of question status objects (not wrapped in an Items container or paginated).
- Parameter casing: accepts both `languageId` and `LanguageId`.
- `Title` is localized to the requested `LanguageId`. For example, with `LanguageId: 2` (Albanian), titles may appear as "Vendosur", "Përgjigj", "Përgjigj jo e zbuluar", "Përgjigj në shkrim".

---

## GetAllQuestions

### Request
```json
{
  "methodName": "GetAllQuestions",
  "LanguageId": 1,
  "CurrentPage": 1,
  "Page": 1,
  "Rows": 10,
  "SearchText": "",
  "RegistrationNumber": "",
  "StatusId": null,
  "From": "",
  "To": "",
  "CommitteeId": null,
  "DateFrom": null,
  "DateTo": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
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
                "description": "Unique identifier for the question"
              },
              "Title": {
                "type": "string",
                "description": "Question text/title"
              },
              "From": {
                "type": "string",
                "description": "Name of the MP who asked the question (questioner)"
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
                "description": "Human-readable status of the question in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered). Maps to QuestionStatusId enum values."
              },
              "DateAsked": {
                "$ref": "#/$defs/AspDate",
                "description": "Date when the question was submitted"
              },
              "QuestionTypeTitle": {
                "type": "string",
                "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question)"
              },
              "TotalRows": {
                "type": "integer",
                "description": "Per-item metadata field. Observed as 0 in all responses; purpose unclear (possibly legacy or unused field)."
              }
            },
            "required": ["Id", "Title", "From", "To", "ToInstitution", "StatusTitle", "DateAsked", "QuestionTypeTitle", "TotalRows"]
          }
        },
        {
          "type": "null",
          "description": "When TotalItems is 0, Items becomes null instead of empty array"
        }
      ]
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Request Schema Details

**Core parameters:**
- **methodName** — Required; must be `"GetAllQuestions"`
- **LanguageId** — Language for response labels (1=Macedonian, 2=Albanian, 3=Turkish)
- **Page** — 1-based page number for pagination
- **Rows** — Number of items per page (typical values: 6, 8, 10, 12, 14, 18)
- **CurrentPage** — Appears alongside `Page`; purpose unclear (possibly legacy/redundant parameter). Typically set to same value as `Page`.

**Optional filters** (all can be empty string or null to omit):
- **SearchText** — Free-text search across question titles and content. Set to `""` (empty string) to omit text filtering.
- **RegistrationNumber** — Filter by question registration number. Set to `""` to omit.
- **From** — Filter by question author name (MP name). Set to `""` to omit.
- **To** — Filter by recipient name (minister/official). Set to `""` to omit.
- **StatusId** — Filter by question status (see QuestionStatusId enum: 17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer). Set to `null` to include all statuses. Example: `19` returns only answered questions.
- **CommitteeId** — Filter questions by committee. UUID or `null` to include all committees.
- **DateFrom / DateTo** — Filter by DateAsked range. AspDate format or `null` to omit date filtering.
- **StructureId** — Parliamentary term UUID. Can be specific UUID (e.g., `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term) or `null` to query across all parliamentary terms/structures.

### Per-operation Notes

- **Pagination behavior**: Uses standard `Page`/`Rows` pagination. Response includes `TotalItems` (full result count) and page subset of `Items`.

- **StatusId filter example**: Setting `StatusId: 19` filters to answered questions only. Setting `StatusId: null` includes questions with all statuses.

- **CurrentPage vs Page**: Both parameters present in actual requests; their distinction is unclear. Recommend setting both to same value until behavior diverges. May be legacy/redundant parameter.

- **StructureId nullable behavior**: Unlike most operations that require `StructureId`, GetAllQuestions accepts `null` for cross-term queries of all questions regardless of parliamentary structure.

- **Empty string filters**: Multiple text filters (`SearchText`, `RegistrationNumber`, `From`, `To`) accept empty string `""` to disable filtering on that dimension.

- **TotalRows in items**: Each item includes `TotalRows: 0` in the response. Purpose is unclear (possibly legacy or reserved field); total count provided via top-level `TotalItems` instead.

- **Question types observed**: "Писмено прашање" (Written question), "Усно прашање" (Oral question). No separate question-type ID exposed; use `QuestionTypeTitle` for filtering/display.

- **Status values observed**: "Доставено" (Delivered, StatusId 17), "Одговорено" (Answered, StatusId 19).

- **Language localization**: Response content (Title, From, To, StatusTitle, QuestionTypeTitle, ToInstitution) is returned in the requested `LanguageId` language.

- **ToInstitution data quality**: May contain placeholder values (e.g., `"/"`) similar to `GetAllInstitutionsForFilter`; handle gracefully in client code. Note: inconsistent formatting in API responses (e.g., "Министерството" vs "Министерство" for ministry names).


---

## GetAllSittingStatuses

### Request
```json
{
  "methodName": "GetAllSittingStatuses",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "array",
  "description": "Returns all sitting status options with localized titles",
  "items": {
    "type": "object",
    "required": ["Id", "Title"],
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId",
        "description": "Numeric identifier for the sitting status (1–6)"
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
- Returns all six sitting status options with titles localized to the requested `LanguageId` (1=Macedonian, 2=Albanian, 3=Turkish)
- The `Id` values (1–6) map directly to the `SittingStatusId` enum in $defs
- `Title` is the human-readable label for the status in the requested language
- Use the returned `Id` values when filtering sittings via the `StatusId` parameter in `GetAllSittings`
- This is a simple array response (not wrapped in TotalItems/Items object)

---

## GetAllSittings

### Notes
Empty results behavior: When no sittings match the filter criteria, the API returns `{"TotalItems": 0, "Items": null}` rather than an empty items array.

The response schema differs significantly from the documented schema. Actual responses include `SittingDate`, `TypeId`, `TypeTitle`, `StatusTitle`, `Location`, `SittingDescriptionTypeTitle`, `Continuations`, `Structure`, and `TotalRows` fields instead of `DateFrom`/`DateTo`, `SittingTypeId`, `CommitteeId`, `Number`, `SessionId`.

`Number` appears in response items for both plenary (`TypeId: 1`) and committee (`TypeId: 2`) sittings, representing the sitting sequence number within that context (e.g., 10th committee sitting, 5th plenary sitting).

`CommitteeTitle` provides the committee name when filtering across multiple committees.

`Continuations` is an empty array in all observed responses; likely populated when a sitting is continued across multiple sessions.

`Structure` and `TotalRows` appear to be metadata fields not populated in list responses.

When `StructureId` is `null`, the API returns sittings from all parliamentary terms/structures, not limited to a single term. `TotalItems` reflects the cross-term total.

### Request
```json
{
  "methodName": "GetAllSittings",
  "Page": 2,
  "Rows": 15,
  "LanguageId": 2,
  "TypeId": 2,
  "CommitteeId": "b8b25861-9b5c-4d47-9717-007b83a8a339",
  "StatusId": 6,
  "DateFrom": null,
  "DateTo": null,
  "SessionId": null,
  "Number": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllSittings"
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
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Sitting type filter: 1=Plenary, 2=Committee. Set to null to include all types."
    },
    "CommitteeId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
        {"type": "null"}
      ],
      "description": "UUID of committee to filter by. Use with TypeId: 2 for committee sittings. Set to null for plenary sittings or to include all committees."
    },
    "StatusId": {
      "anyOf": [
        {"$ref": "#/$defs/SittingStatusId"},
        {"type": "null"}
      ],
      "description": "Filter sittings by status. Set to null to include all statuses."
    },
    "DateFrom": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter sittings by start date. Set to null to omit date filtering."
    },
    "DateTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter sittings by end date. Set to null to omit date filtering."
    },
    "SessionId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
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
      "description": "UUID of parliamentary term/structure. Set to null to retrieve sittings across all structures/terms. Use specific UUID (e.g., 5e00dbd6-ca3c-4d97-b748-f792b2fa3473) to filter by term."
    }
  },
  "required": ["methodName", "Page", "Rows", "LanguageId"]
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
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Number": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Sitting sequence number within the committee (TypeId: 2) or plenary (TypeId: 1). Each committee maintains its own sequence."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Primary sitting date/time"
          },
          "TypeId": {
            "$ref": "#/$defs/AgendaItemTypeId",
            "description": "Sitting type: 1=Plenary, 2=Committee"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Localized sitting type name"
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
            "description": "Physical location of sitting"
          },
          "CommitteeId": {
            "anyOf": [
              {"type": "string", "format": "uuid"},
              {"type": "null"}
            ],
            "description": "UUID of committee. Present for committee sittings (TypeId: 2); null for plenary."
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Localized committee name. Present for committee sittings (TypeId: 2); null for plenary."
          },
          "SittingDescriptionTypeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Localized description of sitting subtype/format (e.g., regular committee sitting, public hearing)"
          },
          "Continuations": {
            "type": "array",
            "description": "Array of continuation sitting references. Empty when sitting has no continuations.",
            "items": {
              "type": "object"
            }
          },
          "Structure": {
            "anyOf": [
              {"type": "object"},
              {"type": "null"}
            ],
            "description": "Structural metadata, typically null in list responses"
          },
          "TotalRows": {
            "type": "integer",
            "description": "Row count metadata, typically 0 in list responses"
          }
        }
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```

---

## GetAllStructuresForFilter

### Request
```json
{
  "methodName": "GetAllStructuresForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID identifier of the parliamentary term/structure. Use this as StructureId in filter operations."
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
        "description": "Boolean flag indicating whether this is the currently active parliamentary term. Only one structure should have IsCurrent: true."
      }
    },
    "required": ["Id", "DateFrom", "DateTo", "IsCurrent"]
  }
}
```

### Notes
- Returns all parliamentary terms/structures in reverse chronological order (current/most recent first, oldest last)
- Exactly one structure has `IsCurrent: true` — this is the active parliamentary term
- The `Id` of the structure with `IsCurrent: true` should be used as the default `StructureId` parameter in other operations when querying current parliamentary data (typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` as of 2024)
- Historical structures are available, dating back to at least June 2008
- `DateTo` for the current term may be set to a far future placeholder date (e.g., `/Date(1851372000000)/` representing 2028)
- Unlike most catalog operations, structures do not include a `Title` or `Name` field; they are identified only by UUID and date range
- The `languageId` parameter does not affect the response structure (no localized fields are present)
- Response is not paginated; returns the complete list of all structures
- Use this operation once per session to obtain the current `StructureId` for use in other filtering operations

---

## GetCommitteeDetails

### Request
```json
{
  "methodName": "GetCommitteeDetails",
  "committeeId": "b8b25861-9b5c-4d47-9717-007b83a8a339",
  "languageId": 1
}
```

### Response
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
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Претседател/Претседателка на комисија')"
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
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
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
      "description": "Administrative/professional staff (advisors, approvers). Note: same person may appear multiple times with different RoleId values if holding multiple roles"
    },
    "Materials": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      },
      "description": "Materials assigned to this committee for review/processing. Can be empty array [] when no materials linked"
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type name (e.g., 'Комисиска седница' = Committee sitting)"
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
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
      "description": "HTML-formatted committee description including mandate, responsibilities, composition requirements. May contain markup tags (<p>, <br/>, <div>). May be truncated with ellipsis (...) in response"
    },
    "Email": {
      "type": "string",
      "description": "Committee contact email address"
    },
    "PhoneNumber": {
      "type": ["string", "null"],
      "description": "Committee contact phone number; may be null when not available"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure this committee belongs to"
    }
  }
}
```

### Request Parameters
- **committeeId** (string, UUID, required) — Committee identifier. Obtain from `GetAllCommitteesForFilter`.
- **languageId** (integer, required) — Language for response text (1=Macedonian, 2=Albanian, 3=Turkish). Affects `Name`, `RoleTitle`, `StatusTitle`, `TypeTitle`, and `Description`.
- **methodName** (string) — Operation name: `GetCommitteeDetails`.

### Response Structure
- **Name** — Committee name in the requested language.
- **CompositionMembers** — Array of elected committee members (MPs) with official roles:
  - RoleId 6 = Committee Chair (Претседател/Претседателка на комисија)
  - RoleId 82 = Vice-Chair (Заменик-претседател/Заменик-претседателка на комисија)
  - RoleId 7 = Member (Член/Членка на комисија)
  - RoleId 83 = Deputy Member (Заменик-член)
- **SecretariatMembers** — Array of administrative/professional staff supporting the committee:
  - RoleId 10 = Approver (Одобрувач/Одобрувачка)
  - RoleId 11 = Advisor (Советник/Советничка на комисија)
  - **Note**: Same person (UserId/FullName) may appear multiple times with different RoleIds when holding multiple staff roles (e.g., both Approver and Advisor). This is expected behavior, not a data error.
- **Materials** — Subset of materials assigned to this committee from GetAllMaterialsForPublicPortal. Uses MaterialStatusId enum (6=Delivered to MPs, 12=Closed, etc.). Returns empty array `[]` when no materials linked (not `null`).
- **Meetings** — Committee sittings/sessions in reverse chronological order (most recent first). TypeTitle typically "Комископска седница" (Committee sitting). Use Meeting.Id with `GetSittingDetails` for full agenda and voting details.
- **Description** — HTML-formatted text describing committee's mandate, composition, responsibilities, and reporting requirements. May contain markup tags; may be truncated with ellipsis.
- **Email** — Official committee contact email.
- **PhoneNumber** — Committee contact phone number; nullable (can be `null` when not available).
- **StructureId** — UUID of the parliamentary term this committee belongs to (typically the current term).

### Usage Notes
- Returns comprehensive details for a single committee identified by `committeeId`.
- **CompositionMembers** contains the official elected committee structure (chairs, members).
- **SecretariatMembers** contains staff roles; individuals may hold multiple roles and appear multiple times.
- **Materials** shows legislative items processed by this committee; filtered subset of GetAllMaterialsForPublicPortal results.
- **Description** contains HTML markup; parse for display in client applications.
- **Meetings** can be used with `GetSittingDetails` to retrieve full agenda, voting results, and documents.
- Response includes `"_truncated": N` in documentation examples when arrays were truncated; actual API responses include all items.

---

## GetCouncilDetails

### Request
```json
{
  "methodName": "GetCouncilDetails",
  "committeeId": "d596538c-f3d4-4440-8ae7-6e25ea094c6a",
  "languageId": 1
}
```

### Response
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
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "enum": [6, 7, 10, 11, 82]
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      },
      "description": "Official council composition members (MPs with voting roles). Typically includes president (RoleId 6), vice-president (82), and members (7)."
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "enum": [6, 7, 10, 11, 82]
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      },
      "description": "Administrative and advisory staff supporting the council. May contain duplicate UserId entries with different RoleId values (same person holding multiple roles)."
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Materials associated with the council. Empty array [] when no materials exist."
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type label (e.g., 'Комисиска седница' = Committee sitting)"
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
        }
      },
      "description": "Past and scheduled council meetings/sittings, ordered by date in reverse chronological order (most recent first)."
    },
    "Description": {
      "anyOf": [
        {
          "type": "string",
          "description": "HTML-formatted description of the council's mandate and responsibilities. May contain markup including paragraphs, links, and styling."
        },
        {
          "type": "null"
        }
      ]
    },
    "Email": {
      "type": "string",
      "description": "Contact email address for the council"
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
      "description": "Contact phone number for the council. Null when not available."
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure this council belongs to"
    }
  }
}
```

### Request Filter
- **committeeId** — UUID of the council to retrieve details for. Obtain from GetAllCouncils response. Identifies which council to fetch information about.
- **languageId** — Requested language for response labels and text (1=Macedonian, 2=Albanian, 3=Turkish). Controls language for Name, RoleTitle, Description, and other text fields.
- **methodName** — Value: "GetCouncilDetails" (lowercase)

### Response Keys

**Name** — Full name of the council in the requested language.

**CompositionMembers** — Array of official council composition members (voting members, typically MPs).
- Same council member may appear in this array with only composition roles (6=President, 82=Vice-President, 7=Member).
- Ordered by role importance (President typically first, then Vice-President, then Members).

**SecretariatMembers** — Array of administrative and support staff.
- RoleId values: 10=Approver (Одобрувач/Одобрувачка), 11=Advisor (Советник/Советничка на комисија).
- Important: Same person (UserId) can appear multiple times with different RoleId values when they hold multiple roles (e.g., person serving as both Approver and Advisor).
- This is expected behavior, not a data quality issue.

**Materials** — Associated materials (e.g., founding decisions, policy documents).
- Returns empty array `[]` when no materials exist (not `null`).
- When populated, contains material objects.

**Meetings** — Council meetings/sittings in reverse chronological order (most recent first).
- **TypeTitle**: Typically "Комископска седница" (Committee sitting) for council meetings.
- **SittingNumber**: Sequential number incremented per council.
- **Location**: Physical venue (e.g., "Сала 4" = Room 4).
- **Date**: AspDate format timestamp.

**Description** — HTML-formatted text describing the council's legal basis, mandate, and responsibilities.
- Can contain extensive HTML markup including `<p>`, `<span>`, `<a>`, `<br/>` tags and inline styles.
- May include links to founding decisions, constitutional references, and other resources.
- Nullable; can be `null` when not provided.

**Email** — Official contact email for the council (e.g., "council-name@sobranie.mk").

**PhoneNumber** — Contact phone number. Nullable; can be `null` when not provided.

**StructureId** — UUID of the parliamentary term/structure to which this council belongs. Common value: `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current parliamentary term. Matches StructureId parameter used in other operations.

### Additional Notes

- **RoleId enum values** (from $defs/RoleId):
  - `6` = Committee President (Претседател/Претседателка на комисија)
  - `82` = Committee Vice President (Заменик-претседател/Заменик-претседателка на комисија)
  - `7` = Committee Member (Член/Членка на комисија)
  - `10` = Approver (Одобрувач/Одобрувачка)
  - `11` = Committee Advisor (Советник/Советничка на комисија)

- **Duplicate users in SecretariatMembers**: A single person may appear multiple times in the SecretariatMembers array with different RoleId values. For example, one staff member can simultaneously hold roles as both Approver (RoleId: 10) and Advisor (RoleId: 11). This reflects that person's actual responsibilities and is expected behavior.

- **Meetings ordering**: The Meetings array is ordered by Date in reverse chronological order (most recent first). Use the Date field to sort or filter client-side if needed.

- **HTML content in Description**: The Description field contains rich HTML markup. Parse as HTML when displaying to end users. May include links to PDF documents and other resources related to the council's establishment and mandate.

- **Parameter casing**: Uses lowercase `methodName` and `languageId` (standard method-based convention).

---

## GetCustomEventsCalendar

### Request
```json
{
  "model": {
    "Language": 1,
    "Month": 1,
    "Year": 2026
  }
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "__type": {
            "type": "string",
            "description": "e.g. moldova.controls.Models.CalendarViewModel"
          },
          "Id": {
            "type": "string",
            "format": "uuid"
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
            "description": "Physical location of event. May be empty string when location is not specified or not applicable"
          },
          "EventDate": {
            "$ref": "#/$defs/AspDate"
          },
          "EventType": {
            "$ref": "#/$defs/EventTypeId"
          }
        },
        "required": ["__type", "Id", "EventDescription", "EventLink", "EventLocation", "EventDate", "EventType"]
      }
    }
  },
  "required": ["d"]
}
```

### Request Filters
- **Language** — LanguageId (1=Macedonian, 2=Albanian, 3=Turkish). Controls language of EventDescription and EventLocation.
- **Month** — Integer 1-12 for the calendar month to retrieve.
- **Year** — Four-digit year (e.g., 2024, 2026) to retrieve events for.

### Notes
- Returns all calendar events for the specified month and year. Response is an array in the `d` property (ASMX wrapper).
- All events in the sample data have `EventType: 5`, corresponding to press conferences, official visits, working sessions, commemorations, and public events. Other EventType values may exist but are not yet documented.
- `EventLocation` can be empty string (`""`) when location is not specified or not applicable to the event type.
- `EventLink` provides URL-safe slugs suitable for constructing event detail page URLs.
- Response may be empty array `[]` if no events exist for the requested month/year.
- `EventDescription` is localized based on the `Language` parameter; same event may return different language text with different Language values.


---

## GetMPsClubDetails

### Description
Retrieves detailed information about a specific MPs club (inter-party parliamentary group), including full member roster with roles.

### Request
```json
{
  "methodName": "GetMPsClubDetails",
  "mpsClubId": "22ded665-2466-4d7e-a04b-03f8a150fc8c",
  "LanguageId": 1
}
```

**Request parameters:**
- **methodName** — String; literal value `"GetMPsClubDetails"`. Uses lowercase `m` in `methodName` (camelCase).
- **mpsClubId** — UUID string; identifier of the MPs club to retrieve. Obtained from `GetAllMPsClubsByStructure`.
- **LanguageId** — Integer; requested language for response text (1=Macedonian, 2=Albanian, 3=Turkish). Uses uppercase `L` in `LanguageId` (PascalCase). This operation mixes camelCase and PascalCase parameter naming.

### Response
```json
{
  "Name": "Пратеничка група на партијата...",
  "Description": "Description text or '-' placeholder",
  "Members": [
    {
      "Id": "550e8400-e29b-41d4-a716-446655440000",
      "FirstName": "Иван",
      "LastName": "Петровски",
      "RoleId": 78,
      "RoleTitle": "Претседател/Претседателка"
    },
    {
      "Id": "550e8400-e29b-41d4-a716-446655440001",
      "FirstName": "Марија",
      "LastName": "Стефановска",
      "RoleId": 81,
      "RoleTitle": "Член/Членка"
    },
    {
      "_truncated": 31
    }
  ],
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

**Response schema:**
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full name of the MPs club in the requested language"
    },
    "Description": {
      "type": "string",
      "description": "Description text for the club. May contain placeholder value '-' when no description is provided"
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs belonging to this club with their roles. May include _truncated placeholder for large lists",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid",
            "description": "UUID identifier for the MP member"
          },
          "FirstName": {
            "type": "string",
            "description": "Member's first name"
          },
          "LastName": {
            "type": "string",
            "description": "Member's last name"
          },
          "RoleId": {
            "type": "integer",
            "enum": [78, 79, 81],
            "description": "Member's role within the club (see MPsClubRoleId in $defs). 78=President/Chairperson, 79=Vice-President, 81=Member"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized human-readable role title, may include gender-inclusive slash notation (e.g., 'Претседател/Претседателка')"
          },
          "_truncated": {
            "type": "integer",
            "description": "Placeholder object indicating N additional members were truncated from response (not present for regular member objects)"
          }
        },
        "required": ["Id", "FirstName", "LastName", "RoleId", "RoleTitle"]
      }
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the parliamentary term/structure this club belongs to (typically current term: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473)"
    }
  },
  "required": ["Name", "Description", "Members", "StructureId"]
}
```

### Per-operation Notes

**Parameter casing:** This operation uses mixed casing: `methodName` (lowercase m) and `mpsClubId` (camelCase) but `LanguageId` (uppercase L). This is a variation of the common pattern where some operations mix PascalCase and camelCase.

**Member role hierarchy:** MPs clubs have a structured membership with distinct roles:
- **RoleId 78** = President/Chairperson (Претседател/Претседателка) — typically one per club
- **RoleId 79** = Vice-President (Заменик-претседател/Заменик-претседателка) — may be zero or multiple
- **RoleId 81** = Member (Член/Членка) — regular club members

**Gendered role titles:** RoleTitle values use gender-inclusive notation with a slash separator, following Macedonian language conventions (e.g., "Претседател/Претседателка" represents masculine/feminine forms). This applies to all role types.

**Description placeholder:** When a club has no description, the API returns the string `"-"` rather than null or an empty string. Client code should detect this placeholder and treat it as "no description provided".

**Response truncation:** The Members array may include a `{"_truncated": N}` placeholder object as the final element, indicating N additional members exist but were not included in the response. For example, `{"_truncated": 31}` means 31 additional members are not shown. This is an API behavior for handling large clubs; client code should be prepared to handle this marker.

**StructureId in response:** The returned StructureId indicates which parliamentary term this club belongs to. This typically matches the StructureId provided to `GetAllMPsClubsByStructure` when retrieving the club list, and is often the current term `5e00dbd6-ca3c-4d97-b748-f792b2fa3473`.

**Localization:** The `Name`, `Description`, and `RoleTitle` fields are localized to the requested `LanguageId`. Test with different language IDs to confirm expected localization behavior for your application.


---

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


---

## GetMonthlyAgenda

### Request
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "const": "GetMonthlyAgenda"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "Month": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Month (1–12) for which to retrieve agenda items"
    },
    "Year": {
      "type": "integer",
      "description": "Four-digit year (e.g. 2025, 2026) for which to retrieve agenda items"
    }
  },
  "required": ["methodName", "LanguageId", "Month", "Year"]
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid",
        "description": "Identifier for the agenda item/sitting"
      },
      "Title": {
        "type": "string",
        "description": "Full descriptive title including sitting number, committee/body name, and location"
      },
      "Location": {
        "type": "string",
        "description": "Physical location/room where the sitting will take place"
      },
      "Start": {
        "$ref": "#/$defs/AspDate",
        "description": "Start date/time of the agenda item"
      },
      "Type": {
        "$ref": "#/$defs/AgendaItemTypeId",
        "description": "1=Plenary, 2=Committee"
      }
    },
    "required": ["Id", "Title", "Location", "Start", "Type"]
  }
}
```

### Notes
- **Request parameters:**
  - `methodName`: Always `"GetMonthlyAgenda"`
  - `LanguageId`: Standard language parameter (1=Macedonian, 2=Albanian, 3=Turkish). Affects language of Title and Location fields.
  - `Month`: Integer 1-12 specifying the calendar month to retrieve agenda items for. Required.
  - `Year`: Four-digit year (e.g. 2025, 2026) specifying the calendar year to retrieve agenda items for. Required.

- **Response structure:** Returns a flat array of agenda items (not wrapped in TotalItems/Items pagination structure).

- **Title format:** Typically follows pattern "Седница бр. {number} на {body name} - {location}" (in Macedonian) or equivalent localization in requested language.

- **Type values:**
  - Type 1 = Plenary sittings (main parliament sessions, typically at "Сала „Македонија"")
  - Type 2 = Committee sittings (committee meetings, typically at "Сала 4", "Сала 5", "Сала 6", etc.)

- **Empty results:** When no agenda items exist for the requested month/year, returns empty array `[]` (not null).

- **Ordering:** Results are ordered by Start date/time.

- **Usage:** Useful for calendar views, scheduling displays, and retrieving upcoming parliamentary sessions. The `Id` can be used with `GetSittingDetails` to fetch detailed sitting information.

---

## GetOfficialVisitsForUser

### Request
```json
{
  "model": "914bff80-4c19-4675-ace4-cb0c7a08f688"
}
```

### Response
```json
{
  "d": []
}
```

### Notes
- **Endpoint format:** ASMX-wrapped POST request
- **Request body:** `model` field contains a UUID string representing the user ID
- **Response format:** `d` property contains array of visit objects (empty array when user has no official visits)
- **Visit object schema:** When visits exist, items in `d` array contain official visit details. Exact schema not yet documented from available examples.


---

## GetParliamentMPsNoImage

### Request
```json
{
  "methodName": "GetParliamentMPsNoImage",
  "languageId": 1,
  "genderId": null,
  "ageFrom": null,
  "ageTo": null,
  "politicalPartyId": null,
  "searchText": null,
  "page": 1,
  "rows": 8,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
  "coalition": "",
  "constituency": ""
}
```

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
      "$ref": "#/$defs/LanguageId",
      "description": "Requested language for MP names and party titles (1=Macedonian, 2=Albanian, 3=Turkish)"
    },
    "genderId": {
      "anyOf": [
        {"$ref": "#/$defs/GenderId"},
        {"type": "null"}
      ],
      "description": "Filter MPs by gender (1=Male, 2=Female). Set to null to include all genders"
    },
    "ageFrom": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Minimum age for filtering MPs. Nullable; set to null to omit age filtering"
    },
    "ageTo": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Maximum age for filtering MPs. Nullable; set to null to omit age filtering"
    },
    "politicalPartyId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of political party to filter MPs. Set to null to include all parties"
    },
    "searchText": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Free-text search filter for MP names. Set to null to omit text search"
    },
    "page": {
      "type": "integer",
      "description": "Page number (1-based) for pagination of MembersOfParliament results"
    },
    "rows": {
      "type": "integer",
      "description": "Number of items per page"
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of parliamentary term/structure. When null, returns empty MP lists but Statistics may still be populated with global counts. Required to retrieve MP data"
    },
    "coalition": {
      "type": "string",
      "description": "Filter by coalition affiliation. Set to empty string '' to omit coalition filtering. Usage may vary"
    },
    "constituency": {
      "type": "string",
      "description": "Filter by electoral constituency. Set to empty string '' to omit constituency filtering. Usage may vary"
    }
  },
  "required": ["methodName", "page", "rows"]
}
```

### Response
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
                "type": "string",
                "format": "uuid"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for MP's photo. Despite operation name 'NoImage', this field contains actual image data"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "type": "integer",
                "description": "MP role identifier (meaning not fully documented; observed values include 1)"
              },
              "PoliticalPartyTitle": {
                "type": "string"
              },
              "PoliticalPartyId": {
                "type": "string",
                "format": "uuid"
              }
            }
          }
        },
        {"type": "null"}
      ],
      "description": "Array of MPs with active mandates in the specified structure. Returns empty array [] when no results"
    },
    "ExpiredMandateMembers": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "UserId": {
                "type": "string",
                "format": "uuid"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for MP's photo"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "type": "integer",
                "description": "MP role identifier (meaning not fully documented; observed values include 1)"
              },
              "PoliticalPartyTitle": {
                "type": "string"
              },
              "PoliticalPartyId": {
                "type": "string",
                "format": "uuid"
              }
            }
          }
        },
        {"type": "null"}
      ],
      "description": "Array of MPs whose mandates have expired in the specified structure. Returns empty array [] when no results"
    },
    "TotalItems": {
      "type": "integer",
      "description": "Total count of MPs with active mandates matching filter criteria"
    },
    "TotalItemsExpiredMandate": {
      "type": "integer",
      "description": "Total count of MPs with expired mandates matching filter criteria"
    },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": {
          "type": "integer",
          "description": "Total count of legislative materials in the system (may be global count)"
        },
        "NumberOfQuestions": {
          "type": "integer",
          "description": "Total count of parliamentary questions"
        },
        "TotalNumberOfMPs": {
          "type": "integer",
          "description": "Total count of MPs with active mandates"
        },
        "TotalNumberOfExpiredMandateMPs": {
          "type": "integer",
          "description": "Total count of MPs with expired mandates"
        },
        "MPsInPoliticalParties": {
          "type": "integer",
          "description": "Count of MPs affiliated with political parties"
        },
        "MPsInParliamentaryGroups": {
          "type": "integer",
          "description": "Count of MPs in parliamentary groups"
        },
        "NumberOfMaterialsInStructure": {
          "type": "integer",
          "description": "Count of materials in the specified structure"
        }
      },
      "description": "Aggregate statistics object. Always returned regardless of MP results. Some fields (e.g., TotalNumberOfMaterials) may reflect global counts even when StructureId is null or filters return no MPs"
    }
  },
  "required": ["MembersOfParliament", "ExpiredMandateMembers", "TotalItems", "TotalItemsExpiredMandate", "Statistics"]
}
```

### Per-operation Notes

#### Operation Name vs. Response Content
**UserImg field:** Despite the operation name "GetParliamentMPsNoImage", the response **does** include the `UserImg` field containing base64-encoded image data for each MP. The "NoImage" in the name may be historical or refer to a different context. Images are present and populated in the response.

#### StructureId Behavior
**When StructureId is null:** The API returns empty MP arrays (`MembersOfParliament: []`, `ExpiredMandateMembers: []`) with `TotalItems: 0` and `TotalItemsExpiredMandate: 0`. However, the `Statistics` object is still returned and may contain non-zero global counts (e.g., `TotalNumberOfMaterials`), suggesting global statistics are returned regardless of structure filter state. **To retrieve MPs for a specific parliamentary term, provide a valid StructureId UUID from GetAllStructuresForFilter.**

#### Pagination
**Pagination parameters:** The `page` and `rows` parameters control pagination of the `MembersOfParliament` array. `TotalItems` reflects the full count of active MPs across all pages; the `MembersOfParliament` array contains only the subset for the requested page. Pagination behavior for `ExpiredMandateMembers` is unclear (separate pagination or single list).

#### Empty Results Behavior
When no MPs match the filter criteria, both `MembersOfParliament` and `ExpiredMandateMembers` return empty arrays `[]` (not `null`), unlike some other operations (e.g., GetAllSittings) where `Items` becomes `null` when `TotalItems: 0`. When requesting a page beyond the result set, empty arrays are returned without error.

#### Filter Interaction
**Gender filtering:** When `genderId` is set (e.g., `1` for male), the response includes only MPs matching that gender. When `null`, all genders are included. The filter affects both active and expired mandate MP lists.

**Political party filtering:** When `politicalPartyId` is set to a valid UUID, only MPs from that party are returned in both arrays. When `null`, all parties are included.

**Text search:** `searchText` filters MPs by name. Set to `null` for no text filtering.

**Coalition and constituency filters:** Both `coalition` and `constituency` accept string values (can be empty string `""` to omit filtering). Exact usage/behavior requires further testing with actual data samples.

#### Statistics Object
The `Statistics` object is always present in the response and provides aggregate counts useful for dashboards or summary displays. Some fields appear to reflect global data (e.g., `TotalNumberOfMaterials`) and remain non-zero even when filter results are empty. Other fields (e.g., `NumberOfMaterialsInStructure`) reflect the filtered result set or specific structure and may be zero when StructureId is null or no data matches the filters.

#### Language Support
MP names, party titles, and other localized fields are returned in the language specified by the `languageId` parameter (1=Macedonian, 2=Albanian, 3=Turkish).


---

## GetParliamentaryGroupDetails

### Request
```json
{
  "methodName": "GetParliamentaryGroupDetails",
  "parliamentaryGroupId": "6f83cbd1-af39-44e5-bfd0-0cde68932844",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string"
    },
    "Description": {
      "type": "string"
    },
    "NumberOfDeputies": {
      "type": "integer"
    },
    "Materials": {
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
        }
      }
    },
    "Amendments": {
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
        }
      }
    },
    "Questions": {
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
          "DateAsked": {
            "$ref": "#/$defs/AspDate"
          },
          "DateAnswered": {
            "anyOf": [
              {"$ref": "#/$defs/AspDate"},
              {"type": "null"}
            ]
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          },
          "MaterialsCount": {
            "type": "integer"
          },
          "AmendmentsCount": {
            "type": "integer"
          },
          "QuestionsCount": {
            "type": "integer"
          }
        }
      }
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Image": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

## Notes

### Parameter Casing
This operation uses mixed parameter casing: lowercase `methodName` and uppercase `LanguageId`.

### Response Behavior

**Array truncation**: The `Materials`, `Amendments`, and `Questions` arrays may be truncated in responses. When an array is truncated, the last item in that array will contain an `_truncated` property with an integer value indicating how many additional items exist but are not included in the response. For example, `{"_truncated": 32}` indicates 32 additional items are available but not shown.

The `Members` array may also be truncated in responses for large parliamentary groups.

**Contact fields**: The `Email`, `Phone`, and `Image` fields are frequently `null` for parliamentary groups. Contact is typically directed through individual members rather than through the group entity itself.

**Description field**: The `Description` field may contain minimal placeholder values (e.g., "-") when no detailed description is available for the parliamentary group.

### Member Roles
Members in the `Members` array include role information via `RoleId` and `RoleTitle`. Observed role IDs:
- `26` = Координатор/Координаторка на политичка партија (Coordinator of political party)
- `72` = Заменик координатор/координаторка на политичка партија (Deputy coordinator of political party)

Each member object includes aggregated activity counts (`MaterialsCount`, `AmendmentsCount`, `QuestionsCount`) showing their parliamentary contributions within this parliamentary group context.

### Questions Field
The `DateAnswered` field is `null` for questions that have not yet been answered (when `StatusId` is `17` = Delivered). For answered questions, this field contains an AspDate timestamp.

### StructureId
The `StructureId` identifies the parliamentary term to which this parliamentary group belongs. Typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current parliamentary term.

---

## GetPoliticalPartyDetails

### Request
```json
{
  "methodName": "GetPoliticalPartyDetails",
  "politicalPartyId": "e693cd9f-5893-49ab-9ede-0abd6e820664",
  "LanguageId": 1
}
```

### Response
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
            "type": "string",
            "format": "uuid",
            "description": "UUID of the material"
          },
          "Title": {
            "type": "string",
            "description": "Material title/name"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date when material was officially registered"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration identifier (format: NN-NNN/N)"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier (see MaterialStatusId enum)"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Human-readable status label in requested language"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      },
      "description": "Materials (legislative proposals, amendments) submitted by this political party"
    },
    "Amendments": {
      "type": "array",
      "items": {},
      "description": "Amendments proposed by the party. Empty array when party has no amendments."
    },
    "Questions": {
      "type": "array",
      "items": {},
      "description": "Parliamentary questions submitted by the party. Empty array when party has no questions."
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid",
            "description": "UUID identifier for the party member/MP"
          },
          "FullName": {
            "type": "string",
            "description": "Complete name of the party member"
          },
          "RoleId": {
            "type": "integer",
            "enum": [27],
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
            "description": "Count of materials submitted by member. Always null in this response."
          },
          "AmendmentsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Count of amendments submitted by member. Always null in this response."
          },
          "QuestionsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Count of questions submitted by member. Always null in this response."
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
      "description": "Party contact email; null when not available"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact phone number; null when not available"
    },
    "Image": {
      "type": "string",
      "description": "Party logo/image; may be base64-encoded data or empty string when not available"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure ID this party data belongs to"
    }
  }
}
```

### Notes
- **Request parameters**: `politicalPartyId` (UUID obtained from GetAllPoliticalParties) and `LanguageId` (1=Macedonian, 2=Albanian, 3=Turkish) control language of response text fields
- **Response structure**: Returns detailed party information including name, member count, associated materials, amendments, questions, and member list
- **Materials array**: Contains all legislative materials (proposals, amendments) submitted by the party with registration dates and current status. Empty when party has no submissions.
- **Amendments array**: Separate collection of amendments proposed by the party; empty in sample but may contain items for other parties
- **Questions array**: Separate collection of parliamentary questions from the party; empty in sample but may contain items for other parties
- **Members array**: Lists all MPs affiliated with the party. All members share RoleId `27` ("Член/Членка на политичка партија"). Count fields (MaterialsCount, AmendmentsCount, QuestionsCount) are always `null` in this endpoint; use dedicated endpoints if per-member activity counts needed
- **Description field**: May be placeholder value like `"-"` if party has no biography text set
- **Image field**: May be empty string `""` when party has no logo; when present contains base64-encoded image data
- **Email/Phone**: Always `null` in observed responses (party-level contact information not exposed via this endpoint)
- **Not paginated**: Returns complete party details without pagination
- **StructureId**: Implicitly matches parliamentary term from which politicalPartyId was obtained

---

## GetProposerTypes

### Request
```json
{
  "methodName": "GetProposerTypes",
  "languageId": 1
}
```

### Response
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
        "type": "string"
      },
      "Order": {
        "type": "integer"
      }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```

### Notes
- **Language fallback behavior**: When `languageId` is set to a non-Macedonian value (e.g., 2=Albanian, 3=Turkish), the API may return `Title` values in Macedonian as fallback. The request structure and response schema remain unchanged, but localization may not be fully applied to all catalog operations.

---

## GetQuestionDetails

### Request
```json
{
  "methodName": "GetQuestionDetails",
  "QuestionId": "0e2039bb-7a4b-462b-9489-6bce448eeb2a",
  "LanguageId": 1
}
```

### Response
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
      "description": "Title/position of the official or minister the question is addressed to"
    },
    "ToInstitution": {
      "type": "string",
      "description": "Full name of the ministry or government body receiving the question"
    },
    "QuestionTypeTitle": {
      "type": "string",
      "description": "Type of question in the requested language (e.g. 'Писмено прашање' = Written question, 'Усно прашање' = Oral question)"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Human-readable status in the requested language (e.g. 'Доставено' = Delivered, 'Одговорено' = Answered)"
    },
    "NumberOfDeliveryLetter": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Delivery letter reference number; null when not assigned"
    },
    "Documents": {
      "type": "array",
      "description": "Array of attached documents. May be empty array [] when no documents attached.",
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
            "enum": [26],
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
        }
      }
    },
    "Sittings": {
      "type": "array",
      "description": "Array of sittings where the question was discussed. Empty array [] when question has not been discussed in any sitting yet.",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer",
            "enum": [1, 2],
            "description": "1=Plenary (Пленарна седница), 2=Committee"
          },
          "SittingTypeTitle": {
            "type": "string",
            "description": "Human-readable sitting type in the requested language"
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
        }
      }
    }
  }
}
```

## Operation Notes

### Parameter Notes
- **QuestionId** — UUID of the parliamentary question to retrieve details for. Obtain from `GetAllQuestions` Items[].Id.
- **LanguageId** — Requested language for response labels (1=Macedonian, 2=Albanian, 3=Turkish).

### Response Field Meanings
- **Title** — Full text of the parliamentary question.
- **From** — Name of the MP who submitted the question.
- **To** — Title/position of the official or minister to whom the question is directed (e.g. "Министерот за внатрешни работи").
- **ToInstitution** — Full name of the ministry or government body receiving the question (e.g. "Министерство за внатрешни работи"). Localized according to LanguageId.
- **QuestionTypeTitle** — Type of question in the requested language (e.g. "Писмено прашање" = Written question, "Усно прашање" = Oral question). Localized according to LanguageId.
- **StatusTitle** — Current status of the question in the requested language (e.g. "Доставено" = Delivered, "Одговорено" = Answered). Corresponds to QuestionStatusId enum values from GetAllQuestionStatuses. Localized according to LanguageId.
- **NumberOfDeliveryLetter** — Reference number for delivery correspondence. Often null in observed data; purpose may be for tracking official delivery letters.
- **Documents** — Array of attached documents related to the question (questions, answers, etc.). Each document has a direct `Url` for download. The `DocumentTypeId` value 26 indicates a question document. Returns empty array `[]` when no documents are attached (not `null`).
- **Sittings** — Array of parliamentary sittings where this question was discussed or answered. For plenary sittings, `CommitteeTitle` is `null` and `SittingTypeId` is 1. For committee sittings, `CommitteeTitle` contains the committee name and `SittingTypeId` is 2. Returns empty array `[]` when the question has not yet been discussed in any sitting (not `null`).

### Schema Notes
- **Empty collections**: Unlike some other endpoints where empty `Items` becomes `null`, both `Documents` and `Sittings` return empty arrays `[]` when no items are present.
- **Localization**: `ToInstitution`, `QuestionTypeTitle`, `StatusTitle`, and `SittingTypeTitle` are localized according to the `LanguageId` parameter. The question `Title` and `From` field may retain their original language regardless of `LanguageId`.
- **Document access**: Document URLs point to SharePoint resources; `IsExported: true` indicates the document is publicly accessible.


---

## GetSittingDetails

### Request
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
      "type": "string",
      "format": "uuid",
      "description": "Sitting identifier from GetAllSittings"
    }
  },
  "required": ["MethodName", "LanguageId", "SittingId"]
}
```

**Parameter casing:** Uses `MethodName` (capital M), `SittingId`, and `LanguageId` (all with capital first letter).

### Response
```json
{
  "type": "object",
  "properties": {
    "StatusId": {
      "$ref": "#/$defs/SittingStatusId"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Localized sitting status (e.g. 'Затворена' for closed)"
    },
    "Location": {
      "type": "string",
      "description": "Physical location/room where sitting is held (e.g. 'Сала 6')"
    },
    "Number": {
      "type": "integer",
      "description": "Sequential sitting number"
    },
    "SittingDate": {
      "$ref": "#/$defs/AspDate"
    },
    "TypeTitle": {
      "type": "string",
      "description": "Localized sitting type (e.g. 'Комисиска седница' for committee sitting)"
    },
    "TypeId": {
      "$ref": "#/$defs/SittingTypeId",
      "description": "Sitting type identifier"
    },
    "CommitteeId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
        {"type": "null"}
      ],
      "description": "Committee identifier (null for plenary sittings)"
    },
    "CommitteeTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee name (null for plenary sittings)"
    },
    "MediaLinks": {
      "type": "array",
      "items": {},
      "description": "Media/video links for the sitting; empty when none available"
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
            ],
            "description": "Often null in practice"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId"
          },
          "DocumentTypeTitle": {
            "type": "string"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether document has been exported/published"
          }
        }
      },
      "description": "Sitting-level documents (e.g. convocation notices)"
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
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
          "description": "May contain XML-like multilingual markup: <MK>...</><AL>...</><EN>...</><FR>...</>"
        },
        "text": {
          "type": "string"
        },
        "type": {
          "$ref": "#/$defs/TreeItemType",
          "description": "ROOT for root agenda node, LEAF for child items"
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
          "description": "See AgendaItemTypeId; null for ROOT nodes"
        },
        "status": {
          "type": "integer",
          "description": "See AgendaItemStatusId; 0 for root, 50=reviewed, 69=new"
        },
        "statusTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
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
          "description": "HTML with material type and proposer info; null for ROOT"
        },
        "children": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
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
              "text": {
                "type": "string"
              },
              "type": {
                "$ref": "#/$defs/TreeItemType"
              },
              "treeItemTypeId": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ]
              },
              "agendaItemType": {
                "type": "integer",
                "description": "See AgendaItemTypeId enum"
              },
              "status": {
                "type": "integer",
                "description": "See AgendaItemStatusId"
              },
              "statusTitle": {
                "type": "string"
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
                ]
              },
              "children": {
                "type": "array",
                "items": {},
                "description": "Nested children (typically empty for LEAF items)"
              },
              "objectId": {
                "anyOf": [
                  {"type": "string", "format": "uuid"},
                  {"type": "null"}
                ],
                "description": "UUID of linked material when objectTypeId=1"
              },
              "objectTypeId": {
                "type": "integer",
                "description": "0=no object, 1=Material"
              },
              "objectTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "e.g. 'Материјал' for materials"
              },
              "objectStatusId": {
                "type": "integer",
                "description": "Material status (see MaterialStatusId)"
              },
              "objectSubTypeId": {
                "type": "integer",
                "description": "Material subtype; e.g. 1=law proposal, 28=reports/analyses"
              },
              "manyAmendments": {
                "type": "boolean"
              },
              "mediaItems": {
                "type": "array",
                "items": {},
                "description": "Media items associated with agenda item"
              },
              "VotingDefinitions": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "Use as VotingDefinitionId for GetVotingResultsForAgendaItem"
                    },
                    "Title": {
                      "type": "string"
                    },
                    "Description": {
                      "type": "string"
                    },
                    "VotingType": {
                      "type": "string",
                      "description": "e.g. 'Јавно' for public voting"
                    },
                    "OverallResult": {
                      "type": "string",
                      "description": "e.g. 'Усвоен' for adopted/passed"
                    }
                  }
                },
                "description": "Voting records for this agenda item; empty when no votes"
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
                      "type": "null"
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
                },
                "description": "Documents associated with agenda item"
              }
            }
          },
          "description": "Agenda items (LEAF nodes) within the sitting"
        },
        "objectId": {
          "type": "null",
          "description": "Null for ROOT node"
        },
        "objectTypeId": {
          "type": "integer",
          "description": "0 for ROOT node"
        },
        "objectTypeTitle": {
          "type": "null",
          "description": "Null for ROOT node"
        },
        "objectStatusId": {
          "type": "integer",
          "description": "0 for ROOT node"
        },
        "objectSubTypeId": {
          "type": "integer",
          "description": "0 for ROOT node"
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
          "items": {}
        },
        "Documents": {
          "type": "array",
          "items": {}
        }
      },
      "description": "Hierarchical tree structure of sitting agenda"
    },
    "Continuations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Number": {
            "type": "integer",
            "description": "May be 0 for continuation sessions"
          },
          "StatusId": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ]
          },
          "StatusTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string"
          }
        }
      },
      "description": "Continuation sittings (empty array if no continuations)"
    },
    "SittingDuration": {
      "anyOf": [
        {"type": "number"},
        {"type": "null"}
      ],
      "description": "Duration of sitting; null for scheduled/incomplete sittings"
    },
    "Absents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Fullname": {
            "type": "string"
          },
          "PoliticalParty": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Political party name or null for independents"
          }
        }
      },
      "description": "MPs absent from the sitting; may be truncated in response with _truncated object"
    },
    "Attendances": {
      "type": "array",
      "items": {},
      "description": "Attendance records (empty for scheduled/future sittings)"
    },
    "DescriptionTypeTitle": {
      "type": "string",
      "description": "Sitting description type label (e.g. 'Комисиска седница')"
    },
    "DescriptionTypeId": {
      "type": "integer",
      "description": "Sitting description type (1=Committee sitting)"
    },
    "Votings": {
      "type": "array",
      "items": {},
      "description": "Voting records at sitting level (empty when no top-level votes)"
    },
    "Structure": {
      "type": "string",
      "description": "Parliamentary term period (e.g. '2024-2028')"
    }
  }
}
```

### Notes

**Request parameters:**
- **SittingId** — UUID of the sitting (from GetAllSittings `Items[].Id`)
- Uses `MethodName` and `LanguageId` (PascalCase), not lowercase variants

**Response structure:**
- Returns detailed sitting information including status, location, date, type, and committee (when applicable)
- **Agenda**: Hierarchical tree structure with root node (type: "ROOT") containing children array of agenda items (type: "LEAF")
  - Leaf nodes link to materials/questions via `objectId` and include status, documents, voting definitions
  - `afterText` provides multilingual reading stage labels in XML-like format: `<MK>text</><AL>text</><EN>text</><FR>text/>`
  - `data` contains HTML-formatted proposer information for materials
- **Absents**: List of MPs absent from the sitting (available for scheduled sittings). `PoliticalParty` may be `null`.
- **Attendances**: Array for attendance tracking (empty for scheduled/future sittings)
- **Votings**: Array of voting results (empty for scheduled sittings; populated after voting occurs)
- **Continuations**: Array of continuation sittings (when sitting is split across multiple sessions)
- **Documents**: Sitting-level documents (e.g. convocation notices) with type 20="Известување за свикување на седница"
- **MediaLinks**: Array of media/video links (empty when no media available)

**Future sitting behavior:**
- For scheduled (StatusId: 1) sittings: `Absents` is pre-populated, `Attendances` and `Votings` are empty arrays
- `SittingDuration` remains `null` until sitting completes

**Committee sittings:**
- When `TypeId: 2`, the sitting is a committee or public discussion. `CommitteeId` and `CommitteeTitle` are populated with the committee details.
- `DescriptionTypeTitle` may provide finer categorization (e.g., "Јавна расправа" = public hearing)

**Agenda item statuses:**
- `status: 50` = Reviewed (Разгледана)
- `status: 69` = New (Нова)
- `status: 0` = Not started/unknown (typically for ROOT node)

**Multilingual content:**
- When `LanguageId: 3` (Turkish) or other language requested, localized strings (StatusTitle, TypeTitle, Location) are returned in that language
- `afterText` may still contain multilingual XML-like markup even when specific language requested

**Absents array:**
- Lists MPs who did not attend. `PoliticalParty` may be `null` for independent MPs or when affiliation not recorded
- Large Absents arrays may be truncated by API with `_truncated` object as last item indicating omitted count

**Document handling:**
- Multiple documents may share the same `DocumentTypeId` (e.g. multiple stenograms)
- `FileName` typically null in practice

**Voting definitions:**
- Each agenda item may have zero or more `VotingDefinitions` with voting event details
- Use `VotingDefinitions[].Id` to retrieve full voting results via `GetVotingResultsForAgendaItem`

**Empty arrays and null handling:**
- `MediaLinks`, `Attendances`, `Votings`, `Continuations`, `Documents` return empty arrays `[]` when empty, not `null`
- `Agenda.afterText`, `Agenda.data`, `Absents[].PoliticalParty`, and other fields are nullable and use `anyOf` with null


---

## GetUserDetailsByStructure

### Request
```json
{
  "methodName": "GetUserDetailsByStructure",
  "userId": "85048fa9-e61b-4eb1-be26-8d537cb1d7c4",
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
  "languageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "FullName": {
      "type": "string"
    },
    "Email": {
      "type": "string"
    },
    "Image": {
      "type": "string",
      "description": "Base64-encoded profile image"
    },
    "MobileNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "PhoneNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Biography": {
      "type": "string",
      "description": "HTML-formatted biographical text with inline tags"
    },
    "RoleId": {
      "type": "integer",
      "description": "See RoleId enum. Example: 1=MP (Пратеник/Пратеничка)"
    },
    "RoleTitle": {
      "type": "string",
      "description": "Localized role title (e.g., 'Пратеник/Пратеничка' for MP)"
    },
    "ElectedFrom": {
      "$ref": "#/$defs/AspDate"
    },
    "ElectedTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "null for current/active mandates"
    },
    "PoliticalPartyId": {
      "type": "string",
      "format": "uuid"
    },
    "PoliticalPartyTitle": {
      "type": "string"
    },
    "Gender": {
      "type": "string",
      "description": "Localized gender string (Машки=Male, Женски=Female)"
    },
    "DateOfBirth": {
      "type": "string",
      "pattern": "^\\d{2}\\.\\d{2}\\.\\d{4}$",
      "description": "DD.MM.YYYY format"
    },
    "Constituency": {
      "type": "string",
      "description": "Electoral constituency number"
    },
    "Coalition": {
      "type": "string",
      "description": "Electoral coalition name"
    },
    "StructureDate": {
      "type": "string",
      "description": "Human-readable parliamentary term range (e.g., '2024 - 2028')"
    },
    "CabinetMembers": {
      "type": "array",
      "items": {}
    },
    "Materials": {
      "type": "array",
      "items": {}
    },
    "Questions": {
      "type": "array",
      "items": {}
    },
    "Delegations": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroups": {
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
          "Description": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
          }
        }
      }
    },
    "Amendments": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present, indicates N additional items not shown"
          }
        }
      },
      "description": "May be truncated with _truncated indicator"
    },
    "Acts": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      },
      "description": "Legislative acts/proposals authored or co-sponsored by the MP"
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "CommitteeId": {
            "type": "string",
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string"
          },
          "Roles": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "type": "integer",
                  "description": "Committee role ID: 6=Chair, 7=Member, 82=Deputy Chair, 83=Deputy Member"
                },
                "Title": {
                  "type": "string",
                  "description": "Localized role title"
                }
              }
            },
            "description": "May contain multiple roles per committee"
          }
        }
      },
      "description": "Committee memberships with roles (MP can have multiple roles in one committee)"
    },
    "CommitteeMemberships": {
      "type": "array",
      "items": {}
    },
    "DelegationMemberships": {
      "type": "array",
      "items": {}
    },
    "DepartmentMemberships": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroupMemberships": {
      "type": "array",
      "items": {}
    },
    "MediaItems": {
      "type": "array",
      "items": {}
    }
  }
}
```

### Per-operation notes

**Request parameters:**
- **userId** — UUID of the MP. Obtain from `GetParliamentMPsNoImage` response Items[].Id
- **structureId** — Parliamentary term UUID. Required. Use `GetAllStructuresForFilter` to obtain valid values. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term
- **languageId** — Requested language (1=Macedonian, 2=Albanian, 3=Turkish). Affects localized text fields (RoleTitle, PoliticalPartyTitle, StatusTitle, Gender)
- **methodName** — Fixed value `"GetUserDetailsByStructure"`

**Response structure:**
- Returns comprehensive MP profile including biographical data, political affiliations, committee roles, and legislative activity
- All relationship arrays (CabinetMembers, Materials, Questions, Delegations, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems) return empty arrays `[]` when no data, not `null`

**Notable field behaviors:**
- **Biography** — HTML-formatted text with inline `<p>` and `<span>` tags. May contain biographical details
- **Image** — Base64-encoded JPEG or PNG image data. Can be very long string (tens of kilobytes)
- **Gender** — Localized text string (e.g., "Машки" for male, corresponding to GenderId 1). In requested language
- **DateOfBirth** — String format DD.MM.YYYY (not AspDate format). Example: "02.03.1974"
- **Constituency** — String value (numeric constituency number, e.g., "6")
- **ElectedTo** — `null` for current/active parliamentary term. Contains AspDate when term has ended
- **MobileNumber / PhoneNumber** — Often `null` when not provided

**Array field notes:**
- **Amendments** — May be truncated with `{"_truncated": N}` object indicating N additional items exist. Uses StatusId 6 (Delivered to MPs) and 12 (Closed). Can be empty `[]` when no amendments
- **Acts** — Array of legislative proposals/laws. Uses same structure as Amendments. Can be empty `[]` when no acts
- **Committees** — Shows all committee memberships. Roles array can have multiple entries per committee when MP holds multiple roles (e.g., both member and deputy). Can be empty `[]` when MP has no committee roles
- **FriendshipGroups** — Descriptions can be empty strings or null. Can be empty `[]` when MP is not part of any friendship groups

**Date format note:**
- ElectedFrom/ElectedTo use AspDate format (`/Date(timestamp)/`)
- DateOfBirth uses DD.MM.YYYY string format (different from AspDate)