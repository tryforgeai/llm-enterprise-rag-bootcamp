const fs = require("fs");
const { chromium } = require("/Users/rosso.han/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

async function run() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const errors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  page.on("pageerror", (error) => errors.push(error.message));

  await page.goto("http://127.0.0.1:4177", { waitUntil: "networkidle" });
  const title = await page.textContent("h1");
  const pathCount = await page.locator(".path-card").count();
  await page.locator(".path-card").nth(0).click();
  const lessonTitle = await page.textContent("#lessonTitle");
  await page.locator(".quiz-button").first().click();
  const correctCount = await page.locator(".quiz-button.correct").count();
  await page.screenshot({ path: "/tmp/curriculum-weaver-desktop.png", fullPage: true });

  await page.setViewportSize({ width: 390, height: 900 });
  await page.reload({ waitUntil: "networkidle" });
  const mobilePathCount = await page.locator(".path-card").count();
  await page.screenshot({ path: "/tmp/curriculum-weaver-mobile.png", fullPage: true });
  await browser.close();

  const result = { title, pathCount, lessonTitle, correctCount, mobilePathCount, errors };
  fs.writeFileSync("/tmp/curriculum-weaver-smoke.json", JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
