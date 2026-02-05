/**
 * Tests for health check endpoints
 */
import { GET as healthGet } from '@/app/api/health/route';
import { GET as readyGet } from '@/app/api/ready/route';

describe('Health Endpoints', () => {
  describe('/api/health', () => {
    it('should return 200 OK with correct structure', async () => {
      const response = await healthGet();
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toHaveProperty('status', 'ok');
      expect(data).toHaveProperty('service', 'frontend');
      expect(data).toHaveProperty('timestamp');
      expect(data.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    });
  });

  describe('/api/ready', () => {
    const originalEnv = process.env;

    beforeEach(() => {
      jest.resetModules();
      process.env = { ...originalEnv };
    });

    afterAll(() => {
      process.env = originalEnv;
    });

    it('should return 200 when all required env vars are set', async () => {
      process.env.DATABASE_URL = 'postgresql://test:test@localhost/test';
      process.env.BETTER_AUTH_SECRET = 'test-secret-key-min-32-characters';

      const response = await readyGet();
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toHaveProperty('status', 'ready');
      expect(data).toHaveProperty('service', 'frontend');
      expect(data).toHaveProperty('checks');
      expect(data.checks.environment).toBe('ok');
      expect(data.checks.database).toBe('n/a');
      expect(data).toHaveProperty('timestamp');
    });

    it('should return 503 when DATABASE_URL is missing', async () => {
      delete process.env.DATABASE_URL;
      process.env.BETTER_AUTH_SECRET = 'test-secret-key-min-32-characters';

      const response = await readyGet();
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data).toHaveProperty('status', 'not_ready');
      expect(data.checks.environment).toBe('failed');
      expect(data.errors).toContain('Missing required environment variable: DATABASE_URL');
    });

    it('should return 503 when BETTER_AUTH_SECRET is missing', async () => {
      process.env.DATABASE_URL = 'postgresql://test:test@localhost/test';
      delete process.env.BETTER_AUTH_SECRET;

      const response = await readyGet();
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data).toHaveProperty('status', 'not_ready');
      expect(data.checks.environment).toBe('failed');
      expect(data.errors).toContain('Missing required environment variable: BETTER_AUTH_SECRET');
    });

    it('should return 503 when all env vars are missing', async () => {
      delete process.env.DATABASE_URL;
      delete process.env.BETTER_AUTH_SECRET;

      const response = await readyGet();
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data).toHaveProperty('status', 'not_ready');
      expect(data.checks.environment).toBe('failed');
      expect(data.errors.length).toBeGreaterThan(0);
    });
  });
});
