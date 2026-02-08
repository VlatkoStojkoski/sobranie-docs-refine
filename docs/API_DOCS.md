# API Schemas

Precise request and response schemas for all operations. From collected responses.

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
  }
}
```

## GetAllApplicationTypes

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
        "type": "integer"
      },
      "Title": {
        "type": "string"
      }
    }
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
  "ItemsPerPage": 5,
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
        "type": "integer"
      },
      "Image": {
        "type": "string"
      }
    }
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
        "type": "integer"
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
  "Rows": 5,
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
        "type": "integer"
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
  "Page": 1,
  "Rows": 5,
  "LanguageId": 1,
  "TypeId": 1,
  "CommitteeId": null,
  "StatusId": 3,
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
          "SittingDate": {
            "$ref": "#/$defs/AspDate"
          },
          "TypeId": {
            "type": "integer"
          },
          "TypeTitle": {
            "type": "string"
          },
          "StatusId": {
            "type": "integer"
          },
          "StatusTitle": {
            "type": "string"
          },
          "Location": {
            "type": "string"
          },
          "CommitteeTitle": {
            "type": "null"
          },
          "SittingDescriptionTypeTitle": {
            "type": "null"
          },
          "Continuations": {
            "type": "array",
            "items": {}
          },
          "Structure": {
            "type": "null"
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
      "type": "null"
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
      "type": "null"
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
            "type": "string",
            "nullable": true
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
        "type": "integer"
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
  "rows": 5,
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
            "type": "string"
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
        "type": "integer"
      },
      "Title": {
        "type": "string"
      },
      "Order": {
        "type": "integer"
      }
    }
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

### Request
```json
{
  "MethodName": "GetSittingDetails",
  "SittingId": "f06b995b-c5c7-42cd-8605-ec2d9ab7aac1",
  "LanguageId": 1
}
```

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
      "type": "null"
    },
    "CommitteeTitle": {
      "type": "null"
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
                    },
                    "VotingType": {
                      "type": "string"
                    },
                    "OverallResult": {
                      "type": "string"
                    }
                  }
                }
              },
              "Documents": {
                "type": "array",
                "items": {}
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
    "DescriptionTypeTitle": {
      "type": "null"
    },
    "DescriptionTypeId": {
      "type": "null"
    },
    "Votings": {
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
          },
          "VotingType": {
            "type": "string"
          },
          "OverallResult": {
            "type": "string"
          }
        }
      }
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

## GetVotingResultsForAgendaItem

### Request
```json
{
  "methodName": "GetVotingResultsForAgendaItem",
  "VotingDefinitionId": "80025712-a092-4e4d-8983-e146896368ae",
  "AgendaItemId": "ccaf7830-3164-46f6-95a3-60816538344d",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {}
}
```

## GetVotingResultsForAgendaItemReportDocument

### Request
```json
{
  "methodName": "GetVotingResultsForAgendaItemReportDocument",
  "VotingDefinitionId": "80025712-a092-4e4d-8983-e146896368ae",
  "AgendaItemId": "ccaf7830-3164-46f6-95a3-60816538344d",
  "LanguageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {}
}
```

## GetVotingResultsForSitting

### Request
```json
{
  "methodName": "GetVotingResultsForSitting",
  "votingDefinitionId": "80025712-a092-4e4d-8983-e146896368ae",
  "sittingId": "f06b995b-c5c7-42cd-8605-ec2d9ab7aac1",
  "languageId": 1
}
```

### Response
```json
{
  "type": "object",
  "properties": {
    "votingOptions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": {
            "type": "string",
            "format": "uuid"
          },
          "VotingDefinitionId": {
            "type": "string",
            "format": "uuid"
          },
          "Title": {
            "type": "string"
          },
          "Order": {
            "type": "integer"
          }
        }
      }
    },
    "sittingItem": {
      "type": "object",
      "properties": {
        "Id": {
          "type": "string",
          "format": "uuid"
        },
        "Number": {
          "type": "integer"
        },
        "Continuation": {
          "type": "integer"
        },
        "Title": {
          "type": "string"
        },
        "SittingDate": {
          "$ref": "#/$defs/AspDate"
        },
        "AgendaItemType": {
          "type": "string"
        }
      }
    },
    "summaryResult": {
      "type": "object",
      "properties": {
        "Present": {
          "type": "integer"
        },
        "Yes": {
          "type": "integer"
        },
        "No": {
          "type": "integer"
        },
        "NotVoted": {
          "type": "integer"
        },
        "VotingType": {
          "type": "string"
        },
        "VotingOutcome": {
          "type": "string"
        }
      }
    },
    "votingResultsByUser": {
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
          "PoliticalParty": {
            "type": "string"
          },
          "PoliticalPartyImage": {
            "type": "string"
          },
          "PoliticalPartyId": {
            "type": "string",
            "format": "uuid"
          },
          "Registered": {
            "type": "boolean"
          },
          "Present": {
            "type": "boolean"
          },
          "Yes": {
            "type": "boolean"
          },
          "No": {
            "type": "boolean"
          },
          "NotVoted": {
            "type": "boolean"
          }
        }
      }
    },
    "votingResultsByFaction": {
      "type": "array",
      "items": {}
    }
  }
}
```

## LoadLanguage

### Response
```json
{
  "type": "object",
  "properties": {
    "Code": {
      "type": "string"
    },
    "Items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Key": {
            "type": "string"
          },
          "Value": {
            "type": "string"
          }
        }
      }
    }
  }
}
```
