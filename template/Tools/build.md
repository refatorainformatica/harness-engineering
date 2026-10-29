# Tools — Build

Adjust the commands to the project stack. Levels aligned with `Governance/permissions.md`: **auto** | **ask** | **deny**.

## Generic / files

| ID | Action | Notes |
|----|--------|-------|
| `fs.read` | Read files | auto |
| `fs.write` | Edit within scope | auto |
| `fs.delete` | Delete file | **ask** if not temp |
| `fs.write.secrets` | Edit secrets | **deny** |

## .NET (optional)

| ID | Command | Notes |
|----|---------|-------|
| `dotnet.restore` | `dotnet restore` | auto |
| `dotnet.build` | `dotnet build` | auto; prefer the touched project |
| `dotnet.format` | `dotnet format` | auto; scope only |
| `dotnet.add.package` | `dotnet add package` | **ask** |

## Node (optional)

| ID | Command | Notes |
|----|---------|-------|
| `node.install` | `npm ci` / `pnpm i` / `yarn` | auto |
| `node.build` | `npm run build` | auto |
| `node.add.dep` | add dependency | **ask** |

## Java / Kotlin (optional)

| ID | Command | Notes |
|----|---------|-------|
| `jvm.build` | `mvn -q compile` / `./gradlew build -x test` | auto; prefer the touched module |
| `jvm.add.dep` | add dependency to `pom.xml` / `build.gradle(.kts)` | **ask** |

## Python (optional)

| ID | Command | Notes |
|----|---------|-------|
| `python.install` | `pip install -r requirements.txt` / `poetry install` / `uv sync` | auto (from the lock file only) |
| `python.add.dep` | `pip install <pkg>` / `poetry add` / `uv add` | **ask** |

## Flutter (optional)

| ID | Command | Notes |
|----|---------|-------|
| `flutter.pub.get` | `flutter pub get` | auto |
| `dart.format` | `dart format` | auto; touched files only |
| `flutter.pub.add` | `flutter pub add` | **ask** |
| `flutter.pub.upgrade` | global upgrade | **deny** |

## Go (optional)

| ID | Command | Notes |
|----|---------|-------|
| `go.mod.download` | `go mod download` | auto |
| `go.build` | `go build ./...` | auto |
| `go.fmt` | `gofmt -w` / `goimports -w` | auto; touched files only |
| `go.add.dep` | `go get <module>` | **ask** |

## Rust (optional)

| ID | Command | Notes |
|----|---------|-------|
| `rust.build` | `cargo build` | auto |
| `rust.fmt` | `cargo fmt` | auto |
| `rust.add.dep` | `cargo add <crate>` | **ask** |

## PHP (optional)

| ID | Command | Notes |
|----|---------|-------|
| `php.install` | `composer install` | auto (from the lock file only) |
| `php.fmt` | `vendor/bin/pint` / `php-cs-fixer fix` | auto; touched files only |
| `php.add.dep` | `composer require <pkg>` | **ask** |

## Ruby (optional)

| ID | Command | Notes |
|----|---------|-------|
| `ruby.install` | `bundle install` | auto (from `Gemfile.lock` only) |
| `ruby.fmt` | `bundle exec rubocop -a` | auto; touched files only |
| `ruby.add.dep` | `bundle add <gem>` | **ask** |

## Android (optional)

| ID | Command | Notes |
|----|---------|-------|
| `android.build` | `./gradlew assembleDebug` | auto |
| `android.release` | signed release build / store upload | **deny** for agents — release process only |

## iOS (optional)

| ID | Command | Notes |
|----|---------|-------|
| `ios.build` | `xcodebuild build -scheme <Scheme> -destination '<simulator>'` / `swift build` | auto |
| `ios.pods` | `pod install` / SwiftPM resolve | auto (from the lock file only) |
| `ios.add.dep` | new Pod / Swift package | **ask** |
| `ios.release` | archive, signing, TestFlight/App Store upload | **deny** for agents — release process only |
