from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Chasqui — WhatsApp Notifications API</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #0d1117;
      --surface:   #161b22;
      --border:    #30363d;
      --green:     #25d366;
      --green-dim: #1a9648;
      --text:      #e6edf3;
      --muted:     #8b949e;
      --red:       #f85149;
      --blue:      #58a6ff;
      --yellow:    #d29922;
      --badge-get:    #1f4a2e;
      --badge-post:   #1a3651;
      --badge-text-get:  #3fb950;
      --badge-text-post: #58a6ff;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      line-height: 1.6;
      min-height: 100vh;
    }

    /* ── Header ────────────────────────────────────────────────────── */
    header {
      border-bottom: 1px solid var(--border);
      padding: 2rem 0;
      background: var(--surface);
    }

    .header-inner {
      max-width: 860px;
      margin: 0 auto;
      padding: 0 1.5rem;
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }

    .logo {
      width: 52px;
      height: 52px;
      background: var(--green);
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .logo svg { width: 30px; height: 30px; fill: #fff; }

    .header-text h1 {
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .header-text p {
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 0.15rem;
    }

    .pill {
      display: inline-block;
      padding: 0.15rem 0.6rem;
      border-radius: 20px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.03em;
      margin-left: 0.5rem;
      vertical-align: middle;
      border: 1px solid var(--green-dim);
      color: var(--green);
    }

    /* ── Main layout ───────────────────────────────────────────────── */
    main {
      max-width: 860px;
      margin: 2.5rem auto;
      padding: 0 1.5rem;
      display: grid;
      gap: 2rem;
    }

    /* ── Status banner ─────────────────────────────────────────────── */
    .status-banner {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 6px var(--green);
      flex-shrink: 0;
    }

    .status-banner span { color: var(--muted); font-size: 0.875rem; }
    .status-banner span strong { color: var(--text); }

    .status-banner a {
      margin-left: auto;
      color: var(--blue);
      font-size: 0.8rem;
      text-decoration: none;
    }
    .status-banner a:hover { text-decoration: underline; }

    /* ── Section ───────────────────────────────────────────────────── */
    section h2 {
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 0.75rem;
    }

    /* ── Endpoint cards ─────────────────────────────────────────────── */
    .endpoint-list {
      display: grid;
      gap: 0.6rem;
    }

    .endpoint {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.9rem 1.1rem;
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 0.5rem 1rem;
      align-items: start;
      transition: border-color 0.15s;
    }

    .endpoint:hover { border-color: var(--muted); }

    .method {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      padding: 0.2rem 0.55rem;
      border-radius: 5px;
      align-self: center;
      white-space: nowrap;
    }

    .method.get  { background: var(--badge-get);  color: var(--badge-text-get); }
    .method.post { background: var(--badge-post); color: var(--badge-text-post); }

    .endpoint-body {}

    .path {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.9rem;
      color: var(--text);
      font-weight: 600;
    }

    .desc {
      font-size: 0.82rem;
      color: var(--muted);
      margin-top: 0.15rem;
    }

    .lock {
      display: inline-block;
      font-size: 0.68rem;
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      margin-left: 0.5rem;
      vertical-align: middle;
      font-weight: 600;
    }

    .lock.jwt   { background: #2d2206; color: var(--yellow); border: 1px solid #5a4a1a; }
    .lock.admin { background: #2a1a1a; color: var(--red);    border: 1px solid #5a2020; }
    .lock.pub   { background: #1a2a1a; color: var(--green);  border: 1px solid #1a4a1a; }

    /* ── Auth info box ──────────────────────────────────────────────── */
    .info-box {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.1rem 1.25rem;
    }

    .info-box h3 {
      font-size: 0.875rem;
      font-weight: 600;
      margin-bottom: 0.6rem;
      color: var(--text);
    }

    .info-box ul {
      list-style: none;
      display: grid;
      gap: 0.45rem;
    }

    .info-box li {
      font-size: 0.82rem;
      color: var(--muted);
      padding-left: 1.1rem;
      position: relative;
    }

    .info-box li::before {
      content: "→";
      position: absolute;
      left: 0;
      color: var(--green);
    }

    .info-box li code {
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.8rem;
      background: var(--bg);
      padding: 0.05rem 0.35rem;
      border-radius: 4px;
      color: var(--text);
    }

    /* ── Footer ─────────────────────────────────────────────────────── */
    footer {
      border-top: 1px solid var(--border);
      padding: 1.5rem 0;
      text-align: center;
      color: var(--muted);
      font-size: 0.78rem;
    }
  </style>
</head>
<body>

  <header>
    <div class="header-inner">
      <div class="logo">
        <!-- WhatsApp-style chat bubble icon -->
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94
          1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
          <path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.557 4.122 1.528 5.855L.057 23.272a.75.75 0 0 0 .92.92l5.417-1.471A11.95 11.95 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.907 0-3.694-.503-5.236-1.383l-.376-.218-3.898 1.058 1.058-3.898-.218-.376A9.959 9.959 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/>
        </svg>
      </div>
      <div class="header-text">
        <h1>Chasqui <span class="pill">v0.1.0</span></h1>
        <p>WhatsApp notifications microservice for Torke &mdash; Meta Cloud API v22.0</p>
      </div>
    </div>
  </header>

  <main>

    <!-- Status -->
    <div class="status-banner">
      <div class="dot"></div>
      <span><strong>Service operational</strong> &mdash; all systems running normally</span>
      <a href="/health">health check →</a>
    </div>

    <!-- Endpoints -->
    <section>
      <h2>Endpoints</h2>
      <div class="endpoint-list">

        <div class="endpoint">
          <span class="method get">GET</span>
          <div class="endpoint-body">
            <div class="path">/health <span class="lock pub">public</span></div>
            <div class="desc">Liveness probe — returns <code>{"status": "ok"}</code></div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method post">POST</span>
          <div class="endpoint-body">
            <div class="path">/auth/token <span class="lock admin">admin</span></div>
            <div class="desc">Issue a JWT for a client. Requires <code>Authorization: Bearer &lt;ADMIN_SECRET&gt;</code></div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method post">POST</span>
          <div class="endpoint-body">
            <div class="path">/messages/send/text <span class="lock jwt">JWT</span></div>
            <div class="desc">Send a plain-text WhatsApp message to a phone number</div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method post">POST</span>
          <div class="endpoint-body">
            <div class="path">/messages/send/template <span class="lock jwt">JWT</span></div>
            <div class="desc">Send a pre-approved Meta message template (can initiate conversations)</div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method post">POST</span>
          <div class="endpoint-body">
            <div class="path">/messages/send/document <span class="lock jwt">JWT</span></div>
            <div class="desc">Send a PDF or other document with an optional caption</div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method get">GET</span>
          <div class="endpoint-body">
            <div class="path">/webhook/whatsapp <span class="lock pub">public</span></div>
            <div class="desc">Meta webhook verification handshake (challenge–response)</div>
          </div>
        </div>

        <div class="endpoint">
          <span class="method post">POST</span>
          <div class="endpoint-body">
            <div class="path">/webhook/whatsapp <span class="lock pub">public</span></div>
            <div class="desc">Receive incoming WhatsApp messages and status updates from Meta</div>
          </div>
        </div>

      </div>
    </section>

    <!-- Auth info -->
    <section>
      <h2>Authentication</h2>
      <div style="display: grid; gap: 0.75rem;">

        <div class="info-box">
          <h3>Issuing a token</h3>
          <ul>
            <li>Call <code>POST /auth/token</code> with <code>Authorization: Bearer &lt;ADMIN_SECRET&gt;</code></li>
            <li>Body: <code>{"client_id": "my-service", "expires_in_days": 90}</code></li>
            <li>Response contains a signed JWT valid for the requested duration</li>
          </ul>
        </div>

        <div class="info-box">
          <h3>Using a token</h3>
          <ul>
            <li>Add <code>Authorization: Bearer &lt;token&gt;</code> to every request to <code>/messages/*</code></li>
            <li>Tokens carry a <code>sub</code> (client ID) and <code>exp</code> (expiry) claim</li>
            <li>A <code>401</code> is returned on missing, expired, or invalid tokens</li>
          </ul>
        </div>

      </div>
    </section>

    <!-- Quick-start -->
    <section>
      <h2>Quick start</h2>
      <div class="info-box">
        <h3>Send a text message</h3>
        <ul>
          <li>Endpoint: <code>POST /messages/send/text</code></li>
          <li>Body: <code>{"to": "59899123456", "body": "Hello from Chasqui!"}</code></li>
          <li>The <code>to</code> field is the recipient's full E.164 phone number (no <code>+</code>)</li>
          <li>Text messages can only be sent within a 24-hour customer-service window</li>
          <li>Use <code>/messages/send/template</code> to initiate a new conversation</li>
        </ul>
      </div>
    </section>

  </main>

  <footer>
    Chasqui &mdash; Meta WhatsApp Business Cloud API &mdash;
    <a href="/docs" style="color: var(--blue); text-decoration: none;">Swagger UI</a> &middot;
    <a href="/redoc" style="color: var(--blue); text-decoration: none;">ReDoc</a>
  </footer>

</body>
</html>"""


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage() -> HTMLResponse:
    return HTMLResponse(content=_HTML)
