#!/usr/bin/env bash
# Kit self-tests: install, fill/enrich, update, legacy-name migration, adapters, check-harness.
# Tool-agnostic: bash + git + python3. Usage: tests/run.sh
set -uo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INIT="$KIT/scripts/init-harness.sh"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/harness-kit-tests.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0

ok() { PASS=$((PASS + 1)); printf '  ok   %s\n' "$1"; }
ko() { FAIL=$((FAIL + 1)); printf '  FAIL %s\n' "$1"; [[ -n "${2:-}" ]] && printf '%s\n' "$2" | sed 's/^/       /'; }
assert() { local label="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$label"; else ko "$label"; fi; }
assert_contains() { if grep -q -- "$2" "$1" 2>/dev/null; then ok "$3"; else ko "$3" "$(head -40 "$1" 2>/dev/null)"; fi; }
assert_not_contains() { if grep -q -- "$2" "$1" 2>/dev/null; then ko "$3" "$(grep -n -- "$2" "$1" | head -5)"; else ok "$3"; fi; }
no_upper_md() { ! find "$1" -name '*.md' | grep -q '/[^/]*[A-Z][^/]*\.md$'; }
check() { python3 "$1/.ai-harness/Tools/bin/check-harness.py" --root "$1" "${@:2}"; }
git_repo() { git -C "$1" init -q && git -C "$1" -c user.email=t@t -c user.name=t add -A && git -C "$1" -c user.email=t@t -c user.name=t commit -qm init; }

section() { printf '\n== %s\n' "$1"; }

# ------------------------------------------------------------------ fixtures
fixture() {
  local dir="$WORK/$1"
  mkdir -p "$dir"
  case "$1" in
    dotnet-blazor-azure)
      echo 'Microsoft Visual Studio Solution File' > "$dir/App.sln"
      mkdir -p "$dir/src/Web"
      echo '<Project Sdk="Microsoft.NET.Sdk.Web"><ItemGroup><PackageReference Include="Microsoft.AspNetCore.Components.Web" /><PackageReference Include="Azure.Identity" /></ItemGroup></Project>' > "$dir/src/Web/Web.csproj"
      echo '@page "/"' > "$dir/src/Web/Index.razor"
      mkdir -p "$dir/infra" && echo 'provider "azurerm" {}' > "$dir/infra/main.tf"
      ;;
    angular)
      echo '{"dependencies":{"@angular/core":"^18.0.0"}}' > "$dir/package.json"
      echo '{}' > "$dir/angular.json"
      ;;
    react-node-gcp)
      echo '{"dependencies":{"react":"^18.0.0","express":"^4.0.0","@google-cloud/storage":"^7.0.0"}}' > "$dir/package.json"
      echo 'steps: []' > "$dir/cloudbuild.yaml"
      ;;
    java-aws)
      echo '<project><dependencies><dependency><groupId>software.amazon.awssdk</groupId></dependency></dependencies></project>' > "$dir/pom.xml"
      echo 'version: 0.2' > "$dir/buildspec.yml"
      ;;
    python)
      echo '[project]' > "$dir/pyproject.toml"
      ;;
    flutter)
      echo 'name: app' > "$dir/pubspec.yaml"
      ;;
    go-oci)
      echo 'module example.com/app' > "$dir/go.mod"
      mkdir -p "$dir/infra" && echo 'provider "oci" {}' > "$dir/infra/main.tf"
      ;;
    rust)
      printf '[package]\nname = "app"\n' > "$dir/Cargo.toml"
      ;;
    php-database)
      echo '{"require":{"laravel/framework":"^11.0"}}' > "$dir/composer.json"
      mkdir -p "$dir/database/migrations" && echo 'CREATE TABLE t (id int);' > "$dir/database/migrations/001_init.sql"
      ;;
    ruby)
      echo "source 'https://rubygems.org'" > "$dir/Gemfile"
      ;;
    vue)
      echo '{"dependencies":{"vue":"^3.4.0"}}' > "$dir/package.json"
      ;;
    react-native)
      echo '{"dependencies":{"react":"^18.0.0","react-native":"^0.74.0"}}' > "$dir/package.json"
      ;;
    android)
      echo "plugins { id 'com.android.application' }" > "$dir/build.gradle"
      mkdir -p "$dir/app/src/main" && echo '<manifest/>' > "$dir/app/src/main/AndroidManifest.xml"
      ;;
    ios)
      mkdir -p "$dir/App.xcodeproj" && echo '// swift-tools-version:5.9' > "$dir/Package.swift"
      ;;
    data)
      echo "name: analytics" > "$dir/dbt_project.yml"
      echo 'pyspark==3.5.0' > "$dir/requirements.txt"
      ;;
  esac
  echo "# $1" > "$dir/README.md"
  printf '%s' "$dir"
}

