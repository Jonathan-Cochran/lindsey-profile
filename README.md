# Lindsey Cochran - recruiting profile

Static HTML/CSS website, with a matching one-page US letter PDF. No accounts or
database are needed to view the profile. Optional Google Analytics runs only
after visitor consent; the complete profile also works without JavaScript.

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
`dist/app.js` enables the print button. `dist/analytics.js` handles optional
analytics and visitor choices; all profile content and links work without JS.

## School-specific recruiting links

Each link opens the same athlete profile with school colors. Bowling Green also
includes the family connection note directly after the championship results.
The main address and PDF stay universal. There is no IP lookup, location prompt,
cookie, or remembered theme; the path alone selects the page.

| School | Recruiting link |
| --- | --- |
| Bowling Green State University | https://lindseycochran.com/bgsu/ |
| Ohio State University | https://lindseycochran.com/ohio-state/ |
| Clemson University | https://lindseycochran.com/clemson/ |
| Indiana University | https://lindseycochran.com/indiana/ |
| University of Notre Dame | https://lindseycochran.com/notre-dame/ |
| University of Cincinnati | https://lindseycochran.com/cincinnati/ |
| University of Georgia | https://lindseycochran.com/georgia/ |
| University of Illinois Urbana-Champaign | https://lindseycochran.com/illinois/ |
| University of Oregon | https://lindseycochran.com/oregon/ |
| Harvard University | https://lindseycochran.com/harvard/ |
| Brown University | https://lindseycochran.com/brown/ |
| University of Arkansas | https://lindseycochran.com/arkansas/ |

Edit `schools.json` to change colors or add an optional `note` with `heading` and
`text`. Use only confirmed, school-specific connections. The `colorSource` fields
record the university brand guides used for each palette. Text colors are adjusted
only where necessary for readability; decorative accents retain the supplied
school colors. No school logos or coach names are included.

The build generates each `dist/<school>/index.html` from the shared template and
`profile.json`; do not maintain separate copies of race data. School pages load
with their colors even without JavaScript, and all assets and the PDF resolve
from the site root. The canonical URL stays the universal profile. Unrecognized
paths display the default profile via GitHub Pages' custom `404.html` (with an HTTP
404 status and `noindex`).

## Content to confirm

- The family supplied an exact GPA of 4.156; weighted/unweighted basis was not
  specified. No grading scale has been assumed.
- The supplied email enables direct recruiting contact in the website and PDF.
- `instagram` holds Lindsey's Instagram profile URL. A secondary link appears
  beside the recruiting contact in the hero and connection sections on every
  page, opens in a new tab, and is excluded from the print resume and PDF.
- The family supplied the athlete photos. The opening race image uses
  `JS_02149-scaled.jpg`; the 1600m awards image uses `20260607_135341.jpg`.
  Website copies are compressed WebP files with camera metadata removed.
  Cropping is handled in CSS; original files remain in the workspace root.
  Race cards use the genuine MileSplit event thumbnails, linked to their hosted footage.
- `seasonNote` holds the latest significant result or confirmed upcoming competition.
  Its optional `source` selects a key in `sources`, and `linkLabel` labels that link.
- `honors` holds recognitions in display order, separately from championship
  finishes. The family supplied the event-specific 2026 indoor and outdoor
  OATCCC All-Ohio honors, OHSAA All-District honors, OCC First Team honors in
  the 800m and 4x800m relay, and the 2025-26 spring Scholar Athlete recognition.
  Related event awards are grouped for readability; indoor and outdoor honors
  remain separate. The earlier general XC conference entry was replaced by this
  more precise list. Do not infer additional event awards from race results.

## Evidence

- MileSplit athlete profile: class, school, outdoor 1600m, 800m, full mile, 400m,
  indoor 800m marks, plus race video listings.
- Athletic.net official result: XC 5K personal best of 18:43.4, fifth place in
  Division 2 Session 2 at OHSAA District - Central - Hilliard Darby on October 24,
  2026. The mark, place, date, and personal-best designation were checked on the
  official result page. The direct result link
  is used in the website, browser-print version, and PDF.
- Athletic.net regional results (October 31, 2026): Lindsey placed 11th in
  19:01.2 at OHSAA Regional - Central - Pickerington, ahead of Granville's
  12th-place finisher in 19:01.3. Official team scores show Big Walnut second
  with 85 points and Granville third with 87. The family described her finishing
  kick; the published times and scores corroborate the margins.
  Individual result: https://www.athletic.net/result/xoFQqqnIppEl2/.
- OHSAA state cross country results (November 7, 2026): 20th in 18:47.1 in the
  Division II girls 5K at Fortress Obetz. Big Walnut placed third with 192 points.
  The championship entry links to the official results. The latest-result note
  links to Lindsey's Athletic.net result and the Instagram post supplied by the family.
