## GetUserDetailsByStructure

### Request
```json
{
  "methodName": "GetUserDetailsByStructure",
  "userId": "85048fa9-e61b-4eb1-be26-8d537cb1d7c4",
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
  "languageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "FullName": {
      "type": "string"
    },
    "Email": {
      "type": "string"
    },
    "Image": {
      "type": "string",
      "description": "Base64-encoded profile image"
    },
    "MobileNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "PhoneNumber": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ]
    },
    "Biography": {
      "type": "string",
      "description": "HTML-formatted biographical text with inline tags"
    },
    "RoleId": {
      "type": "integer",
      "description": "See RoleId enum. Example: 1=MP (Пратеник/Пратеничка)"
    },
    "RoleTitle": {
      "type": "string",
      "description": "Localized role title (e.g., 'Пратеник/Пратеничка' for MP)"
    },
    "ElectedFrom": {
      "$ref": "#/$defs/AspDate"
    },
    "ElectedTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "null for current/active mandates"
    },
    "PoliticalPartyId": {
      "type": "string",
      "format": "uuid"
    },
    "PoliticalPartyTitle": {
      "type": "string"
    },
    "Gender": {
      "type": "string",
      "description": "Localized gender string (Машки=Male, Женски=Female)"
    },
    "DateOfBirth": {
      "type": "string",
      "pattern": "^\\d{2}\\.\\d{2}\\.\\d{4}$",
      "description": "DD.MM.YYYY format"
    },
    "Constituency": {
      "type": "string",
      "description": "Electoral constituency number"
    },
    "Coalition": {
      "type": "string",
      "description": "Electoral coalition name"
    },
    "StructureDate": {
      "type": "string",
      "description": "Human-readable parliamentary term range (e.g., '2024 - 2028')"
    },
    "CabinetMembers": {
      "type": "array",
      "items": {}
    },
    "Materials": {
      "type": "array",
      "items": {}
    },
    "Questions": {
      "type": "array",
      "items": {}
    },
    "Delegations": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroups": {
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
          "Description": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ]
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
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present, indicates N additional items not shown"
          }
        }
      },
      "description": "May be truncated with _truncated indicator"
    },
    "Acts": {
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
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      },
      "description": "Legislative acts/proposals authored or co-sponsored by the MP"
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "CommitteeId": {
            "type": "string",
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string"
          },
          "Roles": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "type": "integer",
                  "description": "Committee role ID: 6=Chair, 7=Member, 82=Deputy Chair, 83=Deputy Member"
                },
                "Title": {
                  "type": "string",
                  "description": "Localized role title"
                }
              }
            },
            "description": "May contain multiple roles per committee"
          }
        }
      },
      "description": "Committee memberships with roles (MP can have multiple roles in one committee)"
    },
    "CommitteeMemberships": {
      "type": "array",
      "items": {}
    },
    "DelegationMemberships": {
      "type": "array",
      "items": {}
    },
    "DepartmentMemberships": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroupMemberships": {
      "type": "array",
      "items": {}
    },
    "MediaItems": {
      "type": "array",
      "items": {}
    }
  }
}
```

### Per-operation notes

**Request parameters:**
- **userId** — UUID of the MP. Obtain from `GetParliamentMPsNoImage` response Items[].Id
- **structureId** — Parliamentary term UUID. Required. Use `GetAllStructuresForFilter` to obtain valid values. Commonly `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current term
- **languageId** — Requested language (1=Macedonian, 2=Albanian, 3=Turkish). Affects localized text fields (RoleTitle, PoliticalPartyTitle, StatusTitle, Gender)
- **methodName** — Fixed value `"GetUserDetailsByStructure"`

**Response structure:**
- Returns comprehensive MP profile including biographical data, political affiliations, committee roles, and legislative activity
- All relationship arrays (CabinetMembers, Materials, Questions, Delegations, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems) return empty arrays `[]` when no data, not `null`

**Notable field behaviors:**
- **Biography** — HTML-formatted text with inline `<p>` and `<span>` tags. May contain biographical details
- **Image** — Base64-encoded JPEG or PNG image data. Can be very long string (tens of kilobytes)
- **Gender** — Localized text string (e.g., "Машки" for male, corresponding to GenderId 1). In requested language
- **DateOfBirth** — String format DD.MM.YYYY (not AspDate format). Example: "02.03.1974"
- **Constituency** — String value (numeric constituency number, e.g., "6")
- **ElectedTo** — `null` for current/active parliamentary term. Contains AspDate when term has ended
- **MobileNumber / PhoneNumber** — Often `null` when not provided

**Array field notes:**
- **Amendments** — May be truncated with `{"_truncated": N}` object indicating N additional items exist. Uses StatusId 6 (Delivered to MPs) and 12 (Closed). Can be empty `[]` when no amendments
- **Acts** — Array of legislative proposals/laws. Uses same structure as Amendments. Can be empty `[]` when no acts
- **Committees** — Shows all committee memberships. Roles array can have multiple entries per committee when MP holds multiple roles (e.g., both member and deputy). Can be empty `[]` when MP has no committee roles
- **FriendshipGroups** — Descriptions can be empty strings or null. Can be empty `[]` when MP is not part of any friendship groups

**Date format note:**
- ElectedFrom/ElectedTo use AspDate format (`/Date(timestamp)/`)
- DateOfBirth uses DD.MM.YYYY string format (different from AspDate)