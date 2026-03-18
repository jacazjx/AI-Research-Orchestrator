# Integration Guide

This guide covers how to integrate AI Research Orchestrator with external tools and services.

## Codex MCP Setup

Codex MCP enables cross-model review using OpenAI models. To set up:

1. Install the Codex MCP server:
   ```bash
   npm install -g @openai/codex-mcp-server
   ```

2. Add to your MCP configuration (`~/.claude/mcp.json`):
   ```json
   {
     "mcpServers": {
       "codex": {
         "command": "codex-mcp-server",
         "args": ["--config", "~/.codex/config.json"]
       }
     }
   }
   ```

3. Configure your OpenAI API key in `~/.codex/config.json`

See the [Codex MCP documentation](https://github.com/openai/codex-mcp) for more details.

## Feishu Notifications

The `feishu-notify` skill can send notifications to Feishu/Lark:

1. Create a Feishu bot and obtain webhook URL
2. Configure in `~/.autoresearch/user-config.yaml`:
   ```yaml
   notifications:
     feishu_webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
   ```

3. Invoke the skill:
   ```
   /airesearchorchestrator:feishu-notify "实验完成"
   ```

## GPU Server Registration

Register GPU servers for running experiments:

1. Edit `~/.autoresearch/gpu-registry.yaml`:
   ```yaml
   devices:
     - id: "gpu-01"
       name: "RTX 4090"
       host: "192.168.1.100"
       ssh_key: "~/.ssh/id_rsa"
       memory: "24GB"
     - id: "gpu-02"
       name: "A100"
       host: "10.0.0.50"
       ssh_key: "~/.ssh/cluster_key"
       memory: "80GB"
   ```

2. Test connection:
   ```bash
   python scripts/gpu_manager.py --test gpu-01
   ```

## Zotero Integration

For paper management with Zotero:

1. Install Better BibTeX plugin in Zotero
2. Enable Zotero API in preferences
3. Configure in project `orchestrator-config.yaml`:
   ```yaml
   zotero:
     library_id: "YOUR_LIBRARY_ID"
     api_key: "YOUR_API_KEY"
   ```

## External Review Services

The orchestrator supports external review via:
- **Codex MCP**: Cross-model review using GPT models
- **Custom endpoints**: Configure in `orchestrator-config.yaml`

See `references/orchestrator-protocol.md` for communication protocols.
