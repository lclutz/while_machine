# while_machine

Interpreter für WHILE-Programme.

## Benutzung

```shell
PS> python .\while_machine.py .\demo\add.while 2 2
x0 = 4
```

## WHILE-Programme

Der [demo-Ordner](./demo) enthält ein paar Beispiele für WHILE-Programme.
WHILE-Programme dürfen aus den folgenden elementaren Anweisungen bestehen

- `xi := xj + c;`
- `xi := xj - c;`
- `WHILE (xi > 0) DO ... END;`

Zusätzlich sind bei diesem interpreter Kommentare mit führendem `#` erlaubt.
(siehe [prime.while](./demo/prime.while) für ein Beispiel)
