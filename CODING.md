# Nebula Coding Standards

This document defines coding conventions, architectural principles, and workflow guidelines for the Nebula project.

## Table of Contents
1. [General Principles](#general-principles)
2. [Code Style](#code-style)
3. [Architecture](#architecture)
4. [Naming Conventions](#naming-conventions)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Git Workflow](#git-workflow)
8. [Security](#security)

---

## General Principles

### 1. Collaboration First
- **No unilateral decisions.** Architectural changes require discussion.
- **Document trade-offs.** When proposing options, explain pros/cons.
- **Readable over clever.** Code should be understood by humans first.

### 2. YAGNI (You Aren't Gonna Need It)
- Build for current requirements, not hypothetical future needs.
- Add complexity only when justified by actual use cases.
- Refactor when patterns emerge, not before.

### 3. Fail Fast, Fail Loud
- Validate inputs at boundaries.
- Use checked exceptions for recoverable errors.
- Use unchecked exceptions for programming errors.
- Never swallow exceptions silently.

---

## Code Style

### Java

#### Formatting
- **Indentation:** 4 spaces (no tabs)
- **Line length:** 120 characters max
- **Braces:** K&R style (opening brace on same line)
- **Imports:** No wildcard imports, organize by IDE

```java
// Good
public class TransactionService {
    private final TransactionRepository repository;
    
    public Transaction getTransaction(String id) {
        return repository.findById(id)
            .orElseThrow(() -> new NotFoundException("Transaction not found: " + id));
    }
}

// Bad - inconsistent formatting, swallowed exception
public class TransactionService{
private final TransactionRepository repository;
public Transaction getTransaction(String id){
try{return repository.findById(id).get();}catch(Exception e){return null;}
}
}
```

#### Language Features
- **Prefer `var`** for local variables when type is obvious
- **Use `Optional`** instead of null checks
- **Use `record`** for DTOs and value objects
- **Prefer `List.of()`, `Map.of()`** for immutable collections

```java
// Good
public record Transaction(String id, BigDecimal amount, String merchant) {}

public Optional<Transaction> findById(String id) {
    var transaction = repository.findById(id);
    return Optional.ofNullable(transaction);
}

// Bad
public class Transaction {
    private String id;
    public Transaction(String id) { this.id = id; }
    // getters/setters for immutable data
}
```

---

## Architecture

### Layered Architecture
```
Controller → Service → Repository → Database
     ↓            ↓
   DTOs         Domain
```

**Controller Layer**
- Handle HTTP concerns only
- Map requests/responses
- Delegate to services
- No business logic

**Service Layer**
- Contains business logic
- Orchestrates repositories
- Transaction boundaries
- No HTTP or database specifics

**Repository Layer**
- Data access only
- Return domain objects
- Hide query complexity

### Dependency Direction
Dependencies must point inward:
- Controllers depend on Services
- Services depend on Repositories
- Domain has no dependencies

### Configuration
- Externalize configuration to `application.yml`
- Use `@ConfigurationProperties` for typed config
- No hardcoded values in code

---

## Naming Conventions

### Classes
| Type | Pattern | Example |
|------|---------|---------|
| Service | `XxxService` | `TransactionService` |
| Repository | `XxxRepository` | `TransactionRepository` |
| Controller | `XxxController` | `TransactionController` |
| DTO | `XxxRequest/Response/Dto` | `CreateTransactionRequest` |
| Exception | `XxxException` | `TransactionNotFoundException` |
| Config | `XxxConfig/Properties` | `GoCardlessProperties` |

### Methods
- **Verbs for actions:** `createTransaction()`, `findById()`
- **Predicates for booleans:** `isValid()`, `hasPermission()`
- **Getters for accessors:** `getTransaction()` (not `fetchTransaction()`)

### Variables
- **Local variables:** camelCase, descriptive
- **Constants:** UPPER_SNAKE_CASE
- **Avoid abbreviations:** `transaction` not `txn`

---

## Testing

### Required Test Types

Every feature must include:

1. **Unit Tests** — Fast, isolated, test business logic
2. **Integration Tests** — Test database/repository layer, API contracts
3. **Functional Tests (Cucumber)** — End-to-end scenarios, user journeys

```
    /\
   /  \  Cucumber E2E (critical paths)
  /----\ Integration Tests (repositories, APIs)
 /______\ Unit Tests (business logic) — majority
```

### Test Structure

```
src/
├── main/java/... (production code)
├── test/
│   ├── java/
│   │   ├── unit/           # Unit tests (JUnit 5)
│   │   ├── integration/    # Integration tests (Spring Boot Test)
│   │   └── cucumber/       # Feature tests (Cucumber)
│   └── resources/
│       ├── features/       # .feature files for Cucumber
│       └── application-test.yml
```

### Unit Tests
- Test one thing per test
- Use `@DisplayName` for readable test names
- Mock external dependencies
- Fast execution (< 100ms per test)

```java
@DisplayName("Transaction Service")
class TransactionServiceTest {
    
    @Test
    @DisplayName("Should calculate points based on transaction amount")
    void shouldCalculatePointsBasedOnAmount() { }
    
    @Test
    @DisplayName("Should throw exception when transaction not found")
    void shouldThrowExceptionWhenTransactionNotFound() { }
}
```

### Integration Tests
- Use `@SpringBootTest` with test database (H2 or Testcontainers)
- Test repository queries
- Test API endpoints with `WebTestClient`
- Verify database state

### Cucumber (Functional) Tests
- Write features in Gherkin syntax
- Focus on user journeys, not implementation
- One feature file per user story
- Use Scenario Outlines for data-driven tests

```gherkin
Feature: Loyalty Points Calculation
  As a customer
  I want to earn points for my purchases
  So that I can redeem rewards

  Scenario: Customer earns points for a purchase
    Given a customer with an active loyalty account
    And a merchant offering 1 point per £1 spent
    When the customer makes a £10 purchase
    Then the customer earns 10 loyalty points
```

### Coverage Requirements
- **Unit Tests:** 80% line coverage minimum
- **Integration Tests:** All repository methods, all API endpoints
- **Cucumber Tests:** All critical user journeys (happy + unhappy paths)

### Test Data
- Use Test Data Builders pattern
- Never use production data in tests
- Each test creates its own data (no shared mutable state)

---

## Documentation

### Code Comments
- **Why, not what.** Code should be self-explanatory.
- **Public APIs:** Javadoc required
- **Complex algorithms:** Explain the approach

```java
/**
 * Calculates loyalty points for a transaction.
 * Points = floor(amount) × merchant multiplier
 * 
 * @param transaction the completed transaction
 * @return calculated points
 * @throws IllegalArgumentException if transaction is pending
 */
public int calculatePoints(Transaction transaction) { }
```

### README
- Every module has a README
- Include: purpose, setup, key classes

---

## Git Workflow

### Branches
- `main` — Production-ready code only
- `feature/xxx` — New features
- `bugfix/xxx` — Bug fixes
- `refactor/xxx` — Code improvements

### Commits
- **Atomic:** One logical change per commit
- **Message format:**
```
Type: Brief summary (50 chars)

Detailed explanation if needed.
- Why this change?
- What was the approach?
- Any breaking changes?

Refs: #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `test:` Tests
- `chore:` Maintenance

### Pull Request Strategy

#### 1. Happy Path First, Unhappy Path Second

**PR 1: Happy Path** (merge first)
- Core functionality working
- Success scenarios only
- Unit + Integration tests
- Example: "User can successfully create loyalty account"

**PR 2: Unhappy Path** (merge after PR 1)
- Error handling, edge cases
- Validation, failures
- Same tests + error scenario tests
- Example: "Handle invalid email, duplicate account"

**Why?**
- Smaller, faster reviews
- Core logic is stable sooner
- Easier to spot issues in error handling when separated

#### 2. PR Size Limits

| Metric | Maximum | Ideal |
|--------|---------|-------|
| **Lines changed** | 400 lines | 200 lines |
| **Files touched** | 15 files | 8 files |
| **Tests added** | Required | 5-10 tests |
| **Review time** | < 30 min | < 15 min |

**If PR is too big:**
- Split into smaller PRs
- One PR per logical component
- Stack PRs: PR 2 branches from PR 1

**Exception:** Refactors that are purely mechanical (rename, move) can be larger if they're 100% automated changes.

### Pull Request Checklist
- [ ] Happy path implemented and tested (PR 1)
- [ ] Unhappy path implemented and tested (PR 2)
- [ ] Cucumber tests for critical scenarios
- [ ] PR size is reasonable (< 400 lines)
- [ ] CI passes (build, tests, coverage)
- [ ] Documentation updated
- [ ] Self-reviewed before requesting review

---

## Security

### Secrets
- **Never commit secrets.** Ever.
- Store in AWS Parameter Store or Secrets Manager
- Access via `CredentialProvider` only
- Rotate credentials regularly

### Input Validation
- Validate at boundaries (controllers)
- Use bean validation (`@Valid`, `@NotNull`)
- Sanitize user inputs
- Escape outputs

### Dependencies
- Check for vulnerabilities: `mvn dependency-check:check`
- Keep dependencies updated
- Minimize dependency count

### Logging
- **Never log:** Passwords, tokens, PII
- **Do log:** Security events (auth failures, access denied)
- Use appropriate levels: `INFO` for business, `DEBUG` for dev

---

## Code Review Checklist

Before submitting PR:
- [ ] Code follows style guide
- [ ] Tests added for new logic
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] No obvious security issues
- [ ] Commit messages are clear

Reviewers check:
- [ ] Logic correctness
- [ ] Test coverage adequate
- [ ] Security implications
- [ ] Performance considerations
- [ ] Maintainability

---

## Architecture Decisions

### Decision Log

| Date | Decision | Context | Status |
|------|----------|---------|--------|
| 2026-02-08 | Java over JS | Team expertise, type safety | Accepted |
| | | | |

### Process
1. Identify architectural need
2. Present 2-3 options with trade-offs
3. Discuss (async or sync)
4. Document decision
5. Implement

---

## Questions?

When in doubt:
1. Check this document
2. Ask in the team chat
3. Propose a change to this document

**Last Updated:** 2026-02-08
**Owner:** Dominic Bao & Skylar Greyn
