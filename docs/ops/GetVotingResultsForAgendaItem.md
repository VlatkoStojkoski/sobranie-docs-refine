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
    "votingOptions": { "type": "array", "items": { "type": "object" } },
    "agendaItem": { "type": "object" },
    "summaryResult": { "type": "object" },
    "votingResultsByUser": { "type": "array", "items": { "type": "object" } }
  }
}
```

### Notes
- Method-based (MakePostRequest). Voting results for a specific agenda item; IDs from GetSittingDetails agenda.
- Refine from collected pairs to complete request/response schema and notes.
