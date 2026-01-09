# Setup Instructions for Next.js 16 Todo Frontend

## ✅ Completed Implementation Status

### Phase 1: Setup (COMPLETED) ✅
All 8 tasks (T001-T008) are complete:
- ✅ Project directory structure created
- ✅ Next.js 16 configuration files created
- ✅ Dependencies defined in package.json
- ✅ Shadcn UI configuration complete
- ✅ ESLint and Prettier configured
- ✅ Tailwind CSS with custom theme configured
- ✅ Environment variables template created
- ✅ TypeScript strict mode configured

### Phase 2: Foundational (MOSTLY COMPLETE) ✅
9 of 10 tasks (T009-T018) are complete:
- ✅ T009: types/task.ts - Task interfaces
- ✅ T010: types/filters.ts - Filter and pagination types
- ✅ T011: types/auth.ts - Authentication types
- ✅ T012: types/api.ts - API client types
- ✅ T013: lib/api-client.ts - Full API client with JWT
- ✅ T014: lib/auth-client.ts - Better Auth configuration
- ✅ T015: lib/utils.ts - Utility functions
- ⏳ T016: components/ui/* - Shadcn UI components (requires npm install)
- ✅ T017: app/layout.tsx - Root layout
- ✅ T018: app/page.tsx - Home page redirect

## 🚀 Next Steps to Complete Setup

### Step 1: Install Dependencies

```bash
cd /mnt/d/todo-hackathon/phase-2-todo-full-stack/frontend
npm install
```

This will install:
- Next.js 16
- React 19
- Better Auth v1.0.0
- Tailwind CSS
- TypeScript
- All other dependencies

### Step 2: Install Shadcn UI Components (T016)

```bash
npx shadcn@latest add button input label dialog select card badge skeleton toast checkbox textarea
```

This completes Task T016 and creates all required UI components in `components/ui/`.

### Step 3: Configure Environment Variables

Edit `.env.local` and set your `BETTER_AUTH_SECRET`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<copy-from-backend-env-file>
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**CRITICAL**: The `BETTER_AUTH_SECRET` must match the value in your FastAPI backend's `.env` file.

### Step 4: Verify TypeScript Compilation

```bash
npm run type-check
```

This should complete without errors once dependencies are installed.

### Step 5: Start Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

## 📁 Created Files Summary

### Configuration Files (Phase 1)
```
✅ package.json - Dependencies and scripts
✅ tsconfig.json - TypeScript strict mode config
✅ next.config.ts - Next.js configuration
✅ tailwind.config.ts - Tailwind CSS with Shadcn UI theme
✅ postcss.config.mjs - PostCSS configuration
✅ .env.local - Environment variables template
✅ .eslintrc.json - ESLint configuration
✅ .prettierrc - Prettier configuration
✅ .gitignore - Git ignore patterns
✅ components.json - Shadcn UI configuration
✅ app/globals.css - Global styles with Shadcn UI variables
✅ README.md - Project documentation
```

### TypeScript Types (Phase 2)
```
✅ types/task.ts - Task, TaskCreate, TaskUpdate, TagWithUsage
✅ types/filters.ts - TaskFilters, PaginationMeta, TaskListResponse
✅ types/auth.ts - UserSession, SignUpForm, SignInForm
✅ types/api.ts - APIRequestConfig, APIError, APIClientError
```

### Library Files (Phase 2)
```
✅ lib/api-client.ts - Full-featured API client with JWT
✅ lib/auth-client.ts - Better Auth client configuration
✅ lib/utils.ts - Utility functions (cn, formatDate, etc.)
```

### App Files (Phase 2)
```
✅ app/layout.tsx - Root layout with Toaster
✅ app/page.tsx - Home page with auth redirect
```

### Directory Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── dashboard/
│   ├── api/auth/[...all]/
│   ├── layout.tsx ✅
│   ├── page.tsx ✅
│   └── globals.css ✅
├── actions/
├── components/
│   ├── auth/
│   ├── dashboard/
│   ├── tasks/
│   ├── layout/
│   └── ui/ (populated after npx shadcn add)
├── lib/
│   ├── api-client.ts ✅
│   ├── auth-client.ts ✅
│   └── utils.ts ✅
├── types/
│   ├── task.ts ✅
│   ├── filters.ts ✅
│   ├── auth.ts ✅
│   └── api.ts ✅
├── .env.local ✅
├── .eslintrc.json ✅
├── .gitignore ✅
├── .prettierrc ✅
├── components.json ✅
├── next.config.ts ✅
├── package.json ✅
├── postcss.config.mjs ✅
├── README.md ✅
├── tailwind.config.ts ✅
└── tsconfig.json ✅
```

## 🔧 What Works Now

After running `npm install` and `npx shadcn add ...`:

1. ✅ **TypeScript Types**: All interfaces defined for Tasks, Filters, Auth
2. ✅ **API Client**: Full-featured client with JWT auto-attachment
3. ✅ **Better Auth**: Client configured for JWT authentication
4. ✅ **Utilities**: Date formatting, cn() helper for Tailwind
5. ✅ **Root Layout**: Global layout with Toaster provider
6. ✅ **Home Page**: Redirect logic (authenticated → dashboard, guest → sign-in)

## ⏭️ What's Next (Phase 3+)

After completing setup, you can implement user stories:

- **Phase 3 (US1)**: Authentication pages (sign-up, sign-in)
- **Phase 4 (US2)**: Dashboard and task list
- **Phase 5 (US3)**: Task creation form
- **Phase 6-10 (US4-US8)**: Task actions, search/filter, tags

See `specs/003-todo-frontend/tasks.md` for full task list.

## 🐛 Troubleshooting

### Dependencies Not Installing
- Check Node.js version: `node --version` (requires 18+)
- Try: `rm -rf node_modules package-lock.json && npm install`

### TypeScript Errors
- Run: `npm run type-check` to see all errors
- Ensure all files are created as listed above

### Shadcn UI Components Not Found
- Run: `npx shadcn@latest add <component-name>`
- Check `components/ui/` directory exists

### Better Auth Errors
- Verify `BETTER_AUTH_SECRET` matches backend
- Check `.env.local` file exists and is not in .gitignore

## 📚 Documentation

- [Feature Spec](../../specs/003-todo-frontend/spec.md)
- [Implementation Plan](../../specs/003-todo-frontend/plan.md)
- [Data Model](../../specs/003-todo-frontend/data-model.md)
- [API Contracts](../../specs/003-todo-frontend/contracts/api-contracts.md)
- [Tasks](../../specs/003-todo-frontend/tasks.md)
- [Quick Start](../../specs/003-todo-frontend/quickstart.md)

## ✨ Summary

**Phase 1 & 2 Implementation: COMPLETE (except T016 - requires npm install)**

- 17 of 18 tasks completed
- All core files created
- Ready for user story implementation after dependency installation

Run these 3 commands to complete setup:
```bash
npm install
npx shadcn@latest add button input label dialog select card badge skeleton toast checkbox textarea
npm run dev
```
