# Alexander Jackson | Product, Engineering & Analytics

Personal portfolio for Alexander Jackson, built with [Quarto](https://quarto.org/) and deployed to GitHub Pages with GitHub Actions.

## Pages

- `index.qmd`: home, featured work, core disciplines, experience.
- `projects.qmd`: image-led portfolio with category filters.
- `projects/*.qmd`: dedicated case studies for five featured projects.
- `capstone.qmd`: the full Risky Business capstone report.
- `experience.qmd`, `about.qmd`, `resume.qmd`: supporting pages.
- `styles.scss`: light editorial design system, shared components, and responsive layout.
- `images/projects/*.svg`: deliberately illustrative cover art for projects.

## Running locally

Install Quarto, then run:

```bash
quarto preview
```

For a static build:

```bash
quarto render
```

The rendered site is written to `_site/`. GitHub Actions publishes from `main`.

## Portfolio imagery

The four other projects and Risky Business currently use conceptual SVG visuals, not actual app screenshots or quantitative results. They are labeled as illustrations on each case-study page. When representative original project screenshots or approved marketing materials are available, replace the respective `images/projects/<slug>.svg` image and update its alt text/caption. The existing capstone report and its supporting files have been preserved.

PairName is a static JavaScript/Supabase app in its current connected repository. The portfolio avoids linking to that private repository or claiming live user metrics. No unpublished client datasets, private assets, or internal screens are included.

## Design principles

- Quiet editorial styling inspired by professional analyst and builder portfolios.
- Serif headings, restrained blue-green accents, generous whitespace, readable typography.
- Real project specifics and appropriately qualified impact estimates.
- Responsive and keyboard-accessible cards and filters.
- Avoid presenting concept artwork as real product screenshots.
