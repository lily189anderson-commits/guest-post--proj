/**
 * Thin API client. Wraps fetch(), attaches the JWT, and centralizes
 * error handling so every module (dashboard.js, auth.js) calls the
 * same small surface instead of hand-rolling fetch() everywhere.
 */
const API_BASE = "";

function getToken() {
  return localStorage.getItem("gp_token");
}

function setToken(token) {
  localStorage.setItem("gp_token", token);
}

function clearToken() {
  localStorage.removeItem("gp_token");
}

async function apiRequest(path, { method = "GET", body = null, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  if (response.status === 401) {
    clearToken();
    window.location.href = "/";
    return null;
  }

  if (response.status === 204) return null;

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message = (data && data.detail) || `Request failed (${response.status})`;
    throw new Error(message);
  }
  return data;
}

const api = {
  login: (username, password) =>
    apiRequest("/api/auth/login", { method: "POST", body: { username, password }, auth: false }),

  listClients: () => apiRequest("/api/clients"),
  createClient: (payload) => apiRequest("/api/clients", { method: "POST", body: payload }),
  deleteClient: (id) => apiRequest(`/api/clients/${id}`, { method: "DELETE" }),

  listWebsites: () => apiRequest("/api/websites"),
  createWebsite: (payload) => apiRequest("/api/websites", { method: "POST", body: payload }),
  deleteWebsite: (id) => apiRequest(`/api/websites/${id}`, { method: "DELETE" }),

  listOrders: () => apiRequest("/api/orders"),
  createOrder: (payload) => apiRequest("/api/orders", { method: "POST", body: payload }),
  recordPayment: (id, amount) =>
    apiRequest(`/api/orders/${id}/payments`, { method: "POST", body: { amount } }),
  deleteOrder: (id) => apiRequest(`/api/orders/${id}`, { method: "DELETE" }),

  checkLink: (orderId, pageUrl) =>
    apiRequest(`/api/link-check/${orderId}`, { method: "POST", body: { page_url: pageUrl } }),

  getAnalyticsSummary: () => apiRequest("/api/analytics/summary"),
};
