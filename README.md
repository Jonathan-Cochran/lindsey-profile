# Lindsey Cochran - recruiting profile

Static HTML/CSS website, with a matching one-page US letter PDF. No accounts,
database, analytics, or browser dependencies are needed to view the profile.

## Update the profile

1. Edit `profile.json`. Keep only selected personal bests and championship results.
2. Update `updated` to the date the information was reviewed.
3. Install dependencies once with `python3 -m pip install -r requirements.txt`.
4. Run `python3 scripts/build.py`, then `python3 scripts/check_build.py`.
5. Preview with `python3 -m http.server 4173 --directory dist`.
6. Review the website and the PDF, commit, and push to `main`.

The workflow rebuilds and validates the website and PDF on every push to `main`.
Pull requests run the same checks without publishing. Set the repository Actions
variable `PAGES_ENABLED` to `true` after GitHub Pages is enabled to automatically
publish `dist` following successful builds. Until then, the workflow only builds
and validates. Deployment does not require a personal access token or any
repository secrets. The workflow can also be run manually from the Actions tab.

Both formats use the same profile data. `template.html` controls the website
layout. `dist/styles.css` includes a condensed browser-print version; the PDF
download is a separately typeset letter-size document with clickable sources.
`dist/app.js` only enables the print button; all content and links work without JS.

## Content to confirm

- The family supplied an exact GPA of 4.156; weighted/unweighted basis was not
  specified. No grading scale has been assumed.
- The supplied email enables direct recruiting contact in the website and PDF.
- The family supplied the athlete photos. The opening race image uses
  `JS_02149-scaled.jpg`; the 1600m awards image uses `20260607_135341.jpg`.
  Website copies are compressed WebP files with camera metadata removed.
  Cropping is handled in CSS; original files remain in the workspace root.
  Race cards use the genuine MileSplit event thumbnails, linked to their hosted footage.
- `seasonNote` holds the latest significant result or confirmed upcoming competition.

## Evidence

- MileSplit athlete profile: class, school, outdoor 1600m, 800m, full mile, 400m,
  indoor 800m marks, plus race video listings.
- Athletic.net official result: XC 5K personal best of 18:48.5, second place at
  Ohio Capital Conference - Capital on October 17, 2026. The direct result link
  is used in the website, browser-print version, and PDF.
- OHSAA 2026 final results: 1600m first, 800m third, 4x800m second. The relay mark
  is explicitly a team time. PDF source links include relevant page anchors.
- MileSplit New Balance Outdoor Nationals freshman results: full mile twelfth in
  5:00.58 and 800m fourteenth in 2:15.00, also corroborated by the meet's
  RunnerSpace results.
- Athletic.net and Runcruit athlete profiles are linked as supplied. Do not label
  Runcruit projections as achieved times.

The source URLs are stored in `profile.json`; use these as the record of evidence.
Do not expand this project into a full meet-results database.

## Hosting

The intended primary address is `https://lindseycochran.com`. Source code is stored
in a private GitHub repository. The current account plan does not support GitHub
Pages for private repositories, so Pages deployment is disabled pending the
hosting decision. The existing public Sites publication continues serving coaches.

If using GitHub Pages, it requires a supported paid plan for the private repository
or explicit approval to make the repository public. Set the repository's Pages
publishing source to **GitHub Actions** and `PAGES_ENABLED` to `true`, then
configure `lindseycochran.com` as its custom domain before pointing DNS to GitHub.
The custom domain setting is managed in GitHub, not a `CNAME` file, because this
project uses an Actions workflow.

At the domain's DNS provider, configure these records:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | jonathan-cochran.github.io |

Replace conflicting parking records for `@` and `www`; retain unrelated mail
records. If using Cloudflare DNS, use DNS-only mode for these records while
GitHub provisions the certificate. Once DNS is valid and the certificate is
issued, enable **Enforce HTTPS** in GitHub Pages. The `www` hostname will redirect
to the primary domain. See GitHub's [custom domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

`.openai/hosting.json` retains the original Sites project identity. The existing
Sites URL remains available separately; GitHub Actions only deploys to GitHub
Pages. Changes pushed to GitHub do not update the old Sites publication.

The complete `dist` directory can also be served by any static host. No private
credentials belong in this repository. Font licenses are in
`dist/assets/FONT-LICENSE.txt`.

Race thumbnails: https://videos.milesplit.com/stills/820055.jpg and
https://videos.milesplit.com/stills/820066.jpg (MileSplit/FloSports).
