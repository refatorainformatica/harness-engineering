# Stack pack — Android (Kotlin)

Layer on top of [java.md](./java.md) (read both; Kotlin rules there apply).

## Code docs

- KDoc in English on every class, property and function (public and private) — summary + remarks; Composables document every parameter.

## Tests

- Unit: JUnit 5/4 + MockK + Turbine (Flows) + `kotlinx-coroutines-test` (`runTest`, `StandardTestDispatcher`); no `Thread.sleep`.
- ViewModels, use cases and repositories unit-tested; Robolectric/Compose UI tests only in the instrumented/UI suite.
- Location: `src/test/java/.../features/<feature>/` mirroring the code.

## Coverage

- JaCoCo or Kover (`koverXmlReport`) → XML report per module; ≥ 80% line per module (UI-only modules: exclude generated code, not logic).

## Logging

- Timber (or the project logger) with structured messages: `Timber.i("Order processed id=%s", id)` using format args, never string templates with sensitive data; no logs of PII/tokens in release builds.

## Annotations to preserve

- `@Composable`, `@Preview`, `@HiltViewModel`, `@Inject`, `@Module`, `@Entity`, `@Dao`, `@Serializable`, `@SerialName`, `@Keep`, ProGuard/R8 rules.

## Security

- Secrets never in the APK/AAB or `BuildConfig`; tokens in EncryptedSharedPreferences/Keystore; `android:exported` explicit; network security config without cleartext.

## Structure

- Feature module or package: `feature/<feature>/` (ui, domain, data) — mirror the existing feature; ViewModels orchestrate, rules in the domain.
