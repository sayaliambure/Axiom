/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        safe: '#10b981',      // Green
        risky: '#f59e0b',     // Amber/Yellow
        dangerous: '#ef4444', // Red
      },
    },
  },
  plugins: [],
}


