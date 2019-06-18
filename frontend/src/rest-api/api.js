import axios from "axios"

import alterKeys from "@/utils/alter-keys"

const api = axios.create({
  baseURL: "http://127.0.0.1:8888/api",

  timeout: 5000,

  headers: {
    "Content-Type": "application/json"
  },

  transformRequest: [
    /**
     * API expects snake_case for JSON keys in the request body, but we want to maintain JS naming conventions in the
     * frontend code.
     */
    function camelToSnake (data) {
      return alterKeys(data, key => {
        return key
          .split(/(?=[A-Z])/)
          .join("_")
          .toLowerCase()
      })
    },

    // last transformRequest function has to return JSON string.
    data => JSON.stringify(data)
  ],

  transformResponse: [
    data => JSON.parse(data),

    /**
     * Converts API response's snake_case JSON keys back to camelCase for use in frontend code.
     */
    function snakeToCamel (data) {
      return alterKeys(data, key => {
        return key.replace(
          /([^_]_[^_])/g, // ignore prefix & suffix underscores.
          substr => substr[0] + substr[2].toUpperCase()
        )
      })
    }
  ],

  xsrfHeaderName: "X-CSRF-TOKEN",

  // in development, backend & frontend run on different ports.
  // the same origin policy is followed & cookies can't be shared.
  // setting `withCredentials` to true allows the cookies to be shared.
  // https://stackoverflow.com/a/14802115
  withCredentials: process.env.NODE_ENV !== "production"
})

api.interceptors.request.use(
  function addCsrfCookie (config) {
    if (config.url === "/auth-token") {
      config.xsrfCookieName = "csrf_refresh_token"
    } else {
      config.xsrfCookieName = "csrf_access_token"
    }
    return config
  }
)

export default api
