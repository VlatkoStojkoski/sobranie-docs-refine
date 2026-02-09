## GetCommitteeDetails

### Request
```json
{
  "methodName": "GetCommitteeDetails",
  "committeeId": "b8b25861-9b5c-4d47-9717-007b83a8a339",
  "languageId": 1
}
```

### Response
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
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "$ref": "#/$defs/CommitteeRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role name (e.g., 'Претседател/Претседателка на комисија')"
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
            "type": "string",
            "format": "uuid"
          },
          "FullName": {
            "type": "string"
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
      "description": "Administrative/professional staff (advisors, approvers). Note: same person may appear multiple times with different RoleId values if holding multiple roles"
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
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      },
      "description": "Materials assigned to this committee for review/processing. Can be empty array [] when no materials linked"
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type name (e.g., 'Комисиска седница' = Committee sitting)"
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
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
      "description": "HTML-formatted committee description including mandate, responsibilities, composition requirements. May contain markup tags (<p>, <br/>, <div>). May be truncated with ellipsis (...) in response"
    },
    "Email": {
      "type": "string",
      "description": "Committee contact email address"
    },
    "PhoneNumber": {
      "type": ["string", "null"],
      "description": "Committee contact phone number; may be null when not available"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure this committee belongs to"
    }
  }
}
```

### Request Parameters
- **committeeId** (string, UUID, required) — Committee identifier. Obtain from `GetAllCommitteesForFilter`.
- **languageId** (integer, required) — Language for response text (1=Macedonian, 2=Albanian, 3=Turkish). Affects `Name`, `RoleTitle`, `StatusTitle`, `TypeTitle`, and `Description`.
- **methodName** (string) — Operation name: `GetCommitteeDetails`.

### Response Structure
- **Name** — Committee name in the requested language.
- **CompositionMembers** — Array of elected committee members (MPs) with official roles:
  - RoleId 6 = Committee Chair (Претседател/Претседателка на комисија)
  - RoleId 82 = Vice-Chair (Заменик-претседател/Заменик-претседателка на комисија)
  - RoleId 7 = Member (Член/Членка на комисија)
  - RoleId 83 = Deputy Member (Заменик-член)
- **SecretariatMembers** — Array of administrative/professional staff supporting the committee:
  - RoleId 10 = Approver (Одобрувач/Одобрувачка)
  - RoleId 11 = Advisor (Советник/Советничка на комисија)
  - **Note**: Same person (UserId/FullName) may appear multiple times with different RoleIds when holding multiple staff roles (e.g., both Approver and Advisor). This is expected behavior, not a data error.
- **Materials** — Subset of materials assigned to this committee from GetAllMaterialsForPublicPortal. Uses MaterialStatusId enum (6=Delivered to MPs, 12=Closed, etc.). Returns empty array `[]` when no materials linked (not `null`).
- **Meetings** — Committee sittings/sessions in reverse chronological order (most recent first). TypeTitle typically "Комископска седница" (Committee sitting). Use Meeting.Id with `GetSittingDetails` for full agenda and voting details.
- **Description** — HTML-formatted text describing committee's mandate, composition, responsibilities, and reporting requirements. May contain markup tags; may be truncated with ellipsis.
- **Email** — Official committee contact email.
- **PhoneNumber** — Committee contact phone number; nullable (can be `null` when not available).
- **StructureId** — UUID of the parliamentary term this committee belongs to (typically the current term).

### Usage Notes
- Returns comprehensive details for a single committee identified by `committeeId`.
- **CompositionMembers** contains the official elected committee structure (chairs, members).
- **SecretariatMembers** contains staff roles; individuals may hold multiple roles and appear multiple times.
- **Materials** shows legislative items processed by this committee; filtered subset of GetAllMaterialsForPublicPortal results.
- **Description** contains HTML markup; parse for display in client applications.
- **Meetings** can be used with `GetSittingDetails` to retrieve full agenda, voting results, and documents.
- Response includes `"_truncated": N` in documentation examples when arrays were truncated; actual API responses include all items.