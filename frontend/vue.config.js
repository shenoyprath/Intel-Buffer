module.exports = {
  assetsDir: "static",
  css: {
    loaderOptions: {
      sass: {
        data: `
          @import "@/styles/vars/global_vars.scss";
          @import "@/styles/mixins/global_mixins.scss";
          @import "@/styles/funcs/global_funcs.scss";
        `
      }
    }
  }
}
