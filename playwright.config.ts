import { defineConfig } from '@playwright/test';

/**
 * Testes de ponta a ponta do app web. Rodam com:  npm run test:e2e
 * (compila o app em dist/ e sobe um servidor local). Por padrão usa o Chromium do Playwright
 * (npx playwright install chromium). Se você já tem o Edge ou o Chrome:  E2E_CHANNEL=msedge npm run test:e2e
 */
export default defineConfig({
  testDir: './e2e',
  timeout: 90_000,
  retries: 0,
  reporter: [['list']],
  use: { baseURL: 'http://localhost:4173', channel: process.env.E2E_CHANNEL || undefined, viewport: { width: 420, height: 860 }, trace: 'retain-on-failure' },
  webServer: { command: 'node scripts/servir-web.mjs', url: 'http://localhost:4173', reuseExistingServer: true, timeout: 30_000 },
});
