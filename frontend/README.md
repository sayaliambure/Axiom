# AXIOM Frontend

React + TypeScript + Tailwind CSS frontend for AXIOM hiring decision intelligence tool.

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```

## Environment Variables

Create a `.env` file in the `frontend` directory:

```
VITE_API_URL=http://localhost:8000/api
```

## Features

- **Authentication**: Login and registration
- **Financial Input**: Enter company financial snapshot
- **Hiring Input**: Enter hiring scenario details
- **Results View**: See hiring impact with risk indicator (🟢 Safe / 🟡 Risky / 🔴 Dangerous)

## UX Principles

- One decision per screen
- No finance jargon - plain language
- Emphasize consequences, not numbers
- Clear risk indicators with color coding


