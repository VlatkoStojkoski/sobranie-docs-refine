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
            "type": "string",
            "description": "Human-readable title/description of the event in the requested language"
          },
          "EventLink": {
            "type": "string",
            "description": "URL-friendly slug for event detail page"
          },
          "EventLocation": {
            "anyOf": [
              {"type": "string"},
              {"const": ""}
            ],
            "description": "Physical location of event. May be empty string when location is not specified or not applicable"
          },
          "EventDate": {
            "$ref": "#/$defs/AspDate"
          },
          "EventType": {
            "$ref": "#/$defs/EventTypeId"
          }
        },
        "required": ["__type", "Id", "EventDescription", "EventLink", "EventLocation", "EventDate", "EventType"]
      }
    }
  },
  "required": ["d"]
}
```

### Request Filters
- **Language** — LanguageId (1=Macedonian, 2=Albanian, 3=Turkish). Controls language of EventDescription and EventLocation.
- **Month** — Integer 1-12 for the calendar month to retrieve.
- **Year** — Four-digit year (e.g., 2024, 2026) to retrieve events for.

### Notes
- Returns all calendar events for the specified month and year. Response is an array in the `d` property (ASMX wrapper).
- All events in the sample data have `EventType: 5`, corresponding to press conferences, official visits, working sessions, commemorations, and public events. Other EventType values may exist but are not yet documented.
- `EventLocation` can be empty string (`""`) when location is not specified or not applicable to the event type.
- `EventLink` provides URL-safe slugs suitable for constructing event detail page URLs.
- Response may be empty array `[]` if no events exist for the requested month/year.
- `EventDescription` is localized based on the `Language` parameter; same event may return different language text with different Language values.
