# KronprinsFrederiksBro

Home Assistant custom integration for possible openings on Kronprins Frederiks Bro.

Starter workspace for a Home Assistant custom integration.

## Structure

- `custom_components/kronprins_frederiks_bro/` integration code
- `custom_components/kronprins_frederiks_bro/api.py` API client stub
- `custom_components/kronprins_frederiks_bro/coordinator.py` DataUpdateCoordinator
- `.github/copilot-instructions.md` project checklist/status
- `pyproject.toml` lint/test placeholders

## Local setup

1. Clone or copy this folder into your Home Assistant config under `custom_components/kronprins_frederiks_bro`.
2. Restart Home Assistant.
3. Go to **Settings -> Devices & Services -> Add Integration**.
4. Search for **Kronprins Frederiks Bro** and complete the config flow.

## Development notes

- Update `manifest.json` metadata before release.
- Replace API stub in `api.py` with real communication logic.
- Add additional platforms (switch, number, button, etc.) as needed.
- Expand tests in `tests/` as behavior is implemented.

## Implemented schedule logic

- The integration calculates next possible opening from a 30-minute slot model.
- Day type is split into Monday-Thursday, Friday, and weekend/public holiday.
- Monthly first/last opening windows are implemented from the provided table.
- Public holidays are calculated for Denmark (Easter-based holidays plus fixed dates).
- Outside the monthly opening window, opening is always treated as closed.
- Green slots are interpreted as possible openings only.
- Actual opening happens on demand when boats need passage under the bridge.

## Sensors

- Possible opening status (possible/not_possible)
- Næste mulige åbning (nedtaelling i minutter)

Status icon behavior:
- `mdi:bridge` when possible opening is active
- `mdi:bridge-lock` when it is outside possible opening periods

Seasonal windows:
- The integration always enforces monthly first/last opening times.
- Winter months therefore use the shortest daily windows from the schedule table.
