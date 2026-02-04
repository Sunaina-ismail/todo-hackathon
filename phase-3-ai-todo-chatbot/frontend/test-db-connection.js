const { neon } = require('@neondatabase/serverless');

async function testConnection() {
  const DATABASE_URL = process.env.DATABASE_URL || 'postgresql://neondb_owner:npg_xAYEF3qM6ZaN@ep-restless-mode-ah98zjld-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require';

  console.log('Testing Neon connection...');
  console.log('Using DATABASE_URL:', DATABASE_URL.replace(/:[^:@]+@/, ':****@'));

  try {
    const sql = neon(DATABASE_URL);

    // Test simple query
    console.log('\n1. Testing simple query...');
    const result = await sql`SELECT NOW() as current_time`;
    console.log('✓ Connection successful!');
    console.log('Current time:', result[0].current_time);

    // Test user table query
    console.log('\n2. Testing user table query...');
    const users = await sql`SELECT COUNT(*) as count FROM "user"`;
    console.log('✓ User table accessible!');
    console.log('User count:', users[0].count);

    // Test the exact query that's failing
    console.log('\n3. Testing the exact failing query...');
    const testEmail = 'test@example.com';
    const userQuery = await sql`
      SELECT "id", "name", "email", "email_verified", "image", "created_at", "updated_at"
      FROM "user"
      WHERE "user"."email" = ${testEmail}
    `;
    console.log('✓ Query successful!');
    console.log('Result:', userQuery);

    console.log('\n✓ All tests passed! Database connection is working.');

  } catch (error) {
    console.error('\n✗ Connection failed:', error);
    console.error('Error details:', {
      message: error.message,
      code: error.code,
      cause: error.cause
    });
    process.exit(1);
  }
}

testConnection();
