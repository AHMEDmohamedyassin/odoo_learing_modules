/** @type {import('tailwindcss').Config} */
const flowbite = require('flowbite/plugin');
module.exports = {
  content: [
    "./**/*.{js,jsx,ts,tsx,xml,html,css}",
    './node_modules/flowbite/**/*.js',
  ],
  important: true,
  theme: {
    extend: {},
  },
  plugins: [
    flowbite
  ],
  darkMode: 'class', // or 'media' or 'class'
} 