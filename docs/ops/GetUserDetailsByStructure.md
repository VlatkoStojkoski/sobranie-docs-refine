## GetUserDetailsByStructure

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetUserDetailsByStructure"
    },
    "userId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MP. Obtain from GetParliamentMPsNoImage Items[].Id"
    },
    "structureId": {
      "anyOf": [
        {
          "$ref": "#/$defs/UUID"
        },
        {
          "type": "null"
        }
      ],
      "description": "UUID of parliamentary term. Obtain from GetAllStructuresForFilter. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current. Required for valid MP data."
    },
    "languageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "1=Macedonian, 2=Albanian, 3=Turkish. Affects localized response fields."
    }
  },
  "required": [
    "methodName",
    "userId",
    "structureId",
    "languageId"
  ]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "FullName": {
      "type": "string",
      "description": "Full name of the MP (FirstName LastName)"
    },
    "Email": {
      "type": "string",
      "description": "Official parliamentary email in format FirstInitial.LastName@sobranie.mk"
    },
    "Image": {
      "type": "string",
      "description": "Base64-encoded profile image (JPEG or PNG). Can be very long string (tens of kilobytes)."
    },
    "MobileNumber": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "Mobile phone number or null if not provided"
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
      "description": "Office phone number or null if not provided"
    },
    "Biography": {
      "type": "string",
      "description": "HTML-formatted biographical text with inline <p> and <span> tags"
    },
    "RoleId": {
      "$ref": "#/$defs/RoleId",
      "description": "Primary role in parliament. Example: 1=MP (Пратеник/Пратеничка)"
    },
    "RoleTitle": {
      "type": "string",
      "description": "Localized role title in requested language (e.g., 'Пратеник/Пратеничка' for MP)"
    },
    "ElectedFrom": {
      "$ref": "#/$defs/AspDate",
      "description": "Start date of mandate (AspDate format)"
    },
    "ElectedTo": {
      "anyOf": [
        {
          "$ref": "#/$defs/AspDate"
        },
        {
          "type": "null"
        }
      ],
      "description": "End date of mandate (AspDate format). null for current/active mandates."
    },
    "PoliticalPartyId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MP's political party"
    },
    "PoliticalPartyTitle": {
      "type": "string",
      "description": "Name of the MP's political party in requested language"
    },
    "Gender": {
      "type": "string",
      "description": "Localized gender string in requested language. Examples: 'Машки' (Male), 'Женски' (Female)"
    },
    "DateOfBirth": {
      "type": "string",
      "pattern": "^\\d{2}\\.\\d{2}\\.\\d{4}$",
      "description": "Date of birth in DD.MM.YYYY format (not AspDate). Example: '02.03.1974'"
    },
    "Constituency": {
      "type": "string",
      "description": "Electoral constituency number as string. Example: '6'"
    },
    "Coalition": {
      "type": "string",
      "description": "Electoral coalition name MP was elected under. Example: 'Коалиција Твоја Македонија'"
    },
    "StructureDate": {
      "type": "string",
      "description": "Human-readable parliamentary term date range. Example: '2024 - 2028'"
    },
    "CabinetMembers": {
      "type": "array",
      "items": {},
      "description": "Cabinet/ministerial positions held by the MP. Empty array [] when no data."
    },
    "Materials": {
      "type": "array",
      "items": {},
      "description": "Materials (bills/acts) associated with the MP. Empty array [] when no data."
    },
    "Questions": {
      "type": "array",
      "items": {},
      "description": "Parliamentary questions submitted by the MP. Empty array [] when no data."
    },
    "Delegations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Name of delegation in requested language"
          },
          "Description": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "description": "Description or null if not set"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present as standalone object, indicates N additional items not shown"
          }
        },
        "required": [
          "Id",
          "Title"
        ]
      },
      "description": "Delegation memberships. May be truncated by API. Empty array [] when no delegations."
    },
    "FriendshipGroups": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Name of friendship group in requested language"
          },
          "Description": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "description": "Description or null if not set"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present as standalone object, indicates N additional items not shown"
          }
        },
        "required": [
          "Id",
          "Title"
        ]
      },
      "description": "Friendship group memberships. May be truncated by API. Empty array [] when no groups."
    },
    "Amendments": {
      "type": "array",
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
            "description": "Registration number in format XX-XXX/X (e.g., '08-750/1')"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status text in requested language"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present as standalone object, indicates N additional items not shown"
          }
        },
        "required": [
          "Id",
          "Title",
          "RegistrationDate",
          "RegistrationNumber",
          "StatusId",
          "StatusTitle"
        ]
      },
      "description": "Amendment proposals submitted by the MP. May be truncated by API with {\"_truncated\": N} standalone object counting toward array length. Empty array [] when no amendments."
    },
    "Acts": {
      "type": "array",
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
            "description": "Registration number in format XX-XXX/X"
          },
          "StatusId": {
            "$ref": "#/$defs/MaterialStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status text in requested language"
          },
          "_truncated": {
            "type": "integer",
            "description": "When present as standalone object, indicates N additional items not shown"
          }
        },
        "required": [
          "Id",
          "Title",
          "RegistrationDate",
          "RegistrationNumber",
          "StatusId",
          "StatusTitle"
        ]
      },
      "description": "Legislative acts/proposals authored or co-sponsored by the MP. May be truncated by API. Empty array [] when no acts."
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "CommitteeId": {
            "$ref": "#/$defs/UUID"
          },
          "CommitteeTitle": {
            "type": "string",
            "description": "Committee name in requested language"
          },
          "Roles": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "$ref": "#/$defs/CommitteeRoleId"
                },
                "Title": {
                  "type": "string",
                  "description": "Localized role title in requested language (e.g., 'Претседател/Претседателка на комисија')"
                }
              },
              "required": [
                "Id",
                "Title"
              ]
            },
            "description": "Roles within the committee. MP can have multiple roles in one committee."
          },
          "_truncated": {
            "type": "integer",
            "description": "When present as standalone object, indicates N additional items not shown"
          }
        },
        "required": [
          "CommitteeId",
          "CommitteeTitle",
          "Roles"
        ]
      },
      "description": "Committee memberships with roles. May be truncated by API. Empty array [] when MP has no committee roles."
    },
    "CommitteeMemberships": {
      "type": "array",
      "items": {},
      "description": "Additional committee membership details. Empty array [] when no data."
    },
    "DelegationMemberships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Name of delegation in requested language"
          },
          "RoleId": {
            "type": "integer",
            "description": "Role ID within delegation"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role title in requested language"
          },
          "FromDate": {
            "$ref": "#/$defs/AspDate"
          },
          "ToDate": {
            "$ref": "#/$defs/AspDate"
          }
        },
        "required": [
          "Id",
          "Title",
          "RoleId",
          "RoleTitle",
          "FromDate",
          "ToDate"
        ]
      },
      "description": "Delegation membership details. Empty array [] when no data."
    },
    "DepartmentMemberships": {
      "type": "array",
      "items": {},
      "description": "Department membership details. Empty array [] when no data."
    },
    "FriendshipGroupMemberships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Name of friendship group in requested language"
          },
          "RoleId": {
            "$ref": "#/$defs/MPsClubRoleId"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized role title in requested language"
          },
          "FromDate": {
            "$ref": "#/$defs/AspDate"
          },
          "ToDate": {
            "$ref": "#/$defs/AspDate"
          }
        },
        "required": [
          "Id",
          "Title",
          "RoleId",
          "RoleTitle",
          "FromDate",
          "ToDate"
        ]
      },
      "description": "Friendship group membership details with role information. Empty array [] when no data."
    },
    "MediaItems": {
      "type": "array",
      "items": {},
      "description": "Media items associated with the MP. Empty array [] when no data."
    }
  },
  "required": [
    "FullName",
    "Email",
    "Image",
    "Biography",
    "RoleId",
    "RoleTitle",
    "ElectedFrom",
    "PoliticalPartyId",
    "PoliticalPartyTitle",
    "Gender",
    "DateOfBirth",
    "Constituency",
    "Coalition",
    "StructureDate"
  ]
}
```

### Notes

**Calling convention:**  
Method-based POST to `https://www.sobranie.mk/Routing/MakePostRequest` with lowercase `methodName` and `languageId` in request body.

