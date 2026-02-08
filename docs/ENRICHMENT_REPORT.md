# Enrichment Report

From collected samples vs docs/API_DOCS.md.

Use this to prompt an assistant to update API_INDEX.md and API_DOCS.md.

## GetAllApplicationTypes

**Comparison Result: OK**

The actual response perfectly matches the documented schema for GetAllApplicationTypes:

- ✅ Response is an array of objects
- ✅ Each object has `Id` (integer) and `ApplicationTitle` (string) properties
- ✅ All field names and types match exactly
- ✅ No extra or missing fields

The sample data shows typical application types in Macedonian, which aligns with the expected multilingual nature of the API.

---

## GetAllCommitteesForFilter

**Comparison Analysis:**

## Issues Found:

### 1. Fields in response not in docs:
- None - the actual response contains only `Id` and `Name` fields as documented.

### 2. Types/values that differ:
- None - both `Id` (UUID string) and `Name` (string) match the documented schema exactly.

### 3. Schema improvements:
- **Missing constraint**: The documented schema should specify `"required": ["Id", "Name"]` to indicate these fields are always present.
- **Array constraint**: Consider adding `"minItems": 0` to clarify that empty arrays are possible.

## Overall Assessment:
The actual response **conforms perfectly** to the documented schema. The response structure, field names, and data types all match exactly. Only minor schema enhancements suggested for completeness.

**Status: OK** (with minor documentation enhancement opportunities)

---

## GetAllCouncils

OK

The actual response perfectly matches the documented schema for GetAllCouncils. All fields are present with correct types:
- `Id`: string (UUID format)
- `Name`: string 
- `TypeId`: integer
- `TypeTitle`: string

No discrepancies found.

---

## GetAllGenders

The actual response matches the documented schema perfectly:

✅ **Schema compliance**: OK

The response correctly returns:
- An array of objects
- Each object has `Id` (integer) and `Title` (string) properties
- Types match exactly as documented
- No extra or missing fields

---

## GetAllInstitutionsForFilter

**OK**

The actual response perfectly matches the documented schema for GetAllInstitutionsForFilter:
- Array structure: ✓
- Object properties: `Id` (string, UUID format) and `Title` (string): ✓  
- Data types and formats: ✓
- No missing or extra fields

The response shows Macedonian government ministries with proper UUID identifiers and titles, all conforming to the expected schema.

---

## GetAllMPsClubsByStructure

**Comparison Result: OK**

The actual API response perfectly matches the documented schema for `GetAllMPsClubsByStructure`:

- **Structure**: Array of objects ✓
- **Field names**: `Id` and `Name` present in all items ✓
- **Data types**: 
  - `Id` is string with UUID format ✓
  - `Name` is string ✓
- **No missing or extra fields**
- **No type mismatches**

The response contains 9 parliamentary club/group items, all conforming exactly to the expected schema.

---

## GetAllMaterialStatusesForFilter

OK.

The actual response perfectly matches the documented schema for GetAllMaterialStatusesForFilter. It's an array of objects with integer `Id` and string `Title` properties, exactly as specified.

---

## GetAllMaterialTypesForFilter

**Comparison Result: OK**

The actual response perfectly matches the documented schema for `GetAllMaterialTypesForFilter`. All items contain:
- `Id` (integer) - matches schema
- `Title` (string) - matches schema

No discrepancies found in fields, types, or values.

---

## GetAllMaterialsForPublicPortal

Comparing the actual response to the documented schema for GetAllMaterialsForPublicPortal:

**1. Fields in response not in docs:**
None - all fields in the actual response are documented.

**2. Types/values that differ:**
- **RegistrationDate values**: The actual response contains dates in the future (year 2026: `/Date(1769693654000)/`, `/Date(1769691810000)/`, etc.) which suggests either test data or a timestamp conversion issue.

**3. Schema improvements:**
- **Authors array handling**: The schema should clarify that when `ResponsibleAuthor` is a non-MP (like a minister), the `Authors` array contains one item with:
  - `Id`: `"00000000-0000-0000-0000-000000000000"` 
  - `FirstName`: Full title/name
  - `LastName`: Empty string
