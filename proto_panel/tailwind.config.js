/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#06B6D4",
          light: "#6EBBDC",
          lighter: "#9CEEFC",
        },
        title: "#74DC6E",
      },
    },
  },
  plugins: [],
};
