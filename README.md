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

`.openai/hosting.json` identifies the Sites project. Static assets are in `dist`.
The website is public for coaches, as approved by the family.
If a custom domain is connected later, update `siteUrl` and rebuild the PDF.

The complete `dist` directory can also be served by any static host. No private
credentials belong in this repository. Font licenses are in
`dist/assets/FONT-LICENSE.txt`.

Race thumbnails: https://videos.milesplit.com/stills/820055.jpg and
https://videos.milesplit.com/stills/820066.jpg (MileSplit/FloSports).
