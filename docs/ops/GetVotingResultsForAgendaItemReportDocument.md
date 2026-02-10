## GetVotingResultsForAgendaItemReportDocument

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "MethodName": { "type": "string", "const": "GetVotingResultsForAgendaItemReportDocument" },
    "LanguageId": { "$ref": "#/$defs/LanguageId" },
    "VotingDefinitionId": { "$ref": "#/$defs/UUID" },
    "AgendaItemId": { "$ref": "#/$defs/UUID" }
  },
  "required": ["MethodName", "LanguageId", "VotingDefinitionId", "AgendaItemId"]
}
```

### Response Schema
```json
{
  "type": "array",
  "items": { "type": "integer" },
  "description": "Document bytes (e.g. PDF); array of byte values"
}
```

### Notes
- Method-based (MakePostRequest). Returns a report document (e.g. PDF) as array of bytes for the given voting/agenda item.
- Refine from collected pairs to confirm response shape and notes.
