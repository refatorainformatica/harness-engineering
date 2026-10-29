# Tools — Test

| ID | Command / action | Notes |
|----|------------------|-------|
| `dotnet.test` | `dotnet test` | auto; feature filter/folder (`Features/<Name>/`) |
| `node.test` | `npm test` / equivalent | auto; feature paths |
| `jvm.test` | `mvn test -Dtest=<Pattern>` / `./gradlew test --tests <pattern>` | auto; feature paths (optional) |
| `python.test` | `pytest tests/features/<id>/` | auto; feature paths (optional) |
| `flutter.test` | `flutter test test/features/<id>/` | auto; feature paths |
| `go.test` | `go test ./internal/features/<feature>/... -coverprofile=coverage.out` | auto; feature paths (optional) |
| `rust.test` | `cargo test features::<feature>` / `cargo llvm-cov` | auto; feature paths (optional) |
| `php.test` | `vendor/bin/phpunit tests/Unit/Features/<Feature>` / `vendor/bin/pest` | auto; feature paths (optional) |
| `ruby.test` | `bundle exec rspec spec/features/<feature>` | auto; feature paths (optional) |
| `android.test` | `./gradlew testDebugUnitTest` | auto; unit tests only (optional) |
| `ios.test` | `xcodebuild test -scheme <Scheme> -destination '<simulator>' -enableCodeCoverage YES` / `swift test` | auto (optional) |
| `data.test` | `dbt test --target dev` + `pytest` for job code | auto; never against production (optional) |
| `test.custom` | project script | **ask** if not documented |

New tests: **always** under the feature folder (`standards.md`). Shared fixtures in `Shared/`.

Gap **AC-G\***: minimal stub in the feature folder, then the scoped test command.

Always record the ID and the result in the run LOG.
