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
            "anyOf": [
              {
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
                    "description": "UUID of committee. Null for plenary sittings (TypeId: 1). May be omitted from response when null."
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
              },
              {
                "type": "object",
                "properties": {
                  "_truncated": {
                    "type": "integer",
                    "description": "Truncation marker: N additional items omitted"
                  }
                },
                "required": ["_truncated"]
              }
            ]
          }
        },
        {"type": "null"}
      ],
      "description": "Array of sittings or null when TotalItems is 0. May include a truncation marker object {\"_truncated\": N} at any position within the array (not as a property on items), indicating N additional items were omitted. The truncation marker counts toward the array length and follows the global listing endpoint truncation pattern."
    }
  },
  "required": ["TotalItems", "Items"]
}
```

### Notes

- **Empty results behavior:** When no sittings match filter criteria, returns `{"TotalItems": 0, "Items": null}` rather than empty array.
- **Sitting sequence number:** `Number` field represents the sitting sequence number within the specific context: for plenary (`TypeId: 1`), the Nth plenary sitting; for committee (`TypeId: 2`), the Nth committee sitting. Each context maintains its own sequence.
- **Committee metadata:** `CommitteeTitle` is populated for committee sittings (`TypeId: 2`) and null for plenary (`TypeId: 1`). `CommitteeId` may be omitted entirely from response objects when null (for plenary sittings) rather than explicitly returned, though the schema permits it as a nullable UUID field.
- **Array truncation:** In the `Items` array, a standalone object `{"_truncated": N}` may appear at any position (including mid-array), indicating N additional items were omitted. This object counts toward the array length. See global "Array truncation" pattern.
- **Continuations:** `Continuations` array is empty in standard responses; likely populated when a sitting spans multiple sessions.
- **Structure field:** Metadata field typically null in list responses.
- **Cross-structure queries:** When `StructureId` is null, returns sittings from all parliamentary terms/structures; `TotalItems` reflects cross-term total.
- **Pagination:** Uses `Page` (1-based) and `Rows` pattern. When `TotalItems: 0`, `Items` is null, not an empty array.
- **Localization:** `TypeTitle`, `StatusTitle`, `CommitteeTitle`, and `SittingDescriptionTypeTitle` are localized according to `LanguageId`.