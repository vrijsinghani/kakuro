# Master Kakuro Website

This is the official landing page for the **Master Kakuro** puzzle book series. The website is built to showcase the books, highlight the cognitive benefits of solving Kakuro puzzles, and provide a premium user experience for potential readers.

## 🚀 Technology Stack

- **Framework**: [React](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Utilities**: `clsx`, `tailwind-merge`

## 🛠️ Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

- [Node.js](https://nodejs.org/) (Latest LTS version recommended)
- `npm` (comes with Node.js)

### Installation

1. Clone the repository (if you haven't already):
   ```bash
   git clone <repository-url>
   cd website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running Locally

Start the development server with Hot Module Replacement (HMR):

```bash
npm run dev
```

The site will be available at `http://localhost:5173` (or another port if 5173 is busy).

### Building for Production

To create a production-ready build:

```bash
npm run build
```

The output will be generated in the `dist` directory. You can preview this build locally using:

```bash
npm run preview
```

## 📂 Project Structure

```
website/
├── public/              # Static assets (favicons, images, etc.)
├── src/
│   ├── components/      # Reusable UI components
│   ├── sections/        # Page sections (Hero, Science, Features, etc.)
│   ├── App.tsx          # Main application component
│   ├── index.css        # Global styles and Tailwind imports
│   └── main.tsx         # Application entry point
├── index.html           # HTML entry point
├── package.json         # Project metadata and dependencies
├── vite.config.ts       # Vite configuration
└── README.md            # Project documentation
```

## ✨ Key Features

- **Modern Aesthetic**: Clean, responsive design focused on readability and user engagement.
- **Science-Backed**: Dedicated sections explaining the cognitive benefits of logic puzzles.
- **Performance**: Optimized build using Vite for fast load times.
- **Responsive**: Fully responsive layouts ensuring a great experience on mobile, tablet, and desktop.

## 🤝 Contributing

1. Ensure your code follows the existing style (ESLint and TypeScript configs are included).
2. Run `npm run lint` to catch any issues before committing.
3. Make sure all new components are responsive and accessible.
