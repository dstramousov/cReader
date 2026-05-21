# Versions

## v0.0.0 -> v0.0.1
- init repo

## v0.0.1 -> v0.0.2
- Added Python package scaffold with CLI entrypoint metadata.
- Added minimal FB2 domain models and namespace-aware parser.
- Added terminal-width text wrapping helpers with tests.
- Added UI theme registry foundation for future Textual screens.

## v0.0.2 -> v0.0.3
- Added FB2 book loader with explicit load errors.
- Added book-to-lines document layout for reader rendering.
- Added minimal Textual reader app with PageUp/PageDown navigation and status bar.
- Connected CLI book opening to the Textual reader and added theme selection.

## v0.0.3 -> v0.0.4
- Added Norton Commander inspired top command menu.
- Added F1 keyboard help modal with reader shortcuts.
- Added F10 exit binding alongside q.


## v0.0.4 -> v0.0.5
- Made the F1 help dialog behave as a compact overlay instead of repainting the whole modal screen.
- Added a Norton Commander style top-menu clock.
- Added F2 theme switching for the reader UI.

## v0.0.5 -> v0.0.6
- Added JSON-backed reader position persistence.
- Added one-line up/down scrolling with arrow keys.
- Added F3 table-of-contents modal with chapter selection and jump navigation.

## v0.0.6 -> v0.0.7
- Fixed restored reader positions rendering only a single visible line after app restart.
- Forced reader viewport refresh when the widget size changes without changing the saved offset.
