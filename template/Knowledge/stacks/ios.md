# Stack pack — iOS (Swift)

Complements [standards.md](../standards.md). Frameworks: SwiftUI, UIKit, Combine, Swift Concurrency.

## Code docs (DocC)

- `///` in English on every type, property and function (public and private): summary line + discussion paragraph as remarks (rule and exception in the baseline); `- Parameters:`, `- Returns:`, `- Throws:`.
- Protocol and conforming type docs identical.

## Tests

- XCTest or Swift Testing (`@Test`, `#expect`); protocols + fakes/mocks for repositories, networking (`URLProtocol` stub) and clock; `async` tests, no `sleep`.
- Test `test_methodName_shouldExpectedBehavior_whenCondition` (or `@Test("should <behavior> when <condition>")`).
- Location: `<App>Tests/Features/<Feature>/` mirroring the code.

## Coverage

- `xcodebuild test -enableCodeCoverage YES`, export with `xcrun xccov` or `slather` (Cobertura XML); ≥ 80% line per target/package.

## Logging

- `os.Logger` with privacy markers: `logger.info("Processing order \(orderId, privacy: .public)")` — its interpolation is structured (`OSLogMessage`), the only interpolation allowed; everything personal stays `.private`; never `String(format:)`/`print`; never log tokens.

## Attributes to preserve

- `@MainActor`, `@Published`, `@State`, `@Observable`, `@objc`, `@IBOutlet`/`@IBAction`, `Codable` `CodingKeys`, property wrappers.

## Security

- Secrets never in the bundle or `Info.plist`; tokens in the Keychain; ATS enabled; universal links validated.

## Structure

- Feature: `<App>/Features/<Feature>/` (Views, ViewModels, Domain, Data) or one Swift package per feature — mirror the existing feature; views stay thin.
