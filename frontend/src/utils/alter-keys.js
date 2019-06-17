/**
 * The function passed as the alteration will be applied recursively to all keys in a particular object.
 */
export default function alterKeys (object, alterationFunc) {
  const alteredObject = {}

  for (const [key, value] of Object.entries(object)) {
    const alteredKey = alterationFunc(key)
    if (
      typeof value === "object" &&
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
