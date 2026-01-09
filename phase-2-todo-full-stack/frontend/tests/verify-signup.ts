/**
 * Test script to verify sign-up stores user in database
 */

import { chromium } from 'playwright';

async function testSignUp() {
  console.log('Starting sign-up test...');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
    // Log all console messages for debugging
    console.log(`[Browser Console] ${msg.type()}: ${msg.text()}`);
  });

  page.on('pageerror', error => {
    errors.push(error.message);
  });

  try {
    // Generate unique email
    const uniqueEmail = `test-${Date.now()}@example.com`;
    console.log(`Testing sign-up with: ${uniqueEmail}`);

    // Navigate to sign-up
    console.log('Navigating to /sign-up...');
    await page.goto('http://localhost:3000/sign-up', { waitUntil: 'networkidle' });

    // Fill form
    console.log('Filling sign-up form...');
    await page.fill('input[name="email"]', uniqueEmail);
    await page.fill('input[name="password"]', 'testpassword123');
    await page.fill('input[name="confirmPassword"]', 'testpassword123');

    // Submit
    console.log('Submitting form...');
    await page.click('button[type="submit"]');

    // Wait for the form submission to complete (look for loading to finish)
    console.log('Waiting for form submission...');
    await page.waitForFunction(() => {
      const btn = document.querySelector('button[type="submit"]');
      return btn && !btn.textContent?.includes('Creating account');
    }, { timeout: 20000 }).catch(() => {
      console.log('Timeout waiting for form to complete');
    });

    // Wait a bit for cookies to be set
    await page.waitForTimeout(2000);

    // Check if cookies are set (success indicator)
    const cookies = await context.cookies();
    console.log('\n--- Cookies ---');
    cookies.forEach(c => console.log(`${c.name}: ${c.value.substring(0, 20)}...`));

    const hasSessionToken = cookies.some(c => c.name === 'better-auth.session_token');
    const hasSessionData = cookies.some(c => c.name === 'better-auth.session_data');

    if (hasSessionToken && hasSessionData) {
      console.log('\n✓ Session cookies set - Sign-up SUCCESSFUL');
      console.log('Navigating to dashboard using page.evaluate to preserve context...');

      // Use page.evaluate to navigate - this preserves cookies and context
      await page.evaluate(() => {
        window.location.href = '/dashboard';
      });

      // Wait for navigation to complete
      await page.waitForURL('**/dashboard', { timeout: 10000 }).catch(() => {
        console.log('Did not navigate to dashboard within timeout');
      });

      const dashboardUrl = page.url();
      console.log(`Current URL: ${dashboardUrl}`);

      if (dashboardUrl.includes('/dashboard')) {
        console.log('✓ Successfully accessed dashboard!');
        console.log('\n=== SIGN-UP FLOW TEST PASSED ===');
      } else {
        console.log(`⚠ Redirected to: ${dashboardUrl}`);
        console.log('\n=== SIGN-UP FLOW TEST FAILED ===');
      }

      // Check for errors
      if (errors.length > 0) {
        console.log('\n--- Console Errors ---');
        errors.forEach(e => console.log(`ERROR: ${e}`));
      } else {
        console.log('\n✓ No console errors detected');
      }
    } else {
      console.log('\n⚠ No session cookies - Sign-up may have failed');
      console.log('\n--- Console Errors ---');
      errors.forEach(e => console.log(`ERROR: ${e}`));
      console.log('\n=== SIGN-UP FLOW TEST FAILED ===');
    }

  } catch (error) {
    console.error('Test error:', error);
  } finally {
    await browser.close();
    console.log('\nTest complete');
  }
}

testSignUp();
