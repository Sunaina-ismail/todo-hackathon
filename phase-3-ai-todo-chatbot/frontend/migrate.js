const { neon } = require('@neondatabase/serverless');
const fs = require('fs');
const path = require('path');

async function runMigration() {
  const sql = neon(process.env.DATABASE_URL);

  console.log('Checking existing tables...');

  try {
    // Check if tables exist
    const tables = await sql`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_name IN ('user', 'session', 'account')
    `;

    console.log('Existing tables:', tables.map(t => t.table_name));

    if (tables.length === 3) {
      console.log('✓ All Better Auth tables already exist!');
      return;
    }

    console.log('Creating Better Auth tables...');

    // Read migration file
    const migrationSQL = fs.readFileSync(
      path.join(__dirname, 'db/migrations/0000_illegal_firestar.sql'),
      'utf8'
    );

    // Split by statement breakpoint and execute each statement
    const statements = migrationSQL
      .split('--> statement-breakpoint')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    for (const statement of statements) {
      console.log('Executing:', statement.substring(0, 50) + '...');
      await sql.unsafe(statement);
    }

    console.log('✓ Migration completed successfully!');

    // Verify tables were created
    const newTables = await sql`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_name IN ('user', 'session', 'account')
    `;

    console.log('Tables after migration:', newTables.map(t => t.table_name));

  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

runMigration();
