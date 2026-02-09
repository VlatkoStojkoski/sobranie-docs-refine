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
