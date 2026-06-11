---
name: oracle-knowledge-base
description: "sqlite-vec vector database + web UI at oracle.shunka.org/kb/. Add web pages, files, search web, RAG answers."
created_by: "agent"
---

# Oracle Knowledge Base

## Location

- **Web UI**: https://oracle.shunka.org/kb/
- **CLI**: `kb` (symlinked to `~/oracle-kb/kb.py`)
- **Library**: `~/oracle-kb/kb_lib.py` (importable from FastAPI or agent)
- **DB files**: `~/oracle-kb/dbs/<name>.db`
- **API key**: from `~/.hermes/.env` (OPENROUTER_API_KEY)

## Stack

- **Storage**: sqlite-vec (each KB = one .db file on disk)
- **Embeddings**: OpenRouter API (`text-embedding-3-small`, 1536 dims) -- zero local RAM
- **Backend**: FastAPI (uvicorn) on port 8010, systemd service `oracle-kb.service`
- **Frontend**: Plain HTML/JS, no framework, served via Nginx at /kb/
- **Web search**: Tavily API (already configured)
- **RAG**: OpenRouter `openai/gpt-4o-mini` for answer generation

## Systemd

```
sudo systemctl status oracle-kb.service
sudo systemctl restart oracle-kb.service
sudo journalctl -u oracle-kb.service -f
```

## Web UI Tabs

| Tab | What it does |
|-----|-------------|
| **Ask** | Type a question, get RAG answer + source snippets from a KB |
| **Add Web** | Paste a URL, fetch content, ingest into a KB |
| **Upload** | Drag/drop .txt or .pdf, extract content, add to KB |
| **Search Web** | Google search via Tavily, preview results, click "+ KB" to add any result |

## CLI commands

```
kb new <name>                    # Create KB
kb list                          # List all KBs
kb add-web <name> <url>          # Ingest a web page
kb add-text <name> <title> <text> # Add raw text
kb query <name> "question" -k 5  # Semantic search
kb ask <name> "question" -k 5    # RAG question + answer
kb drop <name>                   # Delete a KB
kb import-exams <name>           # Seed with 48 exam records
```

## RAM usage

- **~34MB** for FastAPI/uvicorn (systemd service, always on)
- **~2MB** per active database connection
- **Zero** persistent RAM for embedding model (all API calls)

## Reference files

- `references/whatsapp-bridge-api.md` -- WhatsApp bridge HTTP API (send messages to specific numbers, read incoming messages, chat info)