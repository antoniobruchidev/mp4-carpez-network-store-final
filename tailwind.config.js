/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    "./**/forms.py",
  ],
  theme: {
    container: {
      center: true,
    },
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}
