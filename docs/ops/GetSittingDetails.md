## GetSittingDetails

### Request
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
      "type": "string",
      "format": "uuid",
      "description": "Sitting identifier from GetAllSittings"
    }
  },
  "required": ["MethodName", "LanguageId", "SittingId"]
}
```

**Parameter casing:** Uses `MethodName` (capital M), `SittingId`, and `LanguageId` (all with capital first letter).

### Response
```json
{
  "type": "object",
  "properties": {
    "StatusId": {
      "$ref": "#/$defs/SittingStatusId"
    },
    "StatusTitle": {
      "type": "string",
      "description": "Localized sitting status (e.g. 'Затворена' for closed)"
    },
    "Location": {
      "type": "string",
      "description": "Physical location/room where sitting is held (e.g. 'Сала 6')"
    },
    "Number": {
      "type": "integer",
      "description": "Sequential sitting number"
    },
    "SittingDate": {
      "$ref": "#/$defs/AspDate"
    },
    "TypeTitle": {
      "type": "string",
      "description": "Localized sitting type (e.g. 'Комисиска седница' for committee sitting)"
    },
    "TypeId": {
      "$ref": "#/$defs/SittingTypeId",
      "description": "Sitting type identifier"
    },
    "CommitteeId": {
      "anyOf": [
        {"type": "string", "format": "uuid"},
        {"type": "null"}
      ],
      "description": "Committee identifier (null for plenary sittings)"
    },
    "CommitteeTitle": {
      "anyOf": [
        {"type": "string"},
        {"type": "null"}
      ],
      "description": "Committee name (null for plenary sittings)"
    },
    "MediaLinks": {
      "type": "array",
      "items": {},
      "description": "Media/video links for the sitting; empty when none available"
    },
    "Documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Title": {
            "type": "string"
          },
          "Url": {
            "type": "string"
          },
          "FileName": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Often null in practice"
          },
          "DocumentTypeId": {
            "$ref": "#/$defs/DocumentTypeId"
          },
          "DocumentTypeTitle": {
            "type": "string"
          },
          "IsExported": {
            "type": "boolean",
            "description": "Whether document has been exported/published"
          }
        }
      },
      "description": "Sitting-level documents (e.g. convocation notices)"
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
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
          "description": "May contain XML-like multilingual markup: <MK>...</><AL>...</><EN>...</><FR>...</>"
        },
        "text": {
          "type": "string"
        },
        "type": {
          "$ref": "#/$defs/TreeItemType",
          "description": "ROOT for root agenda node, LEAF for child items"
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
          "description": "See AgendaItemTypeId; null for ROOT nodes"
        },
        "status": {
          "type": "integer",
          "description": "See AgendaItemStatusId; 0 for root, 50=reviewed, 69=new"
        },
        "statusTitle": {
          "anyOf": [
            {"type": "string"},
            {"type": "null"}
          ]
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
          "description": "HTML with material type and proposer info; null for ROOT"
        },
        "children": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
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
              "text": {
                "type": "string"
              },
              "type": {
                "$ref": "#/$defs/TreeItemType"
              },
              "treeItemTypeId": {
                "anyOf": [
                  {"type": "integer"},
                  {"type": "null"}
                ]
              },
              "agendaItemType": {
                "type": "integer",
                "description": "See AgendaItemTypeId enum"
              },
              "status": {
                "type": "integer",
                "description": "See AgendaItemStatusId"
              },
              "statusTitle": {
                "type": "string"
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
                ]
              },
              "children": {
                "type": "array",
                "items": {},
                "description": "Nested children (typically empty for LEAF items)"
              },
              "objectId": {
                "anyOf": [
                  {"type": "string", "format": "uuid"},
                  {"type": "null"}
                ],
                "description": "UUID of linked material when objectTypeId=1"
              },
              "objectTypeId": {
                "type": "integer",
                "description": "0=no object, 1=Material"
              },
              "objectTypeTitle": {
                "anyOf": [
                  {"type": "string"},
                  {"type": "null"}
                ],
                "description": "e.g. 'Материјал' for materials"
              },
              "objectStatusId": {
                "type": "integer",
                "description": "Material status (see MaterialStatusId)"
              },
              "objectSubTypeId": {
                "type": "integer",
                "description": "Material subtype; e.g. 1=law proposal, 28=reports/analyses"
              },
              "manyAmendments": {
                "type": "boolean"
              },
              "mediaItems": {
                "type": "array",
                "items": {},
                "description": "Media items associated with agenda item"
              },
              "VotingDefinitions": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {
                      "type": "string",
                      "format": "uuid",
                      "description": "Use as VotingDefinitionId for GetVotingResultsForAgendaItem"
                    },
                    "Title": {
                      "type": "string"
                    },
                    "Description": {
                      "type": "string"
                    },
                    "VotingType": {
                      "type": "string",
                      "description": "e.g. 'Јавно' for public voting"
                    },
                    "OverallResult": {
                      "type": "string",
                      "description": "e.g. 'Усвоен' for adopted/passed"
                    }
                  }
                },
                "description": "Voting records for this agenda item; empty when no votes"
              },
              "Documents": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "Id": {
                      "type": "string",
                      "format": "uuid"
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
                      "type": "integer"
                    },
                    "DocumentTypeTitle": {
                      "type": "string"
                    },
                    "IsExported": {
                      "type": "boolean"
                    }
                  }
                },
                "description": "Documents associated with agenda item"
              }
            }
          },
          "description": "Agenda items (LEAF nodes) within the sitting"
        },
        "objectId": {
          "type": "null",
          "description": "Null for ROOT node"
        },
        "objectTypeId": {
          "type": "integer",
          "description": "0 for ROOT node"
        },
        "objectTypeTitle": {
          "type": "null",
          "description": "Null for ROOT node"
        },
        "objectStatusId": {
          "type": "integer",
          "description": "0 for ROOT node"
        },
        "objectSubTypeId": {
          "type": "integer",
          "description": "0 for ROOT node"
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
          "items": {}
        },
        "Documents": {
          "type": "array",
          "items": {}
        }
      },
      "description": "Hierarchical tree structure of sitting agenda"
    },
    "Continuations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Number": {
            "type": "integer",
            "description": "May be 0 for continuation sessions"
          },
          "StatusId": {
            "anyOf": [
              {"type": "integer"},
              {"type": "null"}
            ]
          },
          "StatusTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string"
          }
        }
      },
      "description": "Continuation sittings (empty array if no continuations)"
    },
    "SittingDuration": {
      "anyOf": [
        {"type": "number"},
        {"type": "null"}
      ],
      "description": "Duration of sitting; null for scheduled/incomplete sittings"
    },
    "Absents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Fullname": {
            "type": "string"
          },
          "PoliticalParty": {
            "anyOf": [
              {"type": "string"},
              {"type": "null"}
            ],
            "description": "Political party name or null for independents"
          }
        }
      },
      "description": "MPs absent from the sitting; may be truncated in response with _truncated object"
    },
    "Attendances": {
      "type": "array",
      "items": {},
      "description": "Attendance records (empty for scheduled/future sittings)"
    },
    "DescriptionTypeTitle": {
      "type": "string",
      "description": "Sitting description type label (e.g. 'Комисиска седница')"
    },
    "DescriptionTypeId": {
      "type": "integer",
      "description": "Sitting description type (1=Committee sitting)"
    },
    "Votings": {
      "type": "array",
      "items": {},
      "description": "Voting records at sitting level (empty when no top-level votes)"
    },
    "Structure": {
      "type": "string",
      "description": "Parliamentary term period (e.g. '2024-2028')"
    }
  }
}
```

### Notes

**Request parameters:**
- **SittingId** — UUID of the sitting (from GetAllSittings `Items[].Id`)
- Uses `MethodName` and `LanguageId` (PascalCase), not lowercase variants

**Response structure:**
- Returns detailed sitting information including status, location, date, type, and committee (when applicable)
- **Agenda**: Hierarchical tree structure with root node (type: "ROOT") containing children array of agenda items (type: "LEAF")
  - Leaf nodes link to materials/questions via `objectId` and include status, documents, voting definitions
  - `afterText` provides multilingual reading stage labels in XML-like format: `<MK>text</><AL>text</><EN>text</><FR>text/>`
  - `data` contains HTML-formatted proposer information for materials
- **Absents**: List of MPs absent from the sitting (available for scheduled sittings). `PoliticalParty` may be `null`.
- **Attendances**: Array for attendance tracking (empty for scheduled/future sittings)
- **Votings**: Array of voting results (empty for scheduled sittings; populated after voting occurs)
- **Continuations**: Array of continuation sittings (when sitting is split across multiple sessions)
- **Documents**: Sitting-level documents (e.g. convocation notices) with type 20="Известување за свикување на седница"
- **MediaLinks**: Array of media/video links (empty when no media available)

**Future sitting behavior:**
- For scheduled (StatusId: 1) sittings: `Absents` is pre-populated, `Attendances` and `Votings` are empty arrays
- `SittingDuration` remains `null` until sitting completes

**Committee sittings:**
- When `TypeId: 2`, the sitting is a committee or public discussion. `CommitteeId` and `CommitteeTitle` are populated with the committee details.
- `DescriptionTypeTitle` may provide finer categorization (e.g., "Јавна расправа" = public hearing)

**Agenda item statuses:**
- `status: 50` = Reviewed (Разгледана)
- `status: 69` = New (Нова)
- `status: 0` = Not started/unknown (typically for ROOT node)

**Multilingual content:**
- When `LanguageId: 3` (Turkish) or other language requested, localized strings (StatusTitle, TypeTitle, Location) are returned in that language
- `afterText` may still contain multilingual XML-like markup even when specific language requested

**Absents array:**
- Lists MPs who did not attend. `PoliticalParty` may be `null` for independent MPs or when affiliation not recorded
- Large Absents arrays may be truncated by API with `_truncated` object as last item indicating omitted count

**Document handling:**
- Multiple documents may share the same `DocumentTypeId` (e.g. multiple stenograms)
- `FileName` typically null in practice

**Voting definitions:**
- Each agenda item may have zero or more `VotingDefinitions` with voting event details
- Use `VotingDefinitions[].Id` to retrieve full voting results via `GetVotingResultsForAgendaItem`

**Empty arrays and null handling:**
- `MediaLinks`, `Attendances`, `Votings`, `Continuations`, `Documents` return empty arrays `[]` when empty, not `null`
- `Agenda.afterText`, `Agenda.data`, `Absents[].PoliticalParty`, and other fields are nullable and use `anyOf` with null
