# API Exploration Findings

Open-ended LLM exploration across all documentable endpoints.
Completed 43 tasks.

---

## GetSittingDetails

*Number=85 TypeId=1 StatusId=1 CommitteeTitle=None*

Looking at this North Macedonian Parliament API response, here are several noteworthy observations for documentation improvement:

## Date Format Issues
• `SittingDate: "/Date(1771408800000)/"` - Uses Microsoft JSON date format, but timestamp appears to be in far future (2026+) for a sitting #85, suggesting possible timezone or epoch issues

## Nested Structure Patterns
• `Agenda` uses tree structure with `type: "ROOT"` vs `type: "LEAF"` - document these enum values
• `Agenda.children[]` can be empty arrays vs other collections that are null when empty (inconsistent null/empty pattern)

## Multilingual Content
• `afterText` contains structured multilingual tags: `<MK>Прво читање</><AL>Leximi i parë</><EN>First reading</><FR>Première lecture</>` - this XML-like format should be documented

## Undocumented/Unclear Fields  
• `Structure: "2024-2028"` - appears to be parliamentary term, not documented in context
• `agendaItemType: 1` vs `agendaItemType: null` - enum values need documentation
• `euCompatible: true/false` - interesting field indicating EU legislation compatibility
• `manyAmendments: false` - boolean field purpose unclear
• `objectStatusId` values (6, 9) vs `objectSubTypeId` values (22, 1) - enum mappings needed

## Status and Type Inconsistencies
• Root agenda has `objectTypeId: 0` while children have `objectTypeId: 1` - zero vs null semantics unclear
• `StatusId: 1` maps to "Закажана" (Scheduled) but many nested items have `status: 0` with `statusTitle: null`

## Data Truncation
• `Absents` shows `_truncated: 121` indicating 121+ absent members - significant attendance issue worth noting
• Empty arrays for `Attendances`, `Votings`, `MediaLinks` suggest sitting hasn't occurred yet

---

## GetSittingDetails

*Number=84 TypeId=1 StatusId=1 CommitteeTitle=None*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Date Format Issues
• `SittingDate: "/Date(1770717600000)/"` - Uses Microsoft JSON date format, but the timestamp (1770717600000) converts to January 1, 2026 - likely a future/test date that should be documented as an edge case

## Enum Values & Status Patterns
• `StatusId: 1` with `StatusTitle: "Закажана"` (Scheduled) - new status value to document
• `objectStatusId: 9, 10` in agenda items - undocumented status values
• `objectSubTypeId: 1, 8, 10` - undocumented subtype classifications
• `agendaItemType: 1` - appears consistently but undocumented
• `status: 0` vs `StatusId: 1` - inconsistent status field naming/values

## Multilingual Content Structure
• `afterText` field contains structured multilingual data:
  - `"<MK>второ читање</><AL>Leximi i dytë</><EN>Second Reading</><FR>Deuxième lecture</>"`
  - Uses XML-like tags for language codes (MK/AL/EN/FR) - this markup pattern should be documented

## Null vs Empty Array Patterns
• `MediaLinks: []` vs `CommitteeId: null` - inconsistent null handling
• `children: []` for leaf nodes vs `null` values elsewhere
• `Attendances: []` while `Absents` has 121+ truncated items - suggests attendance tracking may be incomplete

## Nested Structure Complexity
• `Agenda.children[].data` contains HTML: `"<div>[Предлог закон] - Фатмир Лимани, министер...</div>"` - HTML content structure undocumented
• `objectTypeTitle: "Материјал"` (Material) - appears for all agenda items, may be default value

## Field Documentation Gaps
• `Structure: "2024-2028"` - parliamentary term identifier, undocumented
• `euCompatible: false` - EU compatibility flag, undocumented
• `manyAmendments: false` - amendment tracking flag, undocumented
• `IsExported: true` in Documents - export status flag, undocumented

---

## GetSittingDetails

*Number=83 TypeId=1 StatusId=3 CommitteeTitle=None*

Looking at this North Macedonian Parliament sitting details response, here are notable findings for API documentation:

## Date Format Issues
• `SittingDate`: Uses non-standard `/Date(1769691924000)/` format instead of ISO 8601
• `Continuations[].SittingDate`: Same problematic format
• Both dates appear to be in the future (2026) - possibly test data or incorrect timestamps

## Null vs Empty Patterns
• `MediaLinks`: Empty array `[]` when no media
• `CommitteeId`/`CommitteeTitle`: `null` for plenary sessions
• `FileName`: Consistently `null` across all documents (field may be unused)
• `SittingDuration`: `null` (unclear if this means unavailable or zero duration)

## Multilingual Content
• `afterText` contains structured multilingual tags: `<MK>второ читање</><AL>Leximi i dytë</><EN>Second Reading</><FR>Deuxième lecture</>`
• Pattern suggests `<LANG_CODE>text</LANG_CODE>` format for multiple languages

## Agenda Structure Complexity
• Hierarchical tree with `ROOT` and `LEAF` types
• `agendaItemType`: Uses numeric codes (1 = agenda item)
• `status`: Numeric with corresponding `statusTitle` (50 = "Разгледана")
• `data` field contains HTML with bracketed metadata: `<div>[Предлог закон] - м-р Гордана Димитриеска - Кочоска, министер за финансии</div>`

## Voting Information
• Appears in both `Agenda.children[].VotingDefinitions[]` and top-level `Votings[]`
• Potential duplication - unclear which is canonical
• `VotingType`: "Јавно" (Public), `OverallResult`: "Усвоен"/"Одбиен" (Adopted/Rejected)

## Undocumented Fields
• `Structure`: "2024-2028" (likely parliamentary term)
• `euCompatible`: Boolean flag on agenda items (EU compliance indicator?)
• `manyAmendments`: Boolean (amendment count threshold indicator?)
• `IsExported`: Boolean on documents (publication status?)

## Attendance Data
• Separate `Absents[]` and `Attendances[]` arrays with identical structure
• 35 absents vs 90 attendees (including 4 truncated) suggests low attendance

---

## GetSittingDetails

*Number=82 TypeId=1 StatusId=3 CommitteeTitle=None*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation:

## Date Format Issues
• **SittingDate**: Uses Microsoft JSON date format `/Date(1769680800000)/` (timestamp: Jan 29, 2026) - this appears to be future-dated data, possibly test data

## Multilingual Content Patterns
• **afterText** field contains structured language markers: `"<MK></><AL></><EN></><FR></>"` - suggests multilingual content placeholders that should be documented

## Null vs Empty Patterns
• **MediaLinks**: Empty array `[]`
• **CommitteeId/CommitteeTitle**: `null` values when not committee sitting
• **Continuations**: Empty array `[]` 
• **Votings**: Empty array `[]`
• Various agenda fields: `null` (beforeText, treeItemTypeId, data, objectId)

## Agenda Structure Complexity
• **Agenda**: Deeply nested tree structure with ROOT → LEAF hierarchy
• **agendaItemType**: Integer enum (value: 4 = "Поставување на пратенички прашања")
• **status**: Integer enum (69 = "Нова" status)
• **type**: String enum ("ROOT", "LEAF")

## Attendance Data
• **Absents**: 31 total members (27 truncated)
• **Attendances**: 94 total members (90 truncated)
• Both include **PoliticalParty** field with party names in Macedonian

## Potential Documentation Gaps
• **Structure** field: "2024-2028" appears to indicate parliamentary term
• **IsExported** boolean on documents - purpose unclear
• **euCompatible** boolean consistently `false` - EU compliance indicator?
• **manyAmendments** boolean - threshold for "many" undefined

## Document URLs
• Follow pattern: `https://sp.sobranie.mk/sites/2023/sittings/{sessionId}/Documents/{docId}.doc`
• **FileName** consistently `null` while **Title** populated

---

## GetSittingDetails

*Number=72 TypeId=1 StatusId=5 CommitteeTitle=None*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Date Format Issues
• **SittingDate**: Uses non-standard `/Date(1766751351000)/` format instead of ISO 8601 - needs documentation
• **Continuations[].SittingDate**: Same format issue - appears to be milliseconds since Unix epoch wrapped in `/Date()/`

## Inconsistent Null Handling
• **Continuations[].StatusId**: Inconsistent - main record has `StatusId: 5` but continuation items have `StatusId: null` despite having `StatusTitle`
• **CommitteeId/CommitteeTitle**: Both null for plenary sessions, but unclear if they're always paired
• **FileName**: Always null in Documents array - may be deprecated field

## Undocumented Field Behaviors
• **Agenda.status**: Uses numeric codes (0, 50) without documented enum values
• **Agenda.agendaItemType**: Uses values like 1 without explanation
• **objectSubTypeId**: Values like 22, 8 need enum documentation
• **DocumentTypeId**: Values 19, 43 need mapping to their titles

## Multilingual Content Patterns
• **afterText**: Contains structured multilingual markup `<MK>content</><AL>content</><EN>content</><FR>content</>` - undocumented format
• Language codes and parsing rules need specification

## Array Truncation
• **_truncated**: Convention used but not documented - shows remaining item count
• Applied to Documents (8 more), Agenda children (19 more), Absents (121 more)

## Voting Structure Complexity
• **VotingDefinitions**: Nested within agenda items vs top-level **Votings** array - relationship unclear
• **OverallResult**: "Усвоен" (Adopted) - enum values need documentation

