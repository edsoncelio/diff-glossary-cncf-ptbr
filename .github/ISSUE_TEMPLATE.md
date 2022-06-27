name: Diff main/dev-pt - {{ date | date('DD/MM/YYYY') }}
description: Create a diff between main and dev-pt branch
title: "[Diff]: main/dev-pt - {{ date | date('DD/MM/YYYY') }}"
labels: ["diff"]
body:
  - type: markdown
    attributes:
      value: |
        ## Termos atualizados (updated definitions):
        ```shell
        {{ env.UPDATED_FILES }}
        ```
        ## Termos novos (new definitions added to the main branch):
        ```shell
        {{ env.NEW_FILES }}
        ```
