module.exports = {
  assetsDir: 'static',
  css: {
    loaderOptions: {
      sass: {
        data: `
          @import "@/styles/global_vars.scss";
          @import "@/styles/global_mixins.scss";
        `
      }
    }
  }
}
