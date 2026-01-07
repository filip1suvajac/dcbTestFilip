module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins'], 
      },
    },
  },
  plugins: [require('daisyui')],
}
