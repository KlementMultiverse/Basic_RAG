# Project Notes

## Issues

### Issue #1: Async/Await Mismatch in 1_setup.py
**Status**: Closed  
**File**: 1_setup.py:11-12  
**Description**: Function `main()` is defined as `async` but the OpenAI client call is synchronous (not awaited). Either remove `async` from function definition or use async OpenAI client properly.  
**Priority**: Medium