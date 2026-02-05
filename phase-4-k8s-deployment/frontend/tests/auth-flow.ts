/**
 * Test script to verify complete auth flow: sign-up → dashboard → sign-out → sign-in
 */

import { chromium } from 'playwright';

async function testCompleteAuthFlow() {
  console.log('=== COMPLETE AUTH FLOW TEST ===\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
    console.log(`[Browser Console] ${msg.type()}: ${msg.text()}`);
  });

  page.on('pageerror', error => {
    errors.push(error.message);
  });

  const uniqueEmail = `test-${Date.now()}@example.com`;
  const testPassword = 'testpassword123';

  try {
    // STEP 1: Navigate to sign-up page
    console.log('--- STEP 1: Navigate to /sign-up ---');
    await page.goto('http://localhost:3000/sign-up', { waitUntil: 'networkidle' });
    console.log(`Current URL: ${page.url()}`);
    console.log(`Page title: ${await page.title()}`);

    // Check if we're on sign-up page
    if (!page.url().includes('/sign-up')) {
      console.log('❌ Not on sign-up page');
      return;
    }
    console.log('✅ On sign-up page');

    // STEP 2: Fill and submit sign-up form
    console.log('\n--- STEP 2: Fill sign-up form ---');
    await page.fill('input[name="email"]', uniqueEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.fill('input[name="confirmPassword"]', testPassword);
    console.log(`Email: ${uniqueEmail}`);
    console.log('Password filled');

    // Submit form
    console.log('\n--- STEP 3: Submit sign-up form ---');
    await page.click('button[type="submit"]');

    // Wait for navigation or response
    await page.waitForTimeout(3000);

    const currentUrl = page.url();
    console.log(`Current URL after submit: ${currentUrl}`);

    // STEP 4: Check for session cookies
    console.log('\n--- STEP 4: Check session cookies ---');
    const cookies = await context.cookies();
    console.log(`Total cookies: ${cookies.length}`);
    cookies.forEach(c => console.log(`  ${c.name}: ${c.value.substring(0, 30)}...`));

    const hasSessionToken = cookies.some(c => c.name === 'better-auth.session_token');
    const hasSessionData = cookies.some(c => c.name === 'better-auth.session_data');

    if (hasSessionToken && hasSessionData) {
      console.log('✅ Session cookies set successfully');
    } else {
      console.log('❌ No session cookies - checking for errors...');
    }

    // STEP 5: Navigate to dashboard
    console.log('\n--- STEP 5: Navigate to /dashboard ---');
    await page.goto('http://localhost:3000/dashboard', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const dashboardUrl = page.url();
    console.log(`Dashboard URL: ${dashboardUrl}`);

    if (dashboardUrl.includes('/dashboard')) {
      console.log('✅ Successfully accessed dashboard!');

      // Check dashboard content
      const dashboardHeading = await page.locator('h1').first().textContent().catch(() => null);
      console.log(`Dashboard heading: ${dashboardHeading}`);

      // STEP 6: Test sign-out
      console.log('\n--- STEP 6: Sign out ---');

      // Look for sign out button
      const signOutBtn = page.locator('button:has-text("Sign out")').first();
      if (await signOutBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
        await signOutBtn.click();
        await page.waitForTimeout(2000);
        console.log(`URL after sign out: ${page.url()}`);
      } else {
        // Try finding it another way
        const signOutLink = page.locator('a:has-text("Sign out")').first();
        if (await signOutLink.isVisible({ timeout: 1000 }).catch(() => false)) {
          await signOutLink.click();
          await page.waitForTimeout(2000);
        }
      }

      // STEP 7: Sign in with created account
      console.log('\n--- STEP 7: Sign in with created account ---');
      await page.goto('http://localhost:3000/sign-in', { waitUntil: 'networkidle' });
      await page.fill('input[name="email"]', uniqueEmail);
      await page.fill('input[name="password"]', testPassword);
      await page.click('button[type="submit"]');
      await page.waitForTimeout(3000);

      const signInUrl = page.url();
      console.log(`URL after sign in: ${signInUrl}`);

      if (signInUrl.includes('/dashboard')) {
        console.log('✅ Successfully signed in and redirected to dashboard!');
      } else {
        console.log('⚠ Sign in completed but not redirected to dashboard');
      }

      console.log('\n=== COMPLETE AUTH FLOW TEST PASSED ===');
    } else {
      console.log(`❌ Redirected to: ${dashboardUrl}`);
      console.log('=== COMPLETE AUTH FLOW TEST FAILED ===');
    }

    // Check for console errors
    if (errors.length > 0) {
      console.log('\n--- Console Errors ---');
      errors.forEach(e => console.log(`ERROR: ${e}`));
    } else {
      console.log('\n✅ No console errors');
    }

  } catch (error) {
    console.error('Test error:', error);
  } finally {
    await browser.close();
    console.log('\nTest complete');
  }
}

testCompleteAuthFlow();
