# External Research Tool Requirements: KDP Kakuro Market

This document outlines the functional requirements for external tools needed to perform comprehensive market research for our Kakuro puzzle book venture on Amazon KDP.

## 1. Competitor Analysis Tools
**Objective:** Programmatically collect and analyze data on top-performing Kakuro books on Amazon.

### Requirements:
- **Amazon Product Scraping:** Ability to extract data from search result pages for "Kakuro puzzle book".
- **Data Points:**
  - Full Title and Subtitle.
  - Current Price and Page Count.
  - Best Sellers Rank (BSR) in specific categories (e.g., Logic Puzzles, Mathematical Games).
  - Average Rating and Total Review Count.
  - Publication Date.
  - Delivery Type (Paperback vs. Kindle).
- **Review Sentiment Analysis:** Ability to aggregate and categorize common themes in 1-star and 5-star reviews (e.g., "puzzles too easy", "large print is great").

## 2. Keyword Research & SEO Tools
**Objective:** Identify high-volume, low-competition keywords for Amazon search optimization.

### Requirements:
- **Search Volume Data:** Monthly search volume for specific terms (e.g., "Kakuro", "Japanese cross-sums").
- **Competition Analysis:** Difficulty scores for ranking on the first page of Amazon or Google.
- **Autocomplete Extraction:** Tool to pull the "suggested searches" from Amazon's search bar for Kakuro-related parent terms.
- **Long-tail Discovery:** Generation of niche phrases (e.g., "Kakuro for seniors large print").

## 3. Pricing and Profitability Tools
**Objective:** Calculate net royalties across different price points and specification variations.

### Requirements:
- **KDP Royalty Calculator:** Ability to input trim size (8.5x11), page count (~300), and color options (B&W) to determine printing costs.
- **Scenario Comparison:** Side-by-side comparison of 35% vs 70% royalty tiers.
- **Historical Price Tracking:** Monitoring price fluctuations of top competitors over time.

## 4. Trend and Market Analysis Tools
**Objective:** Identify seasonal spikes and emerging sub-niches in the puzzle market.

### Requirements:
- **Search Interest Over Time:** Access to Google Trends data for "Kakuro" and related puzzle types.
- **Niche Gap Identification:** Tools that flag categories with high BSR (low sales) but high search volume, or vice versa (underserved high-demand).
- **Seasonality Tracking:** Visualizing annual peaks in puzzle book sales (e.g., holiday season).

## Summary Table for Research Agent
| Category | Primary Action | Target Platform |
|----------|----------------|-----------------|
| Competitors | Scrape/Analyze Listings | Amazon |
| Keywords | Volume/Difficulty Metrics | Amazon, Google |
| Pricing | Print Cost/Royalty Math | Amazon KDP |
| Trends | Historical Volume Analytics | Global Search |

Provide a list of tools and APIs that can be used to perform the above tasks.  They are preferably open source and available on GitHub.
