#!/usr/bin/env python3
"""
Simple Google Scholar Metrics Fetcher (No external dependencies except requests)

Installation:
    pip install requests beautifulsoup4

Usage:
    python fetch_scholar_metrics_simple.py
"""

import json
import re
from datetime import datetime
try:
    import requests
    from bs4 import BeautifulSoup
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False
    print("Warning: requests and/or beautifulsoup4 not installed")
    print("Install with: pip install requests beautifulsoup4")

def fetch_scholar_metrics_simple(scholar_id):
    """
    Fetch metrics from Google Scholar using simple HTTP request
    
    Args:
        scholar_id (str): Google Scholar author ID
    
    Returns:
        dict: Dictionary containing citations, h-index, and other metrics
    """
    if not DEPS_AVAILABLE:
        print("Error: Required dependencies not installed")
        return None
        
    try:
        url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract name
        name_elem = soup.find('div', {'id': 'gsc_prf_in'})
        name = name_elem.text if name_elem else 'Unknown'
        
        # Extract affiliation
        affiliation_elem = soup.find('div', {'class': 'gsc_prf_il'})
        affiliation = affiliation_elem.text if affiliation_elem else 'Unknown'
        
        # Extract metrics from the table
        table = soup.find('table', {'id': 'gsc_rsb_st'})
        if not table:
            print("Could not find metrics table")
            return None
            
        rows = table.find_all('tr')
        
        citations = 0
        h_index = 0
        i10_index = 0
        
        for i, row in enumerate(rows):
            cols = row.find_all('td')
            if len(cols) >= 2:
                value = cols[1].text.strip()
                if value.isdigit():
                    if i == 1:  # Citations row
                        citations = int(value)
                    elif i == 2:  # h-index row
                        h_index = int(value)
                    elif i == 3:  # i10-index row
                        i10_index = int(value)
        
        metrics = {
            'name': name,
            'affiliation': affiliation,
            'citations': citations,
            'hIndex': h_index,
            'i10Index': i10_index,
            'lastUpdated': datetime.now().isoformat(),
            'scholarUrl': f"https://scholar.google.com/citations?user={scholar_id}"
        }
        
        return metrics
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def save_to_json(metrics, filename='scholar_metrics.json'):
    """Save metrics to JSON file"""
    with open(filename, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved to {filename}")

def main():
    # Your Google Scholar ID
    SCHOLAR_ID = 'xbeMIhMAAAAJ'
    
    print("=" * 50)
    print("Google Scholar Metrics Fetcher")
    print("=" * 50)
    print(f"\nFetching metrics for Scholar ID: {SCHOLAR_ID}")
    print("Please wait...\n")
    
    metrics = fetch_scholar_metrics_simple(SCHOLAR_ID)
    
    if metrics:
        print("=" * 50)
        print("Google Scholar Metrics")
        print("=" * 50)
        print(f"Name:         {metrics['name']}")
        print(f"Affiliation:  {metrics['affiliation']}")
        print(f"Citations:    {metrics['citations']}")
        print(f"h-index:      {metrics['hIndex']}")
        print(f"i10-index:    {metrics['i10Index']}")
        print(f"Last Updated: {metrics['lastUpdated']}")
        print("=" * 50)
        
        # Save full metrics
        save_to_json(metrics, 'scholar_metrics.json')
        
        # Save simple version for JavaScript
        simple_metrics = {
            'citations': metrics['citations'],
            'hIndex': metrics['hIndex'],
            'i10Index': metrics['i10Index'],
            'lastUpdated': metrics['lastUpdated']
        }
        save_to_json(simple_metrics, 'scholar_metrics_simple.json')
        
        print("\n✓ Success! Metrics files created.")
        print("  - scholar_metrics.json (full)")
        print("  - scholar_metrics_simple.json (for website)")
        
    else:
        print("\n✗ Failed to fetch metrics")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the Scholar ID is correct")
        print("3. Google Scholar might be temporarily blocking requests")
        print("4. Try again in a few minutes")

if __name__ == "__main__":
    main()