- **Date validation**: Consider adding validation for reasonable date ranges in the AspDate pattern.

Otherwise the schema accurately matches the response structure and types.

---

## GetAllParliamentaryGroups

**Comparison Result: OK**

The actual API response perfectly matches the documented schema for GetAllParliamentaryGroups:

- ✅ All fields present: `Id`, `Name`, `NumberOfDeputies`, `Image`
- ✅ Correct types: UUID strings, strings, integers, strings
- ✅ Array structure matches
- ✅ No extra or missing fields

The response is fully compliant with the documented schema.

---

## GetAllPoliticalParties

**Comparison Result: OK**

The actual API response perfectly matches the documented schema for GetAllPoliticalParties:

- ✅ All fields present and correctly typed: `Id` (UUID string), `Name` (string), `NumberOfDeputies` (integer), `Image` (string)
- ✅ Response structure matches: array of objects
- ✅ Field names match exactly (case-sensitive)
- ✅ Data types align with schema definitions
- ✅ UUID format validation would pass for all `Id` values

No discrepancies found.

---

## GetAllProcedureTypes

**Comparison Result: OK**

The actual API response perfectly matches the documented schema for GetAllProcedureTypes:

✅ **Structure**: Array of objects as expected  
✅ **Fields**: Both `Id` (integer) and `Title` (string) present  
✅ **Types**: Correct data types  
✅ **Values**: Proper Macedonian text content  

No discrepancies found.

---

## GetAllQuestionStatuses

The actual response matches the documented schema perfectly. Both show:

- Array of objects
- Each object has `Id` (integer) and `Title` (string) properties
- All data types align correctly

**OK** - No discrepancies found.

---

## GetAllQuestions

Comparing the actual response to the documented schema for GetAllQuestions:

**1. Fields in response not in docs:**
- `ToInstitution` (string) - The institution the question is directed to
- `QuestionTypeTitle` (string) - Type of question (e.g., "Писмено прашање", "Усно прашање")
- `TotalRows` (integer) - Always 0 in the sample

**2. Types/values that differ:**
- `DateAsked` uses AspDate format (`/Date(1769767343000)/`) but this field is missing from the documented schema entirely

**3. Schema improvements needed:**
The documented schema appears to be incomplete - it cuts off mid-sentence at the `From` property and doesn't include the complete response structure. The actual response has 8 additional fields beyond what's documented.

The documented schema should be updated to include all fields present in the actual response.

---

## GetAllSittingStatuses

**Issues found:**

1. **Missing documentation**: The `GetAllSittingStatuses` method is not documented in the provided schema documentation.

2. **Schema needed**: Based on the actual response, the schema should be:

```json
{
  "type": "array",
  "items": {
    "type": "object", 
    "properties": {
      "Id": {
        "type": "integer"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

This follows the same pattern as other similar endpoints like `GetAllQuestionStatuses`, `GetAllProcedureTypes`, etc.

---

## GetAllSittings

Looking at the actual response compared to the documented schema:

**Issues found:**

1. **Missing schema**: There is no documented schema for `GetAllSittings` in the provided API docs. The docs end abruptly in the middle of the `GetAllQuestions` response schema.

2. **Cannot validate**: Without the documented `GetAllSittings` schema, I cannot compare field presence, types, or values.

**Schema needed:**
The docs should include a complete schema for `GetAllSittings` showing:
- Request format 
- Response structure when `TotalItems > 0` and `Items` contains data
- The structure of individual sitting objects in the `Items` array

The current response shows an empty result set, so we'd need a response with actual data to define the complete schema.

---

## GetAllStructuresForFilter

**Issues found:**

1. **Missing from docs**: The `GetAllStructuresForFilter` endpoint is not documented in the provided API_DOCS.md

2. **Schema needed**: Based on the response, the schema should be:
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
      "DateFrom": {
        "$ref": "#/$defs/AspDate"
      },
      "DateTo": {
        "$ref": "#/$defs/AspDate"
      },
      "IsCurrent": {
        "type": "boolean"
      }
    }
  }
}
```

The response follows the expected patterns (UUID strings, AspDate format) but this entire endpoint is missing from the documentation.

