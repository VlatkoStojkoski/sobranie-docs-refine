## GetSittingDetails

### Request Schema

```json
{
  "type": "object",
  "properties": {
    "MethodName": {
      "type": "string",
      "const": "GetSittingDetails"
    },
    "LanguageId": {
      "$ref": "#/$defs/LanguageId"
    },
    "SittingId": {
      "$ref": "#/$defs/UUID",
      "description": "Sitting identifier from GetAllSittings Items[].Id"
    }
  },
  "required": ["MethodName", "LanguageId", "SittingId"]
}
```

### Response Schema

```json
{
  "type": "object",
  "properties": {
    "StatusId": {
      "$ref": "#/$defs/SittingStatusId"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Localized sitting status label (e.g. 'Затворена' for closed, 'Почната' for started). Trim whitespace for display."
    },
    "Location": {
      "type": "string",
      "description": "Physical location/room (e.g. 'Сала 6'). Empty string when not specified."
    },
    "Number": {
      "type": "integer",
      "description": "Sequential sitting number within the committee (TypeId: 2) or plenary (TypeId: 1)"
    },
    "SittingDate": {
      "$ref": "#/$defs/AspDate",
      "description": "Primary date/time of the sitting event"
    },
    "TypeTitle": {
      "type": "string",
      "description": "Localized sitting type (e.g. 'Комисіska седница' for committee, 'Пленарна седница' for plenary). Trim whitespace for display. May contain spelling variations or typos."
    },
    "TypeId": {
      "$ref": "#/$defs/SittingTypeId"
    },
    "CommitteeId": {
      "anyOf": [
        {"$ref": "#/$defs/UUID"},
        {"type": "null"}
      ],
      "description": "Committee UUID when TypeId: 2 (committee sitting). Null for plenary sittings (TypeId: 1)"
    },
    "CommitteeTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee name in requested language. Null for plenary sittings. Trim whitespace for display."
    },
    "DescriptionTypeId": {
      "anyOf": [
        {"type": "integer"},
        {"type": "null"}
      ],
      "description": "Sitting description type; e.g. 1 for committee sitting. Null for plenary sittings."
    },
    "DescriptionTypeTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Localized description type label (e.g. 'Комисiska седница', 'Јавна расправа' for public discussion). Null for plenary sittings. Trim whitespace for display."
    },
    "Structure": {
      "type": "string",
      "description": "Parliamentary term period as string (e.g. '2024-2028')"
    },
    "SittingDuration": {
      "anyOf": [
        {"type": "number"},
        {"type": "null"}
      ],
      "description": "Duration in hours. Null for scheduled sittings or even after completion; may remain unpopulated for closed sittings"
    },
    "MediaLinks": {
      "type": "array",
      "items": {},
      "description": "Media/video links for the sitting. Empty array when none available"
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Title": {
            "type": "string",
            "description": "Document title/name"
          },
          "Url": {
            "type": "string",
            "description": "URL to download or view document"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "File name. Often null in practice"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId"
          },
          "DocumentTypeTitle": {
            "type": "string",
            "description": "Localized document type label"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether document has been exported/published"
          }
        },
        "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
      },
      "description": "Sitting-level documents (e.g. convocation notices). Empty array when none. May include _truncated marker as standalone object within array indicating N additional items omitted, counting toward array length. Multiple documents may share same DocumentTypeId."
    },
    "Continuations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID"
          },
          "Number": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Continuation session number (0, 1, or higher)"
          },
          "StatusId": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ],
            "description": "Continuation sitting status"
          },
          "StatusTitle": {
            "type": "string",
            "description": "Localized continuation sitting status. Trim whitespace for display."
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate",
            "description": "Date/time of continuation sitting"
          },
          "Location": {
            "type": "string",
            "description": "Physical location of continuation sitting"
          }
        },
        "required": ["Id", "StatusTitle", "SittingDate", "Location"]
      },
      "description": "Continuation sittings when sitting spans multiple sessions. Empty array when no continuations."
    },
    "Absents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "$ref": "#/$defs/UUID",
            "description": "MP identifier"
          },
          "Fullname": {
            "type": "string",
            "description": "Full name of absent MP"
          },
          "PoliticalParty": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Political party name, or null for independents"
          }
        },
        "required": ["Id", "Fullname"]
      },
      "description": "MPs absent from the sitting. Available for scheduled sittings. May include _truncated marker as standalone object within array indicating N additional items omitted, counting toward array length."
    },
    "Attendances": {
      "type": "array",
      "items": {},
      "description": "Attendance records. Empty array for scheduled/future sittings; populated after sitting occurs. May include _truncated marker as standalone object within array indicating N additional items omitted, counting toward array length."
    },
    "Votings": {
      "type": "array",
      "items": {},
      "description": "Voting records at sitting level. Empty array for scheduled sittings or when no top-level votes occur. May include _truncated marker as standalone object within array indicating N additional items omitted, counting toward array length."
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {
          "$ref": "#/$defs/UUID"
        },
        "type": {
          "$ref": "#/$defs/TreeItemType",
          "description": "ROOT for root agenda container, LEAF for individual agenda items"
        },
        "text": {
          "type": "string",
          "description": "Root agenda text/title"
        },
        "beforeText": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
        },
        "afterText": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "May contain XML-like multilingual markup: <MK>...</MK><AL>...</AL><EN>...</EN><FR>...</FR> regardless of requested LanguageId"
        },
        "status": {
          "type": "integer",
          "description": "0 for ROOT node. For LEAF items: see AgendaItemStatusId (50=reviewed, 69=new, 60=other)"
        },
        "statusTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
        },
        "treeItemTypeId": {
          "anyOf": [
            {"type": "integer"},
            {"type": "null"}
          ]
        },
        "agendaItemType": {
          "anyOf": [
            {"type": "integer"},
            {"type": "null"}
          ],
          "description": "See AgendaItemTypeId (1=Plenary, 2=Committee, 8=Amendment, other values may exist). Null for ROOT nodes."
        },
        "isActive": {
          "type": "boolean"
        },
        "order": {
          "type": "integer",
          "description": "Display order"
        },
        "euCompatible": {
          "type": "boolean",
          "description": "EU compatibility flag"
        },
        "data": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "HTML-formatted material type and proposer info. Null for ROOT. Parse HTML appropriately for display."
        },
        "objectId": {
          "anyOf": [
            {"$ref": "#/$defs/UUID"},
            {"type": "null"}
          ],
          "description": "UUID of linked material when objectTypeId: 1. Null for ROOT or non-material items. Pass to GetMaterialDetails."
        },
        "objectTypeId": {
          "$ref": "#/$defs/AgendaObjectTypeId",
          "description": "0 for ROOT. 1=Material, 4=Questions/other items."
        },
        "objectTypeTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ],
          "description": "e.g. 'Материјал' for material items. Null for ROOT"
        },
        "objectStatusId": {
          "type": "integer",
          "description": "Material status when objectTypeId: 1. See MaterialStatusId. 0 for ROOT"
        },
        "objectSubTypeId": {
          "anyOf": [
            {"type": "integer"},
            {"type": "null"}
          ],
          "description": "Material subtype (e.g. 1=law proposal, 28=reports). 0 for ROOT. Null in some contexts (e.g. nested amendments)."
        },
        "manyAmendments": {
          "type": "boolean",
          "description": "Indicates multiple amendments to material"
        },
        "mediaItems": {
          "type": "array",
          "items": {},
          "description": "Media items associated with agenda item or ROOT"
        },
        "VotingDefinitions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "Use as VotingDefinitionId parameter in GetVotingResultsForAgendaItem"
              },
              "Title": {
                "type": "string",
                "description": "Voting definition title"
              },
              "Description": {
                "type": "string",
                "description": "Voting description"
              },
              "VotingType": {
                "type": "string",
                "description": "Type of voting (e.g. 'Јавно' for public voting)"
              },
              "OverallResult": {
                "type": "string",
                "description": "Overall voting result (e.g. 'Усвоен' for adopted/passed)"
              }
            },
            "required": ["Id", "Title", "VotingType", "OverallResult"]
          },
          "description": "Voting events for agenda item. Empty array when no votes."
        },
        "Documents": {
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
              "Url": {
                "type": "string"
              },
              "FileName": {
                "type": "null"
              },
              "DocumentTypeId": {
                "$ref": "#/$defs/DocumentTypeId"
              },
              "DocumentTypeTitle": {
                "type": "string"
              },
              "IsExported": {
                "type": "boolean"
              }
            },
            "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
          },
          "description": "Documents associated with agenda item. Empty array when none."
        },
        "children": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "$ref": "#/$defs/UUID"
              },
              "type": {
                "$ref": "#/$defs/TreeItemType",
                "description": "Should be LEAF for child items"
              },
              "text": {
                "type": "string"
              },
              "beforeText": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "afterText": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "status": {
                "type": "integer",
                "description": "See AgendaItemStatusId (50=reviewed, 69=new, 60=other statuses)"
              },
              "statusTitle": {
                "type": "string"
              },
              "treeItemTypeId": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ]
              },
              "agendaItemType": {
                "type": "integer",
                "description": "See AgendaItemTypeId (1=Plenary, 2=Committee, 8=Amendment, other values may exist)"
              },
              "isActive": {
                "type": "boolean"
              },
              "order": {
                "type": "integer"
              },
              "euCompatible": {
                "type": "boolean"
              },
              "data": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "HTML-formatted material/item details. Parse HTML appropriately for display."
              },
              "objectId": {
                "anyOf": [
                  {"$ref": "#/$defs/UUID"},
                  {"type": "null"}
                ],
                "description": "UUID of linked material (when objectTypeId: 1)"
              },
              "objectTypeId": {
                "$ref": "#/$defs/AgendaObjectTypeId"
              },
              "objectTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ]
              },
              "objectStatusId": {
                "type": "integer",
                "description": "Material status"
              },
              "objectSubTypeId": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ],
                "description": "Material subtype. Null in some contexts (e.g. nested amendments)."
              },
              "manyAmendments": {
                "type": "boolean"
              },
              "mediaItems": {
                "type": "array",
                "items": {}
              },
              "VotingDefinitions": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {"$ref": "#/$defs/UUID"},
                    "Title": {"type": "string"},
                    "Description": {"type": "string"},
                    "VotingType": {"type": "string"},
                    "OverallResult": {"type": "string"}
                  },
                  "required": ["Id", "Title", "VotingType", "OverallResult"]
                },
                "description": "Voting events for this leaf item"
              },
              "Documents": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {"$ref": "#/$defs/UUID"},
                    "Title": {"type": "string"},
                    "Url": {"type": "string"},
                    "FileName": {"type": "null"},
                    "DocumentTypeId": {"$ref": "#/$defs/DocumentTypeId"},
                    "DocumentTypeTitle": {"type": "string"},
                    "IsExported": {"type": "boolean"}
                  },
                  "required": ["Id", "Title", "Url", "DocumentTypeId", "DocumentTypeTitle", "IsExported"]
                }
              },
              "children": {
                "type": "array",
                "items": {},
                "description": "Nested children (e.g. amendments within materials); typically empty for LEAF items representing plain agenda items. LEAF nodes representing materials (objectTypeId: 1) may contain nested children for amendments, each with its own objectId, agendaItemType, status, and objectSubTypeId (which may be null)."
              }
            },
            "required": ["id", "type", "text", "status", "agendaItemType", "isActive", "order", "euCompatible", "objectTypeId", "objectStatusId", "objectSubTypeId", "manyAmendments", "mediaItems", "VotingDefinitions", "Documents", "children"]
          },
          "description": "Agenda items (LEAF nodes) within the sitting. Root node (type: ROOT) contains this children array. May include _truncated marker as standalone object within array indicating N additional items omitted, counting toward array length."
        }
      },
      "required": ["id", "type", "text", "status", "isActive", "order", "euCompatible", "objectTypeId", "objectStatusId", "objectSubTypeId", "manyAmendments", "mediaItems", "VotingDefinitions", "Documents", "children"],
      "description": "Hierarchical tree structure of sitting agenda. Root node has type: ROOT with children array of agenda items (type: LEAF)."
    }
  },
  "required": ["StatusId", "StatusTitle", "Location", "Number", "SittingDate", "TypeTitle", "TypeId", "Structure", "MediaLinks", "Documents", "Continuations", "Absents", "Attendances", "Votings", "Agenda"]
}
```

