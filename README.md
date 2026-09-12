# Public landing bundle — draft only

This is a separate, static, crawler-ready landing alternative. It is **DRAFT / UNPUBLISHED** and is not connected to an account, form backend, analytics, inbox, or outbound channel.

## Offer boundary

The offer is a focused review and possible implementation plan for one inbound enquiry source, one tracker, one acknowledgement template, one internal alert route, one follow-up rule, and one weekly report. The demo uses synthetic data; no customer outcomes are claimed. Any implementation requires an agreed scope, customer-owned accounts, written acceptance criteria, and approved pricing. The landing page itself costs $0 and makes no automatic contact.

The CTA is customer-initiated and points to the existing Revenue route:

`https://abubakar-automation-server-01.tail1185d0.ts.net/revenue-demo/`

The existing demo and Tailscale Funnel routes were not modified. LinkedIn Service Page remains unchanged and owner-verified LIVE_PUBLISHED. API/inbox remains `NOT_CONNECTED/UNVERIFIED`.

## Diagnosis

The Tailscale URL was reachable from this server with HTTP 200/TLS during the prior read-only check. Crawler compatibility is unverified and likely unsuitable: its DNS resolves in Tailscale CGNAT space (`100.64.0.0/10`) and the existing synthetic dashboard lacked canonical, Open Graph, and crawler metadata. This does **not** establish that LinkedIn failed; no LinkedIn account or API write was attempted.

## Recommended zero-cost host

Prefer **GitHub Pages** on an owner-controlled repository if the owner already has a GitHub account. It supports static HTML/CSS at no hosting cost and keeps publication under the owner’s control. If the owner has no GitHub account, use Cloudflare Pages/free static hosting instead; neither account path was opened here.

The dedicated repository has been prepared privately at <https://github.com/abubakarbakehouse1250/revenue-agent-landing>. It is **not public** and GitHub Pages is not enabled. The bundle remains **DRAFT / UNPUBLISHED**.

## Owner-only publication boundary

1. Review the private repository contents at <https://github.com/abubakarbakehouse1250/revenue-agent-landing>.
2. If approved, change repository visibility to public at **Settings → Danger Zone → Change repository visibility**.
3. Enable **Settings → Pages** using the `main` branch as the deployment source.
4. Verify the published URL `https://abubakarbakehouse1250.github.io/revenue-agent-landing/` and its metadata at <https://docs.github.com/en/pages/quickstart>.
5. Only at that approved publication step remove the draft `noindex`/`Disallow: /` gate if public indexing is desired.

Changing visibility or enabling Pages makes the page externally accessible and requires owner approval. No such action was performed.

## Local verification

From the repository root:

```sh
python3 public-landing/test_landing.py
python3 -m unittest discover -s demo/tests -p 'test_*.py'
python3 -m py_compile demo/*.py public-landing/test_landing.py
node --check demo/static/app.js
python3 -m http.server 8767 --directory public-landing
```

The HTTP smoke check should fetch `/index.html`, `/styles.css`, and `/robots.txt` locally. No JavaScript or third-party resources are used by this bundle.
