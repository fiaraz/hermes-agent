# WhatsApp Bridge API

The WhatsApp bridge runs as a Node.js process on port 3000. It uses Baileys (WhatsApp Web protocol) and exposes HTTP endpoints.

## Base URL

```
http://127.0.0.1:3000
```

## Endpoints

### Send a message
```
POST /send
Content-Type: application/json

{
  "chatId": "34608929209@c.us",   // international format + @c.us
  "message": "Hello from Oracle"
}
```

Returns: `{"success": true, "messageId": "..."}`

### Read incoming messages (long-poll)
```
GET /messages?timeout=30
```

Returns array of new messages. Blocks for up to `timeout` seconds waiting for messages. Returns `[]` if no messages arrive.

### Get chat info
```
GET /chat/:id
```

Returns `{"name": "...", "isGroup": false, "participants": []}`

### Send media
```
POST /send-media
Content-Type: application/json

{
  "chatId": "34608929209@c.us",
  "filePath": "/path/to/file.pdf",
  "mediaType": "document",    // "document", "image", "audio", "video"
  "caption": "Optional caption",
  "fileName": "report.pdf"
}
```

### Health check
```
GET /health
```

## Chat ID format

- Individual: `{number}@c.us` (e.g. `34608929209@c.us` for +34 608 92 92 09)
- Group: `{group-id}@g.us`

Numbers should be in international format without the `+` prefix.

## Usage from Python

```python
import json, urllib.request

data = json.dumps({"chatId": "34608929209@c.us", "message": "Hello"}).encode()
req = urllib.request.Request("http://127.0.0.1:3000/send", data=data,
    headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
```

## Notes

- The bridge only streams NEW messages via long-poll -- historical messages are not stored.
- The bridge must be running (started via `hermes gateway run` or manually).
- Session data lives in `~/.hermes/whatsapp/session/`.