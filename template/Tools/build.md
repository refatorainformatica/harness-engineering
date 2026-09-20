# Tools — Build

Ajuste os comandos à stack do projeto. Níveis alinhados a `Governance/permissions.md`: **auto** | **ask** | **deny**.

## Genérico / arquivos

| ID | Ação | Notas |
|----|------|-------|
| `fs.read` | Ler arquivos | auto |
| `fs.write` | Editar no escopo | auto |
| `fs.delete` | Apagar arquivo | **ask** se não for temp |
| `fs.write.secrets` | Editar secrets | **deny** |

## .NET (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `dotnet.restore` | `dotnet restore` | auto |
| `dotnet.build` | `dotnet build` | auto; preferir projeto tocado |
| `dotnet.format` | `dotnet format` | auto; só escopo |
| `dotnet.add.package` | `dotnet add package` | **ask** |

## Node (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `node.install` | `npm ci` / `pnpm i` / `yarn` | auto |
| `node.build` | `npm run build` | auto |
| `node.add.dep` | add dependency | **ask** |

## Flutter (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `flutter.pub.get` | `flutter pub get` | auto |
| `dart.format` | `dart format` | auto; só tocados |
| `flutter.pub.add` | `flutter pub add` | **ask** |
| `flutter.pub.upgrade` | upgrade global | **deny** |