## Missing Field Documentation
• **Absents** vs **Attendances**: Absents populated, Attendances empty - mutually exclusive or different use cases?
• **euCompatible**: Boolean flag without explanation of criteria
• **manyAmendments**: Purpose and threshold unclear

The API would benefit from enum value documentation, date format standardization, and clearer null vs empty array patterns.

---

## GetSittingDetails

*Number=75 TypeId=1 StatusId=5 CommitteeTitle=None*

Looking at this parliamentary sitting details response, here are the noteworthy findings for API documentation:

## Date Format Issues
• `SittingDate` uses non-standard format `/Date(1766750424000)/` instead of ISO 8601
• Future date (2025-12-26) suggests test data or timezone conversion issues
• `Continuations[].SittingDate` uses same problematic format

## Field Inconsistencies
• `Documents[].FileName` is `null` for all items while `Documents[].Title` has values - unclear when FileName would be populated
• `Documents[].DocumentTypeTitle` can contain line breaks (`\r\n`) which may cause display issues
• `Agenda.beforeText` and `Agenda.afterText` are `null` vs empty string inconsistency

## Status Patterns
• `StatusId: 5` maps to `"Затворена"` (Closed) - useful for enum documentation
• `Agenda.children[].status: 50` maps to `"Разгледана"` (Reviewed) - different status system than main sitting
• `Continuations[].StatusId` is `null` but `StatusTitle` is populated - data inconsistency

## Nested Structure Complexities
• `Agenda.children[]` contains rich legislative data with `VotingDefinitions[]` arrays
• `VotingType: "Јавно"` and `OverallResult: "Усвоен"` are consistent enum values worth documenting
• `Agenda.data` contains HTML content that should be documented as such

## Array Patterns
• `MediaLinks` is empty array vs `Continuations` has data - different null handling patterns
• Attendance vs Absents both use same object structure with `PoliticalParty` field

## Missing Documentation
• `Structure: "2024-2028"` field appears undocumented
• `euCompatible: false` field purpose unclear
• `manyAmendments: false` field not explained in context

---

## GetSittingDetails

*Number=143 TypeId=2 StatusId=1 CommitteeTitle=Законодавно-правна комисија*

Looking at this North Macedonian Parliament API response, here are several noteworthy observations for API documentation:

## Date Format Issues
• **SittingDate**: `/Date(1770717600000)/` - This timestamp (2026-02-10) appears to be a future date, suggesting possible test data or timezone conversion issues. The .NET JSON date format should be documented.

## Multilingual Content Patterns
• **Agenda.children[0].afterText**: Contains structured multilingual markup `<MK>...</><AL>...</><EN>...</><FR></>` for Macedonian, Albanian, English, and French translations
• This XML-like markup pattern should be documented as it appears to be a standard format for multilingual fields

## Null vs Empty Array Patterns
• **MediaLinks**: `[]` (empty array)
• **Attendances**: `[]` (empty array) 
• **Votings**: `[]` (empty array)
• **Continuations**: `[]` (empty array)
• **SittingDuration**: `null`
• **Absents**: Has data but shows `_truncated` pattern

## Agenda Structure Complexity
• **Agenda**: Deep nested tree structure with ROOT → LEAF hierarchy
• **Agenda.data**: Contains HTML content `<div>[Предлог закон] - Цветан Трипуновски...</div>`
• Multiple status fields at different levels (some `0`, others `null`)
• **euCompatible**: Boolean flag present at agenda item level

## Inconsistent Field Naming
• **CommitteeId**: Uses GUID format
• **id** vs **Id**: Mixed casing in agenda items (`agenda.id`) vs other objects (`Documents.Id`)

## Potential Edge Cases
• **PoliticalParty**: Can be `null` (see Бојан Петрески)
• **beforeText**: Consistently `null` in this example
• Multiple empty arrays suggest this sitting hasn't occurred yet (status "Закажана" = "Scheduled")

The multilingual markup pattern and mixed null/empty patterns are the most significant documentation gaps.

---

## GetSittingDetails

*Number=14 TypeId=2 StatusId=1 CommitteeTitle=Комисија за земјоделство, шумарство и водостопанство*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation:

## Date Format Issues
• `SittingDate: "/Date(1770716700000)/"` - This .NET JSON date format converts to year 2026, suggesting either test data or a date conversion bug

## Null vs Empty Array Patterns
• `MediaLinks: []` - Empty array for no media
• `Continuations: []` - Empty array for no continuations  
• `Attendances: []` - Empty array (interesting that Absents has data but Attendances is empty)
• `Votings: []` - Empty array for no voting records
• But `Agenda.beforeText: null` - Uses null instead of empty string

## Multilingual Content Structure
• `afterText` contains structured multilingual tags: `"<MK>Прво читање</><AL>Leximi i parë</><EN>First reading</><FR>Première lecture</>"`
• This multilingual format should be documented as it appears to be a standard pattern

## Agenda Tree Structure
• `Agenda` is a hierarchical tree with `ROOT` and `LEAF` types
• `children` array can contain nested agenda items
• `agendaItemType: 1` on leaf items vs `null` on root - enum values need documentation

## Inconsistent Field Patterns  
• Some fields use `Id` suffix (`StatusId`, `TypeId`) while others use full `objectId`
• `PoliticalParty` can be `null` (Александар Марковски) or have party name
• `FileName: null` in Documents but other string fields present

## Undocumented Enum Values
• `agendaItemType: 1` - What other values exist?
• `objectTypeId: 1` with `objectTypeTitle: "Материјал"` - Need full enum mapping
• `DocumentTypeId: 20` for "Известување за свикување на седница" - Complete list needed

## Boolean Flags
• `euCompatible: true` on agenda items - EU compliance indicator
• `manyAmendments: false` - Threshold for this flag unclear
• `IsExported: true` in documents - Export status meaning undefined

---

## GetSittingDetails

*Number=35 TypeId=2 StatusId=2 CommitteeTitle=Комисија за транспорт, дигитална трансформација, животна средина и просторно планирање*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation improvements:

## Date Format Issues
• **SittingDate**: Uses non-standard `/Date(1750320000000)/` format instead of ISO 8601
• **Document titles**: Reference date "19.06.2025" (future date) which seems inconsistent with timestamp format

## Nested Structure Complexity
• **Agenda.children**: Deep nesting with varying object structures - ROOT vs LEAF types have different field populations
• **Agenda item status**: Uses numeric code `50` with title "Разгледана" - enum mapping needed
• **agendaItemType**: Value `4` appears without clear documentation of what this represents

## Null vs Empty Patterns
• **MediaLinks**: Empty array `[]`
• **Attendances**: Empty array `[]` 
• **Continuations**: Empty array `[]`
• **beforeText/afterText**: Mix of `null` and empty string `""`
• **PoliticalParty**: Some members have `null`, others have party names

## Field Inconsistencies
• **FileName**: Consistently `null` across all documents - may be deprecated field
• **objectId/objectTypeId**: Multiple instances of these fields with `null`/`0` values at different nesting levels
• **Structure**: Field "2024-2028" appears to be parliamentary term identifier

## Duplicate Documents
• **Documents array**: Contains 4+ identical stenogram entries with same title/date but different IDs and URLs - unclear if this is intentional or data duplication

## Undocumented Enums
• **StatusId**: `2` = "Започната" 
• **TypeId**: `2` = "Јавна расправа"
• **DocumentTypeId**: `20`, `53` with corresponding titles
• **agendaItemType**: `4` (undocumented meaning)

---

## GetSittingDetails

*Number=11 TypeId=2 StatusId=3 CommitteeTitle=Комисија за здравство*

Looking at this GetSittingDetails API response, here are several noteworthy observations for documentation:

## Date Format Issue
- `SittingDate`: "/Date(1770372000000)/" - This timestamp (February 2026) appears to be a future date, possibly indicating test data or a date formatting issue

## Multilingual Content Pattern
- `afterText` field contains structured multilingual content: `<MK>...</><AL>...</><EN>...</><FR>...</>`
- This pattern should be documented as it provides Macedonian, Albanian, English, and French translations

## Agenda Structure Complexity
- `Agenda` has a hierarchical tree structure with `ROOT` and `LEAF` types
- `children` array can be deeply nested (not shown due to truncation)
- `agendaItemType` uses numeric codes (1 = material type)
- `status` field uses numeric codes (50 = "Разгледана"/Reviewed)

## Inconsistent Null vs Empty Patterns
- `MediaLinks`: empty array `[]`
- `Attendances`: empty array `[]` 
- `Votings`: empty array `[]`
- But `beforeText`: `null`, `afterText`: `null` in root agenda
- `PoliticalParty`: can be `null` (Ana Klimovska) or string value

## Enum Values Not in Documentation
- `StatusId`: 3 = "Завршена" (Finished)
- `TypeId`: 2 = "Комисиска седница" (Committee Session)
- `DocumentTypeId`: 20 = "Известување за свикување на седница"
- `objectTypeId`: 1 = "Материјал", 0 = null case
- `objectSubTypeId`: 28 (undocumented meaning)

## Data Field Contains HTML
- `data` field in agenda items contains HTML: `<div>[Анализи, извештаи, информации и друг материјал] - Фонд за...</div>`

## Missing/Null Fields
- `SittingDuration`: `null` (should document when this is populated)
- `FileName`: `null` in Documents (unclear when this differs from Title)

---

## GetSittingDetails

*Number=10 TypeId=2 StatusId=3 CommitteeTitle=Комисија за еднакви можности на жените и мажите*

Looking at this North Macedonian Parliament API response, here are several noteworthy observations for API documentation:

## Date Format Issues
• `SittingDate`: "/Date(1766653200000)/" - This .NET JSON date format (timestamp: 2025-12-25) seems like a future date for a completed sitting, suggesting possible test data or date handling issues

## Multilingual Content Patterns
• `afterText` field contains structured multilingual markup: `<MK>...</><AL>...</><EN>...</><FR></>` for Macedonian, Albanian, English, and French
• This pattern appears consistent but should be documented as a standard format

## Nested Tree Structure Complexity
• `Agenda` has recursive `children` array structure with ROOT→LEAF hierarchy
• Each agenda item contains duplicate field sets (`mediaItems`, `VotingDefinitions`, `Documents`) at multiple levels
• `objectId` is null at ROOT level but populated at LEAF level

## Status/Type Enumeration Values
• `StatusId`: 3 = "Завршена" (Completed)
• `TypeId`: 2 = "Комисиска седница" (Committee Session)  
• `agendaItemType`: 1 (undocumented meaning)
• `objectTypeId`: 1 = "Материјал" (Material)
• `status`: 50 = "Разгледана" (Reviewed)

## Empty vs Null Patterns
• Consistent use of empty arrays `[]` for: `MediaLinks`, `Continuations`, `Attendances`, `Votings`
• Mixed null values in agenda items: `beforeText: null`, `treeItemTypeId: null`

## Data Truncation Indication
• `Absents` array shows `"_truncated": 24` pattern for indicating additional items

## Potential Issues
• `DescriptionTypeTitle` duplicates `TypeTitle` - possible redundancy
• `SittingDuration` is null despite completed status
• Boolean flags like `euCompatible: false`, `manyAmendments: false` lack context about their purpose

---

## GetSittingDetails

*Number=5 TypeId=2 StatusId=3 CommitteeTitle=Комисија за надзор над спроведување на мерките за следење на комуникациите*

Looking at this North Macedonian Parliament API response, here are several noteworthy observations for API documentation:

## Date Format Issues
• `SittingDate`: "/Date(1751882400000)/" - This .NET JSON date format converts to January 7, 2025, which seems like a **future date** for a completed sitting (StatusId=3, "Завршена"). This could indicate test data or a date parsing issue.

## Multilingual Content Pattern
• `afterText` field contains structured multilingual markup:
  - `<MK>Доставен до пратеници</><AL>Dorëzohet deputetëve</><EN>Submitted to MPs</><FR>Livré aux députés</>`
  - Uses custom XML-like tags for Macedonian, Albanian, English, and French
  - This pattern should be documented as it may appear in other text fields

## Null vs Empty Inconsistencies
• `MediaLinks`: empty array `[]`
• `Continuations`: empty array `[]` 
• `Attendances`: empty array `[]`
• `Votings`: empty array `[]`
• But `PoliticalParty`: `null` for some members (e.g., Виолета Умленска)
• Various text fields use `null` (beforeText, afterText, FileName)

## Enum Values & Status Codes
• `agendaItemType`: 1 (undocumented value)
• `status`: 50 with `statusTitle`: "Разгледана" (new status code)
• `objectTypeId`: 1 with title "Материјал"
• `objectSubTypeId`: 28 (undocumented subtype)
• `objectStatusId`: 6 (undocumented status)

## Data Structure Observations
• `Structure`: "2024-2028" appears to indicate parliamentary term
• `Agenda` has complex nested hierarchy with ROOT/LEAF types
• `data` field in agenda item contains HTML: `<div>[Анализи, извештаи, информации и друг материјал] - Јавно обвинителство на Република Северна Македонија</div>`
• `euCompatible`: false (boolean flag that may need documentation)
• `manyAmendments`: false (another undocumented boolean)

## Array Truncation
• `Absents` array shows "_truncated": 9, indicating 9 more absent members not shown in response

---

## GetMaterialDetails

*TypeTitle=Избори, именување и разрешување на јавни и други функции StatusGroupTitle=Доставен до пратеници ProposerTypeTitle=Влада на Република Северна Македонија*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

**Date Format Issues:**
• `RegistrationDate`: "/Date(1770024442000)/" - This timestamp (2026-02-08) appears to be a future date, suggesting potential data quality issues or incorrect timezone handling
• `SittingDate`: "/Date(1771408800000)/" - Also a future date (2026-02-24), same concern
• Date format uses .NET JSON date serialization - should be documented as milliseconds since epoch wrapped in "/Date()/"

**Inconsistent Author Structure:**
• `ResponsibleAuthor`: "д-р Христијан Мицкоски" (string)
• `Authors[0].FirstName`: "д-р Христијан Мицкоски" (object with FirstName containing full name)
• `Authors[0].LastName`: "" (empty string)
• `Authors[0].Id`: all zeros GUID suggests placeholder/missing data

**Null vs Empty Patterns:**
• `Institution`: "/" (slash as null indicator)
• `ParentTitle`: "" (empty string)
• `ProposerCommittee`: null (actual null)
• `TerminationNote`: null
• Mixed approaches need standardization

**Underdocumented Fields:**
• `DocumentTypeId`: 7, 9 - enum values need mapping documentation
• `SittingTypeId`: 1 corresponds to "Пленарна седница" - needs enum documentation  
• `StatusGroupId`, `ObjectStatusId`: both 0, unclear if meaningful or placeholder
• `IsExported`: true for documents - purpose unclear

**Empty Array Patterns:**
• Multiple amendment and sitting arrays are empty - unclear if this indicates no data vs. different procedural stages

**Edge Cases:**
• `AmendmentsTotalRows`: 0 suggests pagination, but no corresponding pagination fields visible
• `VotingResults`: empty array in sitting - may indicate voting hasn't occurred yet

---

## GetMaterialDetails

*TypeTitle=Оставка на носител на јавна и друга функција StatusGroupTitle=Доставен до пратеници ProposerTypeTitle=Влада на Република Северна Македонија*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Date Format Issues
• **RegistrationDate**: Uses `/Date(1769765629000)/` format - this timestamp (2026-01-30) appears to be a future date, suggesting possible test data or timezone conversion issues
• **TerminationDate**: Currently null, but likely uses same problematic format when populated

## Field Inconsistencies
• **ResponsibleAuthor** vs **Authors array**: Same person "д-р Христијан Мицкоски" appears in both - unclear why author data is duplicated
• **Authors[0].Id**: Uses all-zeros GUID `00000000-0000-0000-0000-000000000000` instead of null, suggesting placeholder/system user
• **Authors[0] name split**: FirstName contains full name "д-р Христијан Мицкоски", LastName is empty string - inconsistent with typical name field usage

## Null vs Empty Patterns
• **Institution**: Uses "/" instead of null for missing data
• **ParentTitle**: Empty string `""` for missing parent
• **ProposerCommittee**: Properly null when not applicable
• **FileName**: Null across all documents (may always be null for this document type)

## Array Behavior
• Multiple reading/sitting arrays (`FirstReadingSittings`, `SecondReadingSittings`, etc.) are empty `[]` - unclear if this is because the resignation doesn't require readings or if they're pending
• **Committees**: Empty array - may indicate resignations bypass committee review

## Undocumented Field Relationships
• **DocumentTypeId** mapping needs documentation: `7="Целосен текст на материјалот"`, `1="Документ"`, `9="Известување за нов материјал до пратеници"`
• **IsExported**: All documents show `true` - unclear what `false` would indicate

## Edge Cases
• **EUCompatible**: `false` for resignation - document whether this field applies to personnel changes or only legislation

---

## GetMaterialDetails

*TypeTitle=Анализи, извештаи, информации и друг материјал StatusGroupTitle=Доставен до пратеници ProposerTypeTitle=Друга институција*

Looking at this API response, here are several documentation-worthy observations:

## Date Handling Issues
• **Future dates in data**: `RegistrationDate` shows `/Date(1769161701000)/` (≈2026) and `SittingDate` shows `/Date(1770120000000)/` (≈2026) - indicates test/sample data or clock issues
• **Date format**: Uses .NET JSON date format `/Date(timestamp)/` rather than ISO 8601

## Field Inconsistencies & Patterns
• **Author representation mismatch**: 
  - `ResponsibleAuthor`: "Регулаторна комисија за домување" (string)
  - `Authors[0].FirstName`: "Регулаторна комисија за домување" (using FirstName for full institution name)
  - `Authors[0].LastName`: "" (empty string)
  - `Authors[0].Id`: all zeros GUID suggests institutional vs. personal author

• **Empty vs null patterns**:
  - `Institution`: "" (empty string)
  - `ParentTitle`: "" (empty string) 
  - `ProposerCommittee`: null
  - `FileName`: null (consistent across all documents)

## Underdocumented Fields
• **StatusGroupId vs ObjectStatusId**: Both set to `6` in sitting - relationship unclear
• **DocumentTypeId values**: `7`, `9`, `52` - enum mapping needs documentation
• **SittingTypeId**: Value `2` = "Комисиска седница" - enum needs documentation
• **IsLegislative**: `false` in committee context - usage criteria unclear

## Array Structure Notes
• **Empty procedural arrays**: `FirstReadingAmendments`, `SecondReadingAmendments`, `FirstReadingSittings`, etc. all empty - suggests this material type bypasses standard legislative readings
• **VotingResults**: Empty array in sitting - may populate for materials requiring votes

## Edge Cases
• **Committee.Documents**: Empty array while main Documents array populated - delegation pattern needs clarification
• **AmendmentsTotalRows**: `0` matches empty amendment arrays - redundant or serves specific purpose?

