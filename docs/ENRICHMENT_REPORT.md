# Enrichment Report

From collected samples vs docs/API_DOCS.md.

Use this to prompt an assistant to update API_INDEX.md and API_DOCS.md.

---

**Status:** Applied. API_DOCS.md and API_INDEX.md updated per findings below.

## GetAllApplicationTypes

OK

The actual response matches the documented schema perfectly:
- All fields (`Id`, `ApplicationTitle`) are present with correct types
- No extra fields in the response
- Values conform to expected string/integer types
- Array structure matches exactly

---

## GetAllCommitteesForFilter

Looking at the actual response against the documented schema for GetAllCommitteesForFilter:

**Schema comparison**: OK

The actual response perfectly matches the documented schema:
- Returns an array of objects
- Each object has `Id` (UUID string) and `Name` (string) properties
- All UUIDs are properly formatted
- All names are non-empty strings

The response structure is simple and consistent with the documentation. No improvements needed.

---

## GetAllCouncils

OK

The actual response perfectly matches both the documented schema and inferred schema. All fields, types, and structure align correctly with no discrepancies.

---

## GetAllGenders

OK.

The actual response perfectly matches the documented schema. The response contains exactly two gender entries with IDs 1 and 2, and Macedonian titles "Машки" (Male) and "Женски" (Female), which aligns with the `GenderId` definition in `$defs`.

---

## GetAllInstitutionsForFilter

## Comparison Results

**Issues found:**

1. **Anomalous data**: Entry with `"Title": "/"` (ID: eb0e5bfd-ee7e-40f2-8cab-322cefd440fd) appears to be invalid/placeholder data that should be filtered out or investigated.

**Otherwise**: The actual response perfectly matches both the documented and inferred schemas. All UUIDs are properly formatted and titles are non-empty strings (except for the anomalous "/" entry).

**Schema recommendation**: Consider adding validation to exclude entries with placeholder titles like "/" or add a note about potential data quality issues.

---

## GetAllMPsClubsByStructure

OK

The actual response perfectly matches both the documented schema and inferred schema. All items contain the expected `Id` (UUID format) and `Name` (string) properties with no deviations or additional fields.

---

## GetAllMaterialStatusesForFilter

## Comparison Results

### 1. Fields in response not in docs
None - all fields match.

### 2. Types/values that differ from docs
The actual response is missing some `MaterialStatusId` values from the `$defs`:
- Missing: `0` (Plenary/unknown)
- Present: `6, 9, 10, 11, 12, 24, 64` ✓

### 3. Concrete schema improvements
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

**Note**: The response only includes filterable material statuses (excludes status `0`), which makes sense for a filter endpoint.

---

## GetAllMaterialTypesForFilter

**Analysis of GetAllMaterialTypesForFilter**

## 1. Fields in response not in docs
None - all response fields (`Id`, `Title`) are documented.

## 2. Types/values that differ from docs
None - both `Id` (integer) and `Title` (string) match the documented types.

## 3. Concrete schema improvements
None needed - the documented schema accurately describes the response structure. The inferred schema matches the documented schema exactly.

**OK** - The actual response perfectly conforms to the documented schema.

---

## GetAllMaterialsForPublicPortal

## Comparison Results

### 1. Fields in response not in docs
None - all fields match the documented schema.

### 2. Types/values that differ from docs
None - all types match exactly.

### 3. Concrete schema improvements

The documented schema should use `$defs` reference for the date field:

```json
"RegistrationDate": {
  "$ref": "#/$defs/AspDate"
}
```

Instead of the current inline definition. The inferred schema already shows this correctly.

### Additional observations
- **Institutional authors pattern confirmed**: Multiple examples show `Id: "00000000-0000-0000-0000-000000000000"` with full institutional names in `FirstName` and empty `LastName` (government, committees, state agencies).
- **ResponsibleCommittee behavior**: Can be empty string `""` for some material types (appointments, resignations) rather than always having a committee assignment.

**Status: Schema is accurate, minor improvement suggested for date field reference.**

---

## GetAllParliamentaryGroups

**Comparison Results:**

1. **Fields in response not in docs**: None

2. **Types/values that differ from docs**: None

