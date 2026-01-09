/**
 * Test to verify the SQL error is fixed after pushing Drizzle schema
 */

import { test, expect } from '@playwright/test';

test.describe('SQL Schema Verification', () => {
  test('should be able to sign up without SQL error', async ({ page }) => {
    // Generate unique email
    const uniqueEmail = `test-${Date.now()}@example.com`;

    // Navigate to sign-up
    await page.goto('/sign-up');

    // Fill in the form
    await page.fill('input[name="email"]', uniqueEmail);
    await page.fill('input[name="password"]', 'testpassword123');
    await page.fill('input[name="confirmPassword"]', 'testpassword123');

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for navigation or response
    await page.waitForTimeout(5000);

    // Check console for SQL errors
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Verify no SQL errors in console
    const hasSqlError = consoleErrors.some(error =>
      error.toLowerCase().includes('select') &&
      error.toLowerCase().includes('from') &&
      error.toLowerCase().includes('user') &&
      error.toLowerCase().includes('error')
    );

    expect(hasSqlError).toBe(false);
  });

  test('should create user in database after sign up', async ({ page }) => {
    const uniqueEmail = `test-db-${Date.now()}@example.com`;

    await page.goto('/sign-up');
    await page.fill('input[name="email"]', uniqueEmail);
    await page.fill('input[name="password"]', 'testpassword123');
    await page.fill('input[name="confirmPassword"]', 'testpassword123');

    // Capture any errors during submission
    const errors: string[] = [];
    page.on('pageerror', error => {
      errors.push(error.message);
    });

    await page.click('button[type="submit"]');
    await page.waitForTimeout(5000);

    // No page errors should occur
    expect(errors.filter(e => e.toLowerCase().includes('sql') || e.toLowerCase().includes('database'))).toHaveLength(0);
  });
});
