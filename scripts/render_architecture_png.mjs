import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error("usage: render_architecture_png.mjs <input.svg> <output.png>");
  process.exit(1);
}

const browser = await chromium.launch({ headless: true });

try {
  const page = await browser.newPage({
    viewport: { width: 1600, height: 900 },
    deviceScaleFactor: 1,
  });

  await page.goto(pathToFileURL(inputPath).href, { waitUntil: "load" });
  await page.screenshot({
    path: outputPath,
    type: "png",
    fullPage: false,
  });
} finally {
  await browser.close();
}

console.log(outputPath);
