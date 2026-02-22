# Meta WhatsApp Business API — Integration Guide

## Overview

Chasqui connects to the **Meta WhatsApp Business Cloud API** to send and receive messages. This document covers the full setup path and technical details.

## Setup Phases

### Phase 1: The Phone Number (Clean SIM)

Meta requires a phone number that has **never been registered** with WhatsApp or WhatsApp Business apps.

- Buy a fresh prepaid SIM (Antel, Claro, or Movistar in Uruguay).
- Place it in a secondary phone or dual-SIM device — only for receiving SMS.
- **Do NOT install WhatsApp or WhatsApp Business on that phone.** The number must be completely "virgin" at the application level.

### Phase 2: Local Backend + Tunnel

Meta needs a public HTTPS URL to validate the server and deliver messages.

1. Run the FastAPI server locally on port 8000:
   ```bash
   uvicorn src.chasqui.main:app --reload --port 8000
   ```
2. Expose it via ngrok (or Cloudflare Tunnels):
   ```bash
   ngrok http 8000
   ```
3. Copy the public URL (e.g. `https://abcd-123.ngrok-free.app`) — this is the webhook base.

### Phase 3: Meta for Developers & Business Manager

1. Go to [developers.facebook.com](https://developers.facebook.com) → **Create App**.
2. Choose type: **Others** → **Business**.
3. Name the app (e.g. "Torke App").
4. In the app dashboard, find the **WhatsApp** product and click **Set up**.
5. Meta will ask to select a Business Manager account. Create a new one with the project name and your email. This puts you in **Unverified Business** state (sufficient for development, 250 conversations/day).

### Phase 4: Link the Phone Number + Webhook

1. In Meta's left sidebar: **WhatsApp → API Configuration**.
2. Scroll down → **Add phone number**.
3. Enter a display name (what workshops will see) and select a category.
4. Enter the prepaid SIM number. Meta sends a 6-digit SMS — enter it to verify.
5. Go to **Configuration** tab (under WhatsApp) to set up the webhook:
   - **Callback URL**: `https://<your-ngrok-url>/webhook/whatsapp`
   - **Verify token**: Must match `WHATSAPP_VERIFY_TOKEN` in your `.env` (default: `torke_super_secret_token_2026`)
6. Click **Verify and save**. Meta sends a GET to the endpoint; if it responds correctly, the webhook is linked.
7. Click **Manage webhook fields** → subscribe to the `messages` event.

### Phase 5: First Test Message

1. In **API Configuration**, Meta shows:
   - **Phone Number ID** (the one assigned to your SIM)
   - **Temporary access token** (lasts 24 hours)
2. Put both in your `.env` file.
3. Use the `WhatsAppClient` to send a test:
   ```python
   from chasqui.services.whatsapp import WhatsAppClient
   client = WhatsAppClient()
   await client.send_text_message("59899XXXXXX", "Hola desde Torke!")
   ```
4. The message arrives on the recipient's WhatsApp. If they reply, you'll see the JSON payload in your FastAPI terminal.

## Webhook Technical Details

### Verification (GET /webhook/whatsapp)

Meta sends:
| Query Param | Value |
|---|---|
| `hub.mode` | `subscribe` |
| `hub.verify_token` | Your secret token |
| `hub.challenge` | Random string to echo back |

The server must validate the token and return `hub.challenge` as **plain text** with status 200.

### Incoming Messages (POST /webhook/whatsapp)

Meta sends a nested JSON payload:
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "BIZ_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "59899000000",
          "phone_number_id": "123456789"
        },
        "messages": [{
          "from": "59899111111",
          "id": "wamid.abc123",
          "timestamp": "1709000000",
          "type": "text",
          "text": {"body": "Hola, quiero agendar"}
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## Message Types

| Type | Can Initiate? | Use Case |
|---|---|---|
| **Template** | Yes | Pre-approved messages (appointment reminders, report delivery). Require Meta approval. |
| **Text** | No (24h window) | Free-form replies within an active conversation. |
| **Document** | No (24h window) | Sending PDFs (vehicle reports) within an active conversation. |
| **Media** | No (24h window) | Images, video, audio within an active conversation. |

To start a conversation with a user who hasn't messaged first, you **must** use a template message.

## API Limits (Unverified Business)

- **250 business-initiated conversations per 24-hour rolling window**.
- No cost for these conversations during the test/development phase.
- To increase limits: complete Meta Business Verification (requires fiscal/legal documents).

## Permanent Access Token

The temporary token from the dashboard expires in 24 hours. For production:
1. Go to **Business Settings → System Users** in Meta Business Manager.
2. Create a System User with admin role.
3. Generate a permanent token with `whatsapp_business_messaging` permission.
4. Replace the temporary token in `.env`.
