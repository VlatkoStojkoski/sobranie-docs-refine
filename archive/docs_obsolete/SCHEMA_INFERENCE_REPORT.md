# Schema Inference Report

Run: 2026-02-08_00-06-14. Append-only merge with prior schema.

## GetAllApplicationTypes

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 6, OK: 6

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 1, OK: 1

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

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 1, OK: 1

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

Samples: 5, OK: 5

```json
{
  "type": "object",
  "properties": {
    "TotalItems": {
      "type": "integer"
    },
    "Items": {
      "type": "array",
      "items": {}
    }
  }
}
```

## GetAllStructuresForFilter

Samples: 1, OK: 1

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
        "type": "string",
        "format": "asp-date",
        "pattern": "^/Date\\(\\d+\\)/$"
      },
      "DateTo": {
        "type": "string",
        "format": "asp-date",
        "pattern": "^/Date\\(\\d+\\)/$"
      },
      "IsCurrent": {
        "type": "boolean"
      }
    }
  }
}
```

## GetCommitteeDetails

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 1, OK: 1

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 2, OK: 2

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

Samples: 3, OK: 3

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
      "type": "string",
      "format": "asp-date",
      "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 2, OK: 2

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
        "type": "string",
        "format": "asp-date",
        "pattern": "^/Date\\(\\d+\\)/$"
      },
      "Type": {
        "type": "integer"
      }
    }
  }
}
```

## GetOfficialVisitsForUser

Samples: 1, OK: 1

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

Samples: 3, OK: 3

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

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
          },
          "DateAnswered": {
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 1, OK: 1

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

Samples: 3, OK: 3

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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 4, OK: 4

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
      "type": "string",
      "format": "asp-date",
      "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 2, OK: 2

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
      "type": "string",
      "format": "asp-date",
      "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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
            "type": "string",
            "format": "asp-date",
            "pattern": "^/Date\\(\\d+\\)/$"
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

Samples: 1, OK: 1

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

