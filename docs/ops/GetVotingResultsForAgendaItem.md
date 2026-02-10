## GetVotingResultsForAgendaItem

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "MethodName": { "type": "string", "const": "GetVotingResultsForAgendaItem" },
    "LanguageId": { "$ref": "#/$defs/LanguageId" },
    "VotingDefinitionId": { "$ref": "#/$defs/UUID", "description": "From GetSittingDetails agenda VotingDefinitions" },
    "AgendaItemId": { "$ref": "#/$defs/UUID", "description": "Agenda item id from GetSittingDetails agenda" }
  },
  "required": ["MethodName", "LanguageId", "VotingDefinitionId", "AgendaItemId"]
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "votingOptions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID", "description": "Voting option identifier" },
          "VotingDefinitionId": { "$ref": "#/$defs/UUID" },
          "Title": { "type": "string", "description": "Localized option title (e.g. 'За'=For, 'Против'=Against, 'Не гласал'=Did not vote, 'Воздржан'=Abstain)" },
          "Order": { "type": "integer" }
        }
      }
    },
    "agendaItem": {
      "type": "object",
      "properties": {
        "Id": { "$ref": "#/$defs/UUID" },
        "Title": { "type": "string" },
        "AgendaItemType": { "type": "string", "description": "Localized material type title (e.g. 'Избори, именување и разрешување на јавни и други функции'); not a numeric ID" },
        "SittingDate": { "$ref": "#/$defs/AspDate" },
        "Number": { "type": "integer", "description": "Sitting number" },
        "Continuation": { "type": "integer", "description": "Continuation count" },
        "RegistrationNumber": { "type": "string" },
        "VotingTitle": { "type": "string" }
      }
    },
    "summaryResult": {
      "type": "object",
      "properties": {
        "Present": { "type": "integer", "description": "MPs present" },
        "Yes": { "type": "integer", "description": "Votes for" },
        "No": { "type": "integer", "description": "Votes against" },
        "NotVoted": { "type": "integer", "description": "MPs not voted" },
        "VotingType": { "type": "string", "description": "Voting type (e.g. 'Јавно'=Public)" },
        "VotingOutcome": { "type": "string", "description": "Voting outcome (e.g. 'Усвоен'=Adopted)" }
      }
    },
    "votingResultsByUser": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID", "description": "MP user ID" },
          "FirstName": { "type": "string" },
          "LastName": { "type": "string" },
          "PoliticalParty": { "type": ["string", "null"] },
          "PoliticalPartyImage": { "type": ["string", "null"], "description": "Empty string or null if no party" },
          "PoliticalPartyId": { "$ref": "#/$defs/UUID", "description": "All-zeros UUID if independent" },
          "Registered": { "type": "boolean" },
          "Present": { "type": "boolean" },
          "Yes": { "type": "boolean" },
          "No": { "type": "boolean" },
          "NotVoted": { "type": "boolean" }
        }
      }
    },
    "votingResultsByFaction": {
      "type": "array",
      "items": { "type": "object" },
      "description": "Voting results aggregated by faction/political group (may be empty)"
    }
  }
}
```

### Notes
- Method-based (MakePostRequest). Voting results for a specific agenda item; IDs from GetSittingDetails agenda.
- `votingOptions` array contains all voting choices available for the vote (e.g. For, Against, Did not vote, Abstain); values vary by voting definition.
- `agendaItem.AgendaItemType` is a localized text string (not a numeric ID), containing the material type title as displayed in the parliament system.
- `summaryResult.VotingType` describes the voting mechanism (e.g. 'Јавно' = public/open voting).
- `summaryResult.VotingOutcome` contains the final outcome (e.g. 'Усвоен' = adopted).
- `votingResultsByUser` contains individual MP voting records; `PoliticalParty`, `PoliticalPartyImage`, and `PoliticalPartyId` are `null` or all-zeros UUID for independent MPs.
- `PoliticalPartyImage` may be empty string even when party is present.