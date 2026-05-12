"""
BusinessRuleError  → 422 with { error: message, code: "BUSINESS_RULE_VIOLATION" }
NotFoundError      → 404 with { error: message, code: "NOT_FOUND" }
AuthError          → 401 with { error: message, code: "UNAUTHORIZED" }
ValidationError    → 422 (Pydantic errors, auto-handled by FastAPI)
Exception          → log full traceback internally
                     return 500 { error: "Internal server error", code: "INTERNAL_ERROR" }
                     (never the actual exception message)
"""
