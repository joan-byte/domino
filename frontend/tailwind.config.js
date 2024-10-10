/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        beige: {
          200: '#F5F5DC',
        },
      },
    },
  },
  plugins: [],
}

