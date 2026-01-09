module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/**/*.js'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins'], 
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        mylight: {
          primary: "#3A5AA3",
          "base-100": "#ffffff",   
          "base-50": "#fafaf9",   
          "base-200": "#f5f5f4",  
          "base-300": "#d6d3d1",   
          "base-400": "#a8a29e",   
          "base-500": "#78716c",   
          "base-600": "#57534e",   
          "base-700": "#44403c",   
          "textCol": "#292524",   

          error: "#ef4444",
        },
      },
      {
        mydark: {
          primary: "#3A5AA3", 

          "base-100": "#1c1917",     
          "base-50": "#292524",     
          "base-300": "#44403c",    
          "base-content": "#e7e5e4",

          neutral: "#0c0a09",       
          "neutral-content": "#fafaf9",

          error: "#ef4444",
        },
      },
    ],}
}