// Local demo backend. Requires Node.js 18+; no npm packages or database setup.
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { randomUUID } = require("node:crypto");

const PORT = Number(process.env.PORT) || 3000;
const DATA_FILE = path.join(__dirname, "data.jsocn");
const staticFiles = {
  "/": ["index.html", "text/html; charset=utf-8"],
  "/index.html": ["index.html", "text/html; charset=utf-8"],
  "/style.css": ["style.css", "text/css; charset=utf-8"],
  "/app.js": ["app.js", "text/javascript; charset=utf-8"],
  "/LOGO.png": ["LOGO.png", "image/png"]
};

const photos = {
  books: "https://images.unsplash.com/photo-1636622812372-63074d5214d5?auto=format&fit=crop&w=850&q=78",
  calculator: "https://images.unsplash.com/photo-1710776531873-fa1c10b7a68f?auto=format&fit=crop&w=850&q=78",
  keyboard: "https://images.unsplash.com/photo-1638909067462-1310c4011610?auto=format&fit=crop&w=850&q=78",
  lamp: "https://images.unsplash.com/photo-1713281318582-53ec4ccb8aea?auto=format&fit=crop&w=850&q=78",
  bike: "https://images.unsplash.com/photo-1576855750566-29224ca31db2?auto=format&fit=crop&w=850&q=78",
  headphones: "https://images.unsplash.com/photo-1584433202630-5dc24e240130?auto=format&fit=crop&w=850&q=78"
};

function starterData() {
  const samples = [
    ["Bộ sách nhập môn Marketing", "Học tập", "Tốt", "sale", 95000, "ĐH Kinh tế Quốc dân", "Mai", "Sách có ghi chú bằng bút chì; đủ bộ 3 cuốn.", "student", photos.books],
    ["Máy tính khoa học còn tốt", "Học tập", "Tốt", "sale", 180000, "ĐHQG Hà Nội", "Minh Anh", "Máy hoạt động tốt, kèm nắp và pin đang dùng.", "student", photos.calculator],
    ["Bàn phím cơ gọn nhẹ", "Công nghệ", "Đã qua sử dụng", "trade", 0, "ĐH Bách khoa Hà Nội", "Huy", "Muốn đổi lấy giá đỡ laptop. Bạn xem và thử trước khi đổi nhé.", "student", photos.keyboard],
    ["Đèn bàn học ánh sáng ấm", "Đồ dùng", "Như mới", "sale", 120000, "ĐH Ngoại thương", "Phương", "Đèn gập gọn, có 3 mức sáng, dây sạc đi kèm.", "student", photos.lamp],
    ["Xe đạp đi học", "Di chuyển", "Tốt", "sale", 650000, "ĐH Sư phạm Hà Nội", "Nam", "Lốp và phanh còn ổn, có thể hẹn xem ở cổng trường.", "student", photos.bike],
    ["Tai nghe chụp tai giảm giá", "Công nghệ", "Như mới", "sale", 390000, "Ưu đãi đối tác · minh họa", "Cửa hàng mẫu", "Sản phẩm và mức giá chỉ để minh họa giao diện đối tác.", "retailer", photos.headphones],
    ["Combo sổ tay học kỳ mới", "Học tập", "Như mới", "sale", 79000, "Ưu đãi đối tác · minh họa", "Cửa hàng mẫu", "Tin đối tác mẫu; chưa có liên kết mua hàng thật.", "retailer", ""],
    ["Kệ sách mini để bàn", "Đồ dùng", "Tốt", "trade", 0, "ĐH Tôn Đức Thắng", "Linh", "Kệ chắc chắn, muốn đổi lấy vài cuốn tiểu thuyết hoặc cây nhỏ.", "student", ""]
  ];
  return { listings: samples.map(([title, category, condition, mode, price, campus, seller, description, source, imageUrl], index) => ({
    id: randomUUID(), title, category, condition, mode, price, campus, seller, description, source, imageUrl,
    createdAt: new Date(Date.now() - index * 3600000).toISOString()
  })), messages: [], reports: [] };
}

function saveData(value) {
  const temp = DATA_FILE + ".tmp";
  fs.writeFileSync(temp, JSON.stringify(value, null, 2), "utf8");
  fs.renameSync(temp, DATA_FILE);
}

function loadData() {
  try {
    const parsed = JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
    if (!Array.isArray(parsed.listings) || !Array.isArray(parsed.messages) || !Array.isArray(parsed.reports))
      throw new Error("data.json không hợp lệ");
    return parsed;
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    const fresh = starterData();
    saveData(fresh);
    return fresh;
  }
}

const data = loadData();

function json(res, status, value) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
  res.end(JSON.stringify(value));
}

function fail(message, status = 400) {
  const error = new Error(message);
  error.status = status;
  throw error;
}

