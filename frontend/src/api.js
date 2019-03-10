import axios from 'axios'

/**
 * The function passed as the alteration will be applied recursively to all keys in a particular object.
 * Used for manipulating the keys in the JSON sent to and from the API.
 */
function alterKeys (object, alterationFunc) {
  const alteredObject = {}

  for (const [key, value] of Object.entries(object)) {
    const alteredKey = alterationFunc(key)
    if (
      typeof value === 'object' &&
      !Array.isArray(value) &&
      value != null
    ) {
      alteredObject[alteredKey] = alterKeys(value, alterationFunc)
    } else {
      alteredObject[alteredKey] = value
    }
  }

  return alteredObject
}

const api = axios.create({
  baseURL: 'http://127.0.0.1:8888/api',

  timeout: 5000,

  headers: {
    'Content-Type': 'application/json'
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
          .join('_')
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
  ]
})

export default api