3. **Concrete schema improvements**: 
   - Add `required` fields specification
   - The `Image` field appears to consistently be an empty string rather than containing actual image data/URLs

**Suggested schema refinement:**
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
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0
      },
      "Image": {
        "type": "string"
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

The documented schema matches the actual response structure perfectly.

---

## GetAllPoliticalParties

**Analysis:**

1. **Fields in response not in docs:** None
2. **Types/values that differ from docs:** None
3. **Schema improvements:** None needed

The actual response perfectly matches the documented schema. All fields (`Id`, `Name`, `NumberOfDeputies`, `Image`) are present with correct types (UUID string, string, integer, string). The `Image` field appears to be consistently empty strings in this dataset, but that's valid according to the string type specification.

**OK**

---

## GetAllProcedureTypes

OK

The actual response perfectly matches the documented schema. All fields (`Id`, `Title`) are present with correct types, and the `Id` values (1, 2, 3) align with the `ProcedureTypeId` enum in `$defs`. The response contains the expected procedure types: Regular (Редовна постапка), Shortened (Скратена постапка), and Urgent (Итна постапка).

---

## GetAllQuestionStatuses

**Comparison Results:**

1. **Fields in response not in docs**: None

2. **Types/values that differ from docs**: None

3. **Concrete schema improvements**:
   - Use `$defs` reference for the Id field:
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
       }
     }
   }
   ```

The actual response perfectly matches the documented schema and contains exactly the question status IDs defined in the `QuestionStatusId` enum (17, 19, 20, 21).

---

## GetAllQuestions

## Analysis of GetAllQuestions Response vs Schema

### 1. Fields in response not in docs
None - all fields match the documented schema.

### 2. Types/values that differ from docs
- **DateAsked timestamps**: The actual timestamps (1769767343000, 1769699430000, etc.) represent dates far in the future (around 2026), which seems unusual but follows the correct ASP.NET Date format.

### 3. Concrete schema improvements

The documented schema should use the $defs reference for DateAsked:

```json
{
  "DateAsked": {
    "$ref": "#/$defs/AspDate"
  }
}
```

Instead of defining the pattern inline. The inferred schema correctly shows this pattern, but it should reference the common $defs definition for consistency.

**Minor observation**: Some responses show typos in the `To` field (e.g., "Република Северна Макоеднија" instead of "Македонија"), but this is data quality rather than schema issue.

Overall: **Schema is accurate** - just needs the $defs reference improvement for DateAsked.

---

## GetAllSittingStatuses

## Comparison Results

**1. Fields in response not in docs:** None

**2. Types/values that differ from docs:** None

**3. Concrete schema improvements:**
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

The response perfectly matches the documented schema. The only improvement is using the `SittingStatusId` reference from `$defs` for the `Id` field, which validates that all expected status IDs (1-6) are present in the actual response.

---

## GetAllSittings

## Analysis of GetAllSittings API Response

### 1. Fields in response not in docs
None - all fields match.

### 2. Types/values that differ from docs
**Items field**: 
- Documented as `"type": "array"`
- Actual responses show `"Items": null` when `TotalItems: 0`
- Should allow both array and null

### 3. Concrete schema improvements

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
          "Id": {"type": "string", "format": "uuid"},
          "SittingTypeId": {"$ref": "#/$defs/AgendaItemTypeId"},
          "StatusId": {"$ref": "#/$defs/SittingStatusId"},
          "DateFrom": {"$ref": "#/$defs/AspDate"},
          "DateTo": {"$ref": "#/$defs/AspDate"},
          "CommitteeId": {"type": ["string", "null"], "format": "uuid"},
          "CommitteeTitle": {"type": ["string", "null"]},
          "Number": {"type": ["integer", "null"]},
          "SessionId": {"type": ["string", "null"], "format": "uuid"}
        }
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```

**Key fix**: `Items` should be `["array", "null"]` since it's null when no results exist.

---

## GetAllStructuresForFilter

## Comparison Analysis

### 1. Fields in response not in docs
None - all fields match.

### 2. Types/values that differ from docs
None - all types match exactly.

### 3. Concrete schema improvements

The documented schema should use the `$defs` reference for date fields:

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

The documented schema already correctly uses `$defs/AspDate` - no changes needed.

