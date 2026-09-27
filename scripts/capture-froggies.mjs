// Captures Froggies screens for scripts/froggies_card.py:
//   node scripts/capture-froggies.mjs build/froggies-raw 1440 900 d   (desktop: home, lobby, board)
//   node scripts/capture-froggies.mjs build/froggies-raw 390 844 m    (phone: home)
// Uses the Playwright install from the meui-creative repo.
import { chromium } from '/Users/matejhrabal/DEV/meui-creative/node_modules/playwright/index.mjs';
const [,, S, w, h, tag] = process.argv;
import { mkdirSync } from "node:fs"; mkdirSync(`${S}/frog`, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2, hasTouch: +w < 600, isMobile: +w < 600 });
await p.goto('https://froggies.meui.cz', { waitUntil: 'networkidle' });
await p.waitForTimeout(3000);
await p.screenshot({ path: `${S}/frog/${tag}-0-home.png` });
await p.getByRole('button', { name: /Play solo/ }).first().click();
await p.waitForTimeout(1500);
for (let i = 0; i < 2; i++) { const add = p.getByRole('button', { name: 'Add a bot' }).first(); if (await add.count()) await add.click(); await p.waitForTimeout(400); }
await p.screenshot({ path: `${S}/frog/${tag}-1-lobby.png` });
await p.getByRole('button', { name: /hop in/ }).click();
for (const t of [2500, 3000, 4000, 6000]) { await p.waitForTimeout(t); await p.screenshot({ path: `${S}/frog/${tag}-2-game-${t}.png` }); }
const pts = JSON.parse(process.env.CLICKS || '[]');
for (const [i, [x, y]] of pts.entries()) { await p.mouse.click(x, y); await p.waitForTimeout(1800); await p.screenshot({ path: `${S}/frog/${tag}-3-move-${i}.png` }); }
console.log((await p.evaluate(() => document.body.innerText)).slice(0, 500));
await b.close();
