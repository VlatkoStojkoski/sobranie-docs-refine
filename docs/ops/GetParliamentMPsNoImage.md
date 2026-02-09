## GetParliamentMPsNoImage

Retrieve active and expired-mandate members of parliament from a specified parliamentary term, with optional filtering by gender, age, party, and search text.

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
      "$ref": "#/$defs/LanguageId"
    },
    "genderId": {
      "anyOf": [
        {"$ref": "#/$defs/GenderId"},
        {"type": "null"}
      ],
      "description": "Filter by gender; null includes all genders"
    },
    "ageFrom": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Minimum age for filtering; null = no lower bound"
    },
    "ageTo": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Maximum age for filtering; null = no upper bound"
    },
    "politicalPartyId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Filter by political party; null includes all parties"
    },
    "searchText": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Filter MPs by name substring; null applies no text filtering"
    },
    "page": {
      "type": "integer",
      "minimum": 1,
      "description": "1-based page number for pagination of active MPs"
    },
    "rows": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of results per page"
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Parliamentary term UUID from GetAllStructuresForFilter. null returns empty MP arrays but populates Statistics with global counts"
    },
    "coalition": {
      "type": "string",
      "description": "Coalition filter (empty string when not filtering)"
    },
    "constituency": {
      "type": "string",
      "description": "Constituency filter (empty string when not filtering)"
    }
  },
  "required": ["methodName", "page", "rows"]
}
```

### Response Schema

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
                "$ref": "#/$defs/UUID",
                "description": "Unique identifier for the MP"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for MP's photograph"
              },
              "FullName": {
                "type": "string",
                "description": "MP's full name in requested language"
              },
              "RoleId": {
                "type": "integer",
                "description": "Internal role identifier"
              },
              "PoliticalPartyTitle": {
                "type": "string",
                "description": "Name of the political party"
              },
              "PoliticalPartyId": {
                "$ref": "#/$defs/UUID",
                "description": "UUID of the political party"
              }
            },
            "required": ["UserId", "FullName"]
          },
          "description": "Active-mandate MPs for the current page"
        },
        {"type": "null"}
      ],
      "description": "Array of active MPs matching filters, paginated; empty array [] when no results, null in some edge cases"
    },
    "ExpiredMandateMembers": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "UserId": {
                "$ref": "#/$defs/UUID"
              },
              "UserImg": {
                "type": "string",
                "description": "Base64-encoded image data for expired-mandate MP's photograph"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "type": "integer"
              },
              "PoliticalPartyTitle": {
                "type": "string"
              },
              "PoliticalPartyId": {
                "$ref": "#/$defs/UUID"
              }
            },
            "required": ["UserId", "FullName"]
          },
          "description": "MPs whose mandates have expired"
        },
        {"type": "null"}
      ]
    },
    "TotalItems": {
      "type": "integer",
      "description": "Total count of active-mandate MPs matching the filter criteria (across all pages)"
    },
    "TotalItemsExpiredMandate": {
      "type": "integer",
      "description": "Total count of expired-mandate MPs matching the filter criteria"
    },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": {
          "type": "integer",
          "description": "Global count of materials (non-zero even when filter results are empty)"
        },
        "NumberOfQuestions": {
          "type": "integer",
          "description": "Count of parliamentary questions"
        },
        "TotalNumberOfMPs": {
          "type": "integer",
          "description": "Total active MPs in the structure"
        },
        "TotalNumberOfExpiredMandateMPs": {
          "type": "integer",
          "description": "Total expired-mandate MPs in the structure"
        },
        "MPsInPoliticalParties": {
          "type": "integer",
          "description": "Number of active MPs in political parties"
        },
        "MPsInParliamentaryGroups": {
          "type": "integer",
          "description": "Number of active MPs in parliamentary groups"
        },
        "NumberOfMaterialsInStructure": {
          "type": "integer",
          "description": "Materials count for the specified structure"
        }
      },
      "description": "Aggregate statistics; always present and populated even when filter results are empty"
    }
  },
  "required": ["MembersOfParliament", "ExpiredMandateMembers", "TotalItems", "TotalItemsExpiredMandate", "Statistics"]
}
```

### Notes

#### Operation Name vs. Response Content
Despite the operation name "GetParliamentMPsNoImage", the response **includes** the `UserImg` field containing base64-encoded photograph data for each MP in both `MembersOfParliament` and `ExpiredMandateMembers` arrays. Do not assume images are absent.

#### StructureId Behavior
When `StructureId` is `null`, the operation returns empty MP arrays (`MembersOfParliament: []`, `ExpiredMandateMembers: []`) with `TotalItems: 0` and `TotalItemsExpiredMandate: 0`. However, the `Statistics` object is still populated with aggregate counts that may be global. **Always provide a valid StructureId UUID (e.g., current term from GetAllStructuresForFilter) to retrieve MP data.** The active parliamentary term is marked with `IsCurrent: true`.

#### Pagination
The `page` (1-based) and `rows` parameters control pagination of the `MembersOfParliament` results only. `TotalItems` reflects the full count of active MPs across all pages; the returned array contains only the subset for the requested page. Pagination behavior for `ExpiredMandateMembers` (whether separate pagination or all expired members regardless of page parameters) is not fully documented.

#### Empty Results
When no MPs match the filter criteria, both `MembersOfParliament` and `ExpiredMandateMembers` return empty arrays `[]` (not `null`), unlike some other operations. Requesting a page beyond the result set returns empty arrays without error.

#### Filtering Details
- **genderId:** When set, filters both active and expired MPs by gender (1=Male, 2=Female). When `null`, all genders are included.
- **politicalPartyId:** When set, returns only MPs from that party in both arrays. When `null`, all parties are included.
- **searchText:** Filters MPs by name substring match. When `null`, no text filtering is applied.
- **ageFrom / ageTo:** When set, filters by age range (inclusive). Both are nullable; null means no bound on that end.
- **coalition / constituency:** String filters that can be empty string `""` (no filtering) or set to a value. Exact matching behavior requires testing with actual data.

#### Language Support
MP names (`FullName`), party titles (`PoliticalPartyTitle`), and other localized fields are returned in the language specified by `languageId` (1=Macedonian, 2=Albanian, 3=Turkish).

#### Statistics Object
Always present in the response and provides aggregate counts across the structure. Some fields (e.g., `TotalNumberOfMaterials`) reflect global data and remain non-zero even when all MP filter results are empty. Other fields (e.g., `NumberOfMaterialsInStructure`) reflect the specified structure. These statistics do not change based on MP-specific filters (gender, party, search, age, coalition, constituency).

#### Casing
The operation uses camelCase for most parameters (`methodName`, `languageId`, `genderId`, `politicalPartyId`, `searchText`, `page`, `rows`, `coalition`, `constituency`) but PascalCase for `StructureId`. See per-operation details for parameter casing.
