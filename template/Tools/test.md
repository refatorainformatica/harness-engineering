# Tools — Test

| ID | Comando / ação | Notas |
|----|----------------|-------|
| `dotnet.test` | `dotnet test` | auto; filtro/pasta da feature (`Features/<Name>/`) |
| `node.test` | `npm test` / equivalente | auto; paths da feature |
| `flutter.test` | `flutter test test/features/<id>/` | auto; paths da feature |
| `test.custom` | script do projeto | **ask** se não documentado |

Novos testes: **sempre** sob a pasta da feature (`Standards.md`). Fixtures partilhadas em `Shared/`.

Lacuna **AC-G\***: stub mínimo na pasta da feature, depois comando de teste do escopo.

Registre sempre o ID e o resultado no LOG da run.
