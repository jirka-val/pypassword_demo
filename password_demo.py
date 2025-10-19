#!/usr/bin/env python3
"""
Demonstrace slabého vs. silného ukládání hesel.

Ukazuje rozdíly mezi:
1. Plaintext (čistý text) - NEJHORŠÍ
2. MD5 (starý, rychlý, nesolený hash) - ŠPATNÉ
3. Bcrypt (moderní, pomalý, solený hash) - SPRÁVNÉ
"""

import hashlib
import json

user_database = {}

def register_plaintext(username, password):
    """ŠPATNĚ: Ukládá heslo v čistém textu."""
    print(f"\n[REGISTRACE - PLAINTEXT] Ukládám '{password}' pro uživatele '{username}'")
    user_database[username] = {
        "mode": "plaintext",
        "password_data": password  # Přímo heslo!
    }

def login_plaintext(username, password_attempt):
    """ŠPATNĚ: Kontroluje heslo v čistém textu."""
    if username not in user_database:
        return False

    # Jednoduché porovnání stringů
    return user_database[username]["password_data"] == password_attempt


def register_md5(username, password):
    """ŠPATNĚ: Používá MD5 (rychlý, nesolený hash)."""
    print(f"\n[REGISTRACE - MD5] Ukládám hash pro '{username}'")

    # Vytvoří MD5 hash hesla. .encode() převede string na byty.

    password_hash = hashlib.md5(password.encode()).hexdigest()
    user_database[username] = {
        "mode": "md5",
        "password_data": password_hash
    }

def login_md5(username, password_attempt):
    """ŠPATNĚ: Kontroluje MD5 hash."""
    if username not in user_database:
        return False

    # Znovu zahashuje zadané heslo a porovná ho s uloženým hashem

    hash_to_check = hashlib.md5(password_attempt.encode()).hexdigest()
    return user_database[username]["password_data"] == hash_to_check


def main():
    """Hlavní interaktivní konzole"""
    current_mode = "plaintext"

    print("=" * 60)
    print("DEMONSTRACE UKLÁDÁNÍ HESEL")
    print("=" * 60)
    print("  Příkazy:")
    print("  mode <plaintext|md5>      - Změní režim registrace")
    print("  register <user> <pass>    - Zaregistruje uživatele")
    print("  login <user> <pass>       - Pokusí se přihlásit")
    print("  showdb                    - Ukáže 'databázi'")
    print("  exit                      - Ukončí program")
    print("-" * 60)

    while True:
        try:
            print(f"\nAktuální režim: [{current_mode.upper()}]")
            command = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNashledanou!")
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0].lower()

        if cmd == "exit":
            break

        elif cmd == "mode" and len(parts) > 1:
            new_mode = parts[1].lower()
            if new_mode in ["plaintext", "md5", "bcrypt"]:
                current_mode = new_mode
                print(f"Režim registrace změněn na: {new_mode.upper()}")
            else:
                print("Chyba: Neznámý režim. Použij 'plaintext', 'md5' nebo 'bcrypt'.")

        elif cmd == "register" and len(parts) == 3:
            username = parts[1]
            password = parts[2]

            if current_mode == "plaintext":
                register_plaintext(username, password)
            elif current_mode == "md5":
                register_md5(username, password)
            print("Registrace proběhla. Zkuste se podívat do databáze příkazem 'showdb'.")

        elif cmd == "login" and len(parts) == 3:
            username = parts[1]
            password = parts[2]

            if username not in user_database:
                print("\nLOGIN SELHAL: Uživatel neexistuje.")
                continue

            # Zjistíme, jakou metodou byl uživatel registrován
            user_mode = user_database[username]["mode"]
            success = False

            print(f"\n[LOGIN] Ověřuji heslo pro '{username}' (metodou {user_mode.upper()})...")

            if user_mode == "plaintext":
                success = login_plaintext(username, password)
            elif user_mode == "md5":
                success = login_md5(username, password)
            if success:
                print(">>> LOGIN ÚSPĚŠNÝ! <<<")
            else:
                print(">>> LOGIN SELHAL: Špatné heslo. <<<")

        elif cmd == "showdb":
            print("\n" + "=" * 20 + " OBSAH DATABÁZE " + "=" * 20)
            if not user_database:
                print("(Databáze je prázdná)")
            else:
                print(json.dumps(user_database, indent=2))
            print("=" * 69)

        else:
            print("Chyba: Neznámý příkaz. (Použij 'mode', 'register', 'login', 'showdb', 'exit')")


if __name__ == "__main__":
    main()