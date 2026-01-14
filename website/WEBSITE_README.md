# Master Kakuro Promotion Website

A responsive landing page for the Master Kakuro puzzle book, built with React, Vite, and Tailwind CSS.

## Features

- **Responsive Design**: Mobile-first approach, works on all devices
- **Zen Aesthetic**: Sage green and cream color scheme matching the book cover
- **Fast Performance**: Vite-powered development and production builds
- **SEO Optimized**: Meta tags and semantic HTML for search engines
- **Accessible**: WCAG-compliant markup and interactive elements

## Color Palette

- **Sage Green** (#8B9D83) - Primary background
- **Cream** (#F5E6D3) - Accent and CTA buttons
- **Wood Tones** (#D4B896) - Secondary accents
- **Bamboo Green** (#7A9A65) - Highlights
- **Charcoal** (#2D3436) - Text

## Project Structure

```
website/
├── src/
│   ├── App.tsx           # Main landing page component
│   ├── index.css         # Tailwind CSS configuration
│   ├── main.tsx          # React entry point
│   └── assets/
│       └── cover_front.jpg  # Book cover image
├── index.html            # HTML entry point with SEO meta tags
├── vite.config.ts        # Vite configuration with Tailwind plugin
├── package.json          # Dependencies and scripts
└── dist/                 # Production build output
```

## Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Sections

1. **Hero** - Book cover, title, and primary CTA
2. **Benefits** - Why Kakuro for brain health
3. **Features** - What makes this book different
4. **Difficulty Levels** - Beginner, Intermediate, Expert breakdown
5. **CTA** - Final call-to-action
6. **Footer** - Copyright and branding

## Amazon Link

Update the Amazon purchase link in `src/App.tsx` (currently placeholder `#`).

## Deployment

Build output is in `dist/`. Deploy to any static hosting:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

