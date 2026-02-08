# HAR Analysis Findings

Two-level LLM analysis of HAR capture(s). Pre-filter skipped static/tracking; Level 1 filtered for relevance; Level 2 produced structured notes.

- **Total entries in HAR**: 821
- **Passed to Level 1**: 633
- **Relevant (Level 1)**: 0
- **Analyzed (Level 2)**: 42 (deduplicated from 247)

---

## Entry from logs.har (index 7)

**URL**: `https://www.sobranie.mk/Infrastructure/LoadLanguage`

**Route Type**
POST

**Method Name**
LoadLanguage

**Parameters**
None visible in request body or query string. This endpoint accepts POST with no apparent parameters in the captured request. May accept optional parameters for language selection (e.g., language code, locale identifier) that were not present in this specific call, or may rely on session/cookie data for language context.

**Response Structure**
Empty JSON response in this capture. Status 200 indicates successful processing. The empty response suggests this may be a state-changing endpoint that sets language preferences server-side (possibly in session) without returning data, or this particular call resulted in no data due to default/already-set state.

**Documentation Notes**
Infrastructure/LoadLanguage appears to be a language configuration endpoint for the Sobranie (Assembly) website. Purpose likely includes: (1) Setting user language preference for the session, (2) Loading language-specific resources or translations, (3) Initializing localization context. The empty response combined with 200 status suggests side-effect operation (session modification) rather than data retrieval. Common in multi-language government portals where language selection triggers backend state changes. May work in conjunction with cookie-based session management or Accept-Language headers.

**Other**
Endpoint is under /Infrastructure path, indicating system-level or cross-cutting concern rather than domain-specific functionality. The empty response makes it difficult to determine exact behavior - could be: initialization endpoint called on page load, language switcher backend, or resource preloader. Recommend testing with various language codes as parameters (mk, en, sq, tr - common languages in North Macedonia) via query string, request body JSON, or headers to discover full API contract. Monitor Set-Cookie headers in response for session changes.


---

---

## Entry from logs.har (index 8)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetAllQuestionStatuses

**Parameters**
LanguageId (integer, required) - Language identifier for localization, value 1 observed. Sent as JSON body to /Routing/MakePostRequest endpoint with methodName field specifying the actual API method to invoke.

**Response Structure**
Empty response body returned with 200 status. Expected structure unknown - may return array of question status objects with fields like status_id, status_name, description when data exists, or this endpoint may be non-functional/deprecated.

**Documentation Notes**
This is a routing proxy pattern where /Routing/MakePostRequest acts as a dispatcher. The actual method /GetAllQuestionStatuses retrieves question statuses (likely for parliamentary questions/inquiries). Empty response suggests either no statuses exist for LanguageId=1, endpoint error, or missing authentication. Language parameter indicates multi-language support in the parliament system. Question statuses might include: submitted, pending, answered, rejected, withdrawn, etc.

**Other**
Sobranie.mk is the Assembly of North Macedonia parliament website. This routing architecture abstracts internal API methods behind a single POST endpoint. Similar methods likely exist: GetQuestionById, GetQuestionsByStatus, etc. The empty response is unusual - recommend testing with different LanguageId values (2 for Albanian, 3 for Turkish, etc.) or checking if authentication headers are required. This pattern may be used to obscure API structure or for legacy system integration.


---

---

## Entry from logs.har (index 9)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllCommitteesForFilter

**Parameters**
methodName (string, required): The API method to invoke, value 'GetAllCommitteesForFilter'. languageId (integer, required): Language identifier for localization, value 1 observed (likely Macedonian language).

**Response Structure**
Unknown - request returned HTTP 500 error with empty response body. Expected structure likely contains array of committee objects with properties such as committee ID, name, description, members count, or similar parliamentary committee metadata.

**Documentation Notes**
This is a generic routing endpoint that dispatches to different backend methods based on the methodName parameter. The GetAllCommitteesForFilter method appears designed to retrieve parliamentary committees data, possibly with filtering capabilities. The 500 error suggests either server-side issue, missing authentication, invalid session, or the method may require additional filter parameters not provided in this request. The naming convention suggests there may be related methods like GetCommitteeById, GetCommitteeMembers, etc. The languageId parameter indicates multi-language support in the API.

**Other**
Error response investigation needed. The endpoint follows a generic proxy/router pattern rather than RESTful design. Consider testing with additional parameters such as filter criteria, pagination (page, pageSize), sorting options, or date ranges. May require authentication headers or session cookies not visible in sanitized request. The sobranie.mk domain indicates this is the Assembly (Parliament) of North Macedonia's website. Similar methodName values to explore: GetAllCommittees, GetCommitteeDetails, GetCommitteeMeetings, GetCommitteeMembers.


---

---

## Entry from logs.har (index 10)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllStructuresForFilter

**Parameters**
methodName (string, required): The RPC method to invoke, value 'GetAllStructuresForFilter'. languageId (integer, required): Language identifier for localization, value 1 likely represents Macedonian or primary language.

**Response Structure**
Empty response body returned. Expected structure unknown - may return array of structure objects with filtering metadata when data is available, or endpoint may be deprecated/non-functional. Typical structure response would include id, name, type fields for organizational structures.

**Documentation Notes**
This is an RPC-style endpoint using POST to /Routing/MakePostRequest as a gateway. The actual method invoked is specified in the request body's methodName field. This pattern suggests a centralized routing mechanism where multiple API methods are accessed through a single endpoint. The method GetAllStructuresForFilter implies retrieval of organizational structures (committees, working bodies, parliamentary groups) with filtering capabilities. Empty response may indicate no structures match current filter criteria, authentication required, or the endpoint is not properly configured. This endpoint appears to support the filtering UI components on the sobranie.mk website.

**Other**
Part of a larger RPC-style API architecture. Other methods likely follow similar pattern through same /Routing/MakePostRequest endpoint. The languageId parameter suggests multilingual support (Macedonian/Albanian). Consider testing with languageId values 1, 2 to determine language mappings. Empty response prevents reverse-engineering full data structure. Recommend capturing traffic when filters are actively used or data is present to document complete response schema.


---

---

## Entry from logs.har (index 11)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllInstitutionsForFilter

**Parameters**
methodName (string, required): The RPC-style method to invoke, value 'GetAllInstitutionsForFilter'. languageId (integer, required): Language identifier for localization, value 1 likely represents Macedonian or default language.

**Response Structure**
Empty response body returned. Expected structure unknown - may return array of institution objects with fields like id, name, type, or may return empty array when no institutions exist. Actual structure needs verification with non-empty response.

**Documentation Notes**
This is an RPC-style endpoint at /Routing/MakePostRequest that acts as a generic routing handler for multiple methods. The actual method invoked is determined by the 'methodName' parameter in the request body. This particular method 'GetAllInstitutionsForFilter' appears designed to retrieve a list of institutions for filtering purposes, likely used in dropdown menus or filter interfaces on the sobranie.mk (Macedonian Parliament) website. The empty response suggests either no data exists, an error occurred silently, or the method returns empty when no filters are applied. The languageId parameter indicates multi-language support.

**Other**
Domain sobranie.mk is the Assembly (Parliament) of North Macedonia. This generic routing pattern suggests a custom API architecture rather than REST. Multiple similar methods likely exist using the same endpoint with different methodName values. The institution data might include parliamentary bodies, committees, or related governmental organizations. Investigation needed: test with different languageId values (2, 3, etc.), check if additional filter parameters can be passed, verify response when data exists, identify other available methodName values.


---

---

## Entry from logs.har (index 12)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/questions/questions.html`

**Route Type**
GET

**Method Name**
getQuestionsTemplate

**Parameters**
None - no query parameters or request body. Static file path: /Scripts/Moldova/questions/questions.html

**Response Structure**
Empty HTML response (0 bytes). Expected to be an HTML template or partial view for parliamentary questions interface, but returned empty content.

**Documentation Notes**
This appears to be a static HTML template file located in the Scripts/Moldova/questions directory, likely used as a client-side template for rendering parliamentary questions in the Moldova module. The empty response suggests either: (1) the file doesn't exist at this path, (2) it's been removed/deprecated, (3) it's a placeholder that gets populated dynamically, or (4) there's an access/permission issue. The path structure indicates this is part of a modular frontend architecture where 'Moldova' may refer to a specific parliamentary module or theme. The .html extension in the Scripts directory (typically used for JavaScript) is unusual and suggests this might be an Angular/other framework template file.

**Other**
URL pattern suggests a modular architecture with country/region-specific components (Moldova). The 'questions' subdirectory implies functionality for parliamentary questions/inquiries. Status 200 with empty body is unusual - typically would return 404 if file missing, suggesting intentional empty response or misconfiguration. No authentication headers observed. This endpoint does not appear to be a true API endpoint but rather a static resource request that would typically be cached by browsers. May be deprecated legacy code from when the system supported multiple parliamentary instances (Moldova reference).


