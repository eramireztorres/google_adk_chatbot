import google.adk
import google.adk.agents
try:
    import google.adk.types
    print("google.adk.types found")
except ImportError:
    print("google.adk.types NOT found")

print("google.adk.agents contents:", dir(google.adk.agents))
