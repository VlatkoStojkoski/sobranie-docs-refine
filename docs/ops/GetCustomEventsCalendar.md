## GetCustomEventsCalendar

### Request Schema
```json
{
  "type": "object",
  "properties": {
    "model": {
      "type": "object",
      "properties": {
        "Language": {
          "$ref": "#/$defs/LanguageId",
          "description": "Language for event descriptions and locations (1=Macedonian, 2=Albanian, 3=Turkish)"
        },
        "Month": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12,
          "description": "Month (1–12)"
        },
        "Year": {
          "type": "integer",
          "description": "Four-digit year (e.g., 2024, 2026)"
        }
      },
      "required": ["Language", "Month", "Year"]
    }
  },
  "required": ["model"]
}
```

### Response Schema
```json
{
  "type": "object",
  "properties": {
    "d": {
      "type": "array",
      "description": "Array of calendar events for the requested month/year. May include truncation marker {\"{\\\"_truncated\\\": N}\" as standalone object within array, counting toward array length and indicating N additional items omitted.",
      "items": {
        "anyOf": [
          {
            "type": "object",
            "properties": {
              "__type": {
                "type": "string",
                "description": "ASMX type discriminator (e.g., 'moldova.controls.Models.CalendarViewModel')"
              },
              "Id": {
                "$ref": "#/$defs/UUID",
                "description": "Unique event identifier"
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
                "description": "Physical location/venue of event. May be empty string when location not specified or not applicable to event type"
              },
              "EventDate": {
                "$ref": "#/$defs/AspDate",
                "description": "Scheduled date/time of the event in AspDate format"
              },
              "EventType": {
                "$ref": "#/$defs/EventTypeId",
                "description": "Type of event (currently 5=press conference/visit/working session/commemoration/public event)"
              }
            },
            "required": ["__type", "Id", "EventDescription", "EventLink", "EventLocation", "EventDate", "EventType"]
          },
          {
            "type": "object",
            "properties": {
              "_truncated": {
                "type": "integer",
                "description": "Truncation marker indicating N additional items omitted from the array"
              }
            },
            "required": ["_truncated"]
          }
        ]
      }
    }
  },
  "required": ["d"]
}
```

### Notes
- **ASMX response format:** Endpoint uses ASMX wrapper; results are returned in the `d` property directly as an array (not wrapped in `Items`/`TotalItems` pagination).
- **Empty results:** Returns empty array `[]` if no events exist for the requested month/year.
- **Array truncation:** The `d` array may include a truncation marker `{"_truncated": N}` as a standalone object within the array, counting toward array length and indicating N additional items omitted. Clients should handle this marker by checking for the presence of the `_truncated` key and adjusting pagination or display logic accordingly.
- **Language localization:** `EventDescription` and `EventLocation` are localized based on the `Language` parameter (1=Macedonian, 2=Albanian, 3=Turkish). The same event returns different language text when queried with different `Language` values.
- **Event location handling:** `EventLocation` may be empty string when location is not specified or not applicable to the event type.
- **Event types:** All documented sample events have `EventType: 5` (press conferences, official visits, working sessions, commemorations, public events). Other EventType values may exist but are not yet documented.
- **Event links:** `EventLink` provides URL-safe slugs suitable for constructing event detail page URLs.
- **Endpoint:** Non-standard ASMX endpoint at `https://www.sobranie.mk/Moldova/services/CalendarService.asmx/GetCustomEventsCalendar`; POST with `model` wrapper in request body.