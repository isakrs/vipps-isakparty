# AGENTS.md — isakparty.com

This file tells any AI agent (Claude, Gemini, GPT, Codex, etc.) how to create and publish event pages on the isakparty.com domain family. Read this before doing anything with the repo.

---

## Site architecture

Each subdomain or context is its own GitHub repository and its own GitHub Pages site:

| Domain | Repo | Purpose |
|--------|------|---------|
| `isakparty.com` | `isakrs/isakparty.com` | Personal events and parties |
| `vipps.isakparty.com` | `isakrs/vipps-isakparty` | Work events (Vipps MobilePay) |

Each event within a site lives at its own path:
- `isakparty.com/birthday-june-2026/`
- `vipps.isakparty.com/ai-day-11-06-2026/`

New subdomains are created by spawning a new repo from the template repo:
`https://github.com/isakrs/isakparty-template`

---

## How to create a new event page

### Step 1 — Choose a slug

Short, lowercase, hyphenated. Include a date if the event is recurring.
Examples: `ai-day-11-06-2026`, `summer-party-2025`, `birthday-june`.

### Step 2 — Create the event folder

Create `<slug>/index.html` — a complete, self-contained HTML file.
Optionally add `<slug>/styles.css` and `<slug>/app.js` if they'd be long.

### Step 3 — Design guidelines

Reference page: https://vipps.janschill.de/ (source: https://github.com/janschill/vipps-holmen)

- Mobile-first, clean, minimal — works perfectly on a 375px screen
- Strong hero section at the top: big title, date, location, mood
- Google Fonts — Inter is the default
- One or two accent colors that fit the event; no more
- If photos are provided: responsive grid or masonry layout
- If data is provided (times, scores, results): visualise it — table or animated chart
- Vanilla JavaScript only — no frameworks, no bundlers
- No external dependencies beyond Google Fonts
- All CSS and JS inline or in files in the same folder
- Page weight under 100 KB excluding images

### Step 4 — Update the homepage

In the root `index.html`, add a new card inside `<ul class="events">`:

```html
<li class="event-card">
  <a href="/ai-day-11-06-2026/">
    <span class="event-date">June 2026</span>
    <span class="event-name">AI Day</span>
    <span class="event-arrow">→</span>
  </a>
</li>
```

Also remove the `<li class="empty">` placeholder if it is still there.

### Step 5 — Commit and push

```bash
git add <slug>/ index.html
git commit -m "Add <slug> event page"
git push
```

GitHub Pages deploys automatically within about 30 seconds.

---

## Deployment

- Hosted on GitHub Pages, branch `main`, root `/`
- Custom domain set via `CNAME` file in the repo root
- No build step — files are served as-is
- HTTPS is enforced

---

## How to trigger page creation

### From a phone — GitHub app or github.com (recommended for quick creation)

1. Open the GitHub app or go to github.com on your browser
2. Navigate to the repo (e.g. `isakrs/isakparty.com`)
3. Go to **Actions → Create event page → Run workflow**
4. Fill in `prompt` (describe the event) and `slug` (the URL path)
5. Tap **Run workflow** — done, page is live in ~1 minute

No token needed in chat. The workflow uses secrets stored in the repo.

### From Claude Code on desktop (recommended for pages with images or revisions)

Open Claude Code with the repo as working directory and give a plain-language prompt:

> "Create a page for our AI day on 11 June 2026. Here are some photos [attach]. The agenda was X, the speakers were Y."

Claude will generate the files, commit, and push. GitHub Pages deploys automatically.

### From any AI via the GitHub API (for AIs with HTTP tool use — Claude, Codex, Gemini)

The GitHub personal access token for this repo is stored in your password manager under `isakparty GitHub token`. Retrieve it from there — do not ask the user to type it in the chat.

To trigger the workflow:

```bash
curl -s -X POST \
  -H "Authorization: token <TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/isakrs/isakparty.com/actions/workflows/create-page.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "slug": "ai-day-11-06-2026",
      "prompt": "Describe the event here..."
    }
  }'
```

To commit a file directly without going through Actions:

```bash
# base64-encode the file content first, then:
curl -s -X PUT \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/isakrs/isakparty.com/contents/<slug>/index.html \
  -d '{
    "message": "Add <slug> event page",
    "content": "<base64-encoded HTML>"
  }'
```

### Revisions from a new chat session

You do not need to be in the same chat to revise a page. Open Claude Code in the repo directory and say:

> "Revise the ai-day-11-06-2026 page. Update the results section with these final numbers: ..."

Claude will read the existing file, make the changes, commit, and push.

---

## Creating a new subdomain site

1. Go to `https://github.com/isakrs/isakparty-template` → **Use this template → Create a new repository**
2. Name it to match the subdomain (e.g. `vipps-isakparty` for `vipps.isakparty.com`)
3. Edit `CNAME` in the new repo to contain the subdomain (e.g. `vipps.isakparty.com`)
4. In one.com DNS: add a CNAME record `vipps` → `isakrs.github.io`
5. In the new repo Settings → Pages: set custom domain to `vipps.isakparty.com`
6. Add `ANTHROPIC_API_KEY` to the repo's Actions secrets
7. Done — create pages exactly as above

---

## Notes for agents

- Use relative paths for links (`href="/slug/"` not absolute URLs)
- Ensure pages work without a local server — no ES module imports from node_modules
- When revising, read the existing file first before editing
- After pushing, confirm deployment by checking `https://github.com/isakrs/isakparty.com/actions`