---

## GetCommitteeDetails

**Issues found:**

1. **Missing from docs**: The `GetCommitteeDetails` operation is completely absent from the documented schemas.

2. **Schema needed**: Based on the response, the missing schema should be:

```json
{
  "type": "object", 
  "properties": {
    "Name": { "type": "string" },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "type": "string", "format": "uuid" },
          "FullName": { "type": "string" },
          "RoleId": { "type": "integer" },
          "RoleTitle": { "type": "string" }
        }
      }
    },
    "SecretariatMembers": {
      "type": "array", 
      "items": { "$ref": "#/CompositionMembers/items" }
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "Title": { "type": "string" },
          "RegistrationDate": { "$ref": "#/$defs/AspDate" },
          "RegistrationNumber": { "type": "string" },
          "StatusId": { "type": "integer" },
          "StatusTitle": { "type": "string" }
        }
      }
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object", 
        "properties": {
          "Id": { "type": "string", "format": "uuid" },
          "TypeTitle": { "type": "string" },
          "Date": { "$ref": "#/$defs/AspDate" },
          "Location": { "type": "string" },
          "SittingNumber": { "type": "integer" }
        }
      }
    }
  }
}
```

The documentation is incomplete - missing this entire endpoint.

---

## GetCouncilDetails

Looking at the actual GetCouncilDetails response compared to the documented schemas, I notice:

## Missing from Documentation

The GetCouncilDetails operation is **not documented at all** in the API_DOCS.md file. The response contains these fields that need to be added to the documentation:

1. **Fields in response not in docs**: All fields are missing since the entire operation is undocumented:
   - `Name` (string)
   - `CompositionMembers` (array of objects)
   - `SecretariatMembers` (array of objects) 
   - `Materials` (array)
   - `Meetings` (array of objects)
   - `Description` (string/null)
   - `Email` (string)
   - `PhoneNumber` (string/null)
   - `StructureId` (string/UUID)

2. **Schema patterns observed**:
   - Member objects have: `UserId` (UUID), `FullName` (string), `RoleId` (integer), `RoleTitle` (string)
   - Meeting objects have: `Id` (UUID), `TypeTitle` (string), `Date` (AspDate format), `Location` (string), `SittingNumber` (integer)
   - Follows existing UUID and AspDate patterns from other operations

3. **Schema improvements needed**:
   - Add complete GetCouncilDetails request/response schema
   - Define reusable member and meeting object schemas in `$defs`
   - Document the request parameters (likely councilId and languageId based on other patterns)

The response structure is consistent with other API operations but this entire endpoint needs to be added to the documentation.

---

## GetCustomEventsCalendar

**Issues found:**

1. **Fields in response not in docs:** The API response includes fields not documented anywhere:
   - `__type` (string with .NET type info)
   - `Id` (UUID format)
   - `EventDescription` (string)
   - `EventLink` (string)  
   - `EventLocation` (string)
   - `EventDate` (AspDate format)
   - `EventType` (integer)

2. **Response wrapper differs:** Actual response is wrapped in `{"d": [...]}` but no documented schema shows this wrapper pattern.

3. **Missing schema:** `GetCustomEventsCalendar` is completely missing from the documented schemas.