### Notes

**Parameter casing:**
- Request uses `MethodName`, `LanguageId`, `SittingId` (all PascalCase)
- Do not use lowercase variants (`methodName`, `languageId`, `sittingId`)

**Sitting types:**
- **Plenary sitting** (`TypeId: 1`): `CommitteeId` and `CommitteeTitle` are null. `DescriptionTypeTitle` and `DescriptionTypeId` are null.
- **Committee sitting** (`TypeId: 2`): `CommitteeId` and `CommitteeTitle` are populated. `DescriptionTypeTitle` may be 'Комисiska седница' or other committee-specific type
- **Public hearing**: May appear as `TypeId: 2` with `DescriptionTypeTitle: 'Јавна расправа'`

**Status and timing:**
- **Scheduled sitting** (`StatusId: 1`): `Absents` is pre-populated; `Attendances`, `Votings`, `SittingDuration` are empty/null
- **Started/in progress** (`StatusId: 2`): Fields populating as sitting progresses
- **Completed sitting** (`StatusId: 3`): All fields populated; `SittingDuration` may contain hours or may be null
- **Incomplete sitting** (`StatusId: 4`): Similar to started, may be suspended
- **Closed sitting** (`StatusId: 5`): Similar to completed; `SittingDuration` may remain null even after closure
- **Postponed sitting** (`StatusId: 6`): Rescheduled; `Absents` pre-populated

