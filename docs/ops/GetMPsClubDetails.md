## GetMPsClubDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "enum": ["GetMPsClubDetails"],
      "description": "Operation name. Uses lowercase 'm' in methodName."
    },
    "mpsClubId": {
      "$ref": "#/$defs/UUID",
      "description": "UUID of the MPs club to retrieve. Obtained from GetAllMPsClubsByStructure."
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId",
      "description": "Language for response text localization. Uses uppercase 'L' in LanguageId (PascalCase). Note: this operation mixes camelCase (methodName, mpsClubId) and PascalCase (LanguageId) naming in the same request."
    }
  },
  "required": ["methodName", "mpsClubId", "LanguageId"],
  "additionalProperties": false
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string",
      "description": "Full name of the MPs club in the requested LanguageId."
    },
    "Description": {
      "type": "string",
      "description": "Description or purpose of the club. May be placeholder '-' when no description is provided."
    },
    "Members": {
      "type": "array",
      "description": "Array of MPs belonging to this club with assigned roles. May include a {_truncated: N} object as the final element, indicating N additional members were omitted from response.",
      "items": {
        "oneOf": [
          {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "UUID of the MP."
              },
              "FirstName": {
                "type": "string",
                "description": "First name of the MP."
              },
              "LastName": {
                "type": "string",
                "description": "Last name of the MP."
              },
              "RoleId": {
                "$ref": "#/$defs/MPsClubRoleId",
                "description": "Role ID within the club (78=President, 79=Vice-President, 81=Member)."
              },
              "RoleTitle": {
                "type": "string",
                "description": "Localized role name with gender-inclusive slash notation (e.g., 'Претседател/Претседателка' = President masc./fem., 'Заменик-претседател/Заменик-претседателка' = Vice-President masc./fem., 'Член/Членка' = Member masc./fem.). Respects requested LanguageId."
              }
            },
            "required": ["Id", "FirstName", "LastName", "RoleId", "RoleTitle"],
            "additionalProperties": false
          },
          {
            "type": "object",
            "properties": {
              "_truncated": {
                "type": "integer",
                "description": "Marker object (not a member); appears as final array element when Members list is truncated. Value indicates N additional members omitted."
              }
            },
            "required": ["_truncated"],
            "additionalProperties": false
          }
        ]
      }
    },
    "StructureId": {
      "$ref": "#/$defs/UUID",
      "description": "Parliamentary term/structure UUID (typically current: 5e00dbd6-ca3c-4d97-b748-f792b2fa3473). Indicates the parliamentary term to which this club belongs."
    }
  },
  "required": ["Name", "Description", "Members", "StructureId"],
  "additionalProperties": false
}
```

### Notes

**Parameter casing:** This operation uses mixed casing in the request: `methodName` and `mpsClubId` (camelCase) combined with `LanguageId` (PascalCase). This is intentional and differs from some other operations; follow the exact casing shown in the Request Schema.

**Member roles and RoleId values:**
- **RoleId 78** (Претседател/Претседателка) — President/Chairperson; typically one per club
- **RoleId 79** (Заменик-претседател/Заменик-претседателка) — Vice-President; zero or more
- **RoleId 81** (Член/Членка) — Member; regular members

**Gender-inclusive role titles:** RoleTitle uses Macedonian notation with `/` separator showing masculine and feminine forms. All roles include this dual-form notation. Other languages may use different conventions; test with LanguageId 2 (Albanian) or 3 (Turkish) if needed.

**Description placeholder:** When no description exists, the field returns the placeholder string `"-"` (not `null` or empty string). Client code should recognize and filter this placeholder for display.

**Array truncation:** Large clubs may have their Members array truncated in the response. The final element will be `{"_truncated": N}` (not a regular member object), indicating N additional members were omitted. Client should handle this marker gracefully and may fetch additional context from GetAllMPsClubsByStructure if a complete roster is needed.

**Localization:** Name, Description, and RoleTitle are localized to the requested LanguageId. Test with different language IDs (1=Macedonian, 2=Albanian, 3=Turkish) to verify localization behavior and any fallback patterns.

**StructureId in response:** The returned StructureId reflects the parliamentary term to which the club belongs and typically matches the structure ID used in the GetAllMPsClubsByStructure call that provided the mpsClubId.

**Data ID source:** Obtain mpsClubId from GetAllMPsClubsByStructure listing.