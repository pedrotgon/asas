/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bosch: {
          blue: "#1D428A",
          light: "#4F6AA3",
          dark: "#0F285A"
        }
      }
    }
  },
  plugins: []
};