- OHSAA 2026 final results: 1600m first, 800m third, 4x800m second. The relay mark
  is explicitly a team time. PDF source links include relevant page anchors.
- MileSplit New Balance Outdoor Nationals freshman results: full mile twelfth in
  5:00.58 and 800m fourteenth in 2:15.00, also corroborated by the meet's
  RunnerSpace results.
- Athletic.net and Runcruit athlete profiles are linked as supplied. Do not label
  Runcruit projections as achieved times.
- OHSAA's August 2026 selection criteria call the track recognition "All-Ohio"
  and award it to the top eight placers in each event and division. Lindsey's
  three state podium finishes qualify. The criteria link is labeled accordingly.
- The June 15, 2026 Central Ohio High School Sports Awards announcement lists
  Lindsey among the girls track and field Athlete of the Year nominees. The
  Dispatch article was corroborated by its Yahoo Sports syndication:
  https://sports.yahoo.com/articles/2025-26-central-ohio-high-110225245.html.

The source URLs are stored in `profile.json`; use these as the record of evidence.
Do not expand this project into a full meet-results database.

## Optional analytics

The family's GA4 web stream is `G-P3HMCFQ70E`, stored in
`analyticsMeasurementId` in `profile.json`. This is public configuration.
The versioned analytics script is included on the main page, every school page,
and the fallback. It never loads Google on localhost or other preview hosts.

Visitors can allow or decline using the non-modal prompt, or change their choice
under **Privacy & analytics** at the foot of any page. Choices expire after 180
days. No Google tag or analytics event is sent before acceptance or after a
saved decline. Withdrawal disables tracking, expires this site's GA cookies,
and reloads the page to unload Google's running code. Browser storage failures
fall back to an explicit choice for the current page. Changes in another tab
are honored. Privacy controls are excluded from the printed resume and PDF.

The tag denies all three advertising-consent categories, disables Google signals
and ad personalization, limits GA cookies to 180 days without renewal, and sends
one explicit pageview per load. Measured paths are only the known school path or
`/`; query strings, fragments, raw contact/destination URLs, link text, and
referrers are not included in our event payloads. Each event includes a `school`
label (`default` or the school slug); the built-in Page path dimension also
separates school pages without any additional GA configuration.

| Event | Meaning |
| --- | --- |
| `page_view` | Consenting visit to the main or a school page |
| `resume_download` | Click on the resume PDF link; not confirmation of a completed download |
| `race_video_click` | Click to MileSplit footage, with `race` of `1600m` or `800m`; not playback measurement |
| `evidence_link_click` | Click to a results/recruiting/award source, with a general `provider` label |
| `recruiting_contact_click` | Recruiting email link selected; not confirmation of a sent email |
| `instagram_click` | Instagram profile link selected |
| `resume_print_click` | Print resume button selected; not confirmation of printing |

The family confirmed these GA admin settings on October 31, 2026:
**Enhanced measurement OFF**, **Google signals OFF**, and **granular location and
device collection disabled**. Keep enhanced measurement off: the site supplies
explicit events to avoid duplicate counts and automatic collection of raw link
URLs. Keep email redaction enabled as an additional safeguard. No Google Ads
integration is needed. Google still receives technical request information,
including an IP address; this setup is not a claim of anonymity.

To inspect activity, open GA4's Realtime report, then visit the live site and
allow analytics. Browser blockers and visitors declining analytics reduce
recorded traffic. Standard reports may take longer to populate. A visit to a
school page does not identify a visitor as a coach or prove recruiting interest.
Optional event parameters such as `school`, `race`, and `provider` can be
registered as event-scoped custom dimensions for more detailed reports.

Run `node --test scripts/analytics.test.cjs` to check consent, withdrawal,
cross-tab choices, preview exclusion, and event privacy. GitHub Actions runs
these tests before publication.

## Hosting

The primary address is `https://lindseycochran.com`, hosted by GitHub Pages.
Source code is in the public repository `Jonathan-Cochran/lindsey-profile`, as
approved by the family. GitHub Pages uses **GitHub Actions** as its publishing
source, and the repository variable `PAGES_ENABLED` is `true`.
Configure `lindseycochran.com` as the repository's custom domain before pointing
DNS to GitHub.
The custom domain setting is managed in GitHub, not a `CNAME` file, because this
project uses an Actions workflow.

In AWS Route 53, open **Hosted zones → lindseycochran.com → Create record**.
Use simple routing, turn **Alias** off, and configure these records. For the apex
record, leave the record name blank and enter all four IP addresses as separate
lines in one A record. A TTL of 300 seconds is suitable during setup.

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
