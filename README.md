# Data Science Portfolio Template (Quarto)

A ready-to-ship [Quarto](https://quarto.org) portfolio site for **Willamette
University M.S. Data Science** students. It ships a home page with a round
headshot, a featured **Capstone** page, an **Other Projects** listing, a
**Resume** page, and an **About** page — and it deploys itself with **GitHub
Actions**, so you never commit build output.

> The sample identity is **Blitz Bearcat**. Every page is
> full of `[bracketed placeholders]` — sweep them all and nothing of Blitz's
> should survive.

## Quick start (about 20 minutes to a live site)

### 1. Make your own repo from this template

Click **Use this template → Create a new repository**.

**Name it exactly `your_github_username.github.io`** (your real username). That
special name publishes your site at the clean root URL
`https://your_github_username.github.io/` — no `/portfolio` suffix. Keep it
**public**.

### 2. Turn on GitHub Actions deployment (one-time)

In your new repo: **Settings → Pages → Build and deployment → Source →
“GitHub Actions.”**

That's the whole deployment setup. There is no `gh-pages` branch to manage and
no `_site`/`docs` folder to commit — every push to `main` triggers the workflow
in [`.github/workflows/publish.yml`](.github/workflows/publish.yml), which
renders the site and deploys it.

### 3. Clone and preview locally

```bash
git clone https://github.com/your_github_username/your_github_username.github.io.git
cd your_github_username.github.io
quarto preview
```

Leave `quarto preview` running: edit a file, save, watch it reload.

### 4. Make it yours

| File | What to change |
|------|----------------|
| `_quarto.yml` | Site title, navbar, footer, GitHub/LinkedIn links, `site-url` |
| `index.qmd` | Your name, one-liner, links (round headshot lives here) |
| `images/profile.png` | Replace with your own headshot (square crops best) |
| `capstone.qmd` | Your featured capstone — the most important page |
| `projects/` | One folder per "other" project; delete `example-analysis/` |
| `resume.qmd` + `assets/resume.pdf` | Your resume summary + downloadable PDF |
| `about.qmd` | The longer story in your own voice |
| `styles.scss` | One accent color, one font |

### 5. Publish

```bash
git add .
git commit -m "Make the portfolio mine"
git push
```

Watch the **Actions** tab. When the run goes green, your site is live at
`https://your_github_username.github.io/`. From now on, **push is publish** —
that's the whole update cycle.

## Running code in your pages (freeze)

This template is configured with `execute: freeze: auto` in `_quarto.yml`, and
GitHub Actions installs **only Quarto — not R or Python.** That keeps builds
fast and reliable for a whole cohort.

If you add R or Python chunks (for example in your capstone), render **locally**
so Quarto stores the results in `_freeze/`, then commit that folder:

```bash
quarto render
git add _freeze/
git commit -m "Freeze capstone output"
git push
```

CI then reuses the frozen output instead of running your code — so it never
needs your data or your packages. If a page must never execute in CI, you can
also set `eval: false` on those chunks.

## What's in the box

```
.
├── _quarto.yml                  # site config, navbar, theme, freeze
├── index.qmd                    # Home — round headshot + one-liner
├── capstone.qmd                 # Featured capstone project
├── projects.qmd                 # Listing page for other projects
├── projects/
│   ├── capstone/featured.png    # capstone hero image
│   └── example-analysis/        # sample "other project" (delete me)
├── resume.qmd                   # Resume page (+ assets/resume.pdf)
├── about.qmd                    # About page
├── images/profile.png           # headshot (Blitz sample)
├── styles.scss                  # theme tweaks
└── .github/workflows/publish.yml  # GitHub Actions deploy
```

## Requirements

- [Quarto](https://quarto.org/docs/get-started/) installed locally for preview.
- A GitHub account. Everything here is free on public repos.

Built for **DATA 510: Data Science Capstone**, Willamette University.