---

## GetMaterialDetails

*TypeTitle=Предлог закон StatusGroupTitle=Прво читање ProposerTypeTitle=Влада на Република Северна Македонија*

Looking at this North Macedonian Parliament API response, here are several notable observations for API documentation:

## Date Format Issues
• **RegistrationDate**: `/Date(1769693654000)/` - This appears to be a future date (2026) which seems suspicious for a registration date. This .NET JSON date format should be documented with timezone information.
• **Sitting dates** also use this format and should specify timezone (likely CET/CEST for North Macedonia)

## Data Structure Inconsistencies
• **Authors array**: Contains unusual structure where `FirstName` holds the full title/name and `LastName` is empty string
  - `"FirstName": "Цветан Трипуновски, министер за земјоделство, шумарство и водостопанство", "LastName": ""`
  - This suggests the Authors field may be repurposed for different types of proposers

## Document Structure
• **Documents[].FileName**: All documents show `"FileName": null` - unclear when this would be populated vs null
• **Documents[].DocumentTypeId**: All show value `7` with same `DocumentTypeTitle` despite different document types (law text, letter, fiscal assessment, EU compliance statement)

## Empty vs Null Patterns
• **ParentTitle**: Empty string `""`
• **ProposerCommittee**: `null` 
• **TerminationStatusTitle/Note/Date**: All `null`
• Mixed pattern should be standardized (either consistently null or empty string for absent values)

## Committee Structure
• **Committees[].Documents**: Always empty arrays `[]` - unclear when this would be populated
• **IsLegislative** vs **IsResponsible** flags need clearer documentation of their meaning

## Voting Results
• **VotingResults**: Always empty arrays across all sittings - should document when/how these get populated

## Status/ID Relationships
• **StatusGroupId** and **ObjectStatusId** both show value `9` in sittings - unclear if these should always match or represent different concepts

---

## GetMaterialDetails

*TypeTitle=Ратификација на меѓународни договори StatusGroupTitle=Прво читање ProposerTypeTitle=Влада на Република Северна Македонија*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation:

## Date Format Issues
• `RegistrationDate`: "/Date(1768567757000)/" - This timestamp (2026-01-16) appears to be in the future, suggesting either test data or clock synchronization issues
• `SittingDate`: "/Date(1770717600000)/" - Also future-dated (2026-02-10)
• Date format uses .NET JSON serialization format that may need client-side parsing

## Data Inconsistencies
• `Authors[0].Id`: "00000000-0000-0000-0000-000000000000" - Using null GUID instead of actual ID
• `Authors[0].FirstName`: Contains full title "д-р Тимчо Муцунски, министер за надворешни работи и надворешна трговија" 
• `Authors[0].LastName`: Empty string - inconsistent with FirstName usage
• `ResponsibleAuthor` field duplicates the author name but as a string rather than object

## Empty vs Null Patterns
• `ProposerCommittee`: null
• `ParentTitle`: empty string ""
• `FileName`: null (across all Documents)
• Various amendment/sitting arrays are empty `[]` rather than null

## Committee Structure
• `Committees[].Documents[]`: Always empty in this response - unclear if this field is populated elsewhere
• `IsLegislative` vs `IsResponsible` flags appear mutually exclusive in this example

## Status/Voting Fields
• `StatusGroupId`, `ObjectStatusId`: Both 0 - unclear if this represents "pending" or actual enum values
• `VotingResults[]`: Empty array suggests voting hasn't occurred yet for first reading

## Undocumented Enum Values
• `DocumentTypeId`: 7, 9 - Would benefit from enum documentation
• `SittingTypeId`: 1 corresponds to "Пленарна седница"

---

## GetMaterialDetails

*TypeTitle=Предлог закон StatusGroupTitle=Прво читање ProposerTypeTitle=Влада на Република Северна Македонија*

Looking at this North Macedonian Parliament API response, here are noteworthy findings for documentation:

## Date Format Issues
• **RegistrationDate**: `/Date(1760351804000)/` - This timestamp converts to ~October 2025, which seems like a future date bug
• **SittingDate** values: `/Date(1763024400000)/` and `/Date(1763460000000)/` - These convert to January 2026, also future dates
• Document titles reference "13.11.2025" which confirms future date inconsistencies

## Null vs Empty Patterns
• **ProposerCommittee**: `null` when government proposes (vs committee)
• **ParentTitle**: Empty string `""` instead of `null`
• **CommitteeId/CommitteeTitle**: `null` for plenary sessions, populated for committee sessions
• **FileName**: Consistently `null` across all documents (may be unused field)
• **Amendment arrays**: Empty `[]` when none exist
• **VotingResults**: Empty `[]` in all sittings (possibly populated elsewhere)

## Data Structure Observations
• **Authors array**: Contains government minister with unconventional structure - full title in `FirstName`, empty `LastName`
• **Authors.Id**: All zeros GUID `00000000-0000-0000-0000-000000000000` for government proposals
• **Committee roles**: `IsResponsible` vs `IsLegislative` flags clearly distinguish committee types
• **StatusGroupId/ObjectStatusId**: Both set to `9` across all sittings (unclear distinction)

## Enum Values Found
• **SittingTypeId**: `1` (Пленарна седница), `2` (Комисиска седница)  
• **DocumentTypeId**: `7`, `9`, `52` with corresponding titles
• **ProcedureTypeTitle**: "Редовна постапка" (Regular procedure)

## Potential Documentation Gaps
• **EUCompatible**: Boolean field significance unclear
• **IsExported**: Present on all documents, purpose undocumented
• **AmendmentsTotalRows**: `0` - likely count field for pagination

---

## GetMaterialDetails

*TypeTitle=Предлог закон StatusGroupTitle=Второ читање ProposerTypeTitle=Пратеник*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation:

## Date Format Issues
• **RegistrationDate**: Uses non-standard `/Date(1769691810000)/` format instead of ISO 8601
• Timestamp `1769691810000` appears to be in the future (2026), suggesting test data or clock issues

## Data Consistency Patterns
• **Empty vs null handling**: Mixed patterns
  - `Institution`: empty string `""`
  - `ProposerCommittee`: explicit `null`
  - `ParentTitle`: empty string `""`
  - `TerminationNote`: explicit `null`

## Committee Structure
• **Documents array**: Always empty `[]` in both committees - unclear if this is normal or indicates missing data
• **IsLegislative vs IsResponsible**: Mutually exclusive in this example - worth documenting if this is always the case

## Amendment Arrays
• **All amendment arrays empty**: `FirstReadingAmendments`, `SecondReadingAmendments` all `[]`
• **AmendmentsTotalRows**: `0` confirms no amendments, but redundant with empty arrays

## Document Structure
• **FileName**: Always `null` despite documents having URLs - unclear purpose
• **IsExported**: Always `true` in examples - document when this would be `false`

## Sitting Arrays
• **All sitting arrays empty**: `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings`, `Sittings`
• Unclear relationship between specific reading sittings and general `Sittings` array

## Truncation Indicator
• **Authors array**: Uses `{"_truncated": 2}` object - document this pagination pattern for API consumers

---

## GetMaterialDetails

*TypeTitle=Предлог закон StatusGroupTitle=Второ читање ProposerTypeTitle=Пратеник*

Looking at this North Macedonian Parliament API response, here are noteworthy observations for API documentation:

## Date Format Issues
• **RegistrationDate**: Uses non-standard `/Date(1769607001000)/` format instead of ISO 8601
• Timestamp `1769607001000` converts to year 2026 (January 28, 2026) - likely a future date or data issue

## Null vs Empty Patterns (Inconsistent)
• **Institution**: Empty string `""`
• **ProposerCommittee**: `null`
• **ParentTitle**: Empty string `""`
• **TerminationStatusTitle**, **TerminationNote**, **TerminationDate**: All `null`
• Need to document when fields use empty strings vs null values

## Array Truncation Pattern
• **Authors** array shows `{"_truncated": 2}` as last element indicating 2 more items exist
• Other arrays (FirstReadingAmendments, SecondReadingSittings, etc.) are empty `[]`
• Document this truncation mechanism and how to retrieve full data

## Committee Structure
• **IsLegislative** vs **IsResponsible** flags - document the difference
• "Законодавно-правна комисија" has `IsLegislative: true, IsResponsible: false`
• "Комисија за економски прашања..." has `IsLegislative: false, IsResponsible: true`

## Document Fields
• **FileName**: Always `null` in examples - document when this would be populated
• **DocumentTypeId**: Numeric IDs (7, 9) - need enum documentation for all possible values

## Status/Type Fields
• **ProcedureTypeTitle**: "Скратена постапка" (shortened procedure) - document all possible values
• **EUCompatible**: Boolean field - document criteria for this flag

## Termination Fields
• All termination-related fields are `null` for active proposals - document when these get populated

---

## GetMaterialDetails

*TypeTitle=Предлог закон StatusGroupTitle=Второ читање ProposerTypeTitle=Пратеник*

Looking at this North Macedonian Parliament API response, here are several areas that could improve documentation:

## Date Format Issues
• **RegistrationDate**: Uses non-standard `/Date(1769596048000)/` format instead of ISO 8601 - this appears to be a future date (2026) which seems suspicious
• **TerminationDate**: Shows `null` but unclear if this would use same problematic date format when populated

