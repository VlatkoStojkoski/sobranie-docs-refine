## GetAllSittings

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "methodName": {
      "type": "string",
      "const": "GetAllSittings",
      "description": "Operation name"
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
        {"$ref": "#/$defs/AgendaItemTypeId"},
        {"type": "null"}
      ],
      "description": "1=Plenary, 2=Committee. Set to null to include all types."
    },
    "CommitteeId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "UUID of committee. Use with TypeId: 2. Set to null for plenary or to include all committees."
    },
    "StatusId": {
      "anyOf": [
        {"$ref": "#/$defs/SittingStatusId"},
        {"type": "null"}
      ],
      "description": "Filter by status. Set to null to include all statuses."
    },
    "DateFrom": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter by start date. Set to null to omit."
    },
    "DateTo": {
      "anyOf": [
        {"$ref": "#/$defs/AspDate"},
        {"type": "null"}
      ],
      "description": "Filter by end date. Set to null to omit."
    },
    "SessionId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
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
      "description": "UUID of parliamentary term/structure. Set to null to query across all terms. Commonly 5e00dbd6-ca3c-4d97-b748-f792b2fa3473 for current term."
    }
  },
  "required": ["methodName", "Page", "Rows", "LanguageId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer",
      "description": "Total sittings matching filter across all pages"
    },
    "Items": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "Unique identifier of the sitting"
              },
              "Number": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ],
                "description": "Sitting sequence number within committee or plenary context"
              },
              "SittingDate": {
                "$ref": "#/$defs/AspDate",
                "description": "Primary sitting date/time"
              },
              "TypeId": {
                "$ref": "#/$defs/AgendaItemTypeId",
                "description": "1=Plenary, 2=Committee"
              },
              "TypeTitle": {
                "type": "string",
                "description": "Localized sitting type name (e.g. 'Пленарна седница', 'Комисионска седница')"
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
                "description": "Physical location/room (e.g. 'Сала 4')"
              },
              "CommitteeId": {
                "anyOf": [
                  {"$ref": "#/$defs/UUID"},
                  {"type": "null"}
                ],
                "description": "UUID of committee. Null for plenary sittings (TypeId: 1)."
              },
              "CommitteeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Localized committee name. Null for plenary (TypeId: 1)."
              },
              "SittingDescriptionTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "Localized description of sitting subtype/format"
              },
              "Continuations": {
                "type": "array",
                "description": "Array of continuation sitting references. Empty in standard responses; likely populated when sitting spans multiple sessions.",
                "items": {"type": "object"}
              },
              "Structure": {
                "anyOf": [
                  {"type": "object"},
                  {"type": "null"}
                ],
                "description": "Structural metadata; typically null in list responses"
              },
              "TotalRows": {
                "type": "integer",
                "description": "Row count metadata field"
              }
            }
          }
        },
        {"type": "null"}
      ],
      "description": "Array of sittings or null when TotalItems is 0"
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Notes

- **Empty results behavior:** When no sittings match filter criteria, returns `{"TotalItems": 0, "Items": null}` rather than empty array.
- **Sitting sequence number:** `Number` field represents the sitting sequence number within the specific context: for plenary (`TypeId: 1`), the Nth plenary sitting; for committee (`TypeId: 2`), the Nth committee sitting. Each context maintains its own sequence.
- **Committee metadata:** `CommitteeId` and `CommitteeTitle` are populated only for committee sittings (`TypeId: 2`); both are null for plenary (`TypeId: 1`).
- **Continuations:** `Continuations` array is empty in standard responses; likely populated when a sitting spans multiple sessions.
- **Structure field:** Metadata field typically null in list responses.
- **Cross-structure queries:** When `StructureId` is null, returns sittings from all parliamentary terms/structures; `TotalItems` reflects cross-term total.
- **Pagination:** Uses `Page` (1-based) and `Rows` pattern. When `TotalItems: 0`, `Items` is null, not an empty array.
- **Localization:** `TypeTitle`, `StatusTitle`, `CommitteeTitle`, and `SittingDescriptionTypeTitle` are localized according to `LanguageId`.
