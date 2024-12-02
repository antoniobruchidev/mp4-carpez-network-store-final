/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./bag/**/*.{html,js}",
    "./products/**/*.{html,js}",
    "./checkout/**/*.{html,js}",
    "./dashboard/**/*.{html,js}",
    "./reviews/**/*.{html,js}",
    "./home/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    "./products/forms.py",
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