function text(value, label, min, max) {
  if (typeof value !== "string") fail(label + " không hợp lệ.");
  const result = value.trim();
  if (result.length < min || result.length > max) fail(label + ` cần từ ${min} đến ${max} ký tự.`);
  return result;
}

function choice(value, allowed, label) {
  if (!allowed.includes(value)) fail("Hãy chọn " + label + " hợp lệ.");
  return value;
}

async function readBody(req) {
  if (!(req.headers["content-type"] || "").startsWith("application/json")) fail("Cần gửi JSON.", 415);
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > 65536) fail("Dữ liệu quá lớn.", 413);
    chunks.push(chunk);
  }
  try {
    const result = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    if (!result || typeof result !== "object" || Array.isArray(result)) fail("JSON không hợp lệ.");
    return result;
  } catch { fail("JSON không hợp lệ."); }
}

function imageUrl(value) {
  if (value === "" || value === undefined) return "";
  const url = text(value, "Liên kết ảnh", 1, 500);
  try { if (new URL(url).protocol === "https:") return url; } catch {}
  fail("Ảnh cần một liên kết HTTPS hợp lệ.");
}

function addListing(body) {
  const mode = choice(body.mode, ["sale", "trade"], "hình thức");
  const price = mode === "trade" ? 0 : Number(body.price);
  if (mode === "sale" && (!Number.isInteger(price) || price < 1000 || price > 30000000))
    fail("Giá bán phải từ 1.000 đến 30.000.000 ₫.");
  const listing = {
    id: randomUUID(),
    title: text(body.title, "Tên món đồ", 5, 80),
    category: choice(body.category, ["Học tập", "Công nghệ", "Đồ dùng", "Di chuyển"], "danh mục"),
    condition: choice(body.condition, ["Như mới", "Tốt", "Đã qua sử dụng"], "tình trạng"),
    mode, price,
    campus: text(body.campus, "Trường / khu vực", 2, 70),
    seller: text(body.seller, "Tên hiển thị", 2, 40),
    description: text(body.description, "Mô tả", 10, 800),
    imageUrl: imageUrl(body.imageUrl),
    source: "student",
    createdAt: new Date().toISOString()
  };
  data.listings.unshift(listing);
  saveData(data);
  return listing;
}

function assertListing(id) {
  if (!data.listings.some((listing) => listing.id === id)) fail("Không tìm thấy tin đăng.", 404);
}

async function api(req, res, pathname) {
  if (pathname === "/api/listings" && req.method === "GET")
    return json(res, 200, { listings: data.listings });
  if (req.method !== "POST") return json(res, 405, { error: "Phương thức không được hỗ trợ." });
  const body = await readBody(req);
  if (pathname === "/api/listings")
    return json(res, 201, { listing: addListing(body) });
  if (pathname === "/api/messages") {
    assertListing(body.listingId);
    data.messages.push({ id: randomUUID(), listingId: body.listingId,
      buyerName: text(body.buyerName, "Tên của bạn", 2, 40),
      message: text(body.message, "Lời nhắn", 10, 500), createdAt: new Date().toISOString() });
    saveData(data);
    return json(res, 201, { ok: true });
  }
  if (pathname === "/api/reports") {
    assertListing(body.listingId);
    data.reports.push({ id: randomUUID(), listingId: body.listingId,
      reason: choice(body.reason, ["misleading", "fraud", "unsafe", "other"], "lý do"),
      details: text(body.details || "", "Chi tiết", 0, 500), createdAt: new Date().toISOString() });
    saveData(data);
    return json(res, 201, { ok: true });
  }
  json(res, 404, { error: "Không tìm thấy đường dẫn." });
}

http.createServer(async (req, res) => {
  try {
    const pathname = new URL(req.url, "http://localhost").pathname;
    if (pathname.startsWith("/api/")) return await api(req, res, pathname);
    if (req.method !== "GET") return json(res, 405, { error: "Phương thức không được hỗ trợ." });
    if (!staticFiles[pathname]) return json(res, 404, { error: "Không tìm thấy tệp." });
    const [file, type] = staticFiles[pathname];
    fs.readFile(path.join(__dirname, file), (error, contents) => {
      if (error) return json(res, 404, { error: `Thiếu tệp ${file}.` });
      res.writeHead(200, { "Content-Type": type, "X-Content-Type-Options": "nosniff", "Cache-Control": "no-cache" });
      res.end(contents);
    });
  } catch (error) {
    if (!error.status) console.error(error);
    json(res, error.status || 500, { error: error.status ? error.message : "Lỗi máy chủ." });
  }
}).listen(PORT, "127.0.0.1", () => {
  console.log(`Second Chance đang chạy tại http://localhost:${PORT}`);
});