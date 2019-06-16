module.exports = {
  assetsDir: "static",
  css: {
    loaderOptions: {
      sass: {
        data: `@import "@/styles/_globals.scss";`
      }
    }
  }
}
