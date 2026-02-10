## GetVotingResultsForSitting

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "MethodName": { "type": "string", "const": "GetVotingResultsForSitting" },
    "languageId": { "$ref": "#/$defs/LanguageId" },
    "votingDefinitionId": { "$ref": "#/$defs/UUID" },
    "sittingId": { "$ref": "#/$defs/UUID" }
  },
  "required": ["MethodName", "languageId", "votingDefinitionId", "sittingId"]
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
          "Id": { "$ref": "#/$defs/UUID" },
          "VotingDefinitionId": { "$ref": "#/$defs/UUID" },
          "Title": { "type": "string", "description": "Vote option title (e.g., 'За'=For, 'Не гласал'=Did not vote); localized" },
          "Order": { "type": "integer" }
        }
      },
      "description": "Available vote options for this voting definition"
    },
    "sittingItem": {
      "type": "object",
      "properties": {
        "Id": { "$ref": "#/$defs/UUID" },
        "Number": { "type": "integer" },
        "Continuation": { "anyOf": [{ "type": "string" }, { "type": "null" }], "description": "Continuation marker or null" },
        "Title": { "type": "string" },
        "SittingDate": { "$ref": "#/$defs/AspDate" },
        "AgendaItemType": { "type": "string", "description": "Agenda item type text (e.g., 'Гласање на седница'=Voting at sitting); localized" }
      },
      "description": "Sitting context for the voting"
    },
    "summaryResult": {
      "type": "object",
      "properties": {
        "Present": { "type": "integer", "description": "Count of MPs present" },
        "Yes": { "type": "integer", "description": "Count of Yes votes" },
        "No": { "type": "integer", "description": "Count of No votes" },
        "NotVoted": { "type": "integer", "description": "Count of MPs who did not vote" },
        "VotingType": { "type": "string", "description": "Voting type (e.g., 'Јавно'=Public voting)" },
        "VotingOutcome": { "$ref": "#/$defs/VotingOutcomeId", "description": "Voting outcome/result" }
      },
      "description": "Aggregate voting summary"
    },
    "votingResultsByUser": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Id": { "$ref": "#/$defs/UUID" },
          "FirstName": { "type": "string" },
          "LastName": { "type": "string" },
          "PoliticalParty": { "anyOf": [{ "type": "string" }, { "type": "null" }], "description": "Party name or null for independents" },
          "PoliticalPartyImage": { "anyOf": [{ "type": "string" }, { "type": "null" }], "description": "Party logo URL or empty string; null for independents" },
          "PoliticalPartyId": { "$ref": "#/$defs/UUID", "description": "Party UUID or null-UUID (00000000-0000-0000-0000-000000000000) for MPs without party" },
          "Registered": { "type": "boolean" },
          "Present": { "type": "boolean" },
          "Yes": { "type": "boolean" },
          "No": { "type": "boolean" },
          "NotVoted": { "type": "boolean" }
        },
        "description": "Per-MP voting detail"
      },
      "description": "Voting results by individual MP"
    },
    "votingResultsByFaction": {
      "type": "array",
      "items": { "type": "object" },
      "description": "Voting results aggregated by faction (observed empty)"
    }
  }
}
```

### Notes
- Method-based (MakePostRequest). Voting results for a sitting-level vote; votingDefinitionId and sittingId from GetSittingDetails.
- Response includes per-MP voting breakdown with political party affiliation and boolean flags for Registered/Present/Yes/No/NotVoted.
- summaryResult aggregates counts and voting outcome (e.g., 'Усвоен'=Adopted).
- votingOptions shows available vote option titles (e.g., 'За', 'Не гласал'), localized per languageId.
- sittingItem.AgendaItemType is localized text string, distinct from the integer AgendaItemTypeId enum in global defs.
- PoliticalPartyId is null-UUID (00000000-0000-0000-0000-000000000000) or null for MPs without party affiliation; PoliticalParty and PoliticalPartyImage are also null in such cases.