**Agenda structure:**
- Root node always has `type: 'ROOT'`, `objectTypeId: 0`, `status: 0`, `objectId: null`
- `children` array contains LEAF nodes representing actual agenda items
- Each LEAF node has `objectTypeId` indicating linked item type (1=Material, 4=Questions, 0=None)
- Leaf nodes with `objectTypeId: 1` have `objectId` = material UUID; pass to `GetMaterialDetails`
- Tree may be nested to arbitrary depth; LEAF nodes representing materials may contain nested children for amendments
- Nested amendment nodes may have `agendaItemType: 8`, `status: 60`, and `objectSubTypeId: null`

**Voting definitions:**
- Each agenda item can have zero or more voting definitions
- Use `VotingDefinitions[].Id` as `VotingDefinitionId` parameter in `GetVotingResultsForAgendaItem` to retrieve detailed voting tallies
- `OverallResult` shows high-level outcome (e.g. 'Усвоен' = passed)

**Document types:**
- `DocumentTypeId: 19` = Решение за свикување седница (Decision to convene sitting)
- `DocumentTypeId: 20` = Convocation notice (Известување за свикување)
- `DocumentTypeId: 40` = Известување за презакажување на седница (Notice of sitting rescheduling)
- `DocumentTypeId: 42` = Известување за продолжување на седница (Notice of sitting continuation)
- `DocumentTypeId: 43` = Известување за дополнување на дневен ред (Notice of agenda supplement)
- `DocumentTypeId: 7` = Full text of material
- `DocumentTypeId: 46` = Legislative committee report
- `DocumentTypeId: 52` = Committee report
- Multiple documents may have the same type
- Documents array may be truncated with _truncated marker

