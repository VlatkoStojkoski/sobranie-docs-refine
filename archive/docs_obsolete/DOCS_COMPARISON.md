# Docs Comparison: Current vs Archive

Thorough check of `docs/` vs `archive/` documentation.

## File Mapping

| Current (docs/) | Archive | Notes |
|-----------------|---------|-------|
| API_INDEX.md | API.md (partial) | Archive has no separate index; operations are embedded in API.md |
| API_DOCS.md | API.md + API_DOC_FROM_DATA.md + schema_inference.json | Current separates schemas; archive combines with extensive notes |
| openapi.yaml | openapi.yaml | **Identical** (diff shows no differences) |
| ENRICHMENT_REPORT.md | — | New; LLM comparison of collected vs docs |

---

## Structure

### Archive API.md (~1750 lines)
- **Single monolithic file**: General format, Reusable Schemas, Common patterns, Methods
- **$defs**: ~15 reusable schemas with enums and Macedonian labels:
  - AspDate, GenderId, QuestionStatusId, SittingStatusId, AgendaItemTypeId, EventTypeId
  - DocumentTypeId, DescriptionTypeId, MaterialStatusId, ProposerTypeId, MaterialTypeId
  - ProcedureTypeId, MaterialDocumentTypeId, AgendaItemKindId, AgendaItemStatusId
  - ObjectTypeId, ObjectSubTypeId, VotingOverallResult, TerminationStatusTitle
- **Common patterns**: Institutional authors (zero-UUID), plenary vs committee
- **Per method**: Request example, response schema, response example, notes

### Current docs
- **API_INDEX.md** (95 lines): Operations grouped by Catalogs, Listings, Detail, Non-standard
- **API_DOCS.md** (~2600 lines): Request + response schemas only
- **$defs**: AspDate, LanguageId only (minimal)

---

## Operations Coverage

| Operation | Current API_DOCS | Archive API.md |
|-----------|------------------|----------------|
| GetAllApplicationTypes | ✓ | ✓ |
| GetAllCommitteesForFilter | ✓ | ✓ |
| GetAllCouncils | ✓ | ✓ |
| GetAllGenders | ✓ | ✓ |
| GetAllInstitutionsForFilter | ✓ | ✓ |
| GetAllMPsClubsByStructure | ✓ | ✓ |
| GetAllMaterialStatusesForFilter | ✓ | ✓ |
| GetAllMaterialTypesForFilter | ✓ | ✓ |
| GetAllMaterialsForPublicPortal | ✓ | ✓ |
| GetAllParliamentaryGroups | ✓ | ✓ |
| GetAllPoliticalParties | ✓ | ✓ |
| GetAllProcedureTypes | ✓ | ✓ |
| GetAllQuestionStatuses | ✓ | ✓ |
| GetAllQuestions | ✓ | ✓ |
| GetAllSittingStatuses | ✓ | ✓ |
| GetAllSittings | ✓ | ✓ |
| GetAllStructuresForFilter | ✓ | ✓ |
| GetCommitteeDetails | ✓ | ✓ |
| GetCouncilDetails | ✓ | ✓ |
| GetCustomEventsCalendar | ✓ | ✓ |
| GetMPsClubDetails | ✓ | ✓ |
| GetMaterialDetails | ✓ | ✓ |
| GetMonthlyAgenda | ✓ | ✓ |
| GetOfficialVisitsForUser | ✓ | ✓ |
| GetParliamentMPsNoImage | ✓ | ✓ |
| GetParliamentaryGroupDetails | ✓ | ✓ |
| GetPoliticalPartyDetails | ✓ | ✓ |
| GetProposerTypes | ✓ | ✓ |
| GetQuestionDetails | ✓ | ✓ |
| GetSittingDetails | ✓ | ✓ |
| GetUserDetailsByStructure | ✓ | ✓ |
| GetVotingResultsForAgendaItem | ✓ | ✓ |
| GetVotingResultsForAgendaItemReportDocument | ✓ | ✓ |
| GetVotingResultsForSitting | ✓ | ✓ |
| LoadLanguage | ✓ | ✓ |
| **GetAmendmentDetails** | ✗ (index only) | ✓ (request only; "Response schema not yet documented") |

All operations in current docs are also in archive. GetAmendmentDetails has no response schema in either.

---

## Gaps in Current Docs vs Archive

### 1. Missing $defs (enums)
Archive has rich enum definitions used in schemas. Current uses raw types.

