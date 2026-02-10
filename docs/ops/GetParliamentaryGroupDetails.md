## GetParliamentaryGroupDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetParliamentaryGroupDetails"
    },
    "parliamentaryGroupId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the parliamentary group (from GetAllParliamentaryGroups)"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "parliamentaryGroupId", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full official name of the parliamentary group (localized per LanguageId)"
    },
    "Description": {
      "type": "string",
      "description": "Group description; may be minimal placeholder like '-' when not set"
    },
    "NumberOfDeputies": {
      "type": "integer",
      "description": "Count of MPs in the parliamentary group"
    },
    "Materials": {
      "type": "array",
      "description": "Array of materials proposed by the parliamentary group, may be truncated with _truncated property",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Material registration number (e.g. '08-750/1')"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status label"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present (only on last array item), indicates N additional items exist but are not shown"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      }
    },
    "Amendments": {
      "type": "array",
      "description": "Array of amendments proposed by the parliamentary group, may be truncated",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
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
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      }
    },
    "Questions": {
      "type": "array",
      "description": "Array of parliamentary questions submitted by members of the parliamentary group",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
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
            ],
            "description": "null for unanswered questions (StatusId=17), AspDate timestamp for answered questions"
          },
          "StatusId": {
            "$ref": "#/$defs/QuestionStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized question status label"
          }
        },
        "required": ["Id", "Title", "DateAsked", "DateAnswered", "StatusId", "StatusTitle"]
      }
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs in the parliamentary group with role and activity counts, may be truncated",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "$ref": "#/$defs/RoleId",
            "description": "Role within parliamentary group (see $defs/RoleId for values)"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role label"
          },
          "MaterialsCount": {
            "type": "integer",
            "description": "Count of materials proposed by this member"
          },
          "AmendmentsCount": {
            "type": "integer",
            "description": "Count of amendments proposed by this member"
          },
          "QuestionsCount": {
            "type": "integer",
            "description": "Count of questions submitted by this member"
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle", "MaterialsCount", "AmendmentsCount", "QuestionsCount"]
      }
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Contact email for the parliamentary group, typically null (contact directed through individual members)"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Contact phone for the parliamentary group, typically null"
    },
    "Image": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Image identifier, URL, or base64 data for parliamentary group logo/emblem, null when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of parliamentary term/structure to which this group belongs"
    }
  },
  "required": ["Name", "Description", "NumberOfDeputies", "Materials", "Amendments", "Questions", "Members", "Email", "Phone", "Image", "StructureId"]
}
```

### Notes

**Parameter Casing:** This operation uses mixed PascalCase: lowercase `methodName` and uppercase `LanguageId`.

**Array Truncation:** The `Materials`, `Amendments`, and `Questions` arrays may be truncated due to API display limitations. When truncated, the last item in the array contains an `_truncated` property with an integer value indicating how many additional items exist beyond those shown. The `Members` array may also be truncated for large parliamentary groups. See global "Array truncation" pattern.

**Contact Fields:** `Email`, `Phone`, and `Image` fields are frequently `null` for parliamentary groups. Contact is typically directed through individual members rather than through the group entity itself. See global "Parliamentary group contact" note.

**Response Language:** All localized text fields (Name, StatusTitle, RoleTitle, etc.) are returned in the language specified by the `LanguageId` request parameter.

**Member Roles:** Members include role information via `RoleId`. See `$defs/RoleId` in global documentation for enumerated role values and meanings. In parliamentary group context, observed role IDs include 26 (Coordinator of political party) and 72 (Deputy coordinator of political party).

Each member object includes aggregated activity counts (`MaterialsCount`, `AmendmentsCount`, `QuestionsCount`) showing their legislative contributions within this parliamentary group context.

**Questions Field:** The `DateAnswered` field is `null` for questions that have not yet been answered (when `StatusId=17`, Delivered). For answered questions, this field contains an AspDate timestamp.

**StructureId:** Identifies the parliamentary term to which this parliamentary group belongs. Typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current parliamentary term. See global "StructureId" concept.