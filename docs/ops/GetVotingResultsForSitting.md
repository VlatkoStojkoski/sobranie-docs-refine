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
    "votingOptions": { "type": "array", "items": { "type": "object" } },
    "sittingItem": { "type": "object" },
    "summaryResult": { "type": "object" },
    "votingResultsByUser": { "type": "array", "items": { "type": "object" } }
  }
}
```

### Notes
- Method-based (MakePostRequest). Voting results for a sitting-level vote; votingDefinitionId and sittingId from GetSittingDetails.
- Refine from collected pairs to complete request/response schema and notes.
