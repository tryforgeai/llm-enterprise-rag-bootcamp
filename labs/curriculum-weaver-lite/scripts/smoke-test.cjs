const fs = require("node:fs");
const http = require("node:http");
const os = require("node:os");
const path = require("node:path");
const { chromium } = require("playwright");

const projectDir = path.resolve(__dirname, "..");
const outputDir = fs.mkdtempSync(path.join(os.tmpdir(), "curriculum-weaver-smoke-"));

const mimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
};

function startServer() {
  const server = http.createServer((request, response) => {
    const requestPath = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    const relativePath = requestPath === "/" ? "index.html" : requestPath.replace(/^\/+/, "");
    const filePath = path.resolve(projectDir, relativePath);
    if (!filePath.startsWith(`${projectDir}${path.sep}`)) {
      response.writeHead(403).end("Forbidden");
      return;
    }
    fs.readFile(filePath, (error, content) => {
      if (error) {
        response.writeHead(error.code === "ENOENT" ? 404 : 500).end(error.message);
        return;
      }
      response.writeHead(200, { "Content-Type": mimeTypes[path.extname(filePath)] || "application/octet-stream" });
      response.end(content);
    });
  });
  return new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

async function run() {
  const server = await startServer();
  const address = server.address();
  const baseUrl = `http://127.0.0.1:${address.port}`;
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const errors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.goto(baseUrl, { waitUntil: "networkidle" });
  const title = await page.textContent("h1");
  const pathCount = await page.locator(".path-card").count();
  await page.locator(".path-card").nth(0).click();
  const lessonTitle = await page.textContent("#lessonTitle");
  await page.locator(".quiz-button").first().click();
  const correctCount = await page.locator(".quiz-button.correct").count();
  await page.screenshot({ path: path.join(outputDir, "desktop.png"), fullPage: true });

  await page.setViewportSize({ width: 390, height: 900 });
  await page.reload({ waitUntil: "networkidle" });
  const mobilePathCount = await page.locator(".path-card").count();
  await page.screenshot({ path: path.join(outputDir, "mobile.png"), fullPage: true });
  await browser.close();
  await new Promise((resolve) => server.close(resolve));

  const result = { title, pathCount, lessonTitle, correctCount, mobilePathCount, errors, outputDir };
  fs.writeFileSync(path.join(outputDir, "result.json"), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
