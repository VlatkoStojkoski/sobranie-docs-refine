## GetPoliticalPartyDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetPoliticalPartyDetails"
    },
    "politicalPartyId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the political party obtained from GetAllPoliticalParties"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    }
  },
  "required": ["methodName", "politicalPartyId", "LanguageId"]
}
```

### Response Schema

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
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Material title/name"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string",
            "description": "Official registration identifier (format: NN-NNN/N)"
          },
          "StatusId": {
            "type": "integer",
            "description": "Material status identifier; see MaterialStatusId in global $defs"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Human-readable status label in requested language"
          }
        },
        "required": ["Id", "Title", "RegistrationDate", "RegistrationNumber", "StatusId", "StatusTitle"]
      },
      "description": "Materials (legislative proposals, amendments) submitted by this political party. Empty array when party has no materials."
    },
    "Amendments": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Amendments proposed by the party. Empty array when party has no amendments."
    },
    "Questions": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Parliamentary questions submitted by the party. Empty array when party has no questions."
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "$ref": "#/$defs/UUID"
          },
          "FullName": {
            "type": "string",
            "description": "Complete name of the party member"
          },
          "RoleId": {
            "type": "integer",
            "const": 27,
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
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
          },
          "AmendmentsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
          },
          "QuestionsCount": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Always null in this endpoint; use dedicated endpoints for per-member activity counts"
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
      "description": "Party contact email; typically null"
    },
    "Phone": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Party contact phone number; typically null"
    },
    "Image": {
      "type": "string",
      "description": "Party logo/image; may be base64-encoded data or empty string when not available"
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure ID this party data belongs to"
    }
  },
  "required": ["Name", "NumberOfDeputies", "Materials", "Amendments", "Questions", "Members", "StructureId"]
}
```

### Notes

- **Parameter casing**: Uses lowercase `methodName` and PascalCase `LanguageId`.
- **politicalPartyId source**: Obtain from GetAllPoliticalParties response.
- **LanguageId**: Controls language of all text fields (Name, StatusTitle, RoleTitle, etc.). See global LanguageId enum (1=Macedonian, 2=Albanian, 3=Turkish).
- **Response structure**: Comprehensive party details including name, member count, associated legislative materials/amendments/questions, and full member roster.
- **Materials array**: All legislative materials (proposals) submitted by the party, with registration dates and current status. Empty when party has no submissions. StatusId references MaterialStatusId enum in global $defs.
- **Amendments and Questions arrays**: Separate from Materials; may be empty depending on party activity.
- **Members array**: Lists all MPs currently affiliated with the party. All members have RoleId `27` (member of political party). The *Count fields (MaterialsCount, AmendmentsCount, QuestionsCount) are always `null` in this endpoint response; they are not populated. Use dedicated per-MP endpoints if per-member activity counts are needed.
- **Description field**: May contain placeholder value like `"-"` if party has no biography text set.
- **Image field**: May be empty string `""` when party has no logo; when present contains base64-encoded image data.
- **Email/Phone**: Typically `null` for political parties; contact information is directed through individual members rather than the party entity.
- **Not paginated**: Returns complete party details in a single response (no page/rows parameters).
- **StructureId**: Implicitly matches the parliamentary term from which politicalPartyId was obtained. Identifies which parliamentary term the party data belongs to.
