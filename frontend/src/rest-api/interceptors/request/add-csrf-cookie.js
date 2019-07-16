export default function addCsrfCookie (request) {
  if (request.url === "/auth-token") {
    request.xsrfCookieName = "csrf_refresh_token"
  } else {
    request.xsrfCookieName = "csrf_access_token"
  }
  return request
}