---

---

## Entry from logs.har (index 15)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetAllQuestions

**Parameters**
LanguageId (integer, required): Language selector (1 likely default/Macedonian). CurrentPage (integer): Current page number for pagination. Page (integer): Page number (appears redundant with CurrentPage). Rows (integer): Results per page (15 default). SearchText (string): Free text search filter. RegistrationNumber (string): Filter by question registration number. StatusId (integer, nullable): Filter by question status. From (string): Origin/source filter (empty in sample). To (string): Destination/target filter (empty in sample). CommitteeId (integer, nullable): Filter by parliamentary committee. DateFrom (date, nullable): Start date for date range filter. DateTo (date, nullable): End date for date range filter. StructureId (string, GUID format): Structure/organizational unit identifier (5e00dbd6-ca3c-4d97-b748-f792b2fa3473 in sample).

**Response Structure**
Empty response body in this capture. Expected structure likely includes: array of parliamentary questions with fields such as question ID, registration number, text/content, submitter information, date submitted, status, assigned committee, language, and possibly response/answer data. Pagination metadata expected (total count, pages, current page).

**Documentation Notes**
This is a proxy/routing endpoint pattern where the actual API method is specified in the request body via 'methodName' field rather than the URL path. The /Routing/MakePostRequest acts as a generic POST handler that routes to the actual method /GetAllQuestions. This retrieves parliamentary questions with extensive filtering capabilities including text search, date ranges, committee assignment, status, and registration numbers. The empty response suggests either no questions matched the filters (unlikely with default parameters) or a capture/timing issue. The StructureId GUID appears mandatory and likely corresponds to the current parliamentary session or term. Dual page parameters (CurrentPage and Page) suggest possible legacy API evolution.

**Other**
Architectural pattern: Generic routing proxy endpoint. The sobranie.mk site uses a centralized POST routing mechanism instead of RESTful URL patterns. All POST requests go through /Routing/MakePostRequest with methodName in payload. This is unusual for modern APIs but allows centralized request handling. The StructureId GUID (5e00dbd6-ca3c-4d97-b748-f792b2fa3473) should be investigated as it likely represents the current legislative period/assembly structure and may change between sessions. Empty response body warrants further investigation - may indicate error condition, no results, or incomplete HAR capture. Related endpoints to discover: GetQuestionById, GetQuestionStatuses, GetCommittees, GetStructures.


---

---

## Entry from logs.har (index 16)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetMonthlyAgenda

**Parameters**
methodName (string, required): 'GetMonthlyAgenda' - specifies the RPC-style method to invoke; LanguageId (integer, required): language identifier, value 1 observed (likely Macedonian as primary language); Month (integer, required): month number 1-12, value 1 observed (January); Year (integer, required): four-digit year, value 2026 observed in test request

**Response Structure**
Empty response body returned for this request. This may indicate: (1) no parliamentary agenda items scheduled for January 2026, (2) future dates beyond available data return empty, (3) the endpoint returns empty array/null for no results rather than structured response. Expected structure when data exists likely includes array of agenda items with dates, session details, topics, and parliamentary business scheduled for the specified month.

**Documentation Notes**
This is an RPC-style routing endpoint used by sobranie.mk (North Macedonia Parliament website). The /Routing/MakePostRequest path acts as a generic gateway that dispatches to various backend methods based on the 'methodName' parameter. GetMonthlyAgenda retrieves parliamentary calendar/agenda for a specific month and year. The empty response for January 2026 suggests the system either has no future agenda data or the test used an intentionally out-of-range date. LanguageId=1 likely corresponds to Macedonian language. This endpoint pattern suggests multiple other methods may be available through the same routing mechanism with different methodName values.

**Other**
API Pattern: RPC-style POST routing gateway (anti-RESTful pattern). The same endpoint URL is reused for multiple operations distinguished only by request body content. Testing notes: Future date (2026) returned empty - try current/recent months for populated responses. Related methods to discover: GetWeeklyAgenda, GetDailyAgenda, GetSessionAgenda, GetCommitteeSchedule (speculative). The routing pattern suggests exploring other methodName values for full API surface discovery. Consider testing LanguageId values 2, 3 for Albanian, English or other supported languages.


---

---

## Entry from logs.har (index 17)

**URL**: `https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar`

**Route Type**
POST

**Method Name**
GetCustomEventsCalendar

**Parameters**
JSON body with 'model' object containing: (1) Language (integer, value: 1 - likely language ID where 1 may represent Macedonian or English), (2) Month (integer, range 1-12, value: 1 for January), (3) Year (integer, value: 2026 - supports future date queries). No query parameters. Endpoint follows ASMX web service pattern.

**Response Structure**
Empty response body returned (status 200). Expected structure unknown but likely would return array of calendar events with properties such as event date, title, description, and type when events exist for the requested month/year. Empty response suggests no custom events scheduled for January 2026.

**Documentation Notes**
ASMX web service endpoint for Moldova parliament calendar system. Service path: /Moldova/services/CalendarService.asmx. Method retrieves custom/special calendar events for a specific month and year in a specified language. The 'Custom' prefix suggests this returns non-standard events (possibly parliamentary sessions, committee meetings, or special occasions) as opposed to regular scheduled events. Language parameter enables localization. Response was empty for future date (January 2026), which may indicate either no events scheduled or the system doesn't support queries beyond a certain timeframe.

**Other**
Domain: sobranie.mk (North Macedonia Parliament website). Technology: ASP.NET ASMX web service (legacy .NET framework web service format). The service structure suggests additional calendar-related methods may exist in CalendarService.asmx. The empty response for a future date (2026) could indicate: (1) no events scheduled yet, (2) date range limitation, or (3) events not yet published. Testing with current/past dates would clarify expected response format. The Language parameter value of 1 should be tested against other values to determine supported languages (likely Macedonian and English as official parliament languages).


---

---

## Entry from logs.har (index 32)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetQuestionDetails

**Parameters**
LanguageId (integer, required): Language identifier for localization (e.g., 1 for Macedonian). QuestionId (string/UUID, required): Unique identifier for the parliamentary question in GUID format (e.g., '4899bb7e-11d6-49c4-86d0-87e4d05632ff')

**Response Structure**
Empty response body returned with HTTP 200 status. This may indicate: (1) No question details found for the provided QuestionId, (2) Error condition returning empty response, (3) Question exists but has no additional details, or (4) Possible API malfunction. Expected structure unknown due to empty response.

**Documentation Notes**
This endpoint uses a routing proxy pattern where the actual API method '/GetQuestionDetails' is passed as a parameter to the generic '/Routing/MakePostRequest' endpoint. This is an internal routing mechanism used by sobranie.mk (Macedonian Parliament website) to handle multiple API methods through a single entry point. The endpoint retrieves detailed information about parliamentary questions by their unique identifier. LanguageId=1 likely corresponds to Macedonian language. The empty response in this capture suggests either the question doesn't exist, has been deleted, or there was an error condition. Further investigation with valid QuestionIds is needed to determine the actual response structure.

**Other**
API Pattern: Proxy/Router pattern with methodName routing. Base URL: https://www.sobranie.mk/Routing/MakePostRequest. This appears to be part of a broader API system where multiple methods are routed through a single endpoint. The QuestionId format follows standard GUID/UUID structure. Testing recommendations: Try with different valid QuestionIds to determine normal response structure, test different LanguageId values (likely 1=Macedonian, 2=Albanian, 3=English based on typical sobranie.mk multilingual support), examine whether this relates to Question Time/Parliamentary Questions feature. Related endpoints to explore: /GetQuestions, /GetQuestionsList, /SearchQuestions.


---

---

## Entry from logs.har (index 53)

**URL**: `https://www.sobranie.mk/Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser`

**Route Type**
POST

**Method Name**
GetOfficialVisitsForUser

**Parameters**
model (string, required): UUID/GUID identifier, likely representing a user ID or session token. Example: '914bff80-4c19-4675-ace4-cb0c7a08f688'. Sent as JSON in request body.

**Response Structure**
Returns JSON array or object. Empty response in this capture suggests no official visits exist for the specified user/model ID, or the ID is invalid. Expected structure likely contains visit records when data exists (dates, locations, purposes, officials involved).

**Documentation Notes**
ASMX web service endpoint (legacy ASP.NET Web Services). Part of Moldova subdirectory structure suggesting country-specific implementation. Service name 'OfficialVisits' indicates functionality for tracking/managing official governmental visits. The GetOfficialVisitsForUser method retrieves visit records filtered by user/model identifier. Empty response may indicate: (1) user has no visits, (2) invalid user ID, (3) authorization issues, or (4) data not yet populated. ASMX services typically support both SOAP and JSON protocols; this implementation uses JSON over HTTP POST.

