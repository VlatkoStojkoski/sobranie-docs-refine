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