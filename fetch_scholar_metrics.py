#!/usr/bin/env python3
"""
Google Scholar Metrics Fetcher
Fetches citation count and h-index from Google Scholar

Installation:
    pip install scholarly

Usage:
    python fetch_scholar_metrics.py

This script can be:
1. Run manually to update a JSON file
2. Set up as a GitHub Action to run periodically
3. Used with a simple Flask/FastAPI server
"""

from scholarly import scholarly
import json
from datetime import datetime

def fetch_scholar_metrics(scholar_id):
    """
    Fetch metrics from Google Scholar using scholarly library
    
    Args:
        scholar_id (str): Google Scholar author ID
    
    Returns:
        dict: Dictionary containing citations, h-index, and other metrics
    """
    try:
        # Search for author by ID
        author = scholarly.search_author_id(scholar_id)
        author_info = scholarly.fill(author)
        
        # Extract metrics
        metrics = {
            'name': author_info.get('name', ''),
            'affiliation': author_info.get('affiliation', ''),
            'citations': author_info.get('citedby', 0),
            'hIndex': author_info.get('hindex', 0),
            'i10Index': author_info.get('i10index', 0),
            'publications': len(author_info.get('publications', [])),
            'lastUpdated': datetime.now().isoformat(),
            'scholarUrl': f"https://scholar.google.com/citations?user={scholar_id}"
        }
        
        return metrics
        
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return None

def save_to_json(metrics, filename='scholar_metrics.json'):
    """Save metrics to JSON file"""
    with open(filename, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {filename}")

def main():
    # Your Google Scholar ID
    SCHOLAR_ID = 'xbeMIhMAAAAJ'
    
    print(f"Fetching metrics for Scholar ID: {SCHOLAR_ID}")
    metrics = fetch_scholar_metrics(SCHOLAR_ID)
    
    if metrics:
        print("\n=== Google Scholar Metrics ===")
        print(f"Name: {metrics['name']}")
        print(f"Affiliation: {metrics['affiliation']}")
        print(f"Citations: {metrics['citations']}")
        print(f"h-index: {metrics['hIndex']}")
        print(f"i10-index: {metrics['i10Index']}")
        print(f"Publications: {metrics['publications']}")
        print(f"Last Updated: {metrics['lastUpdated']}")
        
        # Save to JSON file
        save_to_json(metrics)
        
        # Also create a simpler version for JavaScript
        simple_metrics = {
            'citations': metrics['citations'],
            'hIndex': metrics['hIndex'],
            'i10Index': metrics['i10Index'],
            'lastUpdated': metrics['lastUpdated']
        }
        save_to_json(simple_metrics, 'scholar_metrics_simple.json')
        
    else:
        print("Failed to fetch metrics")

if __name__ == "__main__":
    main()
