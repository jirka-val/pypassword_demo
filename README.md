# Demonstrace (špatného) ukládání hesel

Tento skript je jednoduchá interaktivní demonstrace, která ukazuje, proč jsou staré metody ukládání hesel nebezpečné.

Porovnává dvě **špatné** metody:
1.  **Plaintext (čistý text):** Uložení hesla tak, jak je. 
2.  **MD5:** Uložení starého, rychlého a "nesoleného" (unsalted) hashe.

## Účel

Cílem je názorně ukázat, co přesně uvidí útočník, když získá přístup k vaší databázi.

* Při použití `plaintext` uvidí hesla všech uživatelů.
* Při použití `MD5` uvidí hashe, které lze snadno prolomit (např. https://crackstation.net/)

## Jak to spustit?

Není potřeba nic instalovat, stačí mít Python 3.

```bash
py .\password_demo.py
```