**Continuations:**
- Empty array when sitting completes in single session
- Multiple continuation objects when sitting spans multiple days/sessions
- Each continuation has its own date, location, status, and number (which may be 0, 1, or higher, and may be null)

**Absents array:**
- Lists MPs who did not attend
- `PoliticalParty` may be null for independents or when affiliation not recorded
- May be truncated with `_truncated` object as final item indicating number of additional records omitted
- Empty array if all expected members attended

**Attendances array:**
- Populated only after sitting has started or completed
- May be truncated with `_truncated` marker

**Votings array:**
- Sitting-level voting records
- May be truncated with `_truncated` marker

**Truncation behavior:**
- `Documents`, `Continuations`, `Absents`, `Attendances`, `Votings`, and `Agenda.children` arrays may include a standalone `_truncated` object as an element within the array, indicating the number of additional items omitted and counting toward the array length

**Language support:**
- `LanguageId: 1` = Macedonian (default)
- `LanguageId: 2` = Albanian
- `LanguageId: 3` = Turkish
- Affects `StatusTitle`, `TypeTitle`, `CommitteeTitle`, `DescriptionTypeTitle`, `statusTitle` in agenda, and other localized fields
- `afterText` may contain XML-like multilingual markup (`<MK>...</MK><AL>...</AL>`) even when specific language requested

**Data quality:**
- Localized titles may contain leading/trailing whitespace; trim for display
- HTML in `data` fields should be parsed appropriately for client display
- Handle `null` and empty array values consistently in client code
