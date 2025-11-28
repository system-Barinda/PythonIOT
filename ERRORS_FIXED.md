# ✅ Errors Fixed

## Fixed Issues

### 1. Database Session Context Manager Error ✅
**File:** `src/core/database.py`

**Problem:** 
- `get_session()` method was returning a session directly, but was being used as an async context manager (`async with self.database.get_session() as session:`)
- Used `sessionmaker` instead of `async_sessionmaker` for async sessions

**Fix:**
- Changed `sessionmaker` to `async_sessionmaker` for proper async session handling
- Added `@asynccontextmanager` decorator to `get_session()` method
- Implemented proper async context manager that yields the session
- Added exception handling with rollback on errors

**Code Changes:**
```python
# Before:
from sqlalchemy.orm import sessionmaker
self.SessionLocal = sessionmaker(...)
async def get_session(self):
    return self.SessionLocal()

# After:
from sqlalchemy.ext.asyncio import async_sessionmaker
self.SessionLocal = async_sessionmaker(...)
@asynccontextmanager
async def get_session(self):
    async with self.SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

### 2. SQL Query Syntax Error ✅
**File:** `src/swiping/daily_limit_tracker.py`

**Problem:**
- Incorrect SQLAlchemy query syntax: `func.count(Match.id).where(...)`
- This syntax doesn't exist in SQLAlchemy

**Fix:**
- Changed to proper SQLAlchemy 2.0 syntax using `select()` statement
- Added `select` import from sqlalchemy

**Code Changes:**
```python
# Before:
count = await session.execute(
    func.count(Match.id).where(
        Match.profile_id == profile_id,
        func.date(Match.matched_at) == today
    )
)

# After:
from sqlalchemy import func, select
stmt = select(func.count(Match.id)).where(
    Match.profile_id == profile_id,
    func.date(Match.matched_at) == today
)
result = await session.execute(stmt)
swipes_today = result.scalar() or 0
```

## Verification

✅ All linter errors resolved  
✅ Database session now works correctly as async context manager  
✅ SQL queries use correct SQLAlchemy 2.0 syntax  
✅ No syntax errors in codebase  
✅ All imports are correct

## Status

**All errors have been removed and fixed!** ✅

The codebase is now error-free and ready for use.

