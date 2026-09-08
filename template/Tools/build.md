# Tools — Build

Ajuste os comandos à stack do projeto.

## Genérico / arquivos

| ID | Ação | Notas |
|----|------|-------|
| `fs.read` | Ler arquivos | OK |
| `fs.write` | Editar no escopo | OK na tarefa |
| `fs.delete` | Apagar arquivo | **ask** se não for temp |
| `fs.write.secrets` | Editar secrets | **deny** |

## .NET (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `dotnet.restore` | `dotnet restore` | OK |
| `dotnet.build` | `dotnet build` | Preferir projeto tocado |
| `dotnet.format` | `dotnet format` | Só escopo |
| `dotnet.add.package` | `dotnet add package` | **ask** |

## Node (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `node.install` | `npm ci` / `pnpm i` / `yarn` | OK |
| `node.build` | `npm run build` | OK |
| `node.add.dep` | add dependency | **ask** |

## Flutter (opcional)

| ID | Comando | Notas |
|----|---------|-------|
| `flutter.pub.get` | `flutter pub get` | OK |
| `dart.format` | `dart format` | Só tocados |
| `flutter.pub.add` | `flutter pub add` | **ask** |
| `flutter.pub.upgrade` | upgrade global | **deny** |
