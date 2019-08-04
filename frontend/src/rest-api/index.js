import axios from "axios"

import addCsrfCookie from "@/rest-api/interceptors/request/add-csrf-cookie"
import camelToSnakeKeys from "@/rest-api/transformations/request/camel-to-snake-keys"
import snakeToCamelKeys from "@/rest-api/transformations/response/snake-to-camel-keys"

const api = axios.create({
  baseURL: "http://127.0.0.1:8888/api",

  timeout: 5000,

  headers: {
    "Content-Type": "application/json"
  },

  transformRequest: [
    camelToSnakeKeys,
    JSON.stringify // last request transformation has to return JSON string.
  ],

  transformResponse: [
    JSON.parse,
    snakeToCamelKeys
  ],

  xsrfHeaderName: "X-CSRF-TOKEN",

  // in development, backend & frontend run on different ports.
  // the same origin policy is followed & cookies can't be shared.
  // setting `withCredentials` to true allows the cookies to be shared.
  // https://stackoverflow.com/a/14802115
  withCredentials: process.env.NODE_ENV !== "production"
})

api.interceptors.request.use(addCsrfCookie)

export default api
