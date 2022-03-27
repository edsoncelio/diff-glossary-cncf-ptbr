---
title: Diff main/dev-pt - {{ date | date('DD/MM/YYYY') }}
labels: diff
---

Diff de arquivos da branch `main` para a branch `dev-pt`.

## Arquivos atualizados:
```shell
{{ env.UPDATED_FILES }}
```

## Arquivos novos:
```shell
{{ env.NEW_FILES }}
```