| $def | Archive | Current |
|------|---------|---------|
| GenderId | enum [1,2] + labels | integer |
| SittingStatusId | enum [1-6] + labels | integer |
| AgendaItemTypeId | enum [1,2] | integer |
| DocumentTypeId | enum [19,20,40,...] | integer |
| MaterialStatusId | enum [0,6,9,...] | integer |
| MaterialTypeId | enum [1,2,...] | integer |
| ProcedureTypeId | enum [1,2,3] | integer |
| QuestionStatusId | enum [17,19,20,21] | integer |
| ProposerTypeId | enum [1,2,4] | integer |
| AgendaItemKindId, AgendaItemStatusId, etc. | present | absent |

**Impact**: Archive is more precise for validation; current is simpler but less descriptive.

### 2. Missing Common patterns
Archive documents:
- **Institutional authors**: `Authors[].Id` = `"00000000-0000-0000-0000-000000000000"` with full name in FirstName, empty LastName
- **Plenary vs committee**: `CommitteeId`/`CommitteeTitle` null for plenary (TypeId 1)

Current: Authors zero-UUID pattern is in GetAllMaterialsForPublicPortal item description only.

### 3. Missing response examples
Archive includes JSON examples for many methods (e.g. GetAllSittings, GetSittingDetails). Current has none.

### 4. Missing "required" arrays
Archive schemas often have `"required": ["Id", "Name"]` etc. Current schemas omit required.

### 5. Missing per-method notes
Archive has extensive notes per method, e.g.:
- GetAllSittings: TypeId, CommitteeId filters, Structure null in list, TotalRows always 0
- GetSittingDetails: Agenda structure, VotingDefinitions vs Votings, multilingual text tags
- GetAllStructuresForFilter: No Title/Name (unlike other catalogs)

Current: Minimal inline descriptions only.

### 6. GetSittingDetails Agenda schema
Archive has full Agenda schema (beforeText, afterText, treeItemTypeId, agendaItemType, status, children, VotingDefinitions, etc.). Current has `items: {}` for Agenda nested structure.

### 7. GetMaterialDetails
Archive has more detail on Committees (IsLegislative, IsResponsible, Documents). Current has similar but some `items: {}` placeholders.

---

## Where Current Docs Are Better

### 1. Organization
- **Index + schemas** split is cleaner than one 1750-line file
- Easier to find an operation in API_INDEX.md

### 2. Request documentation
- Current documents **request** for every operation (archive sometimes omits)
- LoadLanguage: Current documents empty body; archive says "Empty {} or no body"

### 3. GetUserDetailsByStructure
- Archive: "Response schema not fully documented"
- Current: **Full schema** from collected data (FullName, Email, CabinetMembers, Materials, etc.)

### 4. GetCouncilDetails Materials
- Archive: `"Materials": { "items": {} }`
- Current: Full Materials items schema (Id, Title, RegistrationDate, etc.) — added from enrichment

### 5. Recent enrichments
- GetCustomEventsCalendar `__type` documented
- Authors zero-UUID pattern in GetAllMaterialsForPublicPortal
- GetParliamentMPsNoImage UserImg note
- GetMonthlyAgenda Type description (1=Assembly, 2=Committee)
- GetAllSittings CommitteeTitle/SittingDescriptionTypeTitle as `["string","null"]`

### 6. API_INDEX enhancements
- GetProposerTypes Order field
- LoadLanguage response description
- GetCustomEventsCalendar, GetOfficialVisitsForUser response structure

---

## OpenAPI (openapi.yaml)

** docs/openapi.yaml and archive/openapi.yaml are identical.**

Both include:
- Non-standard paths (GetCustomEventsCalendar, LoadLanguage, GetOfficialVisitsForUser)
- MakePostRequest with method examples
- Components/schemas (AspDate, RpcRequest, etc.)
- Most operations as requestBody examples

---

## Recommendations

1. **Consider porting $defs**: Add enum definitions from archive to API_DOCS.md (or a new DEFS.md) for better validation and readability.
2. **Add Common patterns**: Introduce a short "Common patterns" section (institutional authors, plenary vs committee).
3. **Add GetAmendmentDetails schema**: When response data is collected, add to API_DOCS.md.
4. **Enrich GetSittingDetails Agenda**: Expand Agenda children schema from archive if needed for tooling.
5. **Optional: response examples**: For key operations, add one example from collected data.
6. **Regenerate openapi.yaml**: After API_DOCS changes, run `generate_openapi.py` to refresh openapi.yaml (currently identical to archive).
