/**
 * The function passed as the alteration will be applied recursively to all JSON object keys in a valid JSON value.
 * If the valid JSON value is not an array or an object, then the same value passed to the function is returned.
 */
export default function alterJsonKeys (jsonValue, alterationFunc) {
  if (jsonValue == null || typeof jsonValue !== "object") {
    return jsonValue
  }

  if (Array.isArray(jsonValue)) {
    const alteredArray = []
    for (const item of jsonValue) {
      const alteredItem = alterJsonKeys(item, alterationFunc)
      alteredArray.push(alteredItem)
    }
    return alteredArray
  }

  const alteredObject = {}
  for (const [key, value] of Object.entries(jsonValue)) {
    const alteredKey = alterationFunc(key)
    alteredObject[alteredKey] = alterJsonKeys(value, alterationFunc)
  }
  return alteredObject
}