**Other**
Base path pattern: /Moldova/services/[ServiceName].asmx/[MethodName]. The UUID format for 'model' parameter suggests modern GUID-based user identification. No authentication headers visible in this capture, but may rely on session cookies or other implicit auth. Service architecture appears to use legacy .NET Framework ASMX rather than modern REST/Web API. Consider testing with valid user IDs to discover full response schema. Related endpoints likely exist for creating, updating, or deleting official visits.


---

---

## Entry from logs.har (index 57)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetUserDetailsByStructure

**Parameters**
userId (UUID/GUID string, required) - Identifier for the user being queried; structureId (UUID/GUID string, required) - Identifier for the organizational/parliamentary structure; languageId (integer, required) - Language selection for localized content (1 appears to be default, likely Macedonian)

**Response Structure**
Empty response body returned in this capture. Expected structure unknown - may return user profile data, parliamentary membership details, committee assignments, or role information within the specified structure. Possible fields could include: name, position, biography, contact details, photo URL, term dates, party affiliation, committee memberships.

**Documentation Notes**
This endpoint uses a generic routing mechanism (/Routing/MakePostRequest) with methodName parameter to specify the actual operation (GetUserDetailsByStructure). This pattern suggests a single POST endpoint that routes to multiple backend methods. Empty response could indicate: (1) No data exists for this user-structure combination, (2) User has no active role in the specified structure, (3) Authentication/authorization required but missing, (4) Data sanitization removed all content. The method name suggests retrieving user details filtered or contextualized by a specific organizational structure (e.g., current parliament session, specific committee, administrative body). LanguageId parameter indicates multi-language support, likely for biographical and role description text.

**Other**
The sobranie.mk domain is the Assembly (Parliament) of North Macedonia. This API appears to be part of their internal content management or member information system. The generic routing pattern (/Routing/MakePostRequest) is unusual for modern REST APIs but common in older .NET/MVC frameworks or custom RPC-style implementations. All identifiers use UUID/GUID format suggesting SQL Server or similar backend. The combination of userId and structureId suggests a many-to-many relationship where users can belong to multiple structures and structures contain multiple users. Consider testing with different languageId values (2 for Albanian, 3 for English are possibilities for North Macedonia). Error handling, authentication requirements, and rate limiting are unknown from this single capture.


---

---

## Entry from logs.har (index 74)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetSittingDetails

**Parameters**
SittingId (string/GUID) - Unique identifier for a parliamentary sitting session; LanguageId (integer) - Language selector (1 appears to be default, likely Macedonian)

**Response Structure**
Empty response returned in this instance. Expected structure unknown - may return sitting details including date, time, agenda items, participants, voting records, or session metadata when valid SittingId is provided. Response likely JSON object or array.

**Documentation Notes**
This is a proxy/router endpoint pattern where actual method name is passed in request body. The URL path /Routing/MakePostRequest acts as a generic dispatcher. Multiple API methods likely accessible through this single endpoint by varying MethodName parameter. GUID format for SittingId suggests database-backed system. Empty response may indicate: invalid/expired sitting ID, sitting not yet published, access restrictions, or actual empty sitting record.

**Other**
API uses POST for what appears to be read operations (GetSittingDetails), which is non-RESTful but common for complex parameter passing. The routing pattern suggests internal API not designed for public consumption. GUID indicates modern backend (likely .NET/C# based on MakePostRequest naming convention). LanguageId parameter indicates multilingual support. No authentication tokens visible in this request - may be session-based or publicly accessible endpoints. Consider testing with known valid SittingId values and different LanguageId values (2, 3 for other languages).


---

---

## Entry from logs.har (index 114)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetMaterialDetails

**Parameters**
MaterialId (string/UUID): Unique identifier for the parliamentary material (e.g., '9cc1c0b1-919e-406f-b654-ea3201a57913'). LanguageId (integer): Language selection for content retrieval (1 appears to be default, likely Macedonian). AmendmentsPage (integer): Pagination parameter for amendments list (starts at 1). AmendmentsRows (integer): Number of amendment rows to return per page (5 in this example).

**Response Structure**
Empty response returned in this capture. Expected structure likely contains: material details (title, description, type, date), amendment information (paginated list based on AmendmentsPage/AmendmentsRows parameters), metadata (status, voting information), related documents or links. The empty response may indicate: invalid MaterialId, no data available for this material, session timeout, or error condition not properly returned.

**Documentation Notes**
This is a generic POST routing endpoint for the Macedonian Parliament (Sobranie) website that dispatches to various backend methods. The actual API method is specified in the 'methodName' field of the request body. GetMaterialDetails retrieves detailed information about parliamentary materials including amendments with pagination support. The MaterialId appears to be a UUID format. The response being empty suggests either: (1) the material doesn't exist, (2) authentication/session issues, (3) the material has no details/amendments to return, or (4) an error occurred but wasn't properly communicated. Standard usage would include authentication cookies/headers not visible in sanitized data.

**Other**
API Pattern: Generic router pattern where /Routing/MakePostRequest acts as a dispatcher to multiple backend methods based on 'methodName' parameter. This is a common pattern for consolidating multiple API endpoints behind a single HTTP endpoint. Related Methods: Based on this pattern, other methodName values likely exist for different parliamentary data operations (GetMaterials, GetSessions, GetVotes, etc.). UUID Format: MaterialId uses standard UUID v4 format. Pagination: Implements standard page/rows pagination for amendments subsection. Language Support: Multi-language support via LanguageId parameter. Security Note: The empty response and lack of error messaging may indicate poor API error handling or security through obscurity approach. Testing Recommendation: Try different MaterialIds, LanguageId values (2, 3 for other languages), and pagination parameters to map full response structure.


---

---

## Entry from logs.har (index 159)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllSittingStatuses

**Parameters**
LanguageId (integer, required) - Language identifier for localization, value 1 observed

**Response Structure**
Empty response body returned (status 200). Expected structure unknown - may return array of sitting status objects with properties like id, name, description in specified language when data exists

**Documentation Notes**
This endpoint uses a generic routing pattern where the actual method name is passed in the request body rather than the URL path. The MakePostRequest path acts as a dispatcher/router to various backend methods. GetAllSittingStatuses appears to retrieve all possible statuses for parliamentary sittings/sessions with localized content based on LanguageId. Empty response may indicate no data, system error, or this method requires additional parameters not captured

**Other**
Pattern: Generic POST router at /Routing/MakePostRequest. Real API method specified via 'methodName' body parameter. This architecture suggests a single-endpoint API gateway that routes to multiple backend services. LanguageId=1 likely represents Macedonian language. The sobranie.mk domain is the Assembly of North Macedonia parliament website. Empty response may warrant investigation - could be authentication issue, database empty, or method requires session state


---

---

## Entry from logs.har (index 161)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/sitting/sitting.html`

**Route Type**
GET

**Method Name**
getSittingPage

**Parameters**
None - Static HTML resource request with no query parameters or request body

**Response Structure**
text/html - Returns empty HTML content (0 bytes). This appears to be either a placeholder page, a page that loads content dynamically via JavaScript, or a deprecated/unused endpoint that returns no content.

**Documentation Notes**
This endpoint retrieves a sitting (parliamentary session) page from the Moldova scripts directory. The path structure '/Scripts/Moldova/sitting/sitting.html' suggests this is a static HTML file rather than a dynamic API endpoint. The empty response indicates this may be: 1) A frame/container page that loads actual content via AJAX/JavaScript, 2) A deprecated endpoint no longer serving content, 3) An error condition returning empty content instead of proper error response. The 'Moldova' directory name is notable and may indicate content related to Moldovan parliamentary procedures or a specific system module name. This does not appear to be a RESTful API endpoint but rather a web page resource.

**Other**
URL Pattern: /Scripts/{module}/sitting/sitting.html - Suggests there may be similar paths for other modules or sections. The fact this returns 200 OK with empty body rather than 404 indicates the file exists but has no content. This is unusual behavior and may warrant investigation. The request contains no authentication headers or tokens in the sanitized version. Path components 'Scripts' and 'Moldova' suggest this may be part of a legacy system or specific parliamentary module. Recommend checking browser network tab for subsequent XHR/fetch requests that may load actual content into this page.


---

---

## Entry from logs.har (index 164)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllSittings

**Parameters**
Page (integer, pagination): Current page number, default 1. Rows (integer, pagination): Number of rows per page, default 10. LanguageId (integer, required): Language identifier, 1 appears to be default. TypeId (integer, filter): Type identifier for sitting classification, value 1 used. CommitteeId (string/null, filter): Optional committee identifier for filtering by committee. StatusId (integer/null, filter): Optional status identifier for filtering sittings by status. DateFrom (string/null, filter): Optional start date for date range filtering (format unknown). DateTo (string/null, filter): Optional end date for date range filtering (format unknown). SessionId (integer/null, filter): Optional session identifier for filtering by parliamentary session. Number (integer/null, filter): Optional sitting number for direct lookup. StructureId (string, required): UUID identifier for organizational structure, value '5e00dbd6-ca3c-4d97-b748-f792b2fa3473' used.

