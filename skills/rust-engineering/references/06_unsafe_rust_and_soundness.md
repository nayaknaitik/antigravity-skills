# Unsafe Rust, Soundness Guidelines & FFI Boundaries Reference

## 1. Overview
This reference guide establishes strict guidelines for writing, auditing, and validating `unsafe` Rust code, enforcing safety invariants, sound APIs, and Miri testing.

---

## 2. Fundamental Unsafe Rules

1. **Default Constraint**: Enforce `#![deny(unsafe_code)]` at the workspace level.
2. **Justification Requirement**: If `unsafe` is strictly necessary (e.g. SIMD vectorization, FFI bindings, zero-copy pointer slice casting), it MUST be isolated inside a safe wrapper abstraction.
3. **Mandatory Safety Documentation**: Every `unsafe` block MUST contain a `// SAFETY:` comment explicitly listing the invariant preconditions fulfilled.

### Correct Safety Comment Example:
```rust
// SAFETY:
// 1. `ptr` is non-null and properly aligned for `Header` (checked at allocation time).
// 2. The memory referenced by `ptr` is valid for reads up to `size` bytes.
// 3. No mutable references exist for the lifetime `'a`.
let header: &Header = unsafe { &*(ptr as *const Header) };
```

---

## 3. Soundness vs Undefined Behavior (UB)

An API is **sound** if it is impossible to cause Undefined Behavior (UB) through safe code, regardless of parameters passed.

### Common Sources of UB to Avoid:
- Dereferencing null or dangling pointers.
- Creating aliased `&mut` references to the same memory location.
- Violating memory alignment requirements.
- Data races (concurrent non-atomic read/write to same memory).
- Uninitialized memory reads (`std::mem::uninitialized` is deprecated - use `MaybeUninit`).

---

## 4. Miri Verification Tooling

Verify all unsafe pointer manipulation with Miri:
```bash
cargo miri test
```