**Response structure:**  
Returns comprehensive MP profile including biographical data, political affiliations, committee roles, and legislative activity.

**Array behavior:**  
All relationship arrays (CabinetMembers, Materials, Questions, Delegations, FriendshipGroups, CommitteeMemberships, DelegationMemberships, DepartmentMemberships, FriendshipGroupMemberships, MediaItems, Amendments, Acts, Committees) return empty arrays `[]` when no data, never `null`. Arrays may include a truncation marker `{"_truncated": N}` as a standalone object counting toward array length, indicating N additional items omitted.

**Notable field behaviors:**
- **Biography** — HTML-formatted text with inline `<p>` and `<span>` tags containing biographical details.
- **Image** — Base64-encoded JPEG or PNG image data. Field populated with actual image despite operation name implying "NoImage". Can be tens of kilobytes; clients should handle large string payloads.
- **Gender** — Localized text string in requested language (e.g., "Машки" for male, "Женски" for female), not a numeric GenderId.
- **DateOfBirth** — String format DD.MM.YYYY (distinct from AspDate format). Example: "02.03.1974"
- **Constituency** — String value representing electoral constituency number (e.g., "6").
- **ElectedTo** — `null` for current/active parliamentary term. Contains AspDate when term has ended.
- **MobileNumber / PhoneNumber** — Often `null` when not provided.
- **PoliticalPartyTitle** — Party name in requested language.
- **RoleTitle** — Localized role title (e.g., "Пратеник/Пратеничка" for MP); corresponds to RoleId enum value.

