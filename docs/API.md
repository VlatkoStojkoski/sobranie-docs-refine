# Sobranie.mk API Index

> North Macedonian Parliament (Собрание) — operation index and calling conventions.

## Calling Conventions

### 1. Method-based (standard)

**URL:** `https://www.sobranie.mk/Routing/MakePostRequest`  
**Method:** POST  
**Content-Type:** application/json

Request body includes `methodName` (or `MethodName` for some operations) and operation-specific parameters. The method name selects the operation.

**Parameter casing:** Some operations use `methodName`/`languageId`; others use `MethodName`/`LanguageId`. See per-operation notes.

### 2. ASMX (non-standard)

**Base:** `https://www.sobranie.mk/Moldova/services/`  
**Format:** POST with wrapped request body (e.g. `{ "model": { ... } }`).  
**Response:** Often wrapped in `d` property.

### 3. Infrastructure (non-standard)

**Base:** `https://www.sobranie.mk/Infrastructure/`  
**Format:** POST, no methodName. Different request/response shapes.

---

## Common Conventions

- **Date format:** `/Date(timestamp)/` — milliseconds since Unix epoch
- **LanguageId:** 1 = Macedonian, 2 = Albanian, 3 = Turkish
- **StructureId:** Parliamentary term. From `GetAllStructuresForFilter`. Often `5e00dbd6-ca3c-4d97-b748-f792b2fa3473` (current)

---

## Operations

### Catalogs (reference data)

| Operation | Method-based | Description |
|-----------|--------------|-------------|
| GetAllGenders | ✓ | Gender options (1=Male, 2=Female) |
| GetAllStructuresForFilter | ✓ | Parliamentary terms (StructureId) |
| GetAllCommitteesForFilter | ✓ | Committees per structure |
| GetAllMaterialStatusesForFilter | ✓ | Material status options |
| GetAllMaterialTypesForFilter | ✓ | Material type options |
| GetAllSittingStatuses | ✓ | Sitting status (1–6) |
| GetAllQuestionStatuses | ✓ | Question status (17,19,20,21) |
| GetAllInstitutionsForFilter | ✓ | Institutions (ministries, etc.). May include placeholder entries (Title: "/") |
| GetAllProcedureTypes | ✓ | Procedure types (1,2,3) |
| GetProposerTypes | ✓ | Proposer types (Id, Title, Order) |
| GetAllApplicationTypes | ✓ | Application types |

### Listings (paginated / filterable)

| Operation | Method-based | Description |
|-----------|--------------|-------------|
| GetAllSittings | ✓ | Sittings. Filter: TypeId, CommitteeId, StatusId, dates |
| GetAllQuestions | ✓ | Parliamentary questions |
| GetAllMaterialsForPublicPortal | ✓ | Materials. Uses MethodName. Many filters |
| GetParliamentMPsNoImage | ✓ | MPs. Filter: gender, party, search. Note: includes UserImg (base64) despite name |
| GetMonthlyAgenda | ✓ | Agenda for month/year |
| GetAllPoliticalParties | ✓ | Parties per structure |
| GetAllCouncils | ✓ | Councils |
| GetAllParliamentaryGroups | ✓ | Parliamentary groups |
| GetAllMPsClubsByStructure | ✓ | MPs clubs. Uses MethodName |

### Detail (item by ID)

| Operation | Method-based | ID source |
|-----------|--------------|-----------|
| GetSittingDetails | ✓ MethodName, SittingId | GetAllSittings |
| GetMaterialDetails | ✓ MaterialId | GetAllMaterialsForPublicPortal |
| GetQuestionDetails | ✓ QuestionId | GetAllQuestions |
| GetCommitteeDetails | ✓ committeeId | GetAllCommitteesForFilter |
| GetCouncilDetails | ✓ committeeId | GetAllCouncils |
| GetPoliticalPartyDetails | ✓ politicalPartyId | GetAllPoliticalParties |
| GetParliamentaryGroupDetails | ✓ parliamentaryGroupId | GetAllParliamentaryGroups |
| GetMPsClubDetails | ✓ mpsClubId | GetAllMPsClubsByStructure |
| GetUserDetailsByStructure | ✓ userId, structureId | GetParliamentMPsNoImage |
| GetAmendmentDetails | ✓ amendmentId | GetMaterialDetails |
| GetVotingResultsForSitting | ✓ votingDefinitionId, sittingId | GetSittingDetails |
| GetVotingResultsForAgendaItem | ✓ VotingDefinitionId, AgendaItemId | GetSittingDetails agenda |
| GetVotingResultsForAgendaItemReportDocument | ✓ | Same as above |

