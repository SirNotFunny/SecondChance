const $ = (selector) => document.querySelector(selector);
const state = { listings: [], category: "all", source: "all", savedOnly: false, saved: new Set() };
let selectedListing = null;
let toastTimer;

try { state.saved = new Set(JSON.parse(localStorage.getItem("secondChanceSaved") || "[]")); }
catch { state.saved = new Set(); }

const symbols = { "Học tập": "📚", "Công nghệ": "🎧", "Đồ dùng": "💡", "Di chuyển": "🚲" };
const tones = { "Học tập": "tone-1", "Công nghệ": "tone-2", "Đồ dùng": "tone-3", "Di chuyển": "tone-4" };
const money = (number) => new Intl.NumberFormat("vi-VN").format(number) + " ₫";
const priceText = (item) => item.mode === "trade" ? "Trao đổi" : money(item.price);
const fold = (text) => String(text || "").toLowerCase().normalize("NFD")
  .replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d");

function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}

function media(item, large = false) {
  const box = element("div", (large ? "detail-media " : "card-media ") + (tones[item.category] || "tone-1"));
  box.append(element("span", "item-symbol", symbols[item.category] || "♻"));
  if (item.imageUrl) {
    const image = document.createElement("img");
    image.src = item.imageUrl;
    image.alt = item.title;
    image.loading = "lazy";
    image.onerror = () => image.remove();
    box.append(image);
  }
  return box;
}

function card(item) {
  const article = element("article", "card");
  const open = element("button", "card-open");
  open.type = "button";
  open.setAttribute("aria-label", "Xem chi tiết " + item.title);
  const picture = media(item);
  picture.append(element("span", "card-badge" + (item.source === "retailer" ? " partner" : ""),
    item.source === "retailer" ? "Ưu đãi đối tác · minh họa" : item.mode === "trade" ? "Có thể trao đổi" : "Từ sinh viên"));
  open.append(picture);
  const body = element("span", "card-copy");
  body.append(element("span", "card-category", item.category),
    element("span", "card-title", item.title),
    element("strong", "card-price", priceText(item)),
    element("span", "card-meta", "⌖ " + item.campus + " · " + item.condition));
  open.append(body);
  open.addEventListener("click", () => showDetails(item));
  const save = element("button", "save", state.saved.has(item.id) ? "♥" : "♡");
  save.type = "button";
  save.setAttribute("aria-label", state.saved.has(item.id) ? "Bỏ lưu " + item.title : "Lưu " + item.title);
  save.setAttribute("aria-pressed", String(state.saved.has(item.id)));
  save.addEventListener("click", () => {
    state.saved.has(item.id) ? state.saved.delete(item.id) : state.saved.add(item.id);
    try { localStorage.setItem("secondChanceSaved", JSON.stringify([...state.saved])); } catch {}
    render();
  });
  article.append(open, save);
  return article;
}

function render() {
  const query = fold($("#search").value.trim());
  const maxPrice = $("#max-price").value;
  const sort = $("#sort").value;
  let items = state.listings.filter((item) =>
    (state.category === "all" || item.category === state.category) &&
    (state.source === "all" || (state.source === "trade" ? item.mode === "trade" : item.source === state.source)) &&
    (!state.savedOnly || state.saved.has(item.id)) &&
    (maxPrice === "all" || item.mode === "trade" || item.price <= Number(maxPrice)) &&
    fold(item.title + " " + item.description + " " + item.campus).includes(query));
  items.sort((a, b) => sort === "low" ? a.price - b.price : sort === "high" ? b.price - a.price :
    new Date(b.createdAt) - new Date(a.createdAt));
  $("#listing-grid").replaceChildren(...items.map(card));
  $("#empty-state").hidden = items.length > 0;
  $("#result-count").textContent = items.length + " món đồ";
  $("#saved-count").textContent = state.saved.size;
  $("#saved-toggle").setAttribute("aria-pressed", String(state.savedOnly));
}