**Schema needed:**
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array", 
      "items": {
        "type": "object",
        "properties": {
          "__type": {"type": "string"},
          "Id": {"type": "string", "format": "uuid"},
          "EventDescription": {"type": "string"},
          "EventLink": {"type": "string"},
          "EventLocation": {"type": "string"},
          "EventDate": {"$ref": "#/$defs/AspDate"},
          "EventType": {"type": "integer"}
        }
      }
    }
  }
}
```

---

## GetMPsClubDetails

**Issues found:**

1. **Missing from docs**: The `GetMPsClubDetails` endpoint is not documented at all in the provided schema documentation.

2. **Response structure differs**: The actual response is a single object, not an array like other similar endpoints (e.g., `GetAllMPsClubsByStructure` which returns an array of clubs with `Id` and `Name`).

**Schema needed:**

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
    "Members": {
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
          },
          "RoleId": {
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

---

## GetMaterialDetails

Looking at the GetMaterialDetails response compared to the documented schemas, I notice several issues:

## Missing Schema
**GetMaterialDetails is not documented at all** - this is a major gap since it appears to be a core API operation.

## Fields in response not in any documented schema:
- `Institution`
- `ProposerCommittee` 
- `ProcedureTypeTitle`
- `ParentTitle`
- `FirstReadingAmendments`
- `SecondReadingAmendments`
- `FirstReadingSittings`

## New object structures not documented:
- **Committee objects** with `IsLegislative`, `IsResponsible`, `Documents` properties
- **Document objects** with `DocumentTypeId`, `DocumentTypeTitle`, `IsExported` properties
- **Sitting objects** with `SittingTypeId`, `SittingTypeTitle`, `SittingDate`, `CommitteeId`, `CommitteeTitle`, `StatusGroupId`, `ObjectStatusId`, `SittingTitle`, `SittingNumber`, `VotingResults` properties

## Schema improvements needed:
1. **Add complete GetMaterialDetails schema** to API_DOCS.md
2. **Define reusable object schemas** in `$defs` for:
   - Committee (extended version)
   - Document (with type info)
   - Sitting
   - VotingResult
3. **Update existing schemas** that reference committees/documents to use the fuller object structure

The response suggests this API has much richer data models than currently documented.

---

## GetMonthlyAgenda

The GetMonthlyAgenda schema is **missing from the API documentation**. Based on the actual response, here's what needs to be added:

## Missing Schema: GetMonthlyAgenda

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
      "Title": {
        "type": "string"
      },
      "Location": {
        "type": "string"
      },
      "Start": {
        "$ref": "#/$defs/AspDate"
      },
      "Type": {
        "type": "integer",
        "description": "1=Assembly session, 2=Committee session"
      }
    }
  }
}
```

**Issues found:**
1. Complete schema missing from documentation
2. The response also includes a `"_truncated": 31` field indicating pagination, which should be documented
3. Request schema unknown - needs to be documented

---

## GetOfficialVisitsForUser

**Issue: Missing schema documentation**

The documented schema does not include `GetOfficialVisitsForUser`. The actual response shows:

1. **Response structure**: `{"d": []}` - follows the standard ASP.NET web service wrapper pattern used by other endpoints
2. **Empty array**: Indicates the endpoint returns an array of visit objects when data is present

**Schema needed**:
```json
{
  "type": "object", 
  "properties": {
    "d": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          // Visit object schema to be determined from non-empty response
        }
      }
    }
  }
}
```

The documentation should be updated to include this endpoint's complete schema once a response with actual visit data is available.

---

## GetParliamentMPsNoImage

Comparing the API response to the documented schema:

**Issues found:**

1. **Missing schema**: No documented schema exists for `GetParliamentMPsNoImage` in the provided API_DOCS.md

2. **Response structure analysis** (based on sample):
   - Root object has `MembersOfParliament` array property
   - Each MP object contains:
     - `UserId`: string (UUID format)
     - `UserImg`: string (base64 encoded image data)
     - `FullName`: string 
     - `RoleId`: integer
     - `PoliticalPartyTitle`: string
     - `PoliticalPartyId`: string (UUID format)

3. **Inconsistency**: Method name suggests "NoImage" but response includes `UserImg` field with base64 image data

**Schema needed:**
```json
{
  "type": "object", 
  "properties": {
    "MembersOfParliament": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {"type": "string", "format": "uuid"},
          "UserImg": {"type": "string"},
          "FullName": {"type": "string"},
          "RoleId": {"type": "integer"}, 
          "PoliticalPartyTitle": {"type": "string"},
          "PoliticalPartyId": {"type": "string", "format": "uuid"}
        }
      }
    }
  }
}
```

---

## GetParliamentaryGroupDetails

## Issues Found

**1. Fields in response not documented:**
- `Description` (string)
- `StatusId` (integer) in Materials and Amendments arrays
- `StatusTitle` (string) in Materials and Amendments arrays

**2. Missing schema entirely:**
`GetParliamentaryGroupDetails` is not documented in the provided API_DOCS.md