### Non-standard

| Operation | URL | Format |
|-----------|-----|--------|
| GetCustomEventsCalendar | Moldova/services/CalendarService.asmx/GetCustomEventsCalendar | ASMX, model: {Language, Month, Year}. Response: d array with __type, Id, EventDescription, EventLink, EventLocation, EventDate, EventType |
| LoadLanguage | Infrastructure/LoadLanguage | POST, empty body. Returns Code, Items (Key/Value localization) |
| GetOfficialVisitsForUser | Moldova/services/OfficialVisits.asmx/GetOfficialVisitsForUser | ASMX, model: user UUID. Response: {"d": []} (array of visit objects when data present) |

---

# Schemas and per-operation reference

## $defs

```json
{
  "AspDate": {
    "type": "string",
    "pattern": "^/Date\\(\\d+\\)/$"
  },
  "LanguageId": {
    "type": "integer",
    "description": "1=Macedonian, 2=Albanian, 3=Turkish"
  },
  "GenderId": {
    "type": "integer",
    "enum": [1, 2],
    "description": "1=Male (Машки), 2=Female (Женски)"
  },
  "SittingStatusId": {
    "type": "integer",
    "enum": [1, 2, 3, 4, 5, 6],
    "description": "1=Scheduled, 2=Started, 3=Completed, 4=Incomplete, 5=Closed, 6=Postponed"
  },
  "AgendaItemTypeId": {
    "type": "integer",
    "enum": [1, 2],
    "description": "1=Plenary, 2=Committee"
  },
  "QuestionStatusId": {
    "type": "integer",
    "enum": [17, 19, 20, 21],
    "description": "17=Delivered, 19=Answered, 20=Secret answer, 21=Written answer"
  },
  "MaterialStatusId": {
    "type": "integer",
    "enum": [0, 6, 9, 10, 11, 12, 24, 64],
    "description": "0=Plenary/unknown, 6=Delivered to MPs, 9=First reading, 10=Second, 11=Third, 12=Closed, 24=Rejected, 64=Committee processing"
  },
  "ProposerTypeId": {
    "type": "integer",
    "enum": [1, 2, 4],
    "description": "1=MP, 2=Government, 4=Voter group"
  },
  "ProcedureTypeId": {
    "type": "integer",
    "enum": [1, 2, 3],
    "description": "1=Regular, 2=Shortened, 3=Urgent"
  },
  "UUID": {
    "type": "string",
    "format": "uuid"
  }
}
```

## Common patterns

- **Institutional authors**: `Authors[].Id` = `"00000000-0000-0000-0000-000000000000"` with full name/title in `FirstName`, empty `LastName`. Used for government, committees.
- **Plenary vs committee**: `CommitteeId`/`CommitteeTitle` are `null` for plenary (`TypeId`/`SittingTypeId` 1); populated for committee (2).
- **ResponsibleCommittee**: Can be empty string `""` for some material types (e.g. appointments, resignations).
- **Date format**: `/Date(timestamp)/` — milliseconds since Unix epoch.
- **Data quality**: `GetAllInstitutionsForFilter` may return placeholder entries (e.g. `Title: "/"`); filter or handle as needed.

## Common request filters

*(Add usage notes as refinement discovers them. Deduplicate: document each filter once here if used across multiple operations.)*

- **TypeId** — *(usage)*
- **StatusId** — *(usage)*
- **CommitteeId** — *(usage)*
- **StructureId** — *(usage)*
- **Page / Rows / CurrentPage** — *(usage)*
- **DateFrom / DateTo** — *(usage)*

## Common response keys

*(Add meaning/usage notes as refinement discovers them. Deduplicate globally.)*

- **TotalItems** — *(meaning)*
- **Items** — *(meaning)*
- **d** — *(meaning; ASMX-wrapped responses)*
- **Id / Title** — *(meaning when context-specific)*

---

## GetAllApplicationTypes

