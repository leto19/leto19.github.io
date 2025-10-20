/**
 * Client-side Google Scholar Metrics Loader
 * 
 * This script loads pre-fetched Scholar metrics from a JSON file.
 * This is the recommended approach for static GitHub Pages sites.
 * 
 * Workflow:
 * 1. Run fetch_scholar_metrics.py periodically (manually or via GitHub Actions)
 * 2. Commit the generated scholar_metrics_simple.json to your repo
 * 3. This script loads and displays the metrics
 */

// Load metrics from JSON file
async function loadScholarMetrics() {
  try {
    const response = await fetch('scholar_metrics_simple.json');
    if (!response.ok) {
      throw new Error('Metrics file not found');
    }
    
    const metrics = await response.json();
    return metrics;
  } catch (error) {
    console.error('Error loading Scholar metrics:', error);
    return null;
  }
}

// Update the page with fetched metrics
async function updateScholarMetrics() {
  const metrics = await loadScholarMetrics();
  
  if (!metrics) {
    console.log('Using default metrics from HTML');
    return;
  }

  // Update citation count
  const citationsElement = document.querySelector('.stat-card:nth-child(3) .stat-number');
  if (citationsElement && metrics.citations) {
    animateCounter(citationsElement, 0, metrics.citations, 2000);
  }
  
  // Update h-index
  const hIndexElement = document.querySelector('.stat-card:nth-child(4) .stat-number');
  if (hIndexElement && metrics.hIndex) {
    animateCounter(hIndexElement, 0, metrics.hIndex, 2000);
  }

  // Update i10-index if you add it to the page
  if (metrics.i10Index) {
    const i10Element = document.querySelector('.i10-index-value');
    if (i10Element) {
      animateCounter(i10Element, 0, metrics.i10Index, 2000);
    }
  }

  // Add last updated timestamp to footer
  if (metrics.lastUpdated) {
    const lastUpdated = new Date(metrics.lastUpdated);
    const formattedDate = lastUpdated.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    // Add or update metrics update notice
    const footer = document.querySelector('.footer');
    if (footer) {
      let metricsNote = document.querySelector('.metrics-update');
      if (!metricsNote) {
        metricsNote = document.createElement('p');
        metricsNote.className = 'metrics-update';
        metricsNote.style.fontSize = '0.85rem';
        metricsNote.style.marginTop = '0.5rem';
        metricsNote.style.fontStyle = 'italic';
        footer.appendChild(metricsNote);
      }
      metricsNote.textContent = `Scholar metrics updated: ${formattedDate}`;
    }
  }

  console.log('Scholar metrics loaded successfully:', metrics);
}

// Animate counter from start to end value
function animateCounter(element, start, end, duration) {
  const startTime = performance.now();
  const range = end - start;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function (ease-out)
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(start + range * easeOut);
    
    element.textContent = current;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = end; // Ensure final value is exact
    }
  }

  requestAnimationFrame(update);
}

// Alternative: Fetch directly from Google Scholar using CORS proxy
// (Not recommended due to reliability issues and potential blocking)
async function fetchScholarMetricsDirect(scholarId) {
  try {
    // Using a CORS proxy (use with caution)
    const proxyUrl = 'https://api.allorigins.win/raw?url=';
    const scholarUrl = encodeURIComponent(
      `https://scholar.google.com/citations?user=${scholarId}&hl=en`
    );
    
    const response = await fetch(proxyUrl + scholarUrl);
    const html = await response.text();
    
    // Parse HTML (basic regex parsing - not robust)
    const citationsMatch = html.match(/<td class="gsc_rsb_std">(\d+)<\/td>/);
    const hIndexMatch = html.match(/<td class="gsc_rsb_std">(\d+)<\/td>/g);
    
    if (citationsMatch && hIndexMatch && hIndexMatch.length >= 2) {
      return {
        citations: parseInt(citationsMatch[1]),
        hIndex: parseInt(hIndexMatch[1].match(/\d+/)[0])
      };
    }
    
    return null;
  } catch (error) {
    console.error('Error fetching Scholar metrics directly:', error);
    return null;
  }
}

// Export functions for use in main page
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    loadScholarMetrics,
    updateScholarMetrics,
    fetchScholarMetricsDirect
  };
}
