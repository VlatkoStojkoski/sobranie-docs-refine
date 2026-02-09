## GetCommitteeDetails

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetCommitteeDetails"
    },
    "committeeId": {
      "$ref": "#/$defs/UUID",
      "description": "Committee identifier from GetAllCommitteesForFilter"
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "committeeId", "languageId"]
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Committee name in the requested language"
    },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID",
            "description": "Elected committee member identifier"
          },
          "FullName": {
            "type": "string",
            "description": "Full name of committee member"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Претседател/Претседателка на комисија', 'Член/Членка на комисија')"
          }
        }
      },
      "description": "Elected committee members: chair, vice-chair, members, and deputies with their roles"
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID",
            "description": "Staff member identifier"
          },
          "FullName": {
            "type": "string",
            "description": "Full name of staff member"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Советник/Советничка на комисија', 'Одобрувач/Одобрувачка')"
          }
        }
      },
      "description": "Administrative/professional staff supporting the committee (advisors, approvers). Same person may appear multiple times with different RoleIds when holding multiple roles"
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Material identifier"
          },
          "Title": {
            "type": "string",
            "description": "Material title in the requested language"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration number (e.g., '08-750/1')"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized material status (e.g., 'Доставен до пратеници')"
          }
        }
      },
      "description": "Materials assigned to this committee for review/processing. Empty array [] when no materials linked"
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "Sitting/meeting identifier"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type name in the requested language (e.g., 'Комископска седница')"
          },
          "Date": {
            "$ref": "#/$defs/AspDate",
            "description": "Meeting date/time"
          },
          "Location": {
            "type": "string",
            "description": "Meeting room/venue (e.g., 'Сала 5', 'Сала 6')"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential number of the committee sitting"
          }
        }
      },
      "description": "Committee sittings/meetings, ordered by date (most recent first)"
    },
    "Description": {
      "type": "string",
      "description": "HTML-formatted committee description including mandate, responsibilities, composition requirements. May contain markup tags (<p>, <br/>, <div>). May be truncated with ellipsis in response"
    },
    "Email": {
      "type": "string",
      "description": "Committee contact email address"
    },
    "PhoneNumber": {
      "oneOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee contact phone number; may be null when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID this committee belongs to"
    }
  }
}
```

### Notes
- **CompositionMembers** contains the officially elected committee structure (chairs, members, deputies). Use with `GetUserDetailsByStructure` for full MP profile data.
- **SecretariatMembers** contains professional staff and administrative roles. Same person may appear multiple times with different RoleIds (expected behavior for staff holding multiple roles).
- **Materials** shows a subset of legislative items from `GetAllMaterialsForPublicPortal` assigned to this committee.
- **Description** contains HTML markup; parse appropriately for display in client applications.
- **Meetings** entries can be used with `GetSittingDetails` to retrieve full agenda, voting results, and documents for each sitting.
- Response examples in documentation may show `"_truncated": N` in arrays when actual arrays were truncated for documentation purposes; actual API responses include all available items.
- **languageId** casing: uses camelCase (lowercase) in this operation.
- Date/time values in `Meetings[].Date` follow AspDate format. Use parsing compatible with `/Date(timestamp)/` format.
