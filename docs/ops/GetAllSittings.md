## GetAllSittings

### Notes
Empty results behavior: When no sittings match the filter criteria, the API returns `{"TotalItems": 0, "Items": null}` rather than an empty items array.

The response schema differs significantly from the documented schema. Actual responses include `SittingDate`, `TypeId`, `TypeTitle`, `StatusTitle`, `Location`, `SittingDescriptionTypeTitle`, `Continuations`, `Structure`, and `TotalRows` fields instead of `DateFrom`/`DateTo`, `SittingTypeId`, `CommitteeId`, `Number`, `SessionId`.

`Number` appears in response items for both plenary (`TypeId: 1`) and committee (`TypeId: 2`) sittings, representing the sitting sequence number within that context (e.g., 10th committee sitting, 5th plenary sitting).

`CommitteeTitle` provides the committee name when filtering across multiple committees.

`Continuations` is an empty array in all observed responses; likely populated when a sitting is continued across multiple sessions.

`Structure` and `TotalRows` appear to be metadata fields not populated in list responses.

When `StructureId` is `null`, the API returns sittings from all parliamentary terms/structures, not limited to a single term. `TotalItems` reflects the cross-term total.

### Request
```json
{
  "methodName": "GetAllSittings",
  "Page": 2,
  "Rows": 15,
  "LanguageId": 2,
  "TypeId": 2,
  "CommitteeId": "b8b25861-9b5c-4d47-9717-007b83a8a339",
  "StatusId": 6,
  "DateFrom": null,
  "DateTo": null,
  "SessionId": null,
  "Number": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllSittings"
    },
    "Page": {
      "type": "integer",
      "description": "Page number (1-based)"
    },
    "Rows": {
      "type": "integer",
      "description": "Number of items per page"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "TypeId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Sitting type filter: 1=Plenary, 2=Committee. Set to null to include all types."
    },
    "CommitteeId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
        {"type": "null"}
      ],
      "description": "UUID of committee to filter by. Use with TypeId: 2 for committee sittings. Set to null for plenary sittings or to include all committees."
    },
    "StatusId": {
      "anyOf": [
        {"$ref": "#/$defs/SittingStatusId"},
        {"type": "null"}
      ],
      "description": "Filter sittings by status. Set to null to include all statuses."
    },
    "DateFrom": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter sittings by start date. Set to null to omit date filtering."
    },
    "DateTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter sittings by end date. Set to null to omit date filtering."
    },
    "SessionId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
        {"type": "null"}
      ],
      "description": "Filter by session UUID"
    },
    "Number": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Filter by sitting number"
    },
    "StructureId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of parliamentary term/structure. Set to null to retrieve sittings across all structures/terms. Use specific UUID (e.g., 5e00dbd6-ca3c-4d97-b748-f792b2fa3473) to filter by term."
    }
  },
  "required": ["methodName", "Page", "Rows", "LanguageId"]
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer"
    },
    "Items": {
      "type": ["array", "null"],
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Number": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Sitting sequence number within the committee (TypeId: 2) or plenary (TypeId: 1). Each committee maintains its own sequence."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Primary sitting date/time"
          },
          "TypeId": {
            "$ref": "#/$defs/AgendaItemTypeId",
            "description": "Sitting type: 1=Plenary, 2=Committee"
          },
          "TypeTitle": {
            "type": "string",
            "description": "Localized sitting type name"
          },
          "StatusId": {
            "$ref": "#/$defs/SittingStatusId"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized status name"
          },
          "Location": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Physical location of sitting"
          },
          "CommitteeId": {
            "anyOf": [
              {"type": "string", "format": "uuid"},
              {"type": "null"}
            ],
            "description": "UUID of committee. Present for committee sittings (TypeId: 2); null for plenary."
          },
          "CommitteeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Localized committee name. Present for committee sittings (TypeId: 2); null for plenary."
          },
          "SittingDescriptionTypeTitle": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Localized description of sitting subtype/format (e.g., regular committee sitting, public hearing)"
          },
          "Continuations": {
            "type": "array",
            "description": "Array of continuation sitting references. Empty when sitting has no continuations.",
            "items": {
              "type": "object"
            }
          },
          "Structure": {
            "anyOf": [
              {"type": "object"},
              {"type": "null"}
            ],
            "description": "Structural metadata, typically null in list responses"
          },
          "TotalRows": {
            "type": "integer",
            "description": "Row count metadata, typically 0 in list responses"
          }
        }
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```