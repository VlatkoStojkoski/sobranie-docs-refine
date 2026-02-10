## GetCouncilDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetCouncilDetails"],
      "description": "Operation method name (lowercase)"
    },
    "committeeId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the council to retrieve. Obtain from GetAllCouncils response."
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Requested language for response labels and text (1=Macedonian, 2=Albanian, 3=Turkish). Controls language for Name, RoleTitle, Description, and other text fields."
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
      "description": "Full name of the council in the requested language"
    },
    "CompositionMembers": {
      "type": "array",
      "items": {
        "anyOf": [
          {
            "type": "object",
            "properties": {
              "UserId": {
                "$ref": "#/$defs/UUID"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "$ref": "#/$defs/CommitteeRoleId"
              },
              "RoleTitle": {
                "type": "string",
                "description": "Localized role name (e.g., 'Претседател/Претседателка', 'Член/Членка')"
              }
            },
            "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
          },
          {
            "type": "object",
            "properties": {
              "_truncated": {
                "type": "integer",
                "description": "Truncation marker indicating N additional items omitted"
              }
            },
            "required": ["_truncated"]
          }
        ]
      },
      "description": "Official council composition members (MPs with voting roles). Typically includes president (RoleId 6), vice-president (82), and members (7). Ordered by role importance. May include truncation marker as a standalone object within the array."
    },
    "SecretariatMembers": {
      "type": "array",
      "items": {
        "anyOf": [
          {
            "type": "object",
            "properties": {
              "UserId": {
                "$ref": "#/$defs/UUID"
              },
              "FullName": {
                "type": "string"
              },
              "RoleId": {
                "$ref": "#/$defs/CommitteeRoleId"
              },
              "RoleTitle": {
                "type": "string",
                "description": "Localized role name (e.g., 'Одобрувач', 'Советник на комисија')"
              }
            },
            "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
          },
          {
            "type": "object",
            "properties": {
              "_truncated": {
                "type": "integer",
                "description": "Truncation marker indicating N additional items omitted"
              }
            },
            "required": ["_truncated"]
          }
        ]
      },
      "description": "Administrative and advisory staff supporting the council. RoleId typically 10 (Approver) or 11 (Advisor). Note: Same person (UserId) may appear multiple times with different RoleIds when holding multiple roles. This is expected behavior. May include truncation marker as a standalone object within the array."
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Materials associated with the council (e.g., founding decisions, policy documents). Empty array [] when no materials exist."
    },
    "Meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Meeting type label (e.g., 'Комисска седница' or similar = Committee sitting). May contain spelling variations or typos; see data quality notes."
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string",
            "description": "Physical meeting location (e.g., 'Сала 4' = Room 4)"
          },
          "SittingNumber": {
            "type": "integer",
            "description": "Sequential sitting number for the council"
          }
        },
        "required": ["Id", "TypeTitle", "Date", "Location", "SittingNumber"]
      },
      "description": "Past and scheduled council meetings/sittings, ordered by date in reverse chronological order (most recent first)."
    },
    "Description": {
      "anyOf": [
        {
          "type": "string",
          "description": "HTML-formatted description of the council's mandate and responsibilities. May contain markup including <p>, <span>, <a>, <br/> tags and inline styles. May include links to founding decisions and constitutional references."
        },
        {
          "type": "null"
        }
      ]
    },
    "Email": {
      "type": "string",
      "description": "Contact email address for the council (e.g., 'council-name@sobranie.mk')"
    },
    "PhoneNumber": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "Contact phone number. Null when not available."
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure this council belongs to. Common value: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term. Matches StructureId parameter used in other operations."
    }
  },
  "required": ["Name", "CompositionMembers", "SecretariatMembers", "Materials", "Meetings", "Email", "StructureId"]
}
```

### Notes

- **Parameter casing**: Uses lowercase `methodName` and `languageId` (standard method-based convention).
- **RoleId enum** (CommitteeRoleId): See global $defs. Composition uses 6 (President), 82 (Vice-President), 7 (Member). Secretariat uses 10 (Approver), 11 (Advisor).
- **Duplicate users in SecretariatMembers**: A single person may appear multiple times in the SecretariatMembers array with different RoleId values, reflecting their actual responsibilities. This is expected behavior.
- **Meetings ordering**: The Meetings array is ordered by Date in reverse chronological order (most recent first).
- **HTML content in Description**: Contains rich HTML markup. Parse as HTML when displaying to end users.
- **Materials**: Returns empty array `[]` when no materials exist (not `null`).
- **Array truncation**: CompositionMembers and SecretariatMembers may include a truncation marker as a standalone object `{"_truncated": N}` within the array, counting toward array length and indicating N additional items omitted.
- **Data quality**: TypeTitle in Meetings may contain spelling variations or typos (e.g., 'Комississка' vs 'Комисска'); normalize for display if needed.
