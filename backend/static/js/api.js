/**
 * Helpers for calling same-origin Django / DRF APIs from templates.
 * CSRF: SessionAuthentication requires the csrftoken cookie + X-CSRFToken header on POST.
 */
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function fetchJson(url, options) {
  var opts = options || {};
  var headers = Object.assign(
    {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken") || ""
    },
    opts.headers || {}
  );
  return fetch(url, Object.assign({ credentials: "same-origin" }, opts, { headers: headers })).then(function (res) {
    return res.text().then(function (text) {
      var data;
      try {
        data = text ? JSON.parse(text) : {};
      } catch (e) {
        data = { _raw: text };
      }
      return { ok: res.ok, status: res.status, data: data };
    });
  });
}