**3. Schema needed:**
```json
{
  "methodName": "GetParliamentaryGroupDetails",
  "request": {
    "type": "object",
    "properties": {
      "methodName": {"type": "string"},
      "languageId": {"$ref": "#/$defs/LanguageId"},
      "groupId": {"type": "string", "format": "uuid"}
    }
  },
  "response": {
    "type": "object", 
    "properties": {
      "Name": {"type": "string"},
      "Description": {"type": "string"},
      "NumberOfDeputies": {"type": "integer"},
      "Materials": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Id": {"type": "string", "format": "uuid"},
            "Title": {"type": "string"},
            "RegistrationDate": {"$ref": "#/$defs/AspDate"},
            "RegistrationNumber": {"type": "string"},
            "StatusId": {"type": "integer"},
            "StatusTitle": {"type": "string"}
          }
        }
      },
      "Amendments": {
        "type": "array",
        "items": {
          "type": "object", 
          "properties": {
            "Id": {"type": "string", "format": "uuid"},
            "Title": {"type": "string"},
            "RegistrationDate": {"$ref": "#/$defs/AspDate"},
            "RegistrationNumber": {"type": "string"},
            "StatusId": {"type": "integer"},
            "StatusTitle": {"type": "string"}
          }
        }
      }
    }
  }
}
```

---

## GetPoliticalPartyDetails

**Issues found:**

1. **Missing schema**: No `GetPoliticalPartyDetails` schema exists in the documentation - only `GetAllPoliticalParties` is documented.

2. **Response structure differs**: The documented `GetAllPoliticalParties` returns an array of simple objects, but this response is a detailed single object with nested arrays.

3. **Additional fields not in docs**: 
   - `Description`, `Email`, `Phone`, `StructureId`
   - `Materials[]`, `Amendments[]`, `Questions[]`, `Members[]` arrays
   - Material objects have `StatusId`, `StatusTitle` 
   - Member objects have `UserId`, `RoleId`, `RoleTitle`, count fields

4. **Type differences**:
   - `Image` can be empty string (not just populated string)
   - Various count fields are `null` instead of integers

**Recommendation**: Add complete `GetPoliticalPartyDetails` schema to documentation, as this appears to be a different endpoint from `GetAllPoliticalParties`.

---

## GetProposerTypes

**Issues found:**

1. **Missing from docs**: The `GetProposerTypes` endpoint is not documented in the schema at all.

2. **Response structure**: Based on the actual response, the schema should be:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "Title": {
        "type": "string"
      },
      "Order": {
        "type": "integer"
      }
    }
  }
}
```

3. **Additional field**: The response includes an `Order` field that would need to be documented.

**Schema improvements needed:**
- Add complete documentation for `GetProposerTypes` endpoint
- Include the `Order` field in the response schema
- Add request schema (likely similar to other endpoints with `methodName` and `languageId`)

---

## GetQuestionDetails

Comparing the actual response to the documented schema:

**Issues found:**

1. **Missing schema**: There is no documented schema for `GetQuestionDetails` in the provided API_DOCS.md

2. **Incomplete schema in docs**: The `GetAllQuestions` schema is cut off mid-field (`"From": { "type": "string"`) and doesn't show the complete response structure

**Response structure analysis:**
The actual response contains these fields:
- `Title` (string)
- `From` (string) 
- `To` (string)
- `ToInstitution` (string)
- `QuestionTypeTitle` (string)
- `StatusTitle` (string)
- `NumberOfDeliveryLetter` (null)
- `Documents` (array of objects with Id, Title, Url, FileName, DocumentTypeId, DocumentTypeTitle, IsExported)
- `Sittings` (empty array)

**Recommended addition to API_DOCS.md:**

```json
## GetQuestionDetails

### Response
{
  "type": "object",
  "properties": {
    "Title": {"type": "string"},
    "From": {"type": "string"},
    "To": {"type": "string"},
    "ToInstitution": {"type": "string"},
    "QuestionTypeTitle": {"type": "string"},
    "StatusTitle": {"type": "string"},
    "NumberOfDeliveryLetter": {"type": ["string", "null"]},
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {"type": "string", "format": "uuid"},
          "Title": {"type": "string"},
          "Url": {"type": "string"},
          "FileName": {"type": ["string", "null"]},
          "DocumentTypeId": {"type": "integer"},
          "DocumentTypeTitle": {"type": "string"},
          "IsExported": {"type": "boolean"}
        }
      }
    },
    "Sittings": {"type": "array"}
  }
}
```

---

## GetSittingDetails

**Issues found:**

## (1) Fields in response not in documented schema:
The API response contains many fields not documented in the provided schema. However, **no schema for GetSittingDetails exists in the documentation** - this appears to be a missing endpoint entirely.

## (2) Types/values that differ:
Cannot compare - no GetSittingDetails schema provided.

## (3) Schema needed:
The complete GetSittingDetails response schema should be added to API_DOCS.md:

```json
## GetSittingDetails

