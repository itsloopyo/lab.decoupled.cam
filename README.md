# lab.decoupled.cam

The public site for **Lab**, the Directed Coding workbench. A plain
static site served by GitHub Pages, distinct from the app repo. It also
hosts the Patreon OAuth callback and the supporter download flow.

## Pages

| File | URL | Purpose |
| --- | --- | --- |
| `index.html` | `/` | Landing page (hero + What / How / Get it). |
| `privacy.html` | `/privacy` | Privacy policy. |
| `terms.html` | `/terms` | Terms of service. |
| `eula.html` | `/eula` | End User Licence Agreement. |
| `download.html` | `/download` | Supporter-gated download (OAuth → broker → signed link). |
| `patreon/callback.html` | `/patreon/callback` | OAuth redirect target; bounces `?code&state` into the `lab://` deep link. |
| `support.html` | `/support` | Redirect to Patreon (stable link for the app's Support button). |
| `favicon.png` / `icon.png` | | App icon (use `/icon.png` as the Patreon app icon URL). |

GitHub Pages serves extensionless URLs (`/privacy` → `privacy.html`), so
the clean paths above work with `.nojekyll` on.

## Deploy

1. Push to `main`. Repo → **Settings → Pages** → Source = `main`, root.
2. The `CNAME` file points the site at `lab.decoupled.cam`. In Cloudflare
   DNS add a `CNAME` record `lab` → `itsloopyo.github.io` (proxied is
   fine). HTTPS is provisioned automatically.

## Patreon / broker wiring

For the campaign, give Patreon:

- **App icon:** `https://lab.decoupled.cam/icon.png`
- **Privacy / Terms URLs:** `https://lab.decoupled.cam/privacy` and `/terms`
- **Redirect URIs:** `https://lab.decoupled.cam/patreon/callback` and
  `https://lab.decoupled.cam/download`

Then in `download.html`, set `BROKER` (the worker's URL) and `CLIENT_ID`
to match the desktop app (`src-tauri/src/patreon.rs`) and the worker
(`workers/patreon-broker`) in the Lab repo. The site owns
`lab.decoupled.cam`, so the broker worker lives on its own host
(`*.workers.dev` by default, or a subdomain like `broker.decoupled.cam`).

## Credits

Theme: "The Director's Console": Bricolage Grotesque / Hanken Grotesk /
Spline Sans Mono, warm-charcoal with an ember accent and a teal live-agent
tick. The hero is a dependency-free Canvas2D visualization of a fleet of
agents working under a director's baton.
