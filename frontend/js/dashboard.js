// Guard: bounce to login if no token.
if (!getToken()) {
  window.location.href = "/";
}

// ---- In-memory cache (avoids re-fetching on every keystroke of search) ----
let clientsCache = [];
let websitesCache = [];
let ordersCache = [];
let activeOrderStatusFilter = "all";
let pendingCheckOrderId = null;
let pendingPaymentOrderId = null;

// ---- Toast ----
function showToast(message, type = "success") {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.className = `toast ${type}`;
  el.hidden = false;
  setTimeout(() => { el.hidden = true; }, 3200);
}

// ---- Tabs ----
const titles = {
  overview: "Overview",
  clients: "Clients",
  websites: "Websites",
  orders: "Orders & Links",
  analytics: "Analytics",
};

document.querySelectorAll(".nav-item").forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

function switchTab(tab) {
  document.querySelectorAll(".nav-item").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
  document.querySelectorAll(".tab-panel").forEach((p) => p.classList.add("hidden"));
  document.getElementById(`tab-${tab}`).classList.remove("hidden");
  document.getElementById("pageTitle").textContent = titles[tab];

  if (tab === "overview") loadOverview();
  if (tab === "clients") loadClients();
  if (tab === "websites") loadWebsites();
  if (tab === "orders") loadOrdersAndRefs();
  if (tab === "analytics") loadAnalytics();
}

// ---- Logout ----
document.getElementById("logoutBtn").addEventListener("click", () => {
  clearToken();
  window.location.href = "/";
});

// ================= CLIENTS =================
async function loadClients() {
  clientsCache = await api.listClients();
  renderClients(document.getElementById("clientSearch").value);
}

function renderClients(filterText = "") {
  const q = filterText.trim().toLowerCase();
  const rows = clientsCache.filter(
    (c) => !q || c.name.toLowerCase().includes(q) || c.email.toLowerCase().includes(q)
  );
  const body = document.getElementById("clientsBody");
  body.innerHTML = rows.map((c) => `
    <tr>
      <td>#${c.id}</td>
      <td class="font-ui">${escapeHtml(c.name)}</td>
      <td>${escapeHtml(c.email)}</td>
      <td class="font-ui">${escapeHtml(c.phone || "—")}</td>
      <td class="font-ui">${escapeHtml(c.notes || "—")}</td>
      <td><button class="btn-mini danger" onclick="deleteClient(${c.id})">Delete</button></td>
    </tr>
  `).join("") || `<tr><td colspan="6" class="font-ui muted">No clients yet.</td></tr>`;
}

document.getElementById("clientSearch").addEventListener("input", (e) => renderClients(e.target.value));

document.getElementById("clientForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api.createClient({
      name: document.getElementById("clientName").value,
      email: document.getElementById("clientEmail").value,
      phone: document.getElementById("clientPhone").value || null,
      notes: document.getElementById("clientNotes").value || null,
    });
    e.target.reset();
    showToast("Client added");
    loadClients();
  } catch (err) {
    showToast(err.message, "error");
  }
});

async function deleteClient(id) {
  if (!confirm("Delete this client? Their orders will be removed too.")) return;
  try {
    await api.deleteClient(id);
    showToast("Client deleted");
    loadClients();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// ================= WEBSITES =================
async function loadWebsites() {
  websitesCache = await api.listWebsites();
  renderWebsites(document.getElementById("websiteSearch").value);
}

function renderWebsites(filterText = "") {
  const q = filterText.trim().toLowerCase();
  const rows = websitesCache.filter((w) => !q || w.domain.toLowerCase().includes(q));
  const body = document.getElementById("websitesBody");
  body.innerHTML = rows.map((w) => `
    <tr>
      <td>#${w.id}</td>
      <td class="font-ui">${escapeHtml(w.domain)}</td>
      <td>${w.da_score}</td>
      <td>${w.dr_score}</td>
      <td class="font-ui">${escapeHtml(w.niche || "—")}</td>
      <td><button class="btn-mini danger" onclick="deleteWebsite(${w.id})">Delete</button></td>
    </tr>
  `).join("") || `<tr><td colspan="6" class="font-ui muted">No websites yet.</td></tr>`;
}

document.getElementById("websiteSearch").addEventListener("input", (e) => renderWebsites(e.target.value));

document.getElementById("websiteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api.createWebsite({
      domain: document.getElementById("siteDomain").value,
      da_score: parseInt(document.getElementById("siteDA").value, 10),
      dr_score: parseInt(document.getElementById("siteDR").value, 10),
      niche: document.getElementById("siteNiche").value || null,
    });
    e.target.reset();
    showToast("Website added");
    loadWebsites();
  } catch (err) {
    showToast(err.message, "error");
  }
});

