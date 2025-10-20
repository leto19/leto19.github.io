/**
 * Google Scholar Metrics Proxy Server
 * 
 * This Node.js script creates a simple proxy server to fetch Google Scholar metrics
 * while avoiding CORS issues and rate limiting.
 * 
 * Installation:
 *   npm install express axios cheerio cors
 * 
 * Usage:
 *   node scholar-proxy.js
 * 
 * Then access: http://localhost:3000/api/scholar-metrics?id=xbeMIhMAAAAJ
 */

const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Enable CORS for your GitHub Pages site
app.use(cors({
  origin: ['http://localhost', 'https://leto19.github.io']
}));

// Cache to avoid hitting Google Scholar too frequently
const cache = new Map();
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

app.get('/api/scholar-metrics', async (req, res) => {
  const scholarId = req.query.id;

  if (!scholarId) {
    return res.status(400).json({ error: 'Scholar ID is required' });
  }

  // Check cache first
  const cached = cache.get(scholarId);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return res.json(cached.data);
  }

  try {
    // Fetch Google Scholar profile
    const url = `https://scholar.google.com/citations?user=${scholarId}&hl=en`;
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });

    // Parse HTML with cheerio
    const $ = cheerio.load(response.data);

    // Extract metrics from the citation table
    const citationsAll = $('#gsc_rsb_st tbody tr:nth-child(1) td:nth-child(2)').text().trim();
    const hIndexAll = $('#gsc_rsb_st tbody tr:nth-child(2) td:nth-child(2)').text().trim();
    const i10IndexAll = $('#gsc_rsb_st tbody tr:nth-child(3) td:nth-child(2)').text().trim();

    const metrics = {
      citations: parseInt(citationsAll) || 0,
      hIndex: parseInt(hIndexAll) || 0,
      i10Index: parseInt(i10IndexAll) || 0,
      lastUpdated: new Date().toISOString()
    };

    // Cache the result
    cache.set(scholarId, {
      data: metrics,
      timestamp: Date.now()
    });

    res.json(metrics);

  } catch (error) {
    console.error('Error fetching Scholar metrics:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch metrics',
      message: error.message 
    });
  }
});

app.listen(PORT, () => {
  console.log(`Scholar proxy server running on http://localhost:${PORT}`);
  console.log(`Test endpoint: http://localhost:${PORT}/api/scholar-metrics?id=xbeMIhMAAAAJ`);
});
