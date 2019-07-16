import alterJsonKeys from "@/utils/alter-json-keys"

/**
 * Converts API response's snake_case JSON object keys back to camelCase for use in frontend code.
 */
export default function snakeToCamelKeys (data) {
  return alterJsonKeys(data, key => {
    return key.replace(
      /([^_]_[^_])/g, // ignore prefix & suffix underscores.
      substr => substr[0] + substr[2].toUpperCase()
    )
  })
}