### Response
{
  "type": "object",
  "properties": {
    "StatusId": {"type": "integer"},
    "StatusTitle": {"type": "string"},
    "Location": {"type": "string"},
    "Number": {"type": "integer"},
    "SittingDate": {"$ref": "#/$defs/AspDate"},
    "TypeTitle": {"type": "string"},
    "TypeId": {"type": "integer"},
    "CommitteeId": {"type": "string", "format": "uuid"},
    "CommitteeTitle": {"type": "string"},
    "MediaLinks": {"type": "array"},
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {"type": "string", "format": "uuid"},
          "Title": {"type": "string"},
          "Url": {"type": "string"},
          "FileName": {"type": ["string", "null"]},
          "DocumentTypeId": {"type": "integer"},
          "DocumentTypeTitle": {"type": "string"},
          "IsExported": {"type": "boolean"}
        }
      }
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "text": {"type": "string"},
        "type": {"type": "string"},
        "children": {"type": "array"}
        // ... (nested agenda structure)
      }
    },
    "Absents": {
      "type": "array", 
      "items": {
        "properties": {
          "Id": {"type": "string", "format": "uuid"},
          "Fullname": {"type": "string"},
          "PoliticalParty": {"type": ["string", "null"]}
        }
      }
    }
    // ... (other fields)
  }
}
```

---

## GetUserDetailsByStructure

**Issues found:**

1. **Missing from docs**: The `GetUserDetailsByStructure` endpoint is completely missing from the documented schemas.

2. **Fields in response not documented**:
   - `FullName`, `Email`, `Image`, `MobileNumber`, `PhoneNumber`, `Biography`
   - `RoleId`, `RoleTitle`, `ElectedFrom`, `ElectedTo`
   - `PoliticalPartyId`, `PoliticalPartyTitle`, `Gender`, `DateOfBirth`
   - `Constituency`, `Coalition`, `StructureDate`
   - `CabinetMembers`, `Materials`, `Questions`, `Delegations`
   - `FriendshipGroups`, `Amendments` (with nested objects containing `Id`, `Title`, `RegistrationDate`, `RegistrationNumber`, `StatusId`, `StatusTitle`)

3. **Schema needed**: The docs require a complete schema definition for `GetUserDetailsByStructure` showing:
   - Request format (likely includes `methodName`, `languageId`, `structureId`, `userId`)
   - Response object with all the fields listed above
   - Proper typing for dates (using `AspDate` reference), UUIDs, integers, and nullable fields

This appears to be a user/MP profile endpoint returning detailed biographical and legislative activity data.

---

## LoadLanguage

**Issues found:**

1. **Missing from docs**: The `LoadLanguage` operation is not documented in the provided schema documentation.

2. **Schema needed**: The response structure is:
```json
{
  "type": "object",
  "properties": {
    "Code": {
      "type": "string",
      "description": "Language/locale code (e.g., 'mk-MK')"
    },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Key": {
            "type": "string",
            "description": "Localization key"
          },
          "Value": {
            "type": "string",
            "description": "Localized text value"
          }
        }
      }
    }
  }
}
```

3. **Request schema needed**: Should document the expected request format for `LoadLanguage` (likely includes `methodName` and `languageId` parameters consistent with other operations).

The API_DOCS.md should be updated to include the complete `LoadLanguage` operation documentation.
