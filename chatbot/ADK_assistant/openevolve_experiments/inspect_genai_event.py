try:
    from google.genai import types
    print("google.genai.types found")
    print("types.Content:", types.Content)
except ImportError:
    print("google.genai.types NOT found")

from google.adk.events import Event
print("Event fields:", Event.model_fields.keys())
