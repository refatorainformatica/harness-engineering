# Stack pack — Java / Kotlin (JVM)

Complements [standards.md](../standards.md). Frameworks: Spring Boot, Quarkus, Micronaut, Jakarta EE.

## Code docs (Javadoc / KDoc)

- `/** ... */` in English: first sentence = summary; next paragraph = remarks (rule and exception in the baseline); `@param`, `@return`, `@throws`.
- Interface ↔ implementation with the same member docs.
- Package = physical folder (`com.acme.<app>.features.<feature>`).

## Tests

- JUnit 5 + Mockito (+ AssertJ); Kotlin: JUnit 5 + MockK (+ Kotest assertions) — or whatever the project already uses.
- Class `{ClassName}Test`; method `methodName_shouldExpectedBehavior_whenCondition` (or `@DisplayName` in English).
- Integration: `IT` suffix / Testcontainers only in integration tests — unit tests without a real database.
- No `Thread.sleep`; clock via injected `Clock`; Awaitility when asynchronous.
- Command: `mvn test` / `./gradlew test --tests '*features.<feature>*'`.

## Coverage

- JaCoCo (`jacoco-maven-plugin` / Gradle `jacoco`) → `target/site/jacoco/jacoco.xml` / `build/reports/jacoco/test/jacocoTestReport.xml`; ≥ 80% line per module, enforced with `jacoco:check`/`jacocoTestCoverageVerification`.

## Logging

- SLF4J with placeholders: `log.info("Processing order {}", orderId)`; Kotlin: `logger.info { "..." }` only lazily + structured fields when the project adopts it.
- Never concatenation (`"..." + x`) nor `String.format` in the message; exception as the last argument.

## Annotations

- Preserve class and field annotations (`@Entity`, `@Table`, `@Column`, `@JsonProperty`, `@RestController`, `@Transactional`, `@Valid`, `@NotNull`, …).

## Structure

- Feature: `src/main/java/.../features/<feature>/` (controller, application/service, domain, repository) — mirror the existing feature; tests in `src/test/java/.../features/<feature>/`.
- Controllers and application services only orchestrate; rules live in entities/value objects.