async function deleteWebsite(id) {
  if (!confirm("Delete this website?")) return;
  try {
    await api.deleteWebsite(id);
    showToast("Website deleted");
    loadWebsites();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// ================= ORDERS =================
async function loadOrdersAndRefs() {
  const [clients, websites, orders] = await Promise.all([
    api.listClients(), api.listWebsites(), api.listOrders(),
  ]);
  clientsCache = clients;
  websitesCache = websites;
  ordersCache = orders;
  populateOrderSelects();
  renderOrders();
}

function populateOrderSelects() {
  const clientSel = document.getElementById("orderClient");
  const siteSel = document.getElementById("orderWebsite");
  clientSel.innerHTML = clientsCache.map((c) => `<option value="${c.id}">${escapeHtml(c.name)}</option>`).join("")
    || `<option disabled selected>Add a client first</option>`;
  siteSel.innerHTML = websitesCache.map((w) => `<option value="${w.id}">${escapeHtml(w.domain)} (DA ${w.da_score})</option>`).join("")
    || `<option disabled selected>Add a website first</option>`;
}

function clientName(id) {
  const c = clientsCache.find((c) => c.id === id);
  return c ? c.name : `#${id}`;
}
function websiteDomain(id) {
  const w = websitesCache.find((w) => w.id === id);
  return w ? w.domain : `#${id}`;
}

function linkBadge(status) {
  const map = { active: "Active", broken: "Broken", pending: "Pending" };
  return `<span class="badge badge-${status}">${map[status] || status}</span>`;
}
function paymentBadge(status) {
  const map = { paid: "Paid", partial: "Partial", unpaid: "Unpaid" };
  return `<span class="badge badge-${status}">${map[status] || status}</span>`;
}

function renderOrders() {
  const q = document.getElementById("orderSearch").value.trim().toLowerCase();
  const rows = ordersCache.filter((o) => {
    const matchesFilter = activeOrderStatusFilter === "all" || o.link_status === activeOrderStatusFilter;
    const matchesSearch = !q
      || clientName(o.client_id).toLowerCase().includes(q)
      || websiteDomain(o.website_id).toLowerCase().includes(q)
      || o.anchor_text.toLowerCase().includes(q);
    return matchesFilter && matchesSearch;
  });

  const body = document.getElementById("ordersBody");
  body.innerHTML = rows.map((o) => `
    <tr>
      <td>#${o.id}</td>
      <td class="font-ui">${escapeHtml(clientName(o.client_id))}</td>
      <td class="font-ui">${escapeHtml(websiteDomain(o.website_id))}</td>
      <td class="font-ui">${escapeHtml(o.anchor_text)}</td>
      <td>$${o.price.toFixed(2)}</td>
      <td>$${o.paid_amount.toFixed(2)}</td>
      <td>${paymentBadge(o.payment_status)}</td>
      <td>${linkBadge(o.link_status)}</td>
      <td>
        <div class="row-actions">
          <button class="btn-mini" onclick="openCheckModal(${o.id})">Check Link</button>
          <button class="btn-mini" onclick="openPaymentModal(${o.id})">Add Payment</button>
          <button class="btn-mini danger" onclick="deleteOrder(${o.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join("") || `<tr><td colspan="9" class="font-ui muted">No matching orders.</td></tr>`;
}

document.getElementById("orderSearch").addEventListener("input", renderOrders);

document.querySelectorAll("#statusChips .chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll("#statusChips .chip").forEach((c) => c.classList.remove("active"));
    chip.classList.add("active");
    activeOrderStatusFilter = chip.dataset.filter;
    renderOrders();
  });
});

document.getElementById("orderForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api.createOrder({
      client_id: parseInt(document.getElementById("orderClient").value, 10),
      website_id: parseInt(document.getElementById("orderWebsite").value, 10),
      target_link: document.getElementById("orderTargetLink").value,
      anchor_text: document.getElementById("orderAnchor").value,
      price: parseFloat(document.getElementById("orderPrice").value),
    });
    e.target.reset();
    showToast("Order created");
    loadOrdersAndRefs();
  } catch (err) {
    showToast(err.message, "error");
  }
});

async function deleteOrder(id) {
  if (!confirm("Delete this order?")) return;
  try {
    await api.deleteOrder(id);
    showToast("Order deleted");
    loadOrdersAndRefs();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// ---- Link check modal ----
const checkModalOverlay = document.getElementById("checkModalOverlay");
function openCheckModal(orderId) {
  pendingCheckOrderId = orderId;
  document.getElementById("checkPageUrl").value = "";
  checkModalOverlay.classList.remove("hidden");
}
document.getElementById("checkModalCancel").addEventListener("click", () => {
  checkModalOverlay.classList.add("hidden");
});
document.getElementById("checkModalConfirm").addEventListener("click", async () => {
  const pageUrl = document.getElementById("checkPageUrl").value.trim();
  if (!pageUrl) return;
  try {
    await api.checkLink(pendingCheckOrderId, pageUrl);
    checkModalOverlay.classList.add("hidden");
    showToast("Link checked");
    loadOrdersAndRefs();
  } catch (err) {
    showToast(err.message, "error");
  }
});

// ---- Payment modal ----
const paymentModalOverlay = document.getElementById("paymentModalOverlay");
function openPaymentModal(orderId) {
  pendingPaymentOrderId = orderId;
  document.getElementById("paymentAmount").value = "";
  paymentModalOverlay.classList.remove("hidden");
}
document.getElementById("paymentModalCancel").addEventListener("click", () => {
  paymentModalOverlay.classList.add("hidden");
});
document.getElementById("paymentModalConfirm").addEventListener("click", async () => {
  const amount = parseFloat(document.getElementById("paymentAmount").value);
  if (!amount || amount <= 0) return;
  try {
    await api.recordPayment(pendingPaymentOrderId, amount);
    paymentModalOverlay.classList.add("hidden");
    showToast("Payment recorded");
    loadOrdersAndRefs();
  } catch (err) {
    showToast(err.message, "error");
  }
});

// ================= OVERVIEW =================
async function loadOverview() {
  const [orders, summary] = await Promise.all([api.listOrders(), api.getAnalyticsSummary()]);
  ordersCache = orders;
  clientsCache = await api.listClients();

  document.getElementById("statCollected").textContent = `$${summary.total_revenue_collected.toFixed(2)}`;
  document.getElementById("statPending").textContent = `$${summary.total_pending.toFixed(2)}`;
  document.getElementById("statOrders").textContent = summary.total_orders;
  document.getElementById("statActive").textContent = orders.filter((o) => o.link_status === "active").length;

  const recent = [...orders].sort((a, b) => b.id - a.id).slice(0, 8);
  document.getElementById("overviewOrdersBody").innerHTML = recent.map((o) => `
    <tr>
      <td class="font-ui">${escapeHtml(clientName(o.client_id))}</td>
      <td class="font-ui">${escapeHtml(websiteDomain(o.website_id))}</td>
      <td class="font-ui">${escapeHtml(o.anchor_text)}</td>
      <td>$${o.price.toFixed(2)}</td>
      <td>${linkBadge(o.link_status)}</td>
    </tr>
  `).join("") || `<tr><td colspan="5" class="font-ui muted">No orders yet.</td></tr>`;
}

// ================= ANALYTICS =================
async function loadAnalytics() {
  const summary = await api.getAnalyticsSummary();
  document.getElementById("anCollected").textContent = `$${summary.total_revenue_collected.toFixed(2)}`;
  document.getElementById("anExpected").textContent = `$${summary.total_revenue_expected.toFixed(2)}`;
  document.getElementById("anPending").textContent = `$${summary.total_pending.toFixed(2)}`;

  document.getElementById("analyticsBody").innerHTML = summary.per_client.map((c) => `
    <tr>
      <td class="font-ui">${escapeHtml(c.client_name)}</td>
      <td>${c.total_orders}</td>
      <td>$${c.total_earned.toFixed(2)}</td>
      <td>$${c.total_pending.toFixed(2)}</td>
    </tr>
  `).join("") || `<tr><td colspan="4" class="font-ui muted">No revenue data yet.</td></tr>`;
}

// ---- Utility ----
function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (m) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[m]));
}

// Initial load
loadOverview();
