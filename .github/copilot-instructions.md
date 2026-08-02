# Copilot Instructions for Electronic_load_px100

## Project purpose
- PySide6 desktop app for controlling a PX-100 electronic load and running battery discharge tests.
- Core behavior: discover the instrument over PyVISA serial, stream measurements, update UI/plots, save CSV logs, and optionally send email reports.

## Main architecture
- `main.py`: application bootstrap, thread pool, signal wiring, process shutdown.
- `instr_thread.py`: background worker (`InstrumentWorker`) that reads device data and executes queued commands.
- `instruments/__init__.py`: device discovery (`pyvisa.ResourceManager('@py')`) and driver selection.
- `instruments/px100.py`: PX-100 protocol implementation (read/write frames, command mapping, scaling).
- `data_store.py`: in-memory pandas store for sampled rows and CSV export.
- `gui/gui.py`: main window, plotting, command dispatch, logging + email flow.
- `gui/internal_r.py`: internal resistance measurement state machine.
- `gui/swcccv.py`: software CC-CV helper logic.
- `gui/log_control.py`, `gui/email_settings.py`: settings-driven logging/email controls.

## Local run/build workflow
- Install deps: `pip install --user -r requirements.txt`
- Run app: `python3 main.py`
- Windows packaging is defined in:
  - `.github/workflows/pyinstaller_windows.yml`
  - `px100.spec`
  - `px100.nsi`

## Change guidelines for this repo
1. Keep hardware communication behavior stable unless explicitly requested; protocol changes belong in `instruments/px100.py`.
2. Preserve Qt signal/slot flow between `InstrumentWorker`, `Main`, and GUI subscribers.
3. For UI updates, keep `.py` and `.ui` files aligned and regenerate `gui/ui_*.py` with `pyside6-uic`.
4. Logging/email changes must not block measurement loop; avoid long/blocking operations in the worker path.
5. Keep CSV output and test-completion email behavior consistent (`MainWindow.write_logs`, `DataStore.write`, `InternalR.write`).
6. Prefer focused edits in existing modules over introducing new frameworks or abstractions.

## Testing and validation expectations
- If Python code changes, at minimum run:
  - `python3 main.py` (startup sanity; requires environment with GUI/hardware)
- If packaging files change, ensure the workflow/spec/NSIS files remain consistent with each other.
- For docs-only changes, no runtime validation is required.

## Practical constraints
- App is stateful and event-driven; avoid race-prone cross-thread UI access.
- This project supports Python 3.14 and uses modern pandas (`>=2.2`) with the PySide6/pyvisa/pyserial stack.
- Device availability is not guaranteed during development; when adding logic, keep graceful handling for missing instruments.
