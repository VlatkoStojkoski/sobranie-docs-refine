## GetCouncilDetails

### Request
```json
{
  "methodName": "GetCouncilDetails",
  "committeeId": "d596538c-f3d4-4440-8ae7-6e25ea094c6a",
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
      "description": "Full name of the council in the requested language"
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
            "enum": [6, 7, 10, 11, 82]
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      },
      "description": "Official council composition members (MPs with voting roles). Typically includes president (RoleId 6), vice-president (82), and members (7)."
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
            "enum": [6, 7, 10, 11, 82]
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      },
      "description": "Administrative and advisory staff supporting the council. May contain duplicate UserId entries with different RoleId values (same person holding multiple roles)."
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Materials associated with the council. Empty array [] when no materials exist."
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
            "description": "Meeting type label (e.g., 'Комисиска седница' = Committee sitting)"
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
        }
      },
      "description": "Past and scheduled council meetings/sittings, ordered by date in reverse chronological order (most recent first)."
    },
    "Description": {
      "anyOf": [
        {
          "type": "string",
          "description": "HTML-formatted description of the council's mandate and responsibilities. May contain markup including paragraphs, links, and styling."
        },
        {
          "type": "null"
        }
      ]
    },
    "Email": {
      "type": "string",
      "description": "Contact email address for the council"
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
      "description": "Contact phone number for the council. Null when not available."
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure this council belongs to"
    }
  }
}
```

### Request Filter
- **committeeId** — UUID of the council to retrieve details for. Obtain from GetAllCouncils response. Identifies which council to fetch information about.
- **languageId** — Requested language for response labels and text (1=Macedonian, 2=Albanian, 3=Turkish). Controls language for Name, RoleTitle, Description, and other text fields.
- **methodName** — Value: "GetCouncilDetails" (lowercase)

### Response Keys

**Name** — Full name of the council in the requested language.

**CompositionMembers** — Array of official council composition members (voting members, typically MPs).
- Same council member may appear in this array with only composition roles (6=President, 82=Vice-President, 7=Member).
- Ordered by role importance (President typically first, then Vice-President, then Members).

**SecretariatMembers** — Array of administrative and support staff.
- RoleId values: 10=Approver (Одобрувач/Одобрувачка), 11=Advisor (Советник/Советничка на комисија).
- Important: Same person (UserId) can appear multiple times with different RoleId values when they hold multiple roles (e.g., person serving as both Approver and Advisor).
- This is expected behavior, not a data quality issue.

**Materials** — Associated materials (e.g., founding decisions, policy documents).
- Returns empty array `[]` when no materials exist (not `null`).
- When populated, contains material objects.

**Meetings** — Council meetings/sittings in reverse chronological order (most recent first).
- **TypeTitle**: Typically "Комископска седница" (Committee sitting) for council meetings.
- **SittingNumber**: Sequential number incremented per council.
- **Location**: Physical venue (e.g., "Сала 4" = Room 4).
- **Date**: AspDate format timestamp.

**Description** — HTML-formatted text describing the council's legal basis, mandate, and responsibilities.
- Can contain extensive HTML markup including `<p>`, `<span>`, `<a>`, `<br/>` tags and inline styles.
- May include links to founding decisions, constitutional references, and other resources.
- Nullable; can be `null` when not provided.

**Email** — Official contact email for the council (e.g., "council-name@sobranie.mk").

**PhoneNumber** — Contact phone number. Nullable; can be `null` when not provided.

**StructureId** — UUID of the parliamentary term/structure to which this council belongs. Common value: `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` for current parliamentary term. Matches StructureId parameter used in other operations.

### Additional Notes

- **RoleId enum values** (from $defs/RoleId):
  - `6` = Committee President (Претседател/Претседателка на комисија)
  - `82` = Committee Vice President (Заменик-претседател/Заменик-претседателка на комисија)
  - `7` = Committee Member (Член/Членка на комисија)
  - `10` = Approver (Одобрувач/Одобрувачка)
  - `11` = Committee Advisor (Советник/Советничка на комисија)

- **Duplicate users in SecretariatMembers**: A single person may appear multiple times in the SecretariatMembers array with different RoleId values. For example, one staff member can simultaneously hold roles as both Approver (RoleId: 10) and Advisor (RoleId: 11). This reflects that person's actual responsibilities and is expected behavior.

- **Meetings ordering**: The Meetings array is ordered by Date in reverse chronological order (most recent first). Use the Date field to sort or filter client-side if needed.

- **HTML content in Description**: The Description field contains rich HTML markup. Parse as HTML when displaying to end users. May include links to PDF documents and other resources related to the council's establishment and mandate.

- **Parameter casing**: Uses lowercase `methodName` and `languageId` (standard method-based convention).