function showDetails(item) {
  selectedListing = item;
  const picture = media(item, true);
  picture.id = "detail-media";
  $("#detail-media").replaceWith(picture);
  $("#detail-badge").textContent = item.source === "retailer" ? "ƯU ĐÃI ĐỐI TÁC · MINH HỌA" : "TIN SINH VIÊN";
  $("#detail-title").textContent = item.title;
  $("#detail-price").textContent = priceText(item);
  $("#detail-description").textContent = item.description;
  $("#detail-condition").textContent = item.condition;
  $("#detail-campus").textContent = item.campus;
  $("#detail-seller").textContent = item.seller;
  $("#message-form").reset();
  $("#report-form").reset();
  $("#message-status").textContent = "";
  $("#report-status").textContent = "";
  $(".report").open = false;
  $("#detail-dialog").showModal();
}

function setActive(group, key, value) {
  group.querySelectorAll("button").forEach((button) => {
    const active = button.dataset[key] === value;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

function resetFilters() {
  state.category = "all";
  state.source = "all";
  state.savedOnly = false;
  $("#search").value = "";
  $("#max-price").value = "all";
  $("#sort").value = "newest";
  setActive($("#categories"), "category", "all");
  setActive($("#sources"), "source", "all");
  render();
}

async function request(url, payload) {
  const response = await fetch(url, payload ? {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
  } : undefined);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Có lỗi xảy ra. Vui lòng thử lại.");
  return data;
}

function feedback(selector, message, error = false) {
  const node = $(selector);
  node.textContent = message;
  node.classList.toggle("error", error);
}

function toast(message) {
  const node = $("#toast");
  node.textContent = message;
  node.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => node.classList.remove("show"), 3500);
}

$("#categories").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-category]");
  if (!button) return;
  state.category = button.dataset.category;
  setActive($("#categories"), "category", state.category);
  render();
});
$("#sources").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-source]");
  if (!button) return;
  state.source = button.dataset.source;
  setActive($("#sources"), "source", state.source);
  render();
});
$("#saved-toggle").addEventListener("click", () => { state.savedOnly = !state.savedOnly; render(); $("#explore").scrollIntoView(); });
$("#reset-filters").addEventListener("click", resetFilters);
for (const selector of ["#search", "#max-price", "#sort"]) {
  $(selector).addEventListener(selector === "#search" ? "input" : "change", render);
}

document.querySelectorAll("[data-open-post]").forEach((button) => button.addEventListener("click", () => $("#post-dialog").showModal()));
document.querySelectorAll("[data-close]").forEach((button) => button.addEventListener("click", () => button.closest("dialog").close()));
document.querySelectorAll("dialog").forEach((dialog) => dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
}));

$("#mode").addEventListener("change", () => {
  const trade = $("#mode").value === "trade";
  const price = $("#post-form").elements.price;
  $("#price-label").hidden = trade;
  price.disabled = trade;
  price.required = !trade;
  if (trade) price.value = "0";
  else price.value = "";
});

$("#post-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form));
  data.price = data.mode === "trade" ? 0 : Number(data.price);
  const button = form.querySelector("button[type=submit]");
  button.disabled = true;
  feedback("#post-status", "Đang lưu tin...");
  try {
    const result = await request("/api/listings", data);
    state.listings.unshift(result.listing);
    form.reset();
    $("#mode").dispatchEvent(new Event("change"));
    $("#post-dialog").close();
    resetFilters();
    $("#explore").scrollIntoView();
    toast("Đã đăng tin thử nghiệm thành công.");
  } catch (error) { feedback("#post-status", error.message, true); }
  finally { button.disabled = false; }
});

$("#message-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    await request("/api/messages", { listingId: selectedListing.id, ...Object.fromEntries(new FormData(form)) });
    form.reset();
    feedback("#message-status", "Đã lưu lời nhắn trong bản mẫu; chưa chuyển đến người bán.");
  } catch (error) { feedback("#message-status", error.message, true); }
});

$("#report-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    await request("/api/reports", { listingId: selectedListing.id, ...Object.fromEntries(new FormData(form)) });
    form.reset();
    feedback("#report-status", "Đã lưu báo cáo trong bản mẫu.");
  } catch (error) { feedback("#report-status", error.message, true); }
});

request("/api/listings")
  .then((data) => {
    state.listings = data.listings;
    render();
  })
  .catch((error) => {
    console.error("Product display error:", error);
    $("#result-count").textContent = "Lỗi hiển thị";
    $("#listing-grid").textContent =
      "Lỗi hiển thị sản phẩm: " + error.message;
  });