**Status**: OK - documented schema is correct and complete.

---

## GetCommitteeDetails

## Comparison Results

### 1. Fields in response not in docs
None - all response fields match the documented schema.

### 2. Types/values that differ from docs
- **Date fields**: Documented as `$ref: "#/$defs/AspDate"` but inferred schema shows expanded definition. Should use the reference.
- **PhoneNumber**: Documented as `type: "null"` but should be `type: ["string", "null"]` to allow actual phone numbers.

### 3. Concrete schema improvements

```json
{
  "type": "object",
  "properties": {
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          }
        }
      }
    },
    "Meetings": {
      "type": "array", 
      "items": {
        "type": "object",
        "properties": {
          "Date": {
            "$ref": "#/$defs/AspDate"
          }
        }
      }
    },
    "PhoneNumber": {
      "type": ["string", "null"]
    }
  }
}
```

The documented schema is largely correct but should use `$defs` references consistently and allow for non-null phone numbers.

---

## GetCouncilDetails

## Comparison Results

### 1. Fields in response not in documented schema
- None. All fields present in the response match the documented schema.

### 2. Type/value differences from documented schema
- **`Meetings[].Date`**: Documented as `{"$ref": "#/$defs/AspDate"}` but inferred schema shows `{"type": "string", "format": "asp-date", "pattern": "^/Date\\(\\d+\\)/$"}`. The actual responses confirm ASP.NET date format like `/Date(1764928800000)/`.

### 3. Concrete schema improvements

```json
{
  "type": "object",
  "properties": {
    "Name": {"type": "string"},
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object", 
        "properties": {
          "UserId": {"type": "string", "format": "uuid"},
          "FullName": {"type": "string"},
          "RoleId": {"type": "integer"},
          "RoleTitle": {"type": "string"}
        }
      }
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {"type": "string", "format": "uuid"},
          "FullName": {"type": "string"},
          "RoleId": {"type": "integer"},
          "RoleTitle": {"type": "string"}
        }
      }
    },
    "Materials": {"type": "array", "items": {}},
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {"type": "string", "format": "uuid"},
          "TypeTitle": {"type": "string"},
          "Date": {"$ref": "#/$defs/AspDate"},
          "Location": {"type": "string"},
          "SittingNumber": {"type": "integer"}
        }
      }
    },
    "Description": {"type": ["string", "null"]},
    "Email": {"type": "string"},
    "PhoneNumber": {"type": "null"},
    "StructureId": {"type": "string", "format": "uuid"}
  }
}
```

**Key fix**: Use `{"$ref": "#/$defs/AspDate"}` for `Meetings[].Date` to maintain consistency with the common patterns.

---

## GetCustomEventsCalendar

## Comparison Results

### 1. Fields in response not in docs
- `__type`: Present in all actual items but not documented

### 2. Types/values that differ from docs
- All documented types match actual response values
- `EventDate` follows the expected ASP.NET date format `/Date(\d+)/`
- `EventType` values (all 5 in sample) are integers as expected

### 3. Concrete schema improvements
The documented schema should:
- Add `__type` field:
```json
"__type": {
  "type": "string",
  "const": "moldova.controls.Models.CalendarViewModel"
}
```
- Use `$ref` for EventDate:
```json
"EventDate": {
  "$ref": "#/$defs/AspDate"
}
```

The inferred schema correctly includes the ASP.NET date pattern but misses the `__type` field.

---

## GetMPsClubDetails

The actual API responses match the documented schema perfectly. All fields, types, and structures align correctly:

- **Name**: string ✓
- **Description**: string ✓  
- **Members**: array of objects with Id (uuid), FirstName/LastName (strings), RoleId (integer), RoleTitle (string) ✓
- **StructureId**: uuid string ✓

The responses show consistent role structures:
- RoleId 78 = "Претседател/Претседателка" (President)
- RoleId 79 = "Заменик-претседател/Заменик-претседателка" (Vice President)  
- RoleId 81 = "Член/Членка" (Member)

**OK** - No discrepancies found between documented schema and actual responses.

---

## GetMaterialDetails

## Analysis of GetMaterialDetails Response vs Schema

### 1. Fields in response not in docs
- None. All fields in the actual responses are present in the documented schema.

