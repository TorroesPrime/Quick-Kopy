# Quick-Kopy

Copies selected saved notes right to your clipboard, ready to be pasted.

## How to build an executable

1. Install Poetry (`pip install poetry`)
2. Install the project dependencies (`poetry install --with dev`)
3. Build; if you'd like to use the provided spec file fr convenience, use this:

    ```sh
    poetry run pyinstaller .\quick_kopy.spec
    ```

    Alternatively, you can build manually:

    ```sh
    poetry run pyinstaller -F -n "Quick-Kopy" --add-data "./quick_kopy/data;data" -i "./quick_kopy/data/icon.ico" ./quick_kopy/main.pyw
    ```
