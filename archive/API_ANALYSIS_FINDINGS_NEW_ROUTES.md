# New Routes Schema Analysis

Analyzed 22 responses across new API routes (questions, councils, committees, parties, groups, MPs clubs, voting).

---

## GetAllQuestionStatuses
items=4

[OK] No issues found.

---

## GetAllInstitutionsForFilter
items=24

[OK] No issues found.

---

## GetAllApplicationTypes
items=3

[NEW_ENUM] ApplicationType = 1 (Пријава на случај)
[NEW_ENUM] ApplicationType = 2 (Учество во јавна расправа)
[NEW_ENUM] ApplicationType = 3 (Дискусија)

---

## GetAllCouncils
items=3

[NEW_ENUM] TypeId = 1 (Постојана)
[INTERESTING] All councils have the same TypeId/TypeTitle, suggesting "Постојана" (Permanent) is the standard council type
[INTERESTING] Council names include specific entities like "Budget Council" and "National Council for European Integration"

---

## GetAllParliamentaryGroups
items=6

[OK] No issues found.

---

## GetAllMPsClubsByStructure
items=9

[OK] No issues found.

---

## GetAllQuestions
StatusId=None | TotalItems=517

[INTERESTING] DateAsked uses ASP.NET JSON date format "/Date(timestamp)/" instead of standard ISO format
[INTERESTING] TotalRows field consistently returns 0 across all items, may be deprecated or unused
[INTERESTING] QuestionTypeTitle shows both "Писмено прашање" (Written) and "Усно прашање" (Oral) question types as documented
[NEW_ENUM] StatusTitle = Доставено (Delivered/Submitted)
[NEW_ENUM] StatusTitle = Одговорено (Answered)

---

## GetAllQuestions
StatusId=17 | TotalItems=64

[INTERESTING] DateAsked uses ASP.NET JSON date format "/Date(timestamp)/" which matches the AspDate reference in schema
[INTERESTING] TotalRows field in items is consistently 0, may indicate unused/deprecated field despite being required
[INTERESTING] All items have StatusTitle "Доставено" (Delivered) and QuestionTypeTitle "Писмено прашање" (Written question), showing filtered results
[INTERESTING] Questions are in Macedonian/Cyrillic script with detailed parliamentary question titles including questioner attribution

---

## GetAllQuestions
StatusId=19 | TotalItems=452

[INTERESTING] DateAsked uses ASP.NET date format "/Date(1769699430000)/" which matches the AspDate reference in schema
[INTERESTING] TotalRows field is consistently 0 across all items, suggesting it may be deprecated or unused
[INTERESTING] All questions shown are "Усно прашање" (Oral question) type, likely due to StatusId=19 filter
[NEW_ENUM] StatusId = 19 (Одговорено)

---

## GetQuestionDetails
QuestionId=0e2039bb...

[INTERESTING] Title field contains a typo "екомомска" (should likely be "економска") in what appears to be a parliamentary question about wine grape subsidies
[NEW_ENUM] DocumentTypeId = 26 (Прашање)
[INTERESTING] Documents array contains only one item with a very long title that appears to be truncated at 255 characters
[INTERESTING] Both FileName fields are null while Url points to a .docx file, suggesting filename extraction may be optional
[INTERESTING] Sittings array is empty, indicating this question may not have been scheduled for parliamentary sessions yet

---

## GetQuestionDetails
QuestionId=919d6c67...

[UNDOCUMENTED] Sittings[].Id — UUID field not documented in empty schema
[UNDOCUMENTED] Sittings[].SittingTypeId — integer field not documented in empty schema
[UNDOCUMENTED] Sittings[].SittingTypeTitle — string field not documented in empty schema
[UNDOCUMENTED] Sittings[].SittingDate — date field not documented in empty schema
[UNDOCUMENTED] Sittings[].CommitteeTitle — nullable string field not documented in empty schema
[UNDOCUMENTED] Sittings[].SittingNumber — integer field not documented in empty schema
[NEW_ENUM] SittingTypeId = 1 (Пленарна седница)
[INTERESTING] SittingDate uses .NET JSON date format: /Date(1769680800000)/
[INTERESTING] Response in Macedonian language, matching LanguageId=1 from typical requests

---

## GetCouncilDetails
committeeId=d596538c...

[OK] No issues found.

---

## GetCouncilDetails
committeeId=2b9df53a...

[INTERESTING] Date format uses .NET JSON serialization format "/Date(milliseconds)/" instead of ISO standard
[INTERESTING] Same person (Горан Котевски) appears twice in SecretariatMembers with different roles (10 and 11)
[INTERESTING] Materials array is empty while other arrays contain data
[INTERESTING] External members listed in Description HTML rather than structured data
[INTERESTING] PhoneNumber is null rather than omitted
[NEW_ENUM] RoleId = 6 (Претседател/Претседателка на комисија)
[NEW_ENUM] RoleId = 82 (Заменик-претседател/Заменик-претседателка на комисија)
[NEW_ENUM] RoleId = 7 (Член/Членка на комисија)
[NEW_ENUM] RoleId = 10 (Одобрувач/Одобрувачка)
[NEW_ENUM] RoleId = 11 (Советник/Советничка на комисија)

---

## GetCommitteeDetails
committeeId=b8b25861...

[UNDOCUMENTED] SecretariatMembers item structure (has UserId, FullName, RoleId, RoleTitle properties but schema shows empty items definition)
[NEW_ENUM] RoleId = 6 (Претседател/Претседателка на комисија)
[NEW_ENUM] RoleId = 82 (Заменик-претседател/Заменик-претседателка на комисија)
[NEW_ENUM] RoleId = 7 (Член/Членка на комисија)
[NEW_ENUM] RoleId = 10 (Одобрувач/Одобрувачка)
[NEW_ENUM] RoleId = 11 (Советник/Советничка на комисија)
[NEW_ENUM] StatusId = 6 (Доставен до пратеници)
[NEW_ENUM] StatusId = 10 (Второ читање)
[NEW_ENUM] StatusId = 12 (Затворен)
[INTERESTING] Same person appears multiple times in SecretariatMembers with different roles (Моника Стојаноска with RoleId 10 and 11)
[INTERESTING] Description contains HTML markup (<p>, <br/> tags)

---

## GetCommitteeDetails
committeeId=f70074b5...

[UNDOCUMENTED] SecretariatMembers.UserId — schema shows empty items object but actual response has structured objects
[UNDOCUMENTED] SecretariatMembers.FullName — not documented in schema
[UNDOCUMENTED] SecretariatMembers.RoleId — not documented in schema  
[UNDOCUMENTED] SecretariatMembers.RoleTitle — not documented in schema
[NEW_ENUM] RoleId = 6 (Претседател/Претседателка на комисија)
[NEW_ENUM] RoleId = 82 (Заменик-претседател/Заменик-претседателка на комисија)
[NEW_ENUM] RoleId = 7 (Член/Членка на комисија)
[NEW_ENUM] RoleId = 10 (Одобрувач/Одобрувачка)
[NEW_ENUM] RoleId = 11 (Советник/Советничка на комисија)
[NEW_ENUM] StatusId = 6 (Доставен до пратеници)
[NEW_ENUM] StatusId = 12 (Затворен)
[INTERESTING] SecretariatMembers has same structure as CompositionMembers despite schema showing empty items
[INTERESTING] Same person appears twice in SecretariatMembers with different roles (Петар Митковски)

---

## GetPoliticalPartyDetails
politicalPartyId=e693cd9f...

[UNDOCUMENTED] Amendments — top-level array field not in documented schema
[UNDOCUMENTED] Questions — top-level array field not in documented schema
[UNDOCUMENTED] Members — top-level array field not in documented schema
[UNDOCUMENTED] Email — top-level field not in documented schema
[UNDOCUMENTED] Phone — top-level field not in documented schema
[UNDOCUMENTED] Image — top-level field not in documented schema
[UNDOCUMENTED] StructureId — top-level field not in documented schema
[NEW_ENUM] StatusId = 10 (Второ читање)
[NEW_ENUM] RoleId = 27 (Член/Членка на политичка партија)
[INTERESTING] Members array contains nested user objects with role information and null count fields
[INTERESTING] Response contains significantly more data than documented schema suggests

---

## GetPoliticalPartyDetails
politicalPartyId=81baa692...

[UNDOCUMENTED] Amendments — array field not in documented schema
[UNDOCUMENTED] Questions — array field not in documented schema
[UNDOCUMENTED] Members — array field not in documented schema
[UNDOCUMENTED] Email — field not in documented schema
[UNDOCUMENTED] Phone — field not in documented schema
[UNDOCUMENTED] Image — field not in documented schema
[UNDOCUMENTED] StructureId — field not in documented schema
[UNDOCUMENTED] Members[].UserId — field in Members array not documented
[UNDOCUMENTED] Members[].FullName — field in Members array not documented
[UNDOCUMENTED] Members[].RoleId — field in Members array not documented
[UNDOCUMENTED] Members[].RoleTitle — field in Members array not documented
[UNDOCUMENTED] Members[].MaterialsCount — field in Members array not documented
[UNDOCUMENTED] Members[].AmendmentsCount — field in Members array not documented
[UNDOCUMENTED] Members[].QuestionsCount — field in Members array not documented
[NEW_ENUM] StatusId = 10 (Второ читање)
[NEW_ENUM] StatusId = 12 (Затворен)
[NEW_ENUM] RoleId = 27 (Член/Членка на политичка партија)
[INTERESTING] Response is much richer than documented schema - includes members, amendments, questions arrays
[INTERESTING] All Members have null counts for MaterialsCount, AmendmentsCount, QuestionsCount

---

## GetParliamentaryGroupDetails
parliamentaryGroupId=6f83cbd1...

[UNDOCUMENTED] Description field
[UNDOCUMENTED] NumberOfDeputies field
[UNDOCUMENTED] Amendments array
[UNDOCUMENTED] Questions array
[UNDOCUMENTED] Email field
[UNDOCUMENTED] Phone field
[UNDOCUMENTED] Image field
[DEVIATION] Members structure differs - has UserId/FullName instead of Id/FirstName/LastName, and includes MaterialsCount/AmendmentsCount/QuestionsCount
[NEW_ENUM] StatusId = 12 (Затворен)
[NEW_ENUM] StatusId = 19 (Одговорено)
[NEW_ENUM] RoleId = 26 (Координатор/Координаторка на политичка партија)
[NEW_ENUM] RoleId = 72 (Заменик координатор/координаторка на политичка партија)
[INTERESTING] Date format is /Date(timestamp)/ instead of standard ISO format
[INTERESTING] Response includes comprehensive activity tracking with counts per member

---

## GetParliamentaryGroupDetails
parliamentaryGroupId=d2e3a389...

[UNDOCUMENTED] Description field
[UNDOCUMENTED] NumberOfDeputies field
[UNDOCUMENTED] Amendments array with Id, Title, RegistrationDate, RegistrationNumber, StatusId, StatusTitle
[UNDOCUMENTED] Questions array with Id, Title, DateAsked, DateAnswered, StatusId, StatusTitle
[UNDOCUMENTED] Email field
[UNDOCUMENTED] Phone field
[UNDOCUMENTED] Image field
[DEVIATION] Members contain UserId instead of Id
[DEVIATION] Members contain FullName instead of FirstName/LastName
[UNDOCUMENTED] Members.MaterialsCount field
[UNDOCUMENTED] Members.AmendmentsCount field
[UNDOCUMENTED] Members.QuestionsCount field
[NEW_ENUM] StatusId = 12 (Затворен)
[NEW_ENUM] StatusId = 6 (Доставен до пратеници)
[NEW_ENUM] StatusId = 19 (Одговорено)
[NEW_ENUM] RoleId = 26 (Координатор/Координаторка на политичка партија)
[NEW_ENUM] RoleId = 72 (Заменик координатор/координаторка на политичка партија)

---

## GetMPsClubDetails
mpsClubId=22ded665...

[UNDOCUMENTED] Description — field not mentioned in documented schema
[NEW_ENUM] RoleId = 78 (Претседател/Претседателка)
[NEW_ENUM] RoleId = 81 (Член/Членка)
[INTERESTING] Club name is in Macedonian and relates to environmental protection and climate change
[INTERESTING] Large membership with 41 total members (3 shown + 38 truncated)

---

## GetMPsClubDetails
mpsClubId=a704fa1a...

[UNDOCUMENTED] Description field at root level
[INTERESTING] Club name is in Macedonian/Cyrillic script about Roma rights support
[INTERESTING] Role titles are in Macedonian with gendered alternatives (Претседател/Претседателка)
[NEW_ENUM] RoleId = 78 (Претседател/Претседателка)
[NEW_ENUM] RoleId = 79 (Заменик-претседател/Заменик-претседателка)

---

## GetVotingResultsForSitting
votingDefinitionId=076a2ea4... sittingId=f06b995b...

[UNDOCUMENTED] votingResultsByUser[].PoliticalPartyImage
[UNDOCUMENTED] votingResultsByFaction
[NEW_ENUM] VotingType = Јавно (Public voting)
[NEW_ENUM] AgendaItemType = Гласање на седница (Sitting voting)
[INTERESTING] VotingOptions array only shows 2 of expected 4 options (За/For and Не гласал/Not voted, missing Against and possibly Abstain)
[INTERESTING] SittingDate uses ASP.NET JSON date format /Date(1769691924000)/ which represents a future date (2026)

---
