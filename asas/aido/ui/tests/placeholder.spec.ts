import { expect, test } from "@playwright/test";

test.skip("placeholder", async ({ page }) => {
  await page.route("**/api/sessions**", (route) =>
    route.fulfill({ status: 200, body: JSON.stringify({ sessions: [] }) })
  );
  await page.route("**/api/copilotkit**", (route) =>
    route.fulfill({ status: 200, body: JSON.stringify({}) })
  );

  await page.goto("/", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(1000);
  await expect(page.getByRole("heading", { name: "AIDO Control Center" })).toBeVisible();
});
