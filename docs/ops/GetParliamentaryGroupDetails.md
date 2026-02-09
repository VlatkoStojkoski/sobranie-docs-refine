## GetParliamentaryGroupDetails

### Request
```json
{
  "methodName": "GetParliamentaryGroupDetails",
  "parliamentaryGroupId": "6f83cbd1-af39-44e5-bfd0-0cde68932844",
  "LanguageId": 1
}
```

### Response
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
    "NumberOfDeputies": {
      "type": "integer"
    },
    "Materials": {
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
        }
      }
    },
    "Amendments": {
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
        }
      }
    },
    "Questions": {
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
          "DateAsked": {
            "$ref": "#/$defs/AspDate"
          },
          "DateAnswered": {
            "anyOf": [
              {"$ref": "#/$defs/AspDate"},
              {"type": "null"}
            ]
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          },
          "MaterialsCount": {
            "type": "integer"
          },
          "AmendmentsCount": {
            "type": "integer"
          },
          "QuestionsCount": {
            "type": "integer"
          }
        }
      }
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Image": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

## Notes

### Parameter Casing
This operation uses mixed parameter casing: lowercase `methodName` and uppercase `LanguageId`.

### Response Behavior

**Array truncation**: The `Materials`, `Amendments`, and `Questions` arrays may be truncated in responses. When an array is truncated, the last item in that array will contain an `_truncated` property with an integer value indicating how many additional items exist but are not included in the response. For example, `{"_truncated": 32}` indicates 32 additional items are available but not shown.

The `Members` array may also be truncated in responses for large parliamentary groups.

**Contact fields**: The `Email`, `Phone`, and `Image` fields are frequently `null` for parliamentary groups. Contact is typically directed through individual members rather than through the group entity itself.

**Description field**: The `Description` field may contain minimal placeholder values (e.g., "-") when no detailed description is available for the parliamentary group.

### Member Roles
Members in the `Members` array include role information via `RoleId` and `RoleTitle`. Observed role IDs:
- `26` = Координатор/Координаторка на политичка партија (Coordinator of political party)
- `72` = Заменик координатор/координаторка на политичка партија (Deputy coordinator of political party)

Each member object includes aggregated activity counts (`MaterialsCount`, `AmendmentsCount`, `QuestionsCount`) showing their parliamentary contributions within this parliamentary group context.

### Questions Field
The `DateAnswered` field is `null` for questions that have not yet been answered (when `StatusId` is `17` = Delivered). For answered questions, this field contains an AspDate timestamp.

### StructureId
The `StructureId` identifies the parliamentary term to which this parliamentary group belongs. Typically `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for the current parliamentary term.