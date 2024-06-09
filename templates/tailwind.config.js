/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
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
