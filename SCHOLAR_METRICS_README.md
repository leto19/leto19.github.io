# Google Scholar Metrics (Manual Update)

This site displays Google Scholar metrics (citations, h-index) on the homepage.
The numbers are loaded dynamically from a small JSON file and updated **by hand**.

## How it works now

1. `scholar_metrics_simple.json` holds the current metrics.
2. `scholar-metrics-loader.js` (loaded at the bottom of `index.html`) reads that
   JSON and animates the citation count + h-index into the stat cards, and adds a
   "Scholar metrics updated" date to the footer.
3. There is **no live scraping** of Google Scholar on page load.

## Why it's manual (not automated)

The original design used the `scholarly` Python library in a weekly GitHub
Action (`.github/workflows/update-scholar-metrics.yml`) to scrape Scholar and
commit fresh JSON. In practice this **does not work reliably**: Google Scholar
has no public API and blocks automated requests from cloud IPs (CAPTCHA / rate
limits). The scheduled runs failed repeatedly and the workflow was auto-disabled
after inactivity. Robust automation would require a paid/proxy scraping service,
which is overkill for a personal site whose metrics change a few times a year.

So: update by hand. It takes ~30 seconds.

## How to update (the only step you need)

1. Open your Scholar profile:
   https://scholar.google.com/citations?user=nvdSIdEAAAAJ
2. Note the **Citations (All)**, **h-index (All)**, and **i10-index (All)** from
   the metrics table on the right.
3. Edit `scholar_metrics_simple.json` with the new values and today's date:

   ```json
   {
     "name": "George Close",
     "affiliation": "Zyphra",
     "citations": 161,
     "hIndex": 8,
     "i10Index": 7,
     "publications": 15,
     "lastUpdated": "2026-06-30T00:00:00.000000",
     "scholarUrl": "https://scholar.google.com/citations?user=nvdSIdEAAAAJ"
   }
   ```

4. Commit and push. Pages rebuilds automatically; the homepage shows the new
   numbers.

> Note: the loader currently updates **citations** and **h-index** on the page.
> The hardcoded publication count in `index.html` is maintained separately
> (keep it consistent with the actual publications list).

## Leftover files (optional cleanup)

These were part of the abandoned auto-scrape approach and are no longer used by
the live site. Safe to delete if you want a tidier repo:

- `fetch_scholar_metrics.py`, `fetch_scholar_metrics_simple.py` (scrapers)
- `scholar-proxy.js` (local Node proxy, never deployed)
- `scholar_metrics.json` (duplicate of the `_simple` file)
- `.github/workflows/update-scholar-metrics.yml` (disabled workflow)

Kept for reference unless removed.
