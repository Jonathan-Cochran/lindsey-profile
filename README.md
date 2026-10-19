# Lindsey Cochran - recruiting profile

Static HTML/CSS website, with a matching one-page US letter PDF. No accounts,
database, analytics, or browser dependencies are needed to view the profile.

## Update the profile

1. Edit `profile.json`. Keep only selected personal bests and championship results.
2. Update `updated` to the date the information was reviewed.
3. Run `python3 scripts/build.py` (Python with `reportlab` installed).
4. Preview with `python3 -m http.server 4173 --directory dist`.
5. Review the website and the PDF before deploying the updated `dist` directory.

Both formats use the same profile data. `template.html` controls the website
layout. `dist/styles.css` includes a condensed browser-print version; the PDF
download is a separately typeset letter-size document with clickable sources.
`dist/app.js` only enables the print button; all content and links work without JS.

## Content to confirm

- The family confirmed an XC 5K of 18:48 and will provide its result link.
  It is displayed as family-reported, with a pending source. MileSplit currently
  lists 19:52.05. Add the official URL to `sources`, assign that key to the XC mark's
  `source`, update its context and `xcSourcePending`, and rebuild when confirmed.
- The family supplied an exact GPA of 4.156; weighted/unweighted basis was not
  specified. No grading scale has been assumed.
- The supplied email enables direct recruiting contact in the website and PDF.
- No athlete photo was provided. The design uses original track artwork rather
  than a stand-in athlete. Race cards use the genuine MileSplit event thumbnails, linked to their hosted footage.
- `seasonNote` is editable; no unconfirmed meets or race dates are presented.

## Evidence

- MileSplit athlete profile: class, school, outdoor 1600m, 800m, full mile, 400m,
  indoor 800m, and XC 5K marks, plus race video listings.
- OHSAA 2026 final results: 1600m first, 800m third, 4x800m second. The relay mark
  is explicitly a team time. PDF source links include relevant page anchors.
- MileSplit New Balance Outdoor Nationals freshman results: full mile twelfth in
  5:00.58 and 800m fourteenth in 2:15.00, also corroborated by the meet's
  RunnerSpace results.
- Athletic.net and Runcruit are linked as supplied. Their complete records were
  not independently readable through the public text interface. Do not label
  Runcruit projections as achieved times.

The source URLs are stored in `profile.json`; use these as the record of evidence.
Do not expand this project into a full meet-results database.

## Hosting

`.openai/hosting.json` identifies the Sites project. Static assets are in `dist`.
Sites starts with owner-private access. Public coach access requires changing
the audience to public in Sites; a private preview link is not coach-accessible.
If a custom domain is connected later, update `siteUrl` and rebuild the PDF.

The complete `dist` directory can also be served by any static host. No private
credentials belong in this repository. Font licenses are in
`dist/assets/FONT-LICENSE.txt`.

Race thumbnails: https://videos.milesplit.com/stills/820055.jpg and
https://videos.milesplit.com/stills/820066.jpg (MileSplit/FloSports).