### Notes
*(Add filter usage, key meanings, operation-specific notes here.)*


### Request
```json
{
  "methodName": "GetAllApplicationTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "ApplicationTitle": {
        "type": "string"
      }
    }
  }
}
```

## GetAllCommitteesForFilter

### Request
```json
{
  "methodName": "GetAllCommitteesForFilter",
  "languageId": 1,
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string"
      }
    }
  }
}
```

## GetAllCouncils

### Request
```json
{
  "methodName": "GetAllCouncils",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string"
      },
      "TypeId": {
        "type": "integer"
      },
      "TypeTitle": {
        "type": "string"
      }
    }
  }
}
```

## GetAllGenders

### Request
```json
{
  "methodName": "GetAllGenders",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

## GetAllInstitutionsForFilter

### Request
```json
{
  "methodName": "GetAllInstitutionsForFilter",
  "languageId": 1
}
```

### Response
```json
{
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
      }
    }
  }
}
```

## GetAllMPsClubsByStructure

### Request
```json
{
  "MethodName": "GetAllMPsClubsByStructure",
  "LanguageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string"
      }
    }
  }
}
```

## GetAllMaterialStatusesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialStatusesForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/MaterialStatusId"
      },
      "Title": {
        "type": "string"
      }
    },
    "required": ["Id", "Title"]
  }
}
```

## GetAllMaterialTypesForFilter