**Array field details:**
- **CabinetMembers, Materials, Questions, CommitteeMemberships, DepartmentMemberships, MediaItems** — Documented with minimal item schemas from available samples; full structure may be expanded when more response data available. All return empty `[]` when MP has no entries.
- **Delegations** — Shows delegation memberships with Id, Title, and optional Description. May be truncated. Empty `[]` when MP is not part of any delegations.
- **FriendshipGroups** — Shows friendship group memberships with Id, Title, and optional Description. May be truncated. Empty `[]` when MP is not part of any friendship groups.
- **FriendshipGroupMemberships** — Detailed membership records including RoleId (using MPsClubRoleId enum with values 77=Član/Članка, 78=President, 79=Vice-President, 81=Member), RoleTitle, FromDate, and ToDate. Empty `[]` when no detailed membership data.
- **DelegationMemberships** — Detailed membership records including RoleId, RoleTitle, FromDate, and ToDate. Empty `[]` when no detailed membership data.
- **Amendments** — Array may be truncated by API with `{"_truncated": N}` object as standalone entry, indicating N additional items exist. Uses MaterialStatusId enum (e.g., 6=Delivered to MPs, 12=Closed). Empty `[]` when no amendments.
- **Acts** — Array of legislative proposals/laws the MP authored or co-sponsored. Uses same structure as Amendments. May be truncated. Empty `[]` when no acts.
- **Committees** — Shows all committee memberships. Roles array can have multiple entries per committee when MP holds multiple roles. Roles use CommitteeRoleId enum (6=Chair, 7=Member, 10=Approver, 11=Advisor, 82=Deputy Chair, 83=Deputy Member). May be truncated. Empty `[]` when MP has no committee roles.

**Date formats:**
- **ElectedFrom / ElectedTo** — AspDate format (`/Date(timestamp)/`)
- **DateOfBirth** — DD.MM.YYYY string format (not AspDate)
- **RegistrationDate** (in Amendments/Acts) — AspDate format
- **FromDate / ToDate** (in DelegationMemberships, FriendshipGroupMemberships) — AspDate format

**Localization:**  
Response fields such as RoleTitle, PoliticalPartyTitle, CommitteeTitle, StatusTitle, Gender, and membership role titles are localized based on the requested `languageId`.

**StructureId behavior:**  
When `structureId` is null, results may be empty or cross-term; use current structure UUID from GetAllStructuresForFilter for standard MP profile retrieval.