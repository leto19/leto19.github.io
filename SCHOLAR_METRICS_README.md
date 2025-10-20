# Automatic Google Scholar Metrics Update

This repository includes multiple solutions for automatically fetching and displaying Google Scholar metrics (citations, h-index) on your personal website.

## 📊 Overview

Google Scholar doesn't provide an official API, so we use various workarounds:

1. **Recommended: Python Script + GitHub Actions** (automated, reliable)
2. **Node.js Proxy Server** (for dynamic updates)
3. **Client-side JavaScript** (simple but limited)

## ✅ Recommended Solution: Python + GitHub Actions

This is the **best approach for GitHub Pages** sites.

### Setup Steps:

#### 1. Install Python Dependencies Locally

```bash
pip install scholarly
```

#### 2. Test the Script Manually

```bash
python fetch_scholar_metrics.py
```

This will create two files:
- `scholar_metrics.json` - Full metrics
- `scholar_metrics_simple.json` - Simple metrics for web display

#### 3. Commit the JSON Files

```bash
git add scholar_metrics_simple.json
git commit -m "Add Scholar metrics"
git push
```

#### 4. Enable GitHub Actions

The workflow file `.github/workflows/update-scholar-metrics.yml` is already created.

- It runs automatically **every Monday at midnight UTC**
- You can also trigger it manually from the "Actions" tab in GitHub

#### 5. The Website Automatically Loads the Metrics

The `scholar-metrics-loader.js` script automatically:
- Loads metrics from `scholar_metrics_simple.json`
- Updates the citation count and h-index on the page
- Animates the numbers for a smooth effect
- Shows the last update date

### Manual Update

To update metrics manually at any time:

```bash
python fetch_scholar_metrics.py
git add scholar_metrics_simple.json
git commit -m "Update Scholar metrics"
git push
```

## 🔄 Alternative: Node.js Proxy Server

If you want real-time updates (not suitable for GitHub Pages):

### Setup:

```bash
npm install express axios cheerio cors
node scholar-proxy.js
```

Then update your website to fetch from: `http://localhost:3000/api/scholar-metrics?id=xbeMIhMAAAAJ`

**Note:** This requires a running server and won't work on GitHub Pages.

## 📝 How It Works

### Python Script (`fetch_scholar_metrics.py`)

1. Uses the `scholarly` library to fetch data from Google Scholar
2. Extracts citations, h-index, i10-index
3. Saves to JSON files
4. Can be automated via GitHub Actions

### JavaScript Loader (`scholar-metrics-loader.js`)

1. Fetches the JSON file from your repository
2. Updates the DOM elements on your page
3. Animates the counter for visual appeal
4. Handles errors gracefully (falls back to default values)

### GitHub Actions Workflow

1. Runs on a schedule (weekly)
2. Executes the Python script
3. Commits updated JSON files
4. Pushes changes to the repository

## 🎯 Your Scholar ID

Your Google Scholar ID is: `xbeMIhMAAAAJ`

Found in your Scholar URL: `https://scholar.google.com/citations?user=xbeMIhMAAAAJ`

## 🔧 Customization

### Change Update Frequency

Edit `.github/workflows/update-scholar-metrics.yml`:

```yaml
schedule:
  - cron: '0 0 * * 1'  # Weekly on Monday
  # Other options:
  # - cron: '0 0 * * *'   # Daily
  # - cron: '0 0 1 * *'   # Monthly
```

### Add More Metrics

In `scholar-metrics-loader.js`, you can display i10-index:

```javascript
// Add to your HTML:
<div class="stat-card">
  <span class="stat-number i10-index-value">XX</span>
  <span class="stat-label">i10-index</span>
</div>
```

## 🚨 Limitations

1. **Rate Limiting**: Google Scholar may block frequent requests
   - GitHub Actions approach minimizes this (weekly updates)
   
2. **CORS Issues**: Direct browser requests to Scholar are blocked
   - Solution: Use pre-fetched JSON files
   
3. **No Official API**: These are workarounds that may break if Google changes their site structure

## 🆘 Troubleshooting

### Metrics not updating?

1. Check if `scholar_metrics_simple.json` exists in your repo
2. Check GitHub Actions tab for workflow status
3. Check browser console for JavaScript errors
4. Verify the JSON file is accessible: `https://leto19.github.io/scholar_metrics_simple.json`

### Python script fails?

```bash
# Update scholarly library
pip install --upgrade scholarly

# Check your Scholar ID
python -c "from scholarly import scholarly; print(scholarly.search_author_id('xbeMIhMAAAAJ'))"
```

### Metrics show old values?

- Clear browser cache
- Check the `lastUpdated` timestamp in `scholar_metrics_simple.json`
- Trigger GitHub Actions manually

## 📚 Resources

- [scholarly library documentation](https://scholarly.readthedocs.io/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- Your Scholar profile: https://scholar.google.com/citations?user=xbeMIhMAAAAJ

## 🎉 Quick Start

1. Run: `python fetch_scholar_metrics.py`
2. Commit: `git add scholar_metrics_simple.json && git commit -m "Add metrics"`
3. Push: `git push`
4. Your website now automatically displays updated metrics!