## Inconsistent Null vs Empty Patterns
• **Institution**: Empty string `""` vs **ProposerCommittee**: `null` - should be consistent
• **ParentTitle**: Empty string vs **TerminationStatusTitle**: `null` 
• **FileName**: Consistently `null` across all documents - may be vestigial field

## Undocumented Array Structures
• Multiple empty arrays without clear purpose: `FirstReadingAmendments`, `SecondReadingAmendments`, `FirstReadingSittings`, `SecondReadingSittings`, `ThirdReadingSittings`, `Sittings`
• **Authors** array truncated (`_truncated: 3`) - unclear what full structure contains
• **Committees[].Documents**: Empty arrays - unclear what document types would appear here vs main Documents array

## Document URL Patterns
• **Documents[].Url**: Mix of auto-generated filenames (`639052828064737923.docx`) vs descriptive ones (`Priklucuvanje%20kon%20materijal%20(2).doc`)
• Some URLs have timestamp suffixes (`-20260130142510272.doc`) - pattern undocumented

## Missing Field Documentation
• **ResponsibleAuthor** vs **Authors** array relationship unclear
• **EUCompatible**: Boolean purpose not obvious from context
• **AmendmentsTotalRows**: Shows 0 but relationship to empty amendment arrays unclear
• **IsExported** flag on documents - meaning and implications undocumented

## Committee Structure
• **IsLegislative** vs **IsResponsible** flags - mutual exclusivity rules unclear

---

## GetMaterialDetails

*TypeTitle=Избори, именување и разрешување на јавни и други функции StatusGroupTitle=Затворен ProposerTypeTitle=Работно тело*

Looking at this North Macedonian Parliament API response, here are several documentation-worthy observations:

## Date Format Issues
• **Inconsistent/Invalid dates**: `RegistrationDate` shows `/Date(1769173240000)/` which converts to year 2026 - likely a data error or different epoch
• **Date format**: Uses Microsoft JSON date format `/Date(timestamp)/` rather than ISO 8601

## Field Patterns & Nulls
• **Null vs empty patterns**:
  - `ResponsibleAuthor`: null
  - `Institution`: empty string ""
  - `ParentTitle`: empty string ""
  - `Committees`: empty array []
  - `Authors`: empty array []
• **Inconsistent committee references**: `CommitteeId` and `CommitteeTitle` are null in sittings, but `ProposerCommittee` is populated at root level

## Undocumented/Unclear Fields
• **`IsExported`**: All documents show `true` - unclear what this indicates
• **`FileName`**: All documents show `null` despite having URLs - when is this populated?
• **`StatusGroupId` and `ObjectStatusId`**: Both show `0` in sittings - are these meaningful or placeholder values?
• **`EUCompatible`**: Boolean field not explained - what criteria determine this?

## Data Inconsistencies
• **Duplicate sittings**: Two entries for "83. седница" with different dates but same sitting number
• **Empty voting results**: `VotingResults` arrays are empty - unclear if this means no votes occurred or data not available
• **Amendment arrays**: Multiple amendment-related arrays are empty but `AmendmentsTotalRows: 0` suggests this is intentional

## Missing Documentation
• **Document type IDs**: Values like 1, 7, 8, 9 need enum mapping
• **Sitting type IDs**: `SittingTypeId: 1` needs enum documentation
• **Termination statuses**: "Донесен" appears to be an enum value needing documentation

---

## GetMaterialDetails

*TypeTitle=Интерпелација StatusGroupTitle=Затворен ProposerTypeTitle=Пратеник*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Date Format Issues
• **Inconsistent date values**: `RegistrationDate` shows `/Date(1751357315000)/` which converts to ~2025, likely incorrect for a parliamentary document
• **Future dates in Sittings**: Both sitting dates are in 2025 (`/Date(1753779600000)/`, `/Date(1753964119000)/`) - may indicate timestamp format issues or test data

## Field Documentation Gaps
• **`ResponsibleAuthor` vs `Authors`**: Response shows "Димитар Апасиев" as ResponsibleAuthor and also in Authors array - relationship unclear
• **`Institution`**: Present but empty string - document when this field is populated vs empty
• **`ParentTitle`**: Empty string - needs documentation on parent/child material relationships
• **`EUCompatible`**: Boolean field not mentioned in request context - document purpose and usage

## Inconsistent Null/Empty Patterns
• **`ProposerCommittee`**: null
• **`Institution`**: empty string ""  
• **`ParentTitle`**: empty string ""
• **`Committees`**: empty array []
• **Inconsistent empties**: Mix of null vs empty string vs empty array for "no data" scenarios

## Voting/Status Fields
• **`VotingResults`**: Empty arrays in Sittings - document structure when populated
• **Unused status fields**: `StatusGroupId: 0`, `ObjectStatusId: 0` in Sittings may need enum documentation
• **Reading arrays**: `FirstReadingAmendments`, `SecondReadingAmendments`, etc. all empty - document when these populate

## Document Structure
• **`FileName`**: Always null in Documents array - document when this field is used vs Url
• **`DocumentTypeId` values**: Seen 1, 7, 9, 68 - needs complete enum mapping

## Termination Data
• **`TerminationNote`**: Contains detailed procedural text in Macedonian - document if this follows standard formats or is free-text

---

## GetMaterialDetails

*TypeTitle=Интерпелација StatusGroupTitle=Доставен до пратеници ProposerTypeTitle=Пратеник*

Looking at this North Macedonian Parliament API response, here are several documentation-worthy observations:

**Date Format Issues:**
• `RegistrationDate` uses Microsoft JSON date format `/Date(1748938381000)/` - this timestamp (2025-05-04) appears to be in the future, suggesting either test data or a date formatting issue

**Null vs Empty Patterns:**
• `ProposerCommittee` is explicitly `null`
• `Institution` is empty string `""`
• `ParentTitle` is empty string `""`
• Multiple array fields (`Committees`, `FirstReadingAmendments`, etc.) are empty arrays `[]`
• `TerminationStatusTitle`, `TerminationNote`, `TerminationDate` are all `null`

**Document Structure:**
• `Documents[].FileName` is `null` despite having accessible URLs
• `Documents[].Url` points to SharePoint with encoded paths containing timestamps
• `DocumentTypeId` uses integer values (7, 9) that map to descriptive titles

**Array Truncation:**
• `Authors` array shows truncation pattern `{"_truncated": 4}` indicating 4 additional items not displayed
• Other reading/sitting arrays are empty, unclear if this represents no data or truncated empty results

**Procedural Fields:**
• Multiple reading-specific arrays (`FirstReadingAmendments`, `SecondReadingAmendments`, `ThirdReadingSittings`) suggest complex legislative workflow tracking
• `AmendmentsTotalRows: 0` implies pagination/counting mechanism for amendments

**Boolean Fields:**
• `EUCompatible: false` - specialized field for EU compliance tracking
• `IsWithdrawn: false` and `IsExported: true` (in documents) indicate workflow state tracking

**Inconsistent Casing:**
• Author name in `ResponsibleAuthor` field has different casing than in `Authors` array objects

---

## GetAllSittings

*Params: plenary only*

Looking at this North Macedonian Parliament API response, here are the notable findings for documentation:

## Data Patterns & Field Behaviors

• **Date Format**: Uses Microsoft JSON date format `/Date(timestamp)/` instead of ISO 8601 - should be documented as the standard format

• **Null vs Empty Patterns**: 
  - `CommitteeTitle`: null (expected for plenary sessions)
  - `SittingDescriptionTypeTitle`: null 
  - `Continuations`: empty array `[]`
  - `Structure`: null
  - Pattern appears consistent: objects/strings are null when absent, arrays are empty

• **TotalRows Field**: Always 0 across all items - unclear purpose, may be vestigial or used in different contexts

## Enum Values Observed

• **TypeId/TypeTitle**: 
  - `1` = "Пленарна седница" (Plenary Session)

• **StatusId/StatusTitle**:
  - `1` = "Закажана" (Scheduled)
  - `3` = "Завршена" (Completed)
  - Missing status `2` - likely represents "In Progress" or similar intermediate state

## Structural Notes

• **Pagination**: Standard pattern with `TotalItems` (85) and `Items` array
• **Consistent Structure**: All items follow identical schema
• **Location**: Consistently "Сала „Македонија"" (Macedonia Hall) for plenary sessions
• **Numbering**: Sequential descending order (85, 84, 83, 82...)

## Documentation Recommendations

• Document the Microsoft JSON date format requirement
• Provide complete enum mappings for StatusId and TypeId
• Clarify purpose/usage of `TotalRows` field
• Note that `CommitteeTitle` is expected to be null for plenary sessions

---

## GetAllSittings

*Params: committee only*

Looking at this North Macedonian Parliament API response for committee sittings, here are the notable observations for documentation:

## Date Format Issues
• **SittingDate uses legacy .NET format**: `/Date(1770717600000)/` - this timestamp (2026-02-10) appears to be future dates, possibly test data or scheduling far ahead
• **Documentation should specify**: This is .NET's JavaScriptSerializer date format, not ISO 8601

## Enum Values & Localization
• **TypeId/TypeTitle pairs**:
  - `TypeId: 2` = "Комисиска седница" (Committee session)
• **StatusId/StatusTitle pairs**:
  - `StatusId: 1` = "Закажана" (Scheduled)
  - `StatusId: 3` = "Завршена" (Finished)
  - Missing `StatusId: 2` - likely exists but not in this sample
• **All titles in Macedonian Cyrillic** - document expected language/encoding

## Data Patterns
• **Consistent null/empty patterns**:
  - `Continuations: []` (always empty array)
  - `Structure: null` (always null)
  - `TotalRows: 0` (always zero)
• **These fields may be vestigial** or populated in other contexts

## Location Standardization
• **Location always "Сала 6"** in sample - suggest documenting room naming convention

## Committee Titles
• **Full committee names in Macedonian**:
  - "Законодавно-правна комисија" (Legislative-Legal Commission)
  - "Комисија за земјоделство, шумарство и водостопанство" (Agriculture, Forestry & Water Management)
  - etc.

## Missing Documentation Needs
• **Pagination behavior** with 592 total items
• **Whether `committee only` param filters results** or just metadata
• **Purpose of `TotalRows` field** when always 0

---

## GetAllSittings

*Params: committee completed*

Looking at this North Macedonian Parliament API response, here are the notable findings for documentation:

## Date Format Issues
• **SittingDate uses legacy .NET JSON format**: `/Date(1770372000000)/` - this is problematic as it represents dates far in the future (2026+), likely indicating test data or date parsing issues
• **Recommend documenting expected date format**: Should clarify if this is intentional or if ISO 8601 format would be preferred

## Enum Values Discovered
• **TypeId**: `2` = "Комисиска седница" (Committee session)
• **StatusId**: `3` = "Завршена" (Completed/Finished)
• **Location values**: "Сала 4", "Сала 6" (Room 4, Room 6)

## Data Patterns
• **Structure field**: Consistently `null` across all items - document when this would be populated
• **TotalRows field**: Always `0` - unclear purpose, needs documentation
• **Continuations array**: Always empty `[]` - document structure for when populated
• **CommitteeTitle variations**: Shows different committee names, useful for understanding committee scope

## Pagination Context
• **TotalItems**: 90 total sittings available
• **Response truncated**: Only showing 4 of 90 items, indicating pagination is working
• **Missing pagination fields**: No `page`, `pageSize`, or `hasMore` fields documented

## Consistency
• All items follow identical structure, good consistency
• All sessions are completed committee sessions (StatusId=3, TypeId=2)
• SittingDescriptionTypeTitle appears to duplicate TypeTitle

The response structure is quite consistent, but the date format and several null/zero fields need clarification in documentation.

---

## GetAllSittings

*Params: all scheduled*

Looking at this North Macedonian Parliament API response, here are several notable observations for documentation:

## Date Format Issues
• **SittingDate** uses legacy Microsoft JSON date format `/Date(1771408800000)/` - this should be documented clearly as it's non-standard
• The timestamp `1771408800000` converts to ~2026, suggesting these are future scheduled sittings

## Field Patterns & Nullability
• **CommitteeTitle** is `null` for plenary sessions (TypeId=1) but populated for committee sessions (TypeId=2) - this correlation should be documented
• **SittingDescriptionTypeTitle** follows same pattern - `null` for plenary, matches TypeTitle for committee sessions
• **Structure** is consistently `null` across all items - unclear if this field is deprecated or populated under certain conditions

## Enum Values Identified
• **TypeId**: `1` = "Пленарна седница" (Plenary), `2` = "Комисиска седница" (Committee)
• **StatusId**: `1` = "Закажана" (Scheduled) - only status seen, need other possible values documented

## Structural Oddities
• **TotalRows**: Always `0` - purpose unclear, may be legacy field or populated in different contexts
• **Continuations**: Always empty array - should document when/how this gets populated
• **Number**: Appears to be sitting sequence number, but numbering differs between plenary (84, 85) and committee sessions (14, 143)

## Location Patterns
• Plenary sessions: "Сала „Македонија"" (standardized)
• Committee sessions: "Сала 6" (room numbers)

The API structure is consistent but several fields appear unused in this context, suggesting they may be populated for different sitting types or statuses.

---

## GetAllMaterialsForPublicPortal

*Params: StatusGroupId=6*

Looking at this API response, here are some noteworthy observations for documentation improvements:

## Data Inconsistencies & Patterns

• **Date anomaly**: Item with ID `1b2114f3-72ff-43b5-887e-17316e501592` has a future date report title ("01.07.2025 до 31.12.2025 година") but registration date appears to be from 2025, suggesting either test data or date handling issues

• **Authors array structure**: All authors have the same null GUID (`00000000-0000-0000-0000-000000000000`) with institutional names in `FirstName` field and empty `LastName`, indicating misuse of person-oriented fields for institutional authors

## Field Value Patterns

• **Status field**: Consistently `null` across all items in this status group (StatusGroupId=6), suggesting this field may only populate in other status groups

• **ResponsibleCommittee**: Can be empty string (first two items) or contain committee name, with no apparent correlation to material type

• **ProposerTypeTitle values observed**:
  - "Влада на Република Северна Македонија" (Government)
  - "Друга институција" (Other institution)

• **TypeTitle variations include**:
  - "Избори, именување и разрешување на јавни и други функции"
  - "Оставка на носител на јавна и друга функција" 
  - "Анализи, извештаи, информации и друг материјал"

## Structural Issues

• **TotalItems**: Appears at both root level (96) and item level (`null` for all items), suggesting potential nested pagination structure not being used

• **EUCompatible**: All items show `false` - unclear if this represents actual EU compatibility assessment or default value

• **Registration numbers**: Follow pattern "08-XXXX/1" but vary significantly in the numeric portion (535, 722, 750, 7401)

---

## GetAllMaterialsForPublicPortal

*Params: StatusGroupId=12 closed*

Looking at this North Macedonian Parliament API response, here are several noteworthy findings for documentation:

## Data Quality & Consistency Issues

• **Author data structure inconsistency**: 
  - `Authors[].FirstName` contains full titles like "м-р Гордана Димитриеска - Кочоска, министер за финансии" 
  - `Authors[].LastName` is always empty string `""`
  - This suggests the field mapping doesn't match the actual data structure

• **Placeholder GUIDs**: All `Authors[].Id` values are `"00000000-0000-0000-0000-000000000000"`, indicating these may be placeholder/system-generated rather than real author IDs

## Date Format
• **Non-standard date encoding**: `RegistrationDate` uses .NET JSON date format `/Date(1769173240000)/` instead of ISO 8601 - this should be documented as it requires special parsing

## Field Patterns
• **Null vs Empty distinctions**:
  - `Status` is consistently `null` (may be redundant with StatusGroupTitle)
  - `ResponsibleCommittee` uses empty string `""` when not applicable
  - `ResponsibleAuthor` can be `null` or contain full name/title

• **Unused/unclear fields**: 
  - `TotalItems` at item level is always `null` - purpose unclear
  - `EUCompatible` is consistently `false` across all items

## Enum Values Found
• **ProposerTypeTitle**: "Работно тело", "Влада на Република Северна Македонија"
• **TypeTitle**: "Избори, именување и разрешување на јавни и други функции", "Декларација, резолуција, одлука и препорака", "Предлог закон"
• **StatusGroupTitle**: "Затворен" (closed status as expected from filter)

The author field structure appears to need the most attention in documentation.

---

## GetAllMaterialsForPublicPortal

*Params: MaterialTypeId=1 laws*

Looking at this North Macedonian Parliament API response, here are several noteworthy findings for documentation:

## Date Format Issues
• **RegistrationDate**: Uses non-standard `/Date(1769693654000)/` format instead of ISO 8601
• The timestamp `1769693654000` converts to year 2026, suggesting either test data or future-dated entries

## Inconsistent Author Data Structure
• **Authors[0]** in first item: Has `Id: "00000000-0000-0000-0000-000000000000"` (null GUID) with full name in `FirstName` field and empty `LastName`
• **Authors** in other items: Proper GUIDs with separated `FirstName`/`LastName`
• This suggests different data entry patterns for government vs. individual proposers

## Field Usage Patterns
• **Status**: Always `null` in sample - unclear when this would be populated vs. `StatusGroupTitle`
• **TotalItems**: Always `null` at item level - purpose unclear, possibly vestigial from nested collections
• **ResponsibleAuthor**: Sometimes matches first author exactly, sometimes is a summary/title

## Status Values
• **StatusGroupTitle** enum values found: `"Прво читање"` (First Reading), `"Второ читање"` (Second Reading)

## Proposer Types
• **ProposerTypeTitle** values: `"Влада на Република Северна Македонија"` (Government), `"Пратеник"` (MP/Representative)

## EU Compatibility
• **EUCompatible**: Boolean field - `true` for government proposals, `false` for MP proposals in this sample

## Title Patterns
• Titles may include `"(*)"` and `"по скратена постапка"` (expedited procedure) suffixes

The most critical documentation needs are the date format specification and the dual author data structure patterns.

---

## GetAllMaterialsForPublicPortal

*Params: MaterialTypeId=28 reports*

Looking at this North Macedonian Parliament API response, here are the noteworthy findings for documentation:

## Data Quality Issues
• **Future dates in data**: First item has RegistrationDate `/Date(1769161701000)/` (≈2026) and title mentions "01.07.2025 до 31.12.2025" - suggests test data or data entry errors
• **Date format**: Uses Microsoft JSON date format `/Date(timestamp)/` rather than ISO 8601

## Field Patterns & Null Handling
• **Authors array structure**: All items use placeholder GUID `00000000-0000-0000-0000-000000000000` with institution name in `FirstName` field and empty `LastName` - indicates institutional vs individual author handling
• **Status vs StatusGroupTitle**: `Status` is consistently null while `StatusGroupTitle` has values ("Доставен до пратеници", "Затворен") - suggests Status might be deprecated or unused
• **TotalItems**: Always null at item level, unclear purpose in this context

