# Research Automation Tools Inventory

> For future automation of Kakuro market research

## Overview

This document catalogs open-source tools and APIs that can automate the research areas outlined in `external_tool_requirements.md`.

---

## 1. Amazon Product Scraping

### Recommended: `luminati-io/Amazon-scraper`
- **URL:** https://github.com/luminati-io/Amazon-scraper
- **Language:** Python
- **Last Updated:** Nov 2024
- **Features:** Search results, product details, offers, reviews, Q&A, bestsellers, seller info
- **Install:** `pip install amazon-scraper`

### Alternative: `ShantanuJalkote/amazon-data-scraper`
- **URL:** https://github.com/ShantanuJalkote/amazon-data-scraper
- **Language:** Python (Selenium + BeautifulSoup)
- **Last Updated:** Sep 2025
- **Features:** URL, name, price, rating, reviews, ASIN, description

### Key Libraries
```python
pip install requests beautifulsoup4 selenium pandas
```

### Anti-Block Best Practices
- Rotate User-Agents
- Random delays (2-5s between requests)
- Proxy rotation for IP changes
- Handle CAPTCHAs gracefully

---

## 2. Amazon Keyword Research

### Recommended: `drawrowfly/amazon-keyword-scraper-go`
- **URL:** https://github.com/drawrowfly/amazon-keyword-scraper-go
- **Language:** Go
- **Features:** Generates keywords from Amazon Web API, outputs CSV with product counts

### Alternative: `souvik666/Open-Source-keyword-research-API`
- **URL:** https://github.com/souvik666/Open-Source-keyword-research-API-and-website-look-up
- **Language:** Python
- **Features:** `GET /amazon` endpoint for keyword suggestions

### Manual Approach
Use Amazon's autocomplete API directly:
```
https://completion.amazon.com/api/2017/suggestions?mid=ATVPDKIKX0DER&alias=aps&prefix=kakuro
```

---

## 3. Google Trends Analysis

### Recommended: `pytrends`
- **URL:** https://github.com/GeneralMills/pytrends
- **Language:** Python 3.3+
- **Status:** Active, unofficial API
- **Install:** `pip install pytrends`

### Features
| Function | Description |
|----------|-------------|
| `interest_over_time()` | Historical search volume |
| `interest_by_region()` | Geographic popularity |
| `related_queries()` | Related search terms |
| `trending_searches()` | Current trending topics |
| `suggestions()` | Keyword refinements |

### Example Usage
```python
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(['kakuro', 'sudoku'], timeframe='today 12-m')
df = pytrends.interest_over_time()
```

---

## 4. KDP Pricing Calculator

### No Open-Source Tool Found

**Recommendation:** Build a simple Python script using KDP's published formulas:

```python
def calculate_royalty(list_price: float, page_count: int, 
                      is_large_trim: bool = True) -> float:
    """Calculate KDP royalty for B&W paperback."""
    fixed_cost = 0.85 if is_large_trim else 1.00
    per_page = 0.012
    print_cost = fixed_cost + (page_count * per_page)
    royalty = (list_price * 0.60) - print_cost
    return max(royalty, 0)

# Example: 300-page book at $12.99
print(calculate_royalty(12.99, 300))  # ~$2.94
```

---

## Summary: Automation Priority

| Area | Tool Exists? | Recommendation |
|------|--------------|----------------|
| Amazon Scraping | ✅ Yes | Use `luminati-io/Amazon-scraper` |
| Keyword Research | ⚠️ Limited | Use autocomplete API + Go scraper |
| Trend Analysis | ✅ Yes | Use `pytrends` |
| KDP Pricing | ❌ No | Build simple Python script |

---

## Commercial Alternatives (If Open-Source Fails)

| Tool | Use Case | Pricing |
|------|----------|---------|
| [Book Bolt](https://bookbolt.io) | Full KDP research suite | $10-20/mo |
| [Publisher Rocket](https://publisherrocket.com) | Keyword + competitor analysis | $97 one-time |
| [Helium 10](https://helium10.com) | Amazon SEO (overkill for books) | $39+/mo |