expect_packs() {
  local dir="$1"; shift
  local pack
  for pack in "$@"; do
    assert_contains "$dir/.ai-harness/Agents/project.md" "Knowledge/stacks/$pack" "$(basename "$dir"): pack $pack active"
  done
}

# ------------------------------------------------------------------ kit itself
section "kit"
assert "adapters are in sync with adapters/source" python3 "$KIT/scripts/build-adapters.py" --check
assert "kit markdown file names are lower-case" no_upper_md "$KIT"
assert "scripts compile" python3 -m py_compile "$KIT"/scripts/*.py "$KIT/template/Tools/bin/check-harness.py"
assert "init script syntax" bash -n "$INIT"

# ------------------------------------------------------------------ install + enrich per stack
section "install + enrich per stack"
declare -A PACKS=(
  [dotnet-blazor-azure]="dotnet.md blazor.md devops.md azure.md"
  [angular]="typescript.md angular.md"
  [react-node-gcp]="typescript.md node.md react.md devops.md gcp.md"
  [java-aws]="java.md devops.md aws.md"
  [python]="python.md"
  [flutter]="flutter.md"
  [go-oci]="go.md devops.md oci.md"
  [rust]="rust.md"
  [php-database]="php.md database.md"
  [ruby]="ruby.md"
  [vue]="typescript.md vue.md"
  [react-native]="typescript.md react.md react-native.md"
  [android]="java.md android.md"
  [ios]="ios.md"
  [data]="data.md python.md"
)
for name in "${!PACKS[@]}"; do
  dir="$(fixture "$name")"
  out="$WORK/$name.out"
  if bash "$INIT" "$dir" "$name" --adapters=all --enrich >"$out" 2>&1; then ok "$name: init --enrich"; else ko "$name: init --enrich" "$(tail -20 "$out")"; continue; fi
  assert "$name: harness file names lower-case" no_upper_md "$dir/.ai-harness"
  for f in AGENTS.md CLAUDE.md CONVENTIONS.md .github/copilot-instructions.md .cursor/rules/harness-sdd.mdc .windsurfrules; do
    assert "$name: adapter $f installed with tool name" test -f "$dir/$f"
  done
  # shellcheck disable=SC2086
  expect_packs "$dir" ${PACKS[$name]}
  if check "$dir" >"$out.check" 2>&1; then ok "$name: harness.check passes"; else ko "$name: harness.check passes" "$(cat "$out.check")"; fi
done

# ------------------------------------------------------------------ adapters never overwrite project files
section "adapters"
dir="$WORK/existing-agents"; mkdir -p "$dir"
echo "# Our own agents file" > "$dir/AGENTS.md"
bash "$INIT" "$dir" --adapters=agents-md >/dev/null 2>&1
assert_contains "$dir/AGENTS.md" "Our own agents file" "existing AGENTS.md is not overwritten"

# ------------------------------------------------------------------ update migrates legacy names
section "update + migration"
dir="$WORK/legacy"; mkdir -p "$dir"
bash "$INIT" "$dir" --adapters=none >/dev/null 2>&1
h="$dir/.ai-harness"
echo "custom standards" >> "$h/Knowledge/standards.md"
mv "$h/Knowledge/standards.md" "$h/Knowledge/Standards.md"
mv "$h/agents.md" "$h/AGENTS.md"
mv "$h/Runtime/loop.md" "$h/Runtime/LOOP.md"
mkdir -p "$h/Runtime/state/runs/r1" && echo "status" > "$h/Runtime/state/runs/r1/STATUS.md"
rm -f "$h/Knowledge/stacks/react.md"
if bash "$INIT" "$dir" --update >"$WORK/legacy.out" 2>&1; then ok "update runs"; else ko "update runs" "$(tail -20 "$WORK/legacy.out")"; fi
assert "legacy names migrated" no_upper_md "$h"
assert_contains "$h/Knowledge/standards.md" "custom standards" "user content preserved on migration"
assert "run files migrated" test -f "$h/Runtime/state/runs/r1/status.md"
assert "removed stack pack stays removed" test ! -f "$h/Knowledge/stacks/react.md"
assert "kept stack pack refreshed" test -f "$h/Knowledge/stacks/dotnet.md"

# ------------------------------------------------------------------ check-harness diff rules
section "check-harness --diff"
dir="$WORK/diff"; mkdir -p "$dir/src/Features/Orders"
bash "$INIT" "$dir" --adapters=none >/dev/null 2>&1
cat > "$dir/src/Features/Orders/Order.cs" <<'EOF'
public class Order
{
    [JsonPropertyName("id")]
    public string Id { get; set; }
}
EOF
cat > "$dir/main.tf" <<'EOF'
resource "aws_s3_bucket" "b" {
  lifecycle {
    prevent_destroy = true
  }
}
EOF
git_repo "$dir"
cat > "$dir/src/Features/Orders/Order.cs" <<'EOF'
public class Order
{
    public string Id { get; set; }
}
EOF
printf 'resource "aws_s3_bucket" "b" {\n  acl = "public-read"\n}\n' > "$dir/main.tf"
cat > "$dir/src/Features/Orders/OrderService.cs" <<'EOF'
public class OrderService
{
    private const string Key = "AKIAABCDEFGHIJKLMNOP";
    public void Run(string id, string password)
    {
        var sql = $"SELECT * FROM Orders WHERE Id = {id}";
        _logger.LogInformation($"Processing {id}");
        _logger.LogInformation("Login {Password}", password);
    }
}
EOF
echo 'API_KEY=x' > "$dir/.env"
out="$WORK/diff.out"
check "$dir" --diff HEAD >"$out" 2>&1; rc=$?
assert "diff with violations fails" test "$rc" -ne 0
assert_contains "$out" "attribute/annotation removed" "removed attribute detected"
assert_contains "$out" "IaC protection/metadata removed" "removed prevent_destroy detected"
assert_contains "$out" "possible secret (AWS access key id)" "AWS key detected"
assert_contains "$out" "security: SQL built by concatenation" "SQL injection pattern detected"
assert_contains "$out" "security: public storage" "public bucket detected"
assert_contains "$out" "log message built with interpolation" "interpolated log detected"
assert_contains "$out" "possible secret/PII in a log call" "sensitive log detected"
assert_contains "$out" "sensitive file committed" ".env detected"
assert_contains "$out" "tests: new code without unit tests" "untested new code detected"

dir="$WORK/diff-clean"; mkdir -p "$dir/src/Features/Orders" "$dir/tests/Features/Orders"
bash "$INIT" "$dir" --adapters=none >/dev/null 2>&1
git_repo "$dir"
cat > "$dir/src/Features/Orders/OrderService.cs" <<'EOF'
public class OrderService(ILogger<OrderService> logger)
{
    public void Run(string orderId)
    {
        logger.LogInformation("Processing order {OrderId}", orderId);
    }
}
EOF
cat > "$dir/tests/Features/Orders/OrderServiceTests.cs" <<'EOF'
public class OrderServiceTests
{
    [Fact]
    public void Run_ShouldLogStart_WhenOrderIsValid()
    {
    }
}
EOF
out="$WORK/diff-clean.out"
check "$dir" --diff HEAD >"$out" 2>&1; rc=$?
if [[ "$rc" -eq 0 ]] && ! grep -q '^WARN  src\|^WARN  tests' "$out"; then ok "compliant diff passes with no code warnings"; else ko "compliant diff passes with no code warnings" "$(cat "$out")"; fi

# ------------------------------------------------------------------ check-harness --diff (more languages)
section "check-harness --diff (more languages)"
dir="$WORK/diff-langs"; mkdir -p "$dir/internal/features/orders" "$dir/app/Features/Orders" "$dir/app/src/main" "$dir/db/migrations"
bash "$INIT" "$dir" --adapters=none >/dev/null 2>&1
printf 'type Order struct {\n\tID string `json:"id"`\n}\n' > "$dir/internal/features/orders/order.go"
git_repo "$dir"
printf 'type Order struct {\n\tID string\n}\n' > "$dir/internal/features/orders/order.go"
cat > "$dir/internal/features/orders/order_service.go" <<'GO'
package orders

func (s *Service) Run(id string) {
	s.logger.Info(fmt.Sprintf("processing %s", id))
	q := fmt.Sprintf("SELECT * FROM orders WHERE id = '%s'", id)
	_ = q
}
GO
cat > "$dir/app/Features/Orders/OrderController.php" <<'PHP'
<?php
class OrderController {
    public function show($id) {
        $this->logger->info("Showing order $id");
        return DB::select("SELECT * FROM orders WHERE id = $id");
    }
}
PHP
echo '<application android:usesCleartextTraffic="true"/>' > "$dir/app/src/main/AndroidManifest.xml"
echo 'DROP TABLE orders;' > "$dir/db/migrations/002_drop.sql"
out="$WORK/diff-langs.out"
check "$dir" --diff HEAD >"$out" 2>&1
assert_contains "$out" "internal/features/orders/order.go:2 attribute/annotation removed" "Go struct tag removal detected"
assert_contains "$out" "order_service.go:4 log message built with interpolation" "Go Sprintf log detected"
assert_contains "$out" "order_service.go:5 security: SQL built by formatting" "Go SQL formatting detected"
assert_contains "$out" "OrderController.php:4 log message built with interpolation" "PHP interpolated log detected"
assert_contains "$out" "OrderController.php:5 security: SQL built" "PHP SQL interpolation detected"
assert_contains "$out" "mobile cleartext traffic" "Android cleartext detected"
assert_contains "$out" "destructive migration" "destructive SQL migration detected"

# ------------------------------------------------------------------ coverage
section "check-harness --coverage"
dir="$WORK/diff-clean"
cat > "$dir/cobertura.xml" <<'EOF'
<coverage line-rate="0.85"><packages><package name="App.Orders" line-rate="0.91"/><package name="App.Billing" line-rate="0.62"/></packages></coverage>
EOF
printf 'TN:\nSF:lib/a.dart\nLF:10\nLH:9\nend_of_record\n' > "$dir/lcov.info"
cat > "$dir/jacoco.xml" <<'EOF'
<report name="orders-service"><counter type="LINE" missed="5" covered="95"/></report>
EOF
out="$WORK/cov.out"
check "$dir" --coverage cobertura.xml >"$out" 2>&1; rc=$?
assert "artifact below 80% fails" test "$rc" -ne 0
assert_contains "$out" "App.Billing" "failing artifact reported"
if check "$dir" --coverage lcov.info jacoco.xml >"$out" 2>&1; then ok "LCOV + JaCoCo above 80% pass"; else ko "LCOV + JaCoCo above 80% pass" "$(cat "$out")"; fi
check "$dir" --coverage lcov.info --min-coverage 70 >"$out" 2>&1; rc=$?
assert "floor below 80% is rejected" test "$rc" -ne 0

# ------------------------------------------------------------------ hook
section "git hook"
if check "$dir" --install-hook >/dev/null 2>&1 && grep -q "check-harness.py --staged" "$dir/.git/hooks/pre-commit"; then ok "pre-commit hook installed"; else ko "pre-commit hook installed"; fi

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[[ "$FAIL" -eq 0 ]]