**Response Structure**
Empty response received in this capture. Expected structure unknown but likely returns paginated list of parliamentary sittings with fields such as sitting ID, date, session, committee, type, status, and related metadata. Typical pagination metadata (total records, total pages) likely included in successful responses.

**Documentation Notes**
This is a generic POST routing endpoint that accepts a 'methodName' parameter to invoke different backend methods. GetAllSittings retrieves parliamentary sitting sessions with extensive filtering capabilities including date ranges, committees, sessions, status, and type. The endpoint supports pagination through Page and Rows parameters. Empty response suggests either no data matched filters, an error condition not reflected in status code, or potential issue with the specific parameter combination (particularly the StructureId UUID). The routing pattern suggests this is a centralized API gateway where multiple methods share the same endpoint URL with method selection via the methodName field.

**Other**
The sobranie.mk domain indicates this is the Macedonian Parliament (Sobranie) website API. The generic /Routing/MakePostRequest pattern is unusual - it acts as a single-endpoint RPC-style gateway rather than RESTful design. StructureId UUID suggests hierarchical organizational structure (possibly legislature terms, chambers, or organizational units). Multiple null parameters indicate a flexible query builder pattern. LanguageId=1 likely represents Macedonian language. TypeId=1 may distinguish plenary vs committee sittings. The combination of required StructureId with optional filters suggests structure-scoped queries. Empty response with 200 status is concerning - proper API would return empty array or error status. Worth testing with different StructureId values and simpler parameter sets.


---

---

## Entry from logs.har (index 204)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/sitting/sitting.html`

**Route Type**
GET

**Method Name**
sitting.html

**Parameters**
None - No query parameters, path parameters, or request body. This is a static HTML file request accessing the sitting (session) interface template or frame.

**Response Structure**
HTTP 200 OK with Content-Type: text/html. Response body is empty, suggesting this may be a template file that gets populated dynamically via JavaScript, an iframe placeholder, or the file may have been removed/moved. The empty response could also indicate a redirect scenario not captured in the HAR, or content loaded asynchronously after initial page load.

**Documentation Notes**
This endpoint appears to be part of the Moldova parliamentary sitting/session management system within the sobranie.mk (North Macedonia Parliament) website. The path structure '/Scripts/Moldova/sitting/' suggests this is JavaScript-related content or a dynamic HTML component. The empty response is unusual for a direct HTML file request - typical scenarios: (1) File serves as container for AJAX-loaded content, (2) File has been deprecated/moved, (3) Authentication/session required but not provided, (4) HAR capture timing issue where content wasn't fully captured. The 'Moldova' path component is interesting - may indicate historical naming or a specific legislative framework/system name rather than geographic reference.

**Other**
Related endpoints to investigate: /Scripts/Moldova/sitting/ directory for other resources, potential API endpoints that populate this HTML template, JavaScript files that interact with this page. The sitting.html filename suggests parliamentary session/meeting functionality - likely displays active sessions, session schedules, voting records, or live session feeds. Check for WebSocket connections, polling endpoints, or REST APIs that provide sitting data. Status 200 with empty body warrants further investigation - may need to examine this with proper session cookies or authentication headers.


---

---

## Entry from logs.har (index 220)

**URL**: `https://www.sobranie.mk/scripts/news/singleNewsInstance.min.html`

**Route Type**
GET

**Method Name**
singleNewsInstance

**Parameters**
None visible in this request. However, the path suggests this is likely a template/partial HTML file that may be loaded dynamically and populated with data via JavaScript. The '.min.html' extension indicates this is a minified HTML template. Typical usage would involve parameters passed via JavaScript when instantiating the template, not as URL query parameters.

**Response Structure**
Empty HTML response (0 bytes). This appears to be a minified HTML template file that serves as a client-side component. The empty response could indicate: (1) the template is truly empty/minimal, (2) it's meant to be populated dynamically via JavaScript, (3) it's a placeholder for Angular/React/Vue component rendering, or (4) this is an error state where the template failed to load properly.

**Documentation Notes**
This endpoint serves a client-side HTML template for displaying single news instances. The file is located in /scripts/news/ directory, suggesting it's part of a news module. The '.min.html' extension is unusual - typically minification applies to .js and .css files. This could be part of a client-side templating system where HTML fragments are loaded on-demand. The actual news content would likely be fetched from a separate API endpoint (possibly JSON) and then rendered into this template. To discover the full API, look for: (1) JavaScript files that reference this template, (2) JSON/API endpoints that provide news data, (3) parameters used when this template is instantiated in the browser.

