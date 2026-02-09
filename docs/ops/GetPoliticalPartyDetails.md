## GetPoliticalPartyDetails

### Request
```json
{
  "methodName": "GetPoliticalPartyDetails",
  "politicalPartyId": "e693cd9f-5893-49ab-9ede-0abd6e820664",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Official name of the political party in the requested language"
    },
    "Description": {
      "type": "string",
      "description": "Party description; may be placeholder like '-' when not provided"
    },
    "NumberOfDeputies": {
      "type": "integer",
      "description": "Count of MPs/deputies currently affiliated with this political party"
    },
    "Materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid",
            "description": "UUID of the material"
          },
          "Title": {
            "type": "string",
            "description": "Material title/name"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date when material was officially registered"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration identifier (format: NN-NNN/N)"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier (see MaterialStatusId enum)"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Human-readable status label in requested language"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      },
      "description": "Materials (legislative proposals, amendments) submitted by this political party"
    },
    "Amendments": {
      "type": "array",
      "items": {},
      "description": "Amendments proposed by the party. Empty array when party has no amendments."
    },
    "Questions": {
      "type": "array",
      "items": {},
      "description": "Parliamentary questions submitted by the party. Empty array when party has no questions."
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid",
            "description": "UUID identifier for the party member/MP"
          },
          "FullName": {
            "type": "string",
            "description": "Complete name of the party member"
          },
          "RoleId": {
            "type": "integer",
            "enum": [27],
            "description": "Member role within party (27=Member of political party)"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized human-readable role name (e.g., 'Член/Членка на политичка партија')"
          },
          "MaterialsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Count of materials submitted by member. Always null in this response."
          },
          "AmendmentsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Count of amendments submitted by member. Always null in this response."
          },
          "QuestionsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Count of questions submitted by member. Always null in this response."
          }
        },
        "required": ["UserId", "FullName", "RoleId", "RoleTitle"]
      },
      "description": "All MPs currently affiliated with this political party"
    },
    "Email": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact email; null when not available"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact phone number; null when not available"
    },
    "Image": {
      "type": "string",
      "description": "Party logo/image; may be base64-encoded data or empty string when not available"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "Parliamentary term/structure ID this party data belongs to"
    }
  }
}
```

### Notes
- **Request parameters**: `politicalPartyId` (UUID obtained from GetAllPoliticalParties) and `LanguageId` (1=Macedonian, 2=Albanian, 3=Turkish) control language of response text fields
- **Response structure**: Returns detailed party information including name, member count, associated materials, amendments, questions, and member list
- **Materials array**: Contains all legislative materials (proposals, amendments) submitted by the party with registration dates and current status. Empty when party has no submissions.
- **Amendments array**: Separate collection of amendments proposed by the party; empty in sample but may contain items for other parties
- **Questions array**: Separate collection of parliamentary questions from the party; empty in sample but may contain items for other parties
- **Members array**: Lists all MPs affiliated with the party. All members share RoleId `27` ("Член/Членка на политичка партија"). Count fields (MaterialsCount, AmendmentsCount, QuestionsCount) are always `null` in this endpoint; use dedicated endpoints if per-member activity counts needed
- **Description field**: May be placeholder value like `"-"` if party has no biography text set
- **Image field**: May be empty string `""` when party has no logo; when present contains base64-encoded image data
- **Email/Phone**: Always `null` in observed responses (party-level contact information not exposed via this endpoint)
- **Not paginated**: Returns complete party details without pagination
- **StructureId**: Implicitly matches parliamentary term from which politicalPartyId was obtained