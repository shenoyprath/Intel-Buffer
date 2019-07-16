import alterJsonKeys from "@/utils/alter-json-keys"

/**
 * API expects snake_case for JSON object keys in the request body, but we want to maintain JS naming conventions in
 * the frontend code.
 */
export default function camelToSnakeKeys (data) {
  return alterJsonKeys(data, key => {
    return key
      .split(/(?=[A-Z])/)
      .join("_")
      .toLowerCase()
  })
}