**Other**
File path structure indicates a modular architecture with scripts organized by feature (news). The empty response warrants further investigation - check browser console for errors, examine JavaScript that loads this template, and monitor network requests when news articles are loaded. This may be part of a single-page application (SPA) architecture. Related endpoints to investigate: /api/news/, /scripts/news/*.js files that might load data into this template.


---

---

## Entry from logs.har (index 307)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetVotingResultsForAgendaItem

**Parameters**
VotingDefinitionId (UUID/GUID, required) - Identifies the specific voting instance, example: '9d80de02-11fb-4f79-80ee-181c0f92629d'. AgendaItemId (UUID/GUID, required) - Identifies the agenda item being voted on, example: '98BBFA75-F432-4BBB-9A10-202EFE7E2569'. LanguageId (integer, required) - Language identifier for localization, example: 1 (likely Macedonian). All parameters passed in JSON request body.

**Response Structure**
Empty response body received in this capture. Expected structure likely contains voting results data such as vote counts (for/against/abstain), individual MP votes, timestamps, quorum information, and voting outcome. Response format is application/json but this particular request returned no data, possibly indicating no voting results available for this specific combination of VotingDefinitionId and AgendaItemId, or the voting has not yet occurred.

**Documentation Notes**
This endpoint is part of the Sobranie (Parliament of North Macedonia) API routing system. Uses a generic POST routing mechanism at /Routing/MakePostRequest where the actual method name is specified in the request body 'MethodName' field. This pattern suggests a single-endpoint RPC-style API design. The endpoint retrieves voting results for specific agenda items in parliamentary sessions. The empty response may indicate: (1) voting hasn't occurred yet, (2) results are not yet published, (3) invalid ID combination, or (4) data has been removed/archived. The use of GUIDs suggests a modern database-backed system with proper unique identifiers for all entities.

**Other**
API Pattern: RPC-style routing through single endpoint. Base URL: https://www.sobranie.mk. GUID format used for both VotingDefinitionId and AgendaItemId suggests SQL Server or similar database backend. LanguageId=1 likely corresponds to Macedonian language (primary official language). The parliament website likely supports multiple languages. Related methods probably exist for: listing agenda items, getting voting definitions, retrieving session information, and accessing MP voting records. Security: No authentication headers observed in this request, suggesting public API access for transparency. Status 200 with empty body indicates successful request processing but no data returned rather than an error condition.


---

---

## Entry from logs.har (index 308)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/agenda-item-votings/agenda-item-votings.html`

**Route Type**
Static Resource

**Method Name**
get_agenda_item_votings_html

**Parameters**
None - This is a static HTML file request with no query parameters or request body. The path suggests it may be a template or component file related to displaying voting information for agenda items.

**Response Structure**
Content-Type: text/html, Status: 200. Response body is empty, which suggests this could be: (1) A template file loaded client-side via JavaScript, (2) A placeholder or deleted resource, (3) An intentionally empty HTML fragment used as a component. The empty response with 200 status is unusual for a typical HTML page.

**Documentation Notes**
This appears to be part of the Moldova module within the sobranie.mk (North Macedonian Parliament) website. The path structure '/Scripts/Moldova/agenda-item-votings/' suggests this is a client-side resource, possibly an Angular, React, or other SPA framework template. The 'agenda-item-votings' naming indicates functionality related to displaying or managing votes on parliamentary agenda items. Despite being served as text/html, the empty response suggests it's either: (a) a dynamic template populated by JavaScript, (b) a deprecated endpoint, or (c) requires authentication/session that wasn't provided. This is NOT a REST API endpoint but rather a frontend resource file.

**Other**
Investigation recommendations: (1) Check if this file is referenced in JavaScript bundle files or main application code, (2) Look for API endpoints that actually serve voting data (likely JSON format under /api/ or similar paths), (3) Examine network requests made by the page that loads this resource to find the actual data endpoints, (4) The 'Moldova' path segment is interesting - may indicate multi-tenant architecture or historical naming (Moldova vs North Macedonia). This static resource likely works in conjunction with actual API endpoints that serve voting data in JSON format.


---

---

## Entry from logs.har (index 319)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetVotingResultsForAgendaItemReportDocument

**Parameters**
MethodName (string, required): 'GetVotingResultsForAgendaItemReportDocument' - Specifies the backend method to invoke. LanguageId (integer, required): Language identifier (1 appears to be default, likely Macedonian). VotingDefinitionId (string/UUID, required): Unique identifier for the voting definition (format: UUID with hyphens, e.g., '9d80de02-11fb-4f79-80ee-181c0f92629d'). AgendaItemId (string/UUID, required): Unique identifier for the agenda item (format: UUID with hyphens, uppercase, e.g., '98BBFA75-F432-4BBB-9A10-202EFE7E2569').

**Response Structure**
Empty response body returned (Status 200). This could indicate: (1) No voting results exist for the specified combination of VotingDefinitionId and AgendaItemId, (2) The document generation failed silently, (3) The method may trigger a background process or file generation, (4) The response might be a file download triggered via headers not visible in HAR body, or (5) Invalid/test request IDs were used. Expected response would likely be JSON containing voting results data or a document reference/URL for a report document.

**Documentation Notes**
This is a generic routing endpoint that acts as an RPC-style gateway - the actual method invoked is determined by the MethodName parameter. The endpoint uses POST to /Routing/MakePostRequest for method dispatch. The method name suggests it retrieves voting results formatted for inclusion in a report document for a specific agenda item. The combination of VotingDefinitionId and AgendaItemId suggests a many-to-many relationship where multiple votings can occur on a single agenda item. Empty response may indicate the voting hasn't occurred yet, the IDs are invalid, or the document format is binary/downloadable. Language support is built into the API (LanguageId parameter).

**Other**
URL pattern suggests ASP.NET/MVC framework. The routing mechanism is RPC-style rather than RESTful. UUID formats are mixed case (lowercase with hyphens for VotingDefinitionId, uppercase with hyphens for AgendaItemId) which may indicate different database sources or legacy systems. The empty response with 200 status is unusual and warrants investigation - check response headers for Content-Disposition or file download indicators. This endpoint is part of the Macedonian Parliament (Sobranie) website's internal API for parliamentary voting and agenda management. Consider testing with known valid IDs from active sessions to verify expected response structure.


---

---

## Entry from logs.har (index 356)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetVotingResultsForSitting

**Parameters**
votingDefinitionId (string/UUID): Identifier for the voting definition (e.g., '18ba866e-e347-4e5a-8d8d-4d246402874b'); sittingId (string/UUID): Identifier for the parliamentary sitting (e.g., 'f06b995b-c5c7-42cd-8605-ec2d9ab7aac1'); languageId (integer): Language identifier for localization (1 = likely Macedonian or default language)

**Response Structure**
Empty response returned in this capture. Expected structure unknown but likely contains voting results data such as vote counts (for/against/abstain), individual MP votes, voting timestamp, quorum status, and vote outcome. May return empty array or null when no voting results are available for the specified sitting and voting definition combination.

**Documentation Notes**
This endpoint retrieves detailed voting results for a specific voting event within a parliamentary sitting. The generic routing mechanism at /Routing/MakePostRequest acts as a dispatcher that routes to different methods based on the MethodName parameter. This pattern suggests a single-endpoint RPC-style API rather than RESTful resource-based routing. The empty response in this capture may indicate: (1) voting has not yet occurred, (2) results are not yet published, (3) invalid ID combination, or (4) data has been removed/archived. The use of UUIDs for both votingDefinitionId and sittingId suggests a relational structure where multiple voting events can occur within a single sitting. LanguageId parameter indicates multi-language support in the API responses.

**Other**
Part of sobranie.mk (Assembly of North Macedonia) parliamentary information system. The generic POST routing pattern (/Routing/MakePostRequest) is unusual and suggests all API methods may use this same endpoint with MethodName discrimination. This makes API discovery challenging as endpoint paths don't reveal available methods. Related methods likely include: GetVotingDefinitionsForSitting, GetSittingDetails, GetMPVotingRecord. Security consideration: No authentication tokens visible in this request, suggesting public access to voting records. The votingDefinitionId and sittingId must be obtained from other API calls or UI interactions. Response sanitization note: actual response was empty, not redacted.


---

---

## Entry from logs.har (index 378)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/sitting/sitting.html`

**Route Type**
GET

**Method Name**
get_sitting_html_page

**Parameters**
None - static HTML page request with no query parameters or request body

**Response Structure**
HTML page (text/html) - Response body is empty in this capture, likely due to sanitization or the page being truly empty. Expected structure would be an HTML document containing sitting/session information based on the URL path context.

**Documentation Notes**
This endpoint serves a static HTML page related to parliamentary sittings under the Moldova scripts directory. The path structure '/Scripts/Moldova/sitting/sitting.html' suggests this may be part of a Moldova-specific module or historical section of the parliament website. The empty response in this capture may indicate: (1) the page no longer exists or has been moved, (2) the content was sanitized during HAR capture, (3) the page requires authentication/session that wasn't present, or (4) the page dynamically loads content via JavaScript. This appears to be a legacy endpoint given the 'Scripts' directory naming convention and may not be actively maintained. Not a RESTful API endpoint but rather a traditional web page resource.

**Other**
Content-Type is text/html indicating this is a web page endpoint, not a JSON API. The 'Moldova' reference in the path is interesting as this is the Parliament of North Macedonia (sobranie.mk), suggesting possible historical content or international parliamentary cooperation materials. The empty response with 200 status is unusual - typically would expect either content or a 404/410 status. May warrant further investigation with browser developer tools to see if content loads dynamically. URL pattern suggests there may be related endpoints at /Scripts/Moldova/sitting/ with different HTML files or subdirectories.


---

---

## Entry from logs.har (index 483)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/agenda-item-votings/agenda-item-votings.html`

**Route Type**
Static HTML Template

**Method Name**
GET /Scripts/Moldova/agenda-item-votings/agenda-item-votings.html

**Parameters**
None - This is a GET request with no query parameters, path parameters, or request body. The URL suggests this may be a template file that could be used with dynamic parameters in a client-side application context.

**Response Structure**
Empty HTML response (0 bytes). Status 200 OK with text/html Content-Type. Despite successful status, the response body is empty, suggesting this could be: (1) A template file that gets populated client-side via JavaScript, (2) A partial HTML fragment used in AJAX/dynamic loading, (3) A file that failed to load properly despite 200 status, or (4) A placeholder endpoint.

**Documentation Notes**
This endpoint appears to be part of the North Macedonia Parliament (sobranie.mk) website's voting system interface. The path structure '/Scripts/Moldova/agenda-item-votings/' suggests this is a component for displaying voting information on agenda items. The 'Moldova' directory name is interesting - could indicate code/template reuse from another parliamentary system or a vendor name. The file serves an empty HTML response, which is unusual but indicates it's likely a client-side template that gets populated dynamically through JavaScript or another mechanism. This would typically be loaded as part of a larger page structure or used in an SPA (Single Page Application) architecture. To understand the full functionality, one would need to examine: (1) The JavaScript files that reference this template, (2) Any AJAX calls that populate this template with data, (3) The parent pages that include this template.

**Other**
Security/Architecture observations: The path contains 'Scripts' which might indicate legacy ASP.NET structure or simply organizational naming. The empty response with 200 status is technically valid but unusual - most modern APIs would return structured data or meaningful HTML. This suggests the actual data fetching happens through separate API endpoints that populate this template. For complete API discovery, should investigate: (1) Network requests made after this template loads, (2) Associated JavaScript bundles, (3) Potential API endpoints matching pattern like '/api/agenda-item-votings' or similar RESTful structures. The template name suggests it handles displaying multiple votings for agenda items, implying a one-to-many relationship structure in the data model.


---

---

## Entry from logs.har (index 500)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllGenders

**Parameters**
methodName (string, required): 'GetAllGenders' - Specifies the remote method to invoke; languageId (integer, required): 1 - Language identifier for localization, likely 1=Macedonian or default language

**Response Structure**
Empty response body returned. This may indicate: (1) No gender records exist in the database, (2) An error occurred but was not properly returned, (3) The endpoint successfully processed the request but returns null/empty for this specific method, or (4) Authentication/authorization may be required but was not provided in the sanitized request

**Documentation Notes**
This is a generic RPC-style routing endpoint at /Routing/MakePostRequest that acts as a gateway to invoke various backend methods. The actual method invoked is determined by the 'methodName' parameter in the POST body. GetAllGenders appears to be a reference data endpoint that should return a list of gender options (likely Male/Female/Other or similar categories) for use in forms or filtering. The languageId parameter suggests multi-language support across the application. The empty response is unusual for a 'GetAll' method and warrants investigation - typical response would be an array of gender objects with id, name, and possibly localized labels.

**Other**
Pattern identified: This application uses a single POST endpoint as a method router/dispatcher rather than RESTful resource-based routing. All API calls likely go through /Routing/MakePostRequest with different methodName values. This is a common pattern in older .NET applications or those using a service-oriented architecture. To discover other available methods, monitor the methodName values in other requests. The sobranie.mk domain suggests this is the Parliament of North Macedonia website, so gender data might be used for deputy/member profiles or statistical filtering.


---

---

## Entry from logs.har (index 502)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/parliamentMPs/parliamentMPs.html`

**Route Type**
GET

**Method Name**
getParliamentMPsPage

**Parameters**
None - This is a static HTML page request with no query parameters or request body

**Response Structure**
HTML document (text/html) - Response body appears empty in the capture, likely due to client-side rendering or delayed content loading. Expected structure would be an HTML page containing information about parliament members (MPs) based on the URL path structure

**Documentation Notes**
This endpoint serves an HTML page for displaying parliament members (MPs). The URL path '/Scripts/Moldova/parliamentMPs/parliamentMPs.html' suggests this is part of a Moldova-related section of the sobranie.mk (North Macedonia Parliament) website. The empty response body in the HAR capture likely indicates either: 1) The page loads content dynamically via JavaScript after initial page load, 2) The content requires authentication/session, 3) The page was not fully captured, or 4) There was an error during capture. The naming convention 'parliamentMPs.html' suggests this is a static HTML file rather than a REST API endpoint, though it may contain embedded JavaScript that makes subsequent API calls to fetch actual MP data

**Other**
Status 200 indicates successful request. This appears to be a web page endpoint rather than a data API endpoint. The '/Scripts/' directory in the path is unusual for serving HTML pages and typically contains JavaScript files, suggesting this might be a misplaced resource or legacy URL structure. To discover the actual data API, examine network requests made by this page after it loads, as modern web applications typically load HTML shell pages first, then fetch data via AJAX/fetch calls to JSON API endpoints. The 'Moldova' reference is interesting given this is the North Macedonia parliament website - may indicate historical data, comparative legislature information, or a naming artifact


---

---

## Entry from logs.har (index 503)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetParliamentMPsNoImage

**Parameters**
methodName (string, required): 'GetParliamentMPsNoImage' - Specifies the backend method to invoke. languageId (integer, required): Language identifier (1 observed, likely Macedonian). genderId (integer, nullable): Filter by gender (null = no filter). ageFrom (integer, nullable): Minimum age filter. ageTo (integer, nullable): Maximum age filter. politicalPartyId (string/integer, nullable): Filter by political party. searchText (string, nullable): Text search across MP names/data. page (integer, required): Pagination page number (1-indexed). rows (integer, required): Results per page (12 observed). StructureId (string UUID, required): '5e00dbd6-ca3c-4d97-b748-f792b2fa3473' - Likely identifies the Parliament/legislative structure. coalition (string, optional): Filter by coalition membership (empty string observed). constituency (string, optional): Filter by electoral constituency (empty string observed).

**Response Structure**
Empty response body received in this capture. Expected response would likely be JSON containing: array of MP objects without images, pagination metadata (total records, total pages), each MP record containing: name, political party, constituency, age/birthdate, gender, position/role, mandate period, contact information, biography text. The 'NoImage' suffix suggests image URLs/binary data are excluded from response payload for performance.

**Documentation Notes**
This is a generic routing endpoint that dispatches to backend methods via methodName parameter. The '/Routing/MakePostRequest' path acts as a gateway/proxy pattern. GetParliamentMPsNoImage retrieves Member of Parliament listings without image data, supporting multiple filter dimensions (gender, age range, party, constituency, coalition) and text search. Pagination is implemented with page/rows parameters. The StructureId UUID appears to be a constant for the current parliamentary session/structure. Empty response suggests either: no MPs match the criteria, an error occurred, or response capture failed. Language support indicates multilingual content (languageId=1 likely Macedonian, possibly 2=Albanian given North Macedonia's official languages). This endpoint is optimized for list views where images aren't needed, likely paired with a 'GetParliamentMPs' variant that includes images.

**Other**
API follows a command pattern where all operations POST to single routing endpoint with methodName discriminator. This architectural choice centralizes routing logic server-side rather than using RESTful resource paths. Other potential methodName values to investigate: GetParliamentMPs (with images), GetParliamentMPDetails, GetPoliticalParties, GetConstituencies, GetCoalitions. The UUID format for StructureId suggests multi-tenant or multi-session architecture. Coalition and constituency as separate parameters indicate these are distinct filtering dimensions in North Macedonia's parliamentary system. Age filtering (ageFrom/ageTo) is unusual for MP listings, suggesting analytics or demographic research capabilities. Empty strings vs null values appear semantically different (empty=no filter vs null=not applicable). Security consideration: no authentication tokens visible, suggesting public API or session-based auth via cookies.


---

---

## Entry from logs.har (index 504)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllPoliticalParties

**Parameters**
methodName (string, required): 'GetAllPoliticalParties' - specifies the backend method to invoke; languageId (integer, required): 1 - language identifier for localization (likely 1=Macedonian); StructureId (string, required): '5e00dbd6-ca3c-4d97-b748-f792b2fa3473' - UUID format identifier, possibly references legislative structure/session/term

**Response Structure**
Empty response body returned with 200 status. Expected structure unknown - may return array of political party objects with fields like party ID, name, acronym, seats, logo URL, description when data exists. Empty response could indicate no parties in specified structure or data access issue.

**Documentation Notes**
This is a generic POST routing endpoint that acts as an RPC gateway - the actual method is specified in the request body via 'methodName' parameter rather than URL path. The endpoint pattern '/Routing/MakePostRequest' suggests a centralized router handling multiple backend methods. The StructureId UUID likely corresponds to a specific parliamentary structure/composition period. Response was empty which is unusual for 'GetAll' method - may need different StructureId or this structure has no associated parties. Language ID suggests multi-language support across the API.

**Other**
API uses RPC-style architecture over REST. All requests likely go through this single POST endpoint with method specified in body. The empty response with 200 status (not 404) suggests successful request but no data, possibly because StructureId references invalid/empty structure. Other potential methodName values might include GetAllMPs, GetAllCommittees, GetAllSessions, etc. Consider testing with different StructureId values or omitting it. The sobranie.mk domain is North Macedonia's Parliament website.


---

---

## Entry from logs.har (index 519)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetPoliticalPartyDetails

**Parameters**
politicalPartyId (UUID/GUID format, required) - Identifier for the political party (e.g., '4c57e5ab-2bc1-4943-8ecd-bde1166cf829'); LanguageId (integer, required) - Language selection identifier, value 1 observed, likely corresponds to Macedonian or primary language; methodName (string, required) - Internal routing parameter specifying the target method

**Response Structure**
Empty response body observed in this capture. Expected structure unknown - may return political party details including name, description, members, logo, founding date, ideology, parliamentary representation, or contact information in JSON format when party ID is valid. Empty response could indicate: invalid party ID, party not found, or a soft-delete/inactive status.

**Documentation Notes**
This is a generic POST routing endpoint at /Routing/MakePostRequest that acts as a gateway/dispatcher for multiple backend methods. The actual method invoked is determined by the 'methodName' field in the request body. This pattern suggests a single-endpoint API architecture where all POST requests are routed through this handler. The sobranie.mk domain indicates this is the official website of the Assembly (Parliament) of North Macedonia. The UUID format for politicalPartyId suggests a stable, database-generated identifier system. LanguageId=1 likely represents Macedonian language, with other values potentially for Albanian, English, or other official/supported languages.

**Other**
URL pattern suggests ASP.NET MVC routing convention. The empty response may warrant investigation - could be a test request, expired party ID, or error condition without proper error messaging. For complete API discovery, should test: different LanguageId values (0, 2, 3), valid party IDs from active parties, invalid/malformed UUIDs, missing parameters. The generic routing endpoint likely handles multiple methodName values beyond GetPoliticalPartyDetails - other methods may include GetMPs, GetLegislation, GetSessions, etc. Consider checking network tab for similar requests with different methodName values to map the complete internal API surface.


---

---

## Entry from logs.har (index 540)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetCommitteeDetails

**Parameters**
committeeId (UUID string, required) - Unique identifier for the committee (e.g., 'bb8e23a1-c959-4818-8e6e-ebe450847fd8'); languageId (integer, required) - Language identifier for localization (1 appears to be default, likely Macedonian)

**Response Structure**
Empty response body returned (status 200). Expected structure unknown - may return committee details object with properties like name, description, members, meeting schedules, or may indicate no data available for the given committeeId. Further investigation needed with valid committee IDs.

**Documentation Notes**
This is a generic routing endpoint at /Routing/MakePostRequest that dispatches to different methods based on the 'methodName' parameter in the request body. This pattern suggests a single-endpoint API gateway architecture. The GetCommitteeDetails method retrieves detailed information about parliamentary committees. The empty response may indicate: (1) invalid/non-existent committeeId, (2) committee data not available, (3) authorization/session issue, or (4) API error without proper error response. Standard pattern for this API appears to be: send POST to /Routing/MakePostRequest with methodName field specifying the action and additional parameters as needed.

**Other**
HAR source: sobranie.mk (North Macedonia Parliament website). This is part of a larger API discovery effort for parliamentary data access. The UUID format for committeeId suggests a database-backed system. Language support indicated by languageId parameter suggests multilingual content availability. To fully document this endpoint, need to: (1) obtain valid committee IDs from listing endpoints, (2) test with different languageId values, (3) capture successful responses to document schema. Related methods likely exist for listing committees, getting members, sessions, etc. using the same routing pattern.


---

---

## Entry from logs.har (index 541)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllApplicationTypes

**Parameters**
methodName (string, required): The RPC-style method to invoke, value 'GetAllApplicationTypes'. languageId (integer, required): Language identifier for localization, observed value: 1 (likely Macedonian or default language)

**Response Structure**
Empty response body returned. Expected structure unknown - may return array of application type objects with fields like id, name, description in normal circumstances. Empty response could indicate: no data available, error condition not reflected in HTTP status, or incomplete capture.

**Documentation Notes**
This is an RPC-style POST endpoint at /Routing/MakePostRequest that acts as a gateway/router for multiple backend methods. The actual operation is determined by the 'methodName' parameter in the request body. GetAllApplicationTypes appears to retrieve application/submission types available in the parliamentary system. The languageId parameter suggests multi-language support (North Macedonia has Albanian and Macedonian as official languages). The empty response is unusual and may indicate the method requires authentication, the database has no records, or there was a backend issue not reflected in the 200 status code.

**Other**
Pattern observed: This is part of a generic routing mechanism where a single POST endpoint handles multiple operations based on methodName - common in older AJAX/RPC-style APIs. The sobranie.mk domain is the Parliament of North Macedonia's website. This endpoint likely serves the public-facing portal for viewing parliamentary applications, petitions, or legislative submissions. The empty response warrants further investigation with authenticated requests or different languageId values. Similar MakePostRequest calls likely exist for other parliamentary data retrieval operations.


---

---

## Entry from logs.har (index 623)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/questions/details/question-details.html`

**Route Type**
GET

**Method Name**
getQuestionDetailsTemplate

**Parameters**
None - This endpoint accepts no query parameters or request body. It returns a static HTML template file.

**Response Structure**
HTML template file (empty in this capture). Expected to be an AngularJS or client-side template used for rendering question details in the Moldova module. The file path suggests this is a view template rather than a data endpoint.

**Documentation Notes**
This is NOT a data API endpoint but rather a static HTML template resource. Located in /Scripts/Moldova/questions/details/ directory structure, indicating it's part of the Moldova parliamentary questions module. The template is likely loaded by a JavaScript framework (probably AngularJS given the file structure) to render question detail views on the client side. The empty response body in this capture could indicate the template hasn't been created yet, was deleted, or there was an error serving it. This is a front-end asset, not a backend API route.

**Other**
File extension is .html indicating a template file. The path structure /Scripts/Moldova/questions/details/ suggests a modular frontend architecture. This appears to be part of a larger single-page application (SPA) framework. Not useful for API discovery as it's a UI template, not a data endpoint. To find actual API endpoints for question details, look for XHR/fetch requests to paths like /api/questions/, /data/questions/, or similar JSON-returning endpoints.


---

---

## Entry from logs.har (index 685)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllCouncils

**Parameters**
methodName (string, required): 'GetAllCouncils' - specifies the backend method to invoke; languageId (integer, required): 1 - language identifier for localization (likely 1=Macedonian); StructureId (string, required): UUID format '5e00dbd6-ca3c-4d97-b748-f792b2fa3473' - identifier for organizational structure or council hierarchy

**Response Structure**
Empty response body returned with HTTP 200 status. Expected structure unknown - may return array of council objects with properties like councilId, name, description, members, or structure details when data exists. Empty response could indicate: no councils found for given StructureId, invalid parameters, or data access issue

**Documentation Notes**
This is a generic routing endpoint at /Routing/MakePostRequest that acts as a proxy/dispatcher to various backend methods. The actual method invoked is determined by the 'methodName' parameter in the request body. This pattern suggests a centralized API gateway architecture. The GetAllCouncils method appears designed to retrieve all councils within a parliamentary structure. The empty response warrants investigation - may need different StructureId or this could be an error condition not properly reflected in status code

**Other**
API Pattern: RPC-style POST endpoint using methodName routing rather than RESTful resource paths. Parliament context: sobranie.mk is the Macedonian Parliament website. The StructureId UUID likely references a specific parliamentary session, term, or organizational unit. Language support indicated by languageId parameter. Consider testing with languageId values 2+ for other languages (possibly Albanian, English). Investigate if other methodNames are available through this routing endpoint (GetCouncilById, GetCouncilMembers, etc). Empty response needs clarification - verify if this StructureId is valid or if authentication/authorization is required


---

---

## Entry from logs.har (index 704)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetCouncilDetails

**Parameters**
committeeId (string/UUID format, e.g. 'd596538c-f3d4-4440-8ae7-6e25ea094c6a'), languageId (integer, e.g. 1 for primary language, likely corresponds to Macedonian/Albanian/English language variants)

**Response Structure**
Empty response in this capture - likely returns council/committee details object when valid data exists. Expected structure unknown but probably includes: committee name, members, description, meeting schedule, status. Response format: JSON

**Documentation Notes**
Generic POST endpoint that routes to different methods based on 'methodName' parameter. This is a proxy/router pattern where the actual method is specified in the request body rather than the URL path. GetCouncilDetails retrieves information about a specific council/committee by UUID. The empty response suggests either: (1) invalid/non-existent committeeId, (2) no data available for this committee, or (3) access restrictions. The languageId parameter indicates multi-language support on the sobranie.mk (Macedonian Parliament) website.

**Other**
URL pattern '/Routing/MakePostRequest' indicates a centralized routing mechanism rather than RESTful endpoints. All POST requests appear to go through this single endpoint with methodName discrimination. This architecture suggests exploring other methodName values like: GetCommitteeList, GetMemberDetails, GetSessionDetails, etc. The UUID format for committeeId suggests a modern database backend. Testing with languageId values 1, 2, 3 may reveal Macedonian, Albanian, and English content respectively, reflecting North Macedonia's official languages.


---

---

## Entry from logs.har (index 728)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllParliamentaryGroups

**Parameters**
methodName (string, required): 'GetAllParliamentaryGroups' - specifies the API method to invoke; languageId (integer, required): 1 - language identifier for localization (1 likely represents Macedonian); StructureId (string, required): '5e00dbd6-ca3c-4d97-b748-f792b2fa3473' - UUID format identifier, likely references a specific parliamentary structure or session

**Response Structure**
Empty response body returned with 200 status. This may indicate: (1) no parliamentary groups exist for the given StructureId, (2) authentication/authorization issue returning empty instead of error, (3) the endpoint experienced an error but returned 200 anyway, or (4) data exists but serialization failed

**Documentation Notes**
This is a generic POST routing endpoint at /Routing/MakePostRequest that acts as a dispatcher to multiple backend methods. The actual method invoked is determined by the 'methodName' parameter in the request body. This pattern suggests an RPC-style API design rather than RESTful architecture. The method GetAllParliamentaryGroups is intended to retrieve all parliamentary groups (political parties/factions) for a given parliamentary structure. The empty response with 200 status is unusual and suggests either no data exists, an error condition, or incorrect parameter values. StructureId appears to be a key filtering parameter that may need to match active parliamentary sessions.

**Other**
API Pattern: RPC-style POST dispatcher; Base URL: https://www.sobranie.mk/Routing/MakePostRequest; Domain: sobranie.mk (Assembly/Parliament of North Macedonia); Testing Notes: Try different StructureId values to find active sessions, test with languageId 2 for Albanian or other language variants, investigate if authentication headers are required; Related Methods: Likely other methods exist following pattern 'GetAll*', 'Get*ById', etc. that can be invoked through same endpoint; Error Handling: Returns 200 even when no data available - check for application-level error codes in non-empty responses


---

---

## Entry from logs.har (index 745)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetParliamentaryGroupDetails

**Parameters**
parliamentaryGroupId (UUID, required): Identifier for the parliamentary group (e.g., '6f83cbd1-af39-44e5-bfd0-0cde68932844'); LanguageId (integer, required): Language selection identifier (1 appears to be default, likely Macedonian); methodName (string, required): Internal routing parameter specifying the target method

**Response Structure**
Empty response body returned with HTTP 200 status. Expected structure unknown - may indicate: (1) invalid parliamentaryGroupId, (2) no data available for this group, (3) error condition not properly communicated, or (4) successful operation with no content to return

**Documentation Notes**
This is a proxy/routing endpoint at /Routing/MakePostRequest that dispatches to internal methods. The actual method being called is '/GetParliamentaryGroupDetails' specified in the request body. The endpoint follows a non-RESTful pattern where POST is used for all operations and the method name is passed as a parameter. The empty response suggests this particular parliamentaryGroupId may be invalid or the group has no details to return. This routing pattern is consistent with other sobranie.mk API calls observed.

**Other**
The UUID format for parliamentaryGroupId suggests a database primary key. LanguageId=1 likely corresponds to Macedonian language. The empty response makes it unclear what a successful response would contain - typical parliamentary group details might include: group name, leader information, member count, political affiliation, formation date, etc. Consider testing with different parliamentaryGroupId values to determine valid identifiers and expected response structure.


---

---

## Entry from logs.har (index 765)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetAmendmentDetails

**Parameters**
languageId (integer, required): Language identifier for localization (e.g., 1 for default language). amendmentId (string/UUID, required): Unique identifier for the amendment in UUID format (e.g., '9a130205-3d0a-4394-a0b1-a0ac4b15a047'). methodName (string, required): Internal routing parameter specifying the target endpoint ('/GetAmendmentDetails').

**Response Structure**
Empty response body returned (status 200). This could indicate: (1) No amendment details found for the provided amendmentId, (2) Authentication/authorization failure silently handled, (3) Endpoint implementation issue, or (4) Data not yet available for this amendment.

**Documentation Notes**
This is a meta-routing endpoint where the actual API method is specified via the 'methodName' parameter in the request body. The base path '/Routing/MakePostRequest' acts as a dispatcher/proxy that routes to the real endpoint '/GetAmendmentDetails'. This pattern suggests a single-entry-point architecture for POST requests. The amendment system likely relates to parliamentary legislative amendments given the sobranie.mk (Macedonian Parliament) domain. The empty response may warrant investigation - either the amendmentId is invalid, or there's an error condition not properly communicated in the response. Typical amendment details would include text, proposer information, status, voting records, and related legislation references.

**Other**
The routing pattern suggests other endpoints may follow the same structure: POST to /Routing/MakePostRequest with methodName parameter specifying the actual operation. This is an unconventional API design that obscures the true endpoint structure. The UUID format for amendmentId indicates a modern database schema. Consider testing with different languageId values (likely 1=Macedonian, 2=Albanian, 3=English based on North Macedonia's official languages). The empty response without error status suggests poor API design or incomplete implementation. Recommended to capture successful responses to understand the actual data structure.


---

---

## Entry from logs.har (index 779)

**URL**: `https://www.sobranie.mk/scripts/news/singleNewsInstance.min.html`

**Route Type**
GET

**Method Name**
getSingleNewsInstanceTemplate

**Parameters**
None - This endpoint accepts no query parameters or request body. It returns a static HTML template file.

**Response Structure**
HTML template file (minified). Response body appears empty in this capture, likely due to HAR sanitization or the file being a minimal/stub template. Expected structure would be an Angular/JavaScript template for rendering individual news items, possibly containing placeholder directives or template syntax.

**Documentation Notes**
This endpoint serves a minified HTML template component located at /scripts/news/singleNewsInstance.min.html. The '.min.html' extension indicates this is a minified/optimized template file, commonly used in frontend frameworks for client-side rendering. This appears to be part of a news display system on the Macedonian Parliament (sobranie.mk) website. The template is likely loaded dynamically by JavaScript to render individual news article instances. The empty response body in this capture may indicate: 1) The file is genuinely minimal/empty, 2) HAR sanitization removed content, or 3) The template contains only whitespace or comments that were stripped. This is a static asset endpoint rather than a dynamic API endpoint.

**Other**
File location suggests modular frontend architecture with templates organized under /scripts/news/. The naming convention 'singleNewsInstance' implies there may be related endpoints for news lists or other news-related templates. This is a client-side template resource, not a REST API data endpoint. No authentication headers or cookies appear to be required for access. Status 200 indicates successful retrieval. The .min extension follows common web optimization practices for production deployments.


---

---

## Entry from logs.har (index 788)

**URL**: `https://www.sobranie.mk/Scripts/Moldova/mps-clubs/mps-clubs.html`

**Route Type**
GET

**Method Name**
getMpsClubsTemplate

**Parameters**
None - This is a static HTML template file request with no query parameters or request body

**Response Structure**
text/html - Returns an empty HTML template file (0 bytes). This appears to be a client-side template file that would normally be populated by JavaScript, possibly for displaying Members of Parliament (MPs) and their parliamentary clubs/groups

**Documentation Notes**
This endpoint retrieves an HTML template for the MPs clubs section. The path structure '/Scripts/Moldova/mps-clubs/' suggests this is part of a modular client-side application architecture where HTML templates are loaded separately. The 'Moldova' directory name is notable and may indicate this is related to the Moldova script/template system used by the Macedonian Parliament website. The empty response (0 bytes) could indicate: 1) The template file is genuinely empty and populated entirely by JavaScript, 2) An error condition where the file exists but has no content, or 3) The template is loaded but its content is injected dynamically. This is likely used in conjunction with JavaScript frameworks for single-page application (SPA) functionality to display parliamentary club/caucus information.

**Other**
File Location: /Scripts/Moldova/mps-clubs/mps-clubs.html - This follows a pattern suggesting a larger template system. The 'Scripts' directory typically contains JavaScript and associated resources, but this HTML file appears to be a template rather than executable script. The naming convention 'mps-clubs' (Members of Parliament - Clubs/Parliamentary Groups) indicates this is part of the legislative information system for displaying political groupings within the parliament. No authentication headers observed. No rate limiting headers visible. This is a public resource. Related endpoints likely exist for: /Scripts/Moldova/mps-clubs/mps-clubs.js (JavaScript), /Scripts/Moldova/mps-clubs/mps-clubs.css (styling), and API endpoints that would populate this template with actual MP and club data


---

---

## Entry from logs.har (index 791)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
GetAllMPsClubsByStructure

**Parameters**
MethodName (string, required): The API method to invoke, value 'GetAllMPsClubsByStructure'. LanguageId (integer, required): Language identifier for localization, value 1 observed (likely Macedonian). StructureId (string, required): UUID identifier for parliamentary structure/organization, format GUID, example '5e00dbd6-ca3c-4d97-b748-f792b2fa3473'.

**Response Structure**
Empty response returned in this capture. Expected structure unknown but method name suggests should return collection of MPs (Members of Parliament) organized by clubs/parliamentary groups within a specific structure. Likely returns array of objects with MP details and club/group associations.

**Documentation Notes**
Generic routing endpoint at /Routing/MakePostRequest acts as dispatcher for multiple API methods. Actual method determined by MethodName parameter in POST body. This is a facade/proxy pattern. GetAllMPsClubsByStructure retrieves MPs grouped by parliamentary clubs for a given structure ID. Empty response may indicate: no data for provided StructureId, invalid StructureId, or server-side error without error response. LanguageId 1 likely represents Macedonian language based on .mk domain. Structure appears to be organizational unit within parliament (possibly convocation/term/session).

**Other**
Endpoint uses generic routing mechanism instead of RESTful paths. All POST requests go through same URL with method specified in body. StructureId uses GUID format suggesting database-driven architecture. This pattern common in legacy or .NET applications. To discover other methods, would need to enumerate MethodName values. Response was empty which is unusual - may need authentication, different parameters, or StructureId may be invalid/expired. Consider testing with different StructureIds or checking if session/authentication required.


---

---

## Entry from logs.har (index 809)

**URL**: `https://www.sobranie.mk/Routing/MakePostRequest`

**Route Type**
POST

**Method Name**
/GetMPsClubDetails

**Parameters**
mpsClubId (string, UUID format, required) - Unique identifier for the parliamentary club/group; LanguageId (integer, required) - Language selection (1 appears to be default, likely Macedonian)

**Response Structure**
Empty response body returned in this capture. Expected structure unknown - likely returns details about a parliamentary club/group including name, members, leadership, establishment date, and other metadata when valid data exists.

**Documentation Notes**
This is a routing proxy endpoint pattern where the actual API method is specified via the 'methodName' parameter in the POST body rather than the URL path. The base endpoint /Routing/MakePostRequest acts as a gateway that routes to internal methods. The method /GetMPsClubDetails retrieves information about parliamentary clubs/groups (political party groups in parliament). The mpsClubId uses UUID format suggesting a structured database backend. Empty response may indicate: invalid club ID, club no longer exists, or data access issue. This appears to be part of the Macedonian Parliament (Sobranie) public API for accessing parliamentary data.

**Other**
Part of sobranie.mk (Macedonian Parliament) website API. Uses non-RESTful routing pattern with method name in request body. The 'MPs Club' terminology refers to parliamentary groups/caucuses formed by political parties. Similar endpoints likely exist for individual MPs, sessions, votes, and legislation. The LanguageId parameter suggests multi-language support (Macedonian, Albanian, English likely options). Consider testing with different valid club IDs and language values to map full response structure.


---