### 2. Types/values that differ from docs

**RegistrationDate and SittingDate**:
- **Documented**: Uses `$ref: "#/$defs/AspDate"`
- **Inferred**: Uses inline definition with `"type": "string", "format": "asp-date", "pattern": "^/Date\\(\\d+\\)/$"`
- **Actual**: Contains `/Date(1769693654000)/` format matching the pattern

**CommitteeId in FirstReadingSittings**:
- **Documented**: `"type": "string", "nullable": true`
- **Actual**: Contains UUID strings like `"8811dffb-8d40-4e16-9a72-a51f4eac33e7"`
- **Issue**: Should specify `"format": "uuid"` when not null

### 3. Concrete schema improvements

```json
{
  "RegistrationDate": {
    "$ref": "#/$defs/AspDate"
  },
  "FirstReadingSittings": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "SittingDate": {
          "$ref": "#/$defs/AspDate"
        },
        "CommitteeId": {
          "type": ["string", "null"],
          "format": "uuid"
        }
      }
    }
  }
}
```

**Key fix**: Use `$defs/AspDate` reference consistently instead of inline definitions, and add UUID format to CommitteeId when not null.

---

## GetMonthlyAgenda

## Comparison Results

**1. Fields in response not in docs:**
None - all response fields match documented schema.

**2. Types/values that differ from docs:**
- `Start` field format inconsistency: Documented schema uses `$ref` to AspDate, but inferred schema shows explicit pattern. Both are functionally equivalent.

**3. Concrete schema improvements:**

The documented schema should use the `$defs` reference consistently:

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
        "$ref": "#/$defs/AgendaItemTypeId"
      }
    }
  }
}
```

**Key improvement:** Reference `AgendaItemTypeId` for the `Type` field since the actual values (1=Plenary, 2=Committee) match this definition perfectly.

---

## GetOfficialVisitsForUser

OK

The actual response matches the documented schema perfectly. The response contains an empty array in the `d` property, which aligns with the documented structure. Since the array is empty, no concrete schema improvements for the items can be determined from this response.

---

## GetParliamentMPsNoImage

Analyzing the actual API responses against the documented schema for GetParliamentMPsNoImage:

**Issues found:**

1. **Format inconsistency in ExpiredMandateMembers**: In the documented schema, `ExpiredMandateMembers[].PoliticalPartyId` is typed as `string` (without format), but the inferred schema correctly shows it should be `string` with `format: "uuid"` to match `MembersOfParliament[].PoliticalPartyId`.

2. **Missing $defs references**: The schema could be improved by referencing common UUID pattern from $defs.

**Recommended schema improvements:**

```json
{
  "type": "object",
  "properties": {
    "MembersOfParliament": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "$ref": "#/$defs/UUID" },
          "UserImg": { "type": "string" },
          "FullName": { "type": "string" },
          "RoleId": { "type": "integer" },
          "PoliticalPartyTitle": { "type": "string" },
          "PoliticalPartyId": { "$ref": "#/$defs/UUID" }
        }
      }
    },
    "ExpiredMandateMembers": {
      "type": "array", 
      "items": {
        "type": "object",
        "properties": {
          "UserId": { "$ref": "#/$defs/UUID" },
          "UserImg": { "type": "string" },
          "FullName": { "type": "string" },
          "RoleId": { "type": "integer" },
          "PoliticalPartyTitle": { "type": "string" },
          "PoliticalPartyId": { "$ref": "#/$defs/UUID" }
        }
      }
    },
    "TotalItems": { "type": "integer" },
    "TotalItemsExpiredMandate": { "type": "integer" },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": { "type": "integer" },
        "NumberOfQuestions": { "type": "integer" },
        "TotalNumberOfMPs": { "type": "integer" },
        "TotalNumberOfExpiredMandateMPs": { "type": "integer" },
        "MPsInPoliticalParties": { "type": "integer" },
        "MPsInParliamentaryGroups": { "type": "integer" },
        "NumberOfMaterialsInStructure": { "type": "integer" }
      }
    }
  }
}
```

**Additional $def needed:**
```json
"UUID": {
  "type": "string",
  "format": "uuid"
}
```

The actual responses match the expected structure correctly.

---

## GetParliamentaryGroupDetails

## Schema Comparison Analysis

### 1. Fields in response not in docs
- None. All fields match the documented schema.

### 2. Types/values that differ from docs
- **Date fields**: Schema uses `$ref: "#/$defs/AspDate"` but inferred schema correctly shows these as `type: "string"` with `format: "asp-date"` and `pattern: "^/Date\\(\\d+\\)/$"` - this is more explicit and accurate.

### 3. Concrete schema improvements

The documented schema should use explicit date formatting instead of `$ref` for better clarity:

```json
{
  "RegistrationDate": {
    "type": "string",
    "format": "asp-date", 
    "pattern": "^/Date\\(\\d+\\)/$"
  },
  "DateAsked": {
    "type": "string",
    "format": "asp-date",
    "pattern": "^/Date\\(\\d+\\)/$"
  },
  "DateAnswered": {
    "type": "string", 
    "format": "asp-date",
    "pattern": "^/Date\\(\\d+\\)/$"
  }
}
```

**Note**: StatusId values observed (6, 10, 12) don't match any existing $defs enum. These appear to be material/amendment-specific status codes that should be documented separately from the existing MaterialStatusId enum.

Otherwise, the schema accurately represents the actual API responses.

---

## GetPoliticalPartyDetails

## Comparison Results

### 1. Fields in response not in docs
None - all fields match.

### 2. Types/values that differ from docs
None - all types match correctly.

### 3. Concrete schema improvements

The documented schema should use `$ref` for the AspDate pattern:

```json
{
  "RegistrationDate": {
    "$ref": "#/$defs/AspDate"
  }
}
```

Instead of the current inline definition. This matches the inferred schema which correctly uses the `$defs` reference.

**OK** - The response structure perfectly matches the documented schema, just needs the AspDate reference improvement.

---

## GetProposerTypes

## Comparison Results

**1. Fields in response not in docs:** None

**2. Types/values that differ from docs:** None

**3. Concrete schema improvements:**

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

The actual response confirms the existing `ProposerTypeId` enum values (1, 2, 4) and their meanings (MP, Government, Voter group).

---

## GetQuestionDetails

OK.

The actual responses perfectly match the documented schema. All fields, types, and values align correctly:

- **Date format**: Uses proper ASP.NET format `/Date(1769680800000)/`
- **Field types**: All string, integer, boolean, null, and array types match exactly
- **Document structure**: Consistent with documented properties and types
- **Sittings structure**: Matches schema including proper `SittingTypeId` values and null `CommitteeTitle` for plenary sessions

The inferred schema correctly uses the `AspDate` reference from `$defs`, which is the only minor improvement over the documented schema's inline pattern definition.

---

## GetUserDetailsByStructure

## Comparison Results

**1. Fields in response not in docs:**
None - all response fields match the documented schema.

**2. Types/values that differ from docs:**

- `ElectedFrom`: Documented as `{"$ref": "#/$defs/AspDate"}` but should be consistent with inferred schema showing the pattern inline
- `RegistrationDate` in `Amendments` and `Acts` arrays: Same issue - should use `{"$ref": "#/$defs/AspDate"}` instead of inline pattern

**3. Schema improvements:**

```json
{
  "ElectedFrom": {
    "$ref": "#/$defs/AspDate"
  },
  "Amendments": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "RegistrationDate": {
          "$ref": "#/$defs/AspDate"
        }
      }
    }
  },
  "Acts": {
    "type": "array", 
    "items": {
      "type": "object",
      "properties": {
        "RegistrationDate": {
          "$ref": "#/$defs/AspDate"
        }
      }
    }
  }
}
```

The documented schema is correct but should consistently use `$defs/AspDate` references instead of mixing with inline patterns.

---

## LoadLanguage

**Analysis of LoadLanguage response:**

**1. Fields in response not in docs:** None

**2. Types/values that differ from docs:** None

**3. Schema improvements:** 
- Add `required: ["Code", "Items"]` to main object
- Add `required: ["Key", "Value"]` to items
- Consider adding `additionalProperties: false` for stricter validation

The actual response perfectly matches the documented schema. The response contains localization key-value pairs in Macedonian (`mk-MK`), which aligns with the expected structure.