### Request
```json
{
  "methodName": "GetAllMaterialTypesForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

## GetAllMaterialsForPublicPortal

### Request
```json
{
  "MethodName": "GetAllMaterialsForPublicPortal",
  "LanguageId": 1,
  "ItemsPerPage": 9,
  "CurrentPage": 1,
  "SearchText": "",
  "AuthorText": "",
  "ActNumber": "",
  "StatusGroupId": null,
  "MaterialTypeId": 1,
  "ResponsibleCommitteeId": null,
  "CoReportingCommittees": null,
  "OpinionCommittees": null,
  "RegistrationNumber": null,
  "EUCompatible": null,
  "DateFrom": null,
  "DateTo": null,
  "ProcedureTypeId": null,
  "InitiatorTypeId": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
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
          "TypeTitle": {
            "type": "string"
          },
          "Status": {
            "type": "null"
          },
          "StatusGroupTitle": {
            "type": "string"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "ResponsibleAuthor": {
            "type": "string"
          },
          "Authors": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "type": "string",
                  "format": "uuid"
                },
                "FirstName": {
                  "type": "string"
                },
                "LastName": {
                  "type": "string"
                }
              }
            }
          },
          "ProposerTypeTitle": {
            "type": "string"
          },
          "ResponsibleCommittee": {
            "type": "string"
          },
          "EUCompatible": {
            "type": "boolean"
          },
          "TotalItems": {
            "type": "null"
          }
        }
      }
    }
  }
}
```

## GetAllParliamentaryGroups

### Request
```json
{
  "methodName": "GetAllParliamentaryGroups",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string"
      },
      "NumberOfDeputies": {
        "type": "integer",
        "minimum": 0
      },
      "Image": {
        "type": "string"
      }
    },
    "required": ["Id", "Name", "NumberOfDeputies", "Image"]
  }
}
```

## GetAllPoliticalParties

### Request
```json
{
  "methodName": "GetAllPoliticalParties",
  "languageId": 1,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "Name": {
        "type": "string"
      },
      "NumberOfDeputies": {
        "type": "integer"
      },
      "Image": {
        "type": "string"
      }
    }
  }
}
```

## GetAllProcedureTypes

### Request
```json
{
  "methodName": "GetAllProcedureTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "integer"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

## GetAllQuestionStatuses

### Request
```json
{
  "methodName": "GetAllQuestionStatuses",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/QuestionStatusId"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

## GetAllQuestions

### Request
```json
{
  "methodName": "GetAllQuestions",
  "LanguageId": 1,
  "CurrentPage": 1,
  "Page": 1,
  "Rows": 10,
  "SearchText": "",
  "RegistrationNumber": "",
  "StatusId": null,
  "From": "",
  "To": "",
  "CommitteeId": null,
  "DateFrom": null,
  "DateTo": null,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473"
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
          "From": {
            "type": "string"
          },
          "To": {
            "type": "string"
          },
          "ToInstitution": {
            "type": "string"
          },
          "StatusTitle": {
            "type": "string"
          },
          "DateAsked": {
            "$ref": "#/$defs/AspDate"
          },
          "QuestionTypeTitle": {
            "type": "string"
          },
          "TotalRows": {
            "type": "integer"
          }
        }
      }
    }
  }
}
```

## GetAllSittingStatuses

### Request
```json
{
  "methodName": "GetAllSittingStatuses",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/SittingStatusId"
      },
      "Title": {
        "type": "string"
      }
    }
  }
}
```

## GetAllSittings

### Request
```json
{
  "methodName": "GetAllSittings",
  "Page": 2,
  "Rows": 7,
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
          "SittingTypeId": {
            "$ref": "#/$defs/AgendaItemTypeId"
          },
          "StatusId": {
            "$ref": "#/$defs/SittingStatusId"
          },
          "DateFrom": {
            "$ref": "#/$defs/AspDate"
          },
          "DateTo": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": ["string", "null"]
          },
          "Number": {
            "type": ["integer", "null"]
          },
          "SessionId": {
            "type": ["string", "null"],
            "format": "uuid"
          }
        }
      }
    }
  },
  "required": ["TotalItems", "Items"]
}
```

## GetAllStructuresForFilter

### Request
```json
{
  "methodName": "GetAllStructuresForFilter",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "type": "string",
        "format": "uuid"
      },
      "DateFrom": {
        "$ref": "#/$defs/AspDate"
      },
      "DateTo": {
        "$ref": "#/$defs/AspDate"
      },
      "IsCurrent": {
        "type": "boolean"
      }
    }
  }
}
```

## GetCommitteeDetails

### Request
```json
{
  "methodName": "GetCommitteeDetails",
  "committeeId": "b8b25861-9b5c-4d47-9717-007b83a8a339",
  "languageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string"
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
    },
    "Materials": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
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
            "type": "string"
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          }
        }
      }
    },
    "Description": {
      "type": "string"
    },
    "Email": {
      "type": "string"
    },
    "PhoneNumber": {
      "type": ["string", "null"]
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

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
      "type": "string"
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
    },
    "Materials": {
      "type": "array",
      "items": {}
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
            "type": "string"
          },
          "Date": {
            "$ref": "#/$defs/AspDate"
          },
          "Location": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          }
        }
      }
    },
    "Description": {
      "type": "string",
      "nullable": true
    },
    "Email": {
      "type": "string"
    },
    "PhoneNumber": {
      "type": ["string", "null"]
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

## GetCustomEventsCalendar

### Request
```json
{
  "model": {
    "Language": 1,
    "Month": 1,
    "Year": 2026
  }
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "__type": {
            "type": "string",
            "description": "e.g. moldova.controls.Models.CalendarViewModel"
          },
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "EventDescription": {
            "type": "string"
          },
          "EventLink": {
            "type": "string"
          },
          "EventLocation": {
            "type": "string"
          },
          "EventDate": {
            "$ref": "#/$defs/AspDate"
          },
          "EventType": {
            "type": "integer"
          }
        }
      }
    }
  }
}
```

## GetMPsClubDetails

### Request
```json
{
  "methodName": "GetMPsClubDetails",
  "mpsClubId": "22ded665-2466-4d7e-a04b-03f8a150fc8c",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string"
    },
    "Description": {
      "type": "string"
    },
    "Members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "FirstName": {
            "type": "string"
          },
          "LastName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          }
        }
      }
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

## GetMaterialDetails

### Request
```json
{
  "methodName": "GetMaterialDetails",
  "MaterialId": "759ba4db-41e1-4fdd-9176-21cb7c260522",
  "LanguageId": 1,
  "AmendmentsPage": 1,
  "AmendmentsRows": 5
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string"
    },
    "StatusGroupTitle": {
      "type": "string"
    },
    "TypeTitle": {
      "type": "string"
    },
    "ProposerTypeTitle": {
      "type": "string"
    },
    "ResponsibleAuthor": {
      "type": "string"
    },
    "Institution": {
      "type": "string"
    },
    "ProposerCommittee": {
      "type": "null"
    },
    "ProcedureTypeTitle": {
      "type": "string"
    },
    "RegistrationNumber": {
      "type": "string"
    },
    "RegistrationDate": {
      "$ref": "#/$defs/AspDate"
    },
    "EUCompatible": {
      "type": "boolean"
    },
    "ParentTitle": {
      "type": "string"
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "Name": {
            "type": "string"
          },
          "IsLegislative": {
            "type": "boolean"
          },
          "IsResponsible": {
            "type": "boolean"
          },
          "Documents": {
            "type": "array",
            "items": {}
          }
        }
      }
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
      }
    },
    "FirstReadingAmendments": {
      "type": "array",
      "items": {}
    },
    "SecondReadingAmendments": {
      "type": "array",
      "items": {}
    },
    "FirstReadingSittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeId": {
            "type": ["string", "null"],
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string",
            "nullable": true
          },
          "StatusGroupId": {
            "type": "integer"
          },
          "ObjectStatusId": {
            "type": "integer"
          },
          "SittingTitle": {
            "type": "string"
          },
          "SittingNumber": {
            "type": "integer"
          },
          "VotingResults": {
            "type": "array",
            "items": {}
          }
        }
      }
    },
    "SecondReadingSittings": {
      "type": "array",
      "items": {}
    },
    "ThirdReadingSittings": {
      "type": "array",
      "items": {}
    },
    "Sittings": {
      "type": "array",
      "items": {}
    },
    "Authors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "FirstName": {
            "type": "string"
          },
          "LastName": {
            "type": "string"
          }
        }
      }
    },
    "IsWithdrawn": {
      "type": "boolean"
    },
    "TerminationStatusTitle": {
      "type": "null"
    },
    "TerminationNote": {
      "type": "null"
    },
    "TerminationDate": {
      "type": "null"
    },
    "AmendmentsTotalRows": {
      "type": "integer"
    }
  }
}
```

## GetMonthlyAgenda

### Request
```json
{
  "methodName": "GetMonthlyAgenda",
  "LanguageId": 1,
  "Month": 1,
  "Year": 2026
}
```

### Response
```json
{
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
      "Location": {
        "type": "string"
      },
      "Start": {
        "$ref": "#/$defs/AspDate"
      },
      "Type": {
        "$ref": "#/$defs/AgendaItemTypeId"
      }
    }
  }
}
```

## GetOfficialVisitsForUser

### Request
```json
{
  "model": "914bff80-4c19-4675-ace4-cb0c7a08f688"
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "items": {}
    }
  }
}
```

## GetParliamentMPsNoImage

### Request
```json
{
  "methodName": "GetParliamentMPsNoImage",
  "languageId": 1,
  "genderId": null,
  "ageFrom": null,
  "ageTo": null,
  "politicalPartyId": null,
  "searchText": null,
  "page": 1,
  "rows": 8,
  "StructureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
  "coalition": "",
  "constituency": ""
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "MembersOfParliament": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid"
          },
          "UserImg": {
            "type": "string"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer"
          },
          "PoliticalPartyTitle": {
            "type": "string"
          },
          "PoliticalPartyId": {
            "type": "string",
            "format": "uuid"
          }
        }
      }
    },
    "ExpiredMandateMembers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "UserId": {
            "type": "string",
            "format": "uuid"
          },
          "UserImg": {
            "type": "string"
          },
          "FullName": {
            "type": "string"
          },
          "RoleId": {
            "type": "integer"
          },
          "PoliticalPartyTitle": {
            "type": "string"
          },
          "PoliticalPartyId": {
            "type": "string",
            "format": "uuid"
          }
        }
      }
    },
    "TotalItems": {
      "type": "integer"
    },
    "TotalItemsExpiredMandate": {
      "type": "integer"
    },
    "Statistics": {
      "type": "object",
      "properties": {
        "TotalNumberOfMaterials": {
          "type": "integer"
        },
        "NumberOfQuestions": {
          "type": "integer"
        },
        "TotalNumberOfMPs": {
          "type": "integer"
        },
        "TotalNumberOfExpiredMandateMPs": {
          "type": "integer"
        },
        "MPsInPoliticalParties": {
          "type": "integer"
        },
        "MPsInParliamentaryGroups": {
          "type": "integer"
        },
        "NumberOfMaterialsInStructure": {
          "type": "integer"
        }
      }
    }
  }
}
```

## GetParliamentaryGroupDetails

### Request
```json
{
  "methodName": "GetParliamentaryGroupDetails",
  "parliamentaryGroupId": "6f83cbd1-af39-44e5-bfd0-0cde68932844",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Name": {
      "type": "string"
    },
    "Description": {
      "type": "string"
    },
    "NumberOfDeputies": {
      "type": "integer"
    },
    "Materials": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Amendments": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Questions": {
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
          "DateAsked": {
            "$ref": "#/$defs/AspDate"
          },
          "DateAnswered": {
            "$ref": "#/$defs/AspDate"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Members": {
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          },
          "MaterialsCount": {
            "type": "integer"
          },
          "AmendmentsCount": {
            "type": "integer"
          },
          "QuestionsCount": {
            "type": "integer"
          }
        }
      }
    },
    "Email": {
      "type": "null"
    },
    "Phone": {
      "type": "null"
    },
    "Image": {
      "type": "null"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

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
      "type": "string"
    },
    "Description": {
      "type": "string"
    },
    "NumberOfDeputies": {
      "type": "integer"
    },
    "Materials": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Amendments": {
      "type": "array",
      "items": {}
    },
    "Questions": {
      "type": "array",
      "items": {}
    },
    "Members": {
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
            "type": "integer"
          },
          "RoleTitle": {
            "type": "string"
          },
          "MaterialsCount": {
            "type": "null"
          },
          "AmendmentsCount": {
            "type": "null"
          },
          "QuestionsCount": {
            "type": "null"
          }
        }
      }
    },
    "Email": {
      "type": "null"
    },
    "Phone": {
      "type": "null"
    },
    "Image": {
      "type": "string"
    },
    "StructureId": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

