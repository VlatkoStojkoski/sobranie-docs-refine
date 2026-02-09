## GetMPsClubDetails

### Description
Retrieves detailed information about a specific MPs club (inter-party parliamentary group), including full member roster with roles.

### Request
```json
{
  "methodName": "GetMPsClubDetails",
  "mpsClubId": "22ded665-2466-4d7e-a04b-03f8a150fc8c",
  "LanguageId": 1
}
```

**Request parameters:**
- **methodName** — String; literal value `"GetMPsClubDetails"`. Uses lowercase `m` in `methodName` (camelCase).
- **mpsClubId** — UUID string; identifier of the MPs club to retrieve. Obtained from `GetAllMPsClubsByStructure`.
- **LanguageId** — Integer; requested language for response text (1=Macedonian, 2=Albanian, 3=Turkish). Uses uppercase `L` in `LanguageId` (PascalCase). This operation mixes camelCase and PascalCase parameter naming.

### Response
```json
{
  "Name": "Пратеничка група на партијата...",
  "Description": "Description text or '-' placeholder",
  "Members": [
    {
      "Id": "550e8400-e29b-41d4-a716-446655440000",
      "FirstName": "Иван",
      "LastName": "Петровски",
      "RoleId": 78,
      "RoleTitle": "Претседател/Претседателка"
    },
    {
      "Id": "550e8400-e29b-41d4-a716-446655440001",
      "FirstName": "Марија",
      "LastName": "Стефановска",
      "RoleId": 81,
      "RoleTitle": "Член/Членка"
    },
    {
      "_truncated": 31
    }
  ],
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

**Response schema:**
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full name of the MPs club in the requested language"
    },
    "Description": {
      "type": "string",
      "description": "Description text for the club. May contain placeholder value '-' when no description is provided"
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs belonging to this club with their roles. May include _truncated placeholder for large lists",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid",
            "description": "UUID identifier for the MP member"
          },
          "FirstName": {
            "type": "string",
            "description": "Member's first name"
          },
          "LastName": {
            "type": "string",
            "description": "Member's last name"
          },
          "RoleId": {
            "type": "integer",
            "enum": [78, 79, 81],
            "description": "Member's role within the club (see MPsClubRoleId in $defs). 78=President/Chairperson, 79=Vice-President, 81=Member"
          },
          "RoleTitle": {
            "type": "string",
            "description": "Localized human-readable role title, may include gender-inclusive slash notation (e.g., 'Претседател/Претседателка')"
          },
          "_truncated": {
            "type": "integer",
            "description": "Placeholder object indicating N additional members were truncated from response (not present for regular member objects)"
          }
        },
        "required": ["Id", "FirstName", "LastName", "RoleId", "RoleTitle"]
      }
    },
    "StructureId": {
      "type": "string",
      "format": "uuid",
      "description": "UUID of the parliamentary term/structure this club belongs to (typically current term: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473)"
    }
  },
  "required": ["Name", "Description", "Members", "StructureId"]
}
```

### Per-operation Notes

**Parameter casing:** This operation uses mixed casing: `methodName` (lowercase m) and `mpsClubId` (camelCase) but `LanguageId` (uppercase L). This is a variation of the common pattern where some operations mix PascalCase and camelCase.

**Member role hierarchy:** MPs clubs have a structured membership with distinct roles:
- **RoleId 78** = President/Chairperson (Претседател/Претседателка) — typically one per club
- **RoleId 79** = Vice-President (Заменик-претседател/Заменик-претседателка) — may be zero or multiple
- **RoleId 81** = Member (Член/Членка) — regular club members

**Gendered role titles:** RoleTitle values use gender-inclusive notation with a slash separator, following Macedonian language conventions (e.g., "Претседател/Претседателка" represents masculine/feminine forms). This applies to all role types.

**Description placeholder:** When a club has no description, the API returns the string `"-"` rather than null or an empty string. Client code should detect this placeholder and treat it as "no description provided".

**Response truncation:** The Members array may include a `{"_truncated": N}` placeholder object as the final element, indicating N additional members exist but were not included in the response. For example, `{"_truncated": 31}` means 31 additional members are not shown. This is an API behavior for handling large clubs; client code should be prepared to handle this marker.

**StructureId in response:** The returned StructureId indicates which parliamentary term this club belongs to. This typically matches the StructureId provided to `GetAllMPsClubsByStructure` when retrieving the club list, and is often the current term `5e00dbd6-ca3c-4d97-b748-f792b2fa3473`.

**Localization:** The `Name`, `Description`, and `RoleTitle` fields are localized to the requested `LanguageId`. Test with different language IDs to confirm expected localization behavior for your application.
