## ADDED Requirements

### Requirement: Landing Page Structure
The website SHALL provide a single-page landing experience with the following sections:
- Hero section with book cover and primary value proposition
- Features section highlighting brain health benefits
- Book details section with difficulty level breakdown
- Call-to-action section with purchase link

#### Scenario: User visits landing page
- **WHEN** a user navigates to the website root URL
- **THEN** the landing page loads with all sections visible
- **AND** the book cover image is prominently displayed
- **AND** the Amazon purchase button is accessible

### Requirement: Responsive Design
The website SHALL be fully responsive across device sizes:
- Mobile: 320px - 768px
- Tablet: 768px - 1024px
- Desktop: 1024px+

#### Scenario: Mobile user views site
- **WHEN** a user visits on a mobile device
- **THEN** the layout adapts to single-column format
- **AND** all content remains readable and accessible
- **AND** buttons are tap-friendly (minimum 44px touch target)

### Requirement: Visual Theme
The website SHALL use a zen/natural color scheme consistent with the book cover's aesthetic:
- Primary background: Sage green (#8B9D83 or similar muted olive)
- Accent color: Cream/beige (#F5E6D3 for badges, cards, CTAs)
- Secondary accents: Wood tones (tan #D4B896) and bamboo green (#7A9A65)
- Text: Dark charcoal on light backgrounds, cream on green backgrounds
- Typography: Clean, readable sans-serif fonts conveying calm sophistication

#### Scenario: Brand consistency
- **WHEN** the website is viewed alongside the book cover
- **THEN** the color palette matches the sage green and cream aesthetic
- **AND** the calming, nature-inspired visual style is maintained
- **AND** the design evokes relaxation and mental clarity

### Requirement: Purchase Call-to-Action
The website SHALL include prominent call-to-action buttons linking to the Amazon product page.

#### Scenario: User clicks purchase button
- **WHEN** a user clicks the "Buy on Amazon" button
- **THEN** the user is navigated to the Amazon product listing in a new tab
- **AND** the link uses appropriate affiliate tracking if configured

### Requirement: Book Content Display
The website SHALL display content sourced from `books/master-kakuro/BOOK_DESCRIPTION.md`:
- Book title and subtitle
- Brain health benefits
- Puzzle count and difficulty breakdown
- Target audience messaging

#### Scenario: Content accuracy
- **WHEN** the landing page is displayed
- **THEN** the puzzle counts match: 75 Beginner, 95 Intermediate, 80 Expert
- **AND** the total of 250 puzzles is stated
- **AND** the large print format (8.5" × 11") is mentioned