## Enum Values Observed
• **StatusGroupTitle**: "Доставен до пратеници", "Затворен"
• **ProposerTypeTitle**: "Друга институција" (Other institution)
• **TypeTitle**: "Анализи, извештаи, информации и друг материјал" (consistent across all items for MaterialTypeId=28)

## Structural Consistency
• **EUCompatible**: Consistently false across all items
• **ResponsibleCommittee**: Various parliamentary committees, properly populated
• All required fields appear consistently populated with appropriate data types

The main documentation needs are around the author structure workaround for institutions and clarifying the Status field usage.

---

## GetMonthlyAgenda

*Params: current month*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Date Format Issues
• **Field**: `Start` - Uses legacy Microsoft JSON date format `/Date(1770120000000)/` instead of ISO 8601
• **Problem**: Timestamps appear to be in far future (year 2026) - likely test data or incorrect timezone handling
• **Recommendation**: Document expected date format and timezone handling

## Undocumented Field Details
• **Field**: `Type` - All examples show value `2`, but enum values/meanings not documented
  - What do different Type values represent? (Committee vs Plenary vs Other?)
• **Field**: `Id` - All are UUIDs, but format requirements not specified
• **Field**: `Location` - Mix of simple names ("Сала 6") and quoted names ("Сала „Борис Трајковски"") - document naming conventions

## Structure Inconsistencies
• **Pagination**: Uses non-standard `{"_truncated": 4}` object instead of typical pagination metadata
  - Missing `TotalItems`, `PageSize`, `CurrentPage` fields mentioned in endpoint description
  - Unclear if `_truncated: 4` means "4 more items" or "truncated at 4 items"

## Missing Documentation
• **Language**: All content in Macedonian Cyrillic - document if localization parameters exist
• **Required fields**: No indication which fields are required vs optional
• **Null handling**: No examples showing how null/empty values appear

## Edge Cases to Document
• How are cancelled/rescheduled sessions handled?
• What happens for months with no agenda items?
• Maximum title/location length limits?

The response structure doesn't match the described "TotalItems + Items" format, suggesting documentation is outdated.

---

## GetMonthlyAgenda

*Params: previous month*

Looking at this North Macedonian Parliament API response, here are the notable findings:

## Date Format Issues
• **Suspicious timestamp values**: All entries show `/Date(1768208400000)/` which converts to **January 11, 2026** - this seems like placeholder/test data since the request was for "previous month"
• **Non-standard date format**: Using Microsoft JSON date format `/Date(timestamp)/` instead of ISO 8601 - should be documented clearly

## Field Observations
• **Type field**: All entries show `Type: 2` - documentation should clarify what this enum represents (likely meeting/session types)
• **Title structure**: Appears to follow pattern "Седница бр. [number] на [Committee Name] - [Location]" - could be useful for parsing committee info
• **Location consistency**: Locations include both simple room numbers ("Сала 5") and named halls ("Сала „Борис Трајковски"")

## Response Structure
• **Array format**: Simple array structure (no pagination wrapper with TotalItems/Items despite endpoint description suggesting otherwise)
• **Truncation notation**: Uses `{"_truncated": 37}` to indicate 37 more items - this truncation method should be documented
• **Missing fields**: No end time, duration, or status fields that might be expected for agenda items

## Language/Encoding
• **Macedonian Cyrillic**: All content in Macedonian - ensure UTF-8 encoding is specified in API docs
• **No multilingual support**: No indication of alternative language options

The timestamp issue is the most concerning - either test data is being returned or there's a date calculation problem.

---

## GetParliamentMPsNoImage

*Params: page 1, rows=20*

Looking at this North Macedonian Parliament API response, here are notable findings for documentation improvement:

## Data Structure & Pagination Issues
• **Misleading endpoint name**: Despite being called "GetParliamentMPsNoImage", the `UserImg` field contains large base64-encoded images (130k+ characters each)
• **Non-standard pagination**: Uses two separate arrays (`MembersOfParliament`, `ExpiredMandateMembers`) with separate totals instead of traditional pagination
• **Pagination params ignored**: Request specified `page=1, rows=20` but received 20 current MPs + 13 expired MPs (33 total items)

## Field Inconsistencies
• **Political party data patterns**:
  - Current MPs: Have populated `PoliticalPartyTitle` and `PoliticalPartyId`
  - Expired MPs: Mix of populated vs empty - some have empty string `""` for title and `null` for ID, others have full party data
• **Null vs empty string handling**: `PoliticalPartyTitle` uses empty string `""` while `PoliticalPartyId` uses `null` for missing values

## Undocumented Fields
• **RoleId**: Present in all records with value `1` - appears to be an enum but no documentation of possible values
• **Statistics object**: Contains extensive metadata not mentioned in endpoint description:
  - `TotalNumberOfMaterials`, `NumberOfQuestions`, `NumberOfMaterialsInStructure`
  - `MPsInPoliticalParties` vs `MPsInParliamentaryGroups` distinction (120 vs 110)

## Technical Concerns
• **Performance impact**: Base64 image data makes responses extremely large despite "NoImage" endpoint name
• **Character encoding**: Cyrillic names in `FullName` field - ensure UTF-8 support is documented

---

## GetParliamentMPsNoImage

*Params: page 2*

Looking at this North Macedonian Parliament API response, here are some notable observations for documentation improvement:

## Data Structure & Naming
• **Inconsistent naming**: Endpoint is "GetParliamentMPsNoImage" but response contains `UserImg` fields with full base64 image data (113K+ chars each) - contradicts the "NoImage" naming
• **Mixed language fields**: `FullName` values are in Cyrillic/Macedonian while field names are in English

## Field Documentation Needs
• **RoleId enumeration**: All visible MPs have `RoleId: 1` - needs documentation of what role IDs represent (1 = active MP?)
• **Political party mapping**: Several parties appear:
  - "Левица" (Levica/The Left)
  - "Социјалдемократски сојуз на Македонија" (SDSM)
  - "ВМРО-ДПМНЕ" (VMRO-DPMNE)
• **UserImg format**: Base64 PNG data with consistent prefix `iVBORw0KGgoAAAANSUhEUgAAAMgAAAEsCAYAAACG+vy+AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8...`

## Pagination & Data Consistency
• **Empty vs null patterns**: `ExpiredMandateMembers: []` is empty array, not null
• **Statistics discrepancy**: `TotalNumberOfMPs: 120` vs `TotalNumberOfExpiredMandateMPs: 13` but `ExpiredMandateMembers` is empty - suggests expired members might be filtered out or on different pages

## Potential Issues
• **Performance concern**: Large base64 images in "NoImage" endpoint seems unintentional
• **Missing pagination info**: No indication of current page number or total pages despite being page 2

The most significant issue is the endpoint name suggesting no images while actually returning large image payloads.

---

## GetParliamentMPsNoImage

*Params: politicalPartyId filter*

Looking at this North Macedonian Parliament API response, here are several documentation improvements needed:

## Structure & Naming Inconsistencies
• **Misleading endpoint name**: Called "GetParliamentMPsNoImage" but response contains large base64 `UserImg` data (125K+ chars each)
• **Inconsistent naming**: Main array is `MembersOfParliament` but statistics refer to `TotalNumberOfMPs` and `TotalNumberOfExpiredMandateMPs`

## Undocumented Fields & Patterns
• **RoleId field**: Present in all MPs with value `1` - needs enum documentation (what roles exist? President, Vice-President, regular MP?)
• **Statistics object**: Completely undocumented with 7 fields that seem unrelated to MP listing:
  - `TotalNumberOfMaterials: 10959`
  - `NumberOfQuestions: 517` 
  - `NumberOfMaterialsInStructure: 976`
  - `MPsInParliamentaryGroups: 110` (vs 120 total - what's the difference?)

## Data Consistency Issues
• **Image data contradiction**: Endpoint suggests no images, but massive base64 strings present
• **Statistics mismatch**: 120 total MPs but only 110 in parliamentary groups - needs explanation
• **Empty vs populated arrays**: `ExpiredMandateMembers: []` is empty array, but `MembersOfParliament` has 5 items despite `TotalItems: 6`

## Missing Documentation
• **PoliticalPartyId filter**: All results show same party "Левица" (e693cd9f-5893-49ab-9ede-0abd6e820664) - unclear if filter is working or if this party actually has 6 members
• **UserImg format**: Should document this is PNG base64 data, expected size ranges
• **Pagination**: No obvious pagination fields despite this being noted as a list endpoint

## Data Quality Questions
• **TotalItems vs actual count**: Says 6 total but only 5 items shown (including truncation marker)

---

## GetParliamentMPsNoImage

*Params: genderId=1*

Looking at this North Macedonian Parliament API response, here are the notable findings for documentation improvement:

## Data Structure Issues

• **Inconsistent counts**: `Statistics.TotalNumberOfExpiredMandateMPs: 13` but `TotalItemsExpiredMandate: 11` and only 11 items returned - clarification needed on which count is authoritative

• **Missing pagination info**: No indication if this is paginated data or complete dataset, despite `TotalItems: 71` with only ~20 items shown

## Field Patterns & Null Handling

• **Political party data inconsistency**: 
  - Active MPs have populated `PoliticalPartyTitle` and `PoliticalPartyId`
  - Expired mandate MPs show `"PoliticalPartyTitle": ""` (empty string) and `"PoliticalPartyId": null`
  - Some expired MPs retain party info (e.g., "ВМРО-ДПМНЕ") while others are empty

• **UserImg field**: Contains base64-encoded image data (~100-135k characters) despite endpoint name suggesting "NoImage" - misleading naming

## Undocumented Fields

• **Statistics object** contains fields not mentioned in endpoint description:
  - `TotalNumberOfMaterials: 10959`
  - `NumberOfQuestions: 517` 
  - `MPsInPoliticalParties: 71`
  - `MPsInParliamentaryGroups: 62`
  - `NumberOfMaterialsInStructure: 976`

## Parameter Behavior

• **genderId=1 filter**: Unclear what gender this represents or if other values (0, 2, etc.) are valid - enum documentation needed

• **RoleId field**: All MPs show `"RoleId": 1` - other possible values undocumented

## Language/Encoding

• **Macedonian Cyrillic text** in names and party titles - character encoding requirements should be documented

---

## GetParliamentMPsNoImage

*Params: searchText='а'*

Looking at this North Macedonian Parliament API response, here are notable observations for documentation improvement:

**Data Structure & Pagination:**
• No standard pagination fields (page, limit, offset) - uses direct array truncation instead
• `TotalItems: 107` vs actual `MembersOfParliament` showing ~20 items (16 truncated + 4 visible)
• `TotalItemsExpiredMandate: 11` vs `ExpiredMandateMembers` showing ~11 items (7 truncated + 4 visible)

**Inconsistent Political Party Data:**
• Active MPs have populated `PoliticalPartyTitle` and `PoliticalPartyId` fields
• Expired mandate members show mixed patterns:
  - Some: `"PoliticalPartyTitle": ""` with `"PoliticalPartyId": null` 
  - Others: `"PoliticalPartyTitle": "ВМРО-ДПМНЕ"` with valid GUID
• This null vs empty string inconsistency should be documented

**Image Data Handling:**
• `UserImg` contains base64-encoded images (~100-160k characters each)
• Endpoint name suggests "NoImage" but images are included - naming inconsistency
• Image sizes vary significantly (104k-161k chars) - no apparent standardization

**Statistics Discrepancies:**
• `Statistics.TotalNumberOfMPs: 120` doesn't match `TotalItems: 107`
• `Statistics.TotalNumberOfExpiredMandateMPs: 13` doesn't match `TotalItemsExpiredMandate: 11`
• Unclear if search filtering affects these counts differently

**Missing Documentation:**
• `RoleId: 1` appears consistently but role enum values not documented
• Search behavior: unclear if `searchText='а'` searches names, parties, or both
• No indication of sort order (appears alphabetical by first name)

**Language & Character Encoding:**
• All content in Macedonian Cyrillic - character encoding requirements should be specified
• Political party names use specific formatting that should be preserved

---

## GetParliamentMPsNoImage

*Params: StructureId=09f340db... (different assembly)*

Looking at this API response, I found several noteworthy observations for documentation improvements:

## Data Inconsistencies & Edge Cases

• **Inconsistent totals**: `Statistics.TotalNumberOfExpiredMandateMPs: 6` but `ExpiredMandateMembers` array only contains 3 items and `TotalItemsExpiredMandate: 3` - suggests pagination or filtering

• **Political party data patterns**:
  - Active MPs have populated `PoliticalPartyTitle` and `PoliticalPartyId`
  - Expired mandate MPs show mixed patterns: some have empty string `""` for title with `null` ID, others have full party details

• **Image data handling**: Despite endpoint name "NoImage", many MPs have base64 encoded images in `UserImg` field (100K+ characters), while others have empty string `""`

## Undocumented Fields & Structure

• **Statistics object** contains multiple undocumented metrics:
  - `TotalNumberOfMaterials: 10959`
  - `NumberOfQuestions: 1034` 
  - `MPsInPoliticalParties: 118`
  - `MPsInParliamentaryGroups: 10`
  - `NumberOfMaterialsInStructure: 1994`

• **RoleId field**: All MPs show `RoleId: 1` - enum values/meanings undocumented

• **Dual totals pattern**: `TotalItems` vs `TotalItemsExpiredMandate` suggests separate pagination for each array

## Null vs Empty Patterns

• **PoliticalPartyId**: Uses `null` for missing values
• **PoliticalPartyTitle**: Uses empty string `""` for missing values  
• **UserImg**: Uses empty string `""` when no image present

## Questions for Clarification

• Why does "NoImage" endpoint still return image data?
• Are `MembersOfParliament` and `ExpiredMandateMembers` separately paginated?
• What triggers the different political party null/empty patterns?

---

## GetCustomEventsCalendar

*Params: Month=2 Year=2026*

Looking at this North Macedonian Parliament calendar API response, here are the noteworthy observations for documentation:

## Structure & Data Format
• **Unexpected nesting**: Response is wrapped in a `"d"` property rather than direct array or standard pagination structure
• **No pagination metadata**: Despite being described as a list endpoint with potential pagination, there's no `TotalItems`, page info, or standard pagination fields
• **Future date handling**: API accepts and returns events for 2026 (future years), suggesting it supports scheduled/planned events

## Field Analysis
• **EventDate format**: Uses Microsoft JSON date format `/Date(1770800400000)/` instead of ISO 8601 - should document this legacy format
• **EventType enumeration**: All events show `EventType: 5` - documentation should clarify what this numeric code represents and list all possible values
• **EventLocation variations**: 
  - Formal venue: `"Сала „Борис Трајковски""` (Boris Trajkovski Hall)
  - Functional space: `"Прес-центар"` (Press Center)
• **EventLink patterns**: Appears to be URL slug format, sometimes with date suffixes (e.g., `-622026`, `-222026`)

## Content Patterns
• **Language consistency**: All content is in Macedonian (Cyrillic script)
• **Event type diversity**: Mix of parliamentary oversight events, educational promotions, and press conferences
• **Duplicate descriptions**: Multiple "Прес-конференција за медиуми" events with different IDs and dates

## Missing Documentation
• **EventType enum values**: What do the numeric codes represent?
• **Date format specification**: Document the Microsoft JSON date format expectation
• **EventLink usage**: Is this always a URL slug? Are there formatting rules?

---

## GetCustomEventsCalendar

*Params: Month=10 Year=2025*

Looking at this North Macedonian Parliament calendar API response, here are several documentation-worthy observations:

## Date Format Issues
• **EventDate uses legacy .NET format**: `/Date(1760425200000)/` instead of standard ISO 8601
• **Future dates concern**: Timestamps like `1760425200000` convert to ~October 2025, but request was for October 2025 - should verify if this is intentional or a bug

## Type System & Metadata
• **Unexpected __type field**: `"moldova.controls.Models.CalendarViewModel"` suggests this might be shared code between Moldova and North Macedonia parliaments, or legacy naming
• **EventType enum values**: Only seeing `EventType: 5` across all events - need documentation for other possible values and their meanings

## Structure & Consistency
• **No pagination metadata**: Response is a direct array in `"d"` field with no `TotalItems`, `PageSize`, etc. despite being described as a list endpoint
• **Truncation handling**: The `{"_truncated": 14}` pattern is non-standard - typically APIs use pagination or return full results

## Content Patterns
• **Consistent location format**: All locations follow pattern `Сала "[Name]"` (Hall "[Name]") 
• **EventLink slugification**: Links are URL-friendly Macedonian transliterations (e.g., `edukativna-aktivnost-imam-stav-za-ucenici-od-srednite-ucilista-141025`)
• **Language**: All content is in Macedonian Cyrillic - should document if other language variants exist

## Missing Documentation Needs
• EventType enumeration values and meanings
• Expected date range behavior for future months
• Explanation of the "moldova" namespace reference
• Pagination strategy for large result sets

---

## Catalogs (batch)

*All reference/catalog endpoints combined*

Looking at this North Macedonian Parliament API catalog response, here are the notable findings for documentation:

## Data Inconsistencies & Patterns

• **Mixed ID types**: Some catalogs use integer IDs (`GetAllGenders`, `GetAllMaterialStatusesForFilter`) while others use GUIDs (`GetAllStructuresForFilter`, `GetAllCommitteesForFilter`)

• **Date format**: Uses Microsoft JSON date format `/Date(timestamp)/` in `GetAllStructuresForFilter` - should document this format and conversion requirements

• **Empty Image fields**: `GetAllPoliticalParties` has empty string `"Image": ""` for all entries - unclear if this indicates missing data or intentional empty state

## Field Documentation Gaps

• **GetAllStructuresForFilter**:
  - `IsCurrent` boolean field - only one structure marked as current
  - Date ranges appear to represent parliamentary terms/periods
  - Missing title/name field unlike other catalogs

• **GetProposerTypes**:
  - Has `Order` field not present in other catalogs
  - Only shows 3 entries with orders 1, 2, 4 (missing order 3) - potential data gap

• **GetAllPoliticalParties**:
  - `NumberOfDeputies` field provides current seat count
  - Wide range in deputy counts (1-15 from visible data)

## Potential Edge Cases

• **Committee names**: All in Cyrillic - confirm UTF-8 encoding requirements
• **Material statuses**: Reference legislative reading stages (1st, 2nd, 3rd) - useful for workflow documentation
• **Sitting statuses**: Include "Незавршена" (Unfinished) status - may indicate interrupted sessions

## Completeness Notes

• All catalogs appear well-structured with consistent field naming within each type
• Truncation indicates significant additional data available (27 committees, 35 material types, etc.)

---
