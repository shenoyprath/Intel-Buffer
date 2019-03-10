import Vue from "vue"
import Router from "vue-router"
import Home from "./views/Home.vue"

Vue.use(Router)

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/sign_in",
      name: "sign-in",
      component: () => import("@/views/SignIn")
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/Register")
    }
  ]
})