## GetProposerTypes

### Request
```json
{
  "methodName": "GetProposerTypes",
  "languageId": 1
}
```

### Response
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Id": {
        "$ref": "#/$defs/ProposerTypeId"
      },
      "Title": {
        "type": "string"
      },
      "Order": {
        "type": "integer"
      }
    },
    "required": ["Id", "Title", "Order"]
  }
}
```

## GetQuestionDetails

### Request
```json
{
  "methodName": "GetQuestionDetails",
  "QuestionId": "0e2039bb-7a4b-462b-9489-6bce448eeb2a",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "Title": {
      "type": "string"
    },
    "From": {
      "type": "string"
    },
    "To": {
      "type": "string"
    },
    "ToInstitution": {
      "type": "string"
    },
    "QuestionTypeTitle": {
      "type": "string"
    },
    "StatusTitle": {
      "type": "string"
    },
    "NumberOfDeliveryLetter": {
      "type": "null"
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
      }
    },
    "Sittings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "SittingTypeId": {
            "type": "integer"
          },
          "SittingTypeTitle": {
            "type": "string"
          },
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "CommitteeTitle": {
            "type": "null"
          },
          "SittingNumber": {
            "type": "integer"
          }
        }
      }
    }
  }
}
```

## GetSittingDetails

### Response
```json
{
  "type": "object",
  "properties": {
    "StatusId": {
      "type": "integer"
    },
    "StatusTitle": {
      "type": "string"
    },
    "Location": {
      "type": "string"
    },
    "Number": {
      "type": "integer"
    },
    "SittingDate": {
      "$ref": "#/$defs/AspDate"
    },
    "TypeTitle": {
      "type": "string"
    },
    "TypeId": {
      "type": "integer"
    },
    "CommitteeId": {
      "type": "string",
      "format": "uuid"
    },
    "CommitteeTitle": {
      "type": "string"
    },
    "MediaLinks": {
      "type": "array",
      "items": {}
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
      }
    },
    "Agenda": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
        },
        "beforeText": {
          "type": "null"
        },
        "afterText": {
          "type": "null"
        },
        "text": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "treeItemTypeId": {
          "type": "null"
        },
        "agendaItemType": {
          "type": "null"
        },
        "status": {
          "type": "integer"
        },
        "statusTitle": {
          "type": "null"
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
          "type": "null"
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
                "type": "null"
              },
              "afterText": {
                "type": "string"
              },
              "text": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "treeItemTypeId": {
                "type": "null"
              },
              "agendaItemType": {
                "type": "integer"
              },
              "status": {
                "type": "integer"
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
                "type": "string",
                "nullable": true
              },
              "children": {
                "type": "array",
                "items": {}
              },
              "objectId": {
                "type": "string",
                "nullable": true
              },
              "objectTypeId": {
                "type": "integer"
              },
              "objectTypeTitle": {
                "type": "string",
                "nullable": true
              },
              "objectStatusId": {
                "type": "integer"
              },
              "objectSubTypeId": {
                "type": "integer"
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
                }
              }
            }
          }
        },
        "objectId": {
          "type": "null"
        },
        "objectTypeId": {
          "type": "integer"
        },
        "objectTypeTitle": {
          "type": "null"
        },
        "objectStatusId": {
          "type": "integer"
        },
        "objectSubTypeId": {
          "type": "integer"
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
      }
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
            "type": "integer"
          },
          "StatusId": {
            "type": "null"
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
      }
    },
    "SittingDuration": {
      "type": "null"
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
            "type": "string"
          }
        }
      }
    },
    "Attendances": {
      "type": "array",
      "items": {}
    },
    "DescriptionTypeTitle": {
      "type": "string"
    },
    "DescriptionTypeId": {
      "type": "integer"
    },
    "Votings": {
      "type": "array",
      "items": {}
    },
    "Structure": {
      "type": "string"
    }
  }
}
```

## GetUserDetailsByStructure

### Request
```json
{
  "methodName": "GetUserDetailsByStructure",
  "userId": "85048fa9-e61b-4eb1-be26-8d537cb1d7c4",
  "structureId": "5e00dbd6-ca3c-4d97-b748-f792b2fa3473",
  "languageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "FullName": {
      "type": "string"
    },
    "Email": {
      "type": "string"
    },
    "Image": {
      "type": "string"
    },
    "MobileNumber": {
      "type": "null"
    },
    "PhoneNumber": {
      "type": "null"
    },
    "Biography": {
      "type": "string"
    },
    "RoleId": {
      "type": "integer"
    },
    "RoleTitle": {
      "type": "string"
    },
    "ElectedFrom": {
      "$ref": "#/$defs/AspDate"
    },
    "ElectedTo": {
      "type": "null"
    },
    "PoliticalPartyId": {
      "type": "string",
      "format": "uuid"
    },
    "PoliticalPartyTitle": {
      "type": "string"
    },
    "Gender": {
      "type": "string"
    },
    "DateOfBirth": {
      "type": "string"
    },
    "Constituency": {
      "type": "string"
    },
    "Coalition": {
      "type": "string"
    },
    "StructureDate": {
      "type": "string"
    },
    "CabinetMembers": {
      "type": "array",
      "items": {}
    },
    "Materials": {
      "type": "array",
      "items": {}
    },
    "Questions": {
      "type": "array",
      "items": {}
    },
    "Delegations": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroups": {
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
          "Description": {
            "type": "string"
          }
        }
      }
    },
    "Amendments": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Acts": {
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
          "RegistrationDate": {
            "$ref": "#/$defs/AspDate"
          },
          "RegistrationNumber": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          }
        }
      }
    },
    "Committees": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "CommitteeId": {
            "type": "string",
            "format": "uuid"
          },
          "CommitteeTitle": {
            "type": "string"
          },
          "Roles": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Id": {
                  "type": "integer"
                },
                "Title": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    },
    "CommitteeMemberships": {
      "type": "array",
      "items": {}
    },
    "DelegationMemberships": {
      "type": "array",
      "items": {}
    },
    "DepartmentMemberships": {
      "type": "array",
      "items": {}
    },
    "FriendshipGroupMemberships": {
      "type": "array",
      "items": {}
    },
    "MediaItems": {
      "type": "array",
      "items": {}
    }
  }
}
```

## LoadLanguage

### Request
POST to `Infrastructure/LoadLanguage`, empty body or minimal params.

### Response
```json
{
  "type": "object",
  "properties": {
    "Code": {
      "type": "string",
      "description": "Language/locale code (e.g. mk-MK)"
    },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Key": {
            "type": "string",
            "description": "Localization key"
          },
          "Value": {
            "type": "string",
            "description": "Localized text"
          }
        },
        "required": ["Key", "Value"]
      }
    }
  },
  "required": ["Code", "Items"]
}
```
