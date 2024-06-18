module.exports = {
  purge: [],
  content: ["./*.{html}"],
  darkMode: false, // or 'media' or 'class'
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
  variants: {
    extend: {},
  },
  plugins: [],
};
