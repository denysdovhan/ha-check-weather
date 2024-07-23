[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

![HA Check Weather Logo](./icons/logo.svg)

# HA Check Weather

[![GitHub Release][gh-release-image]][gh-release-url]
[![GitHub Downloads][gh-downloads-image]][gh-downloads-url]
[![hacs][hacs-image]][hacs-url]
[![GitHub Sponsors][gh-sponsors-image]][gh-sponsors-url]
[![Patreon][patreon-image]][patreon-url]
[![Buy Me A Coffee][buymeacoffee-image]][buymeacoffee-url]
[![Twitter][twitter-image]][twitter-url]

> A simple binary sensor for [Home Assistant][home-assistant] that checks the weather for the next hours and turns on when it fits certain conditions.

This is a very simple binary sensor that checks the weather for the next few hours and turns on when it fits certain conditions.

Ideas on how to use this sensor:

- **🚴‍♂️ Bike Day** – check if the weather is good enough to go out for a ride.
- **🚶 Walkable Weather** – check if the weather is good enough to go out for a walk.
- **☔️ Will it Rain** – check if it will rain today.

You can rename the sensor to anything more meaningful to you.

## Sponsorship

Your generosity will help me maintain and develop more projects like this one.

- 💖 [Sponsor me on GitHub][gh-sponsors-url]
- ☕️ [Buy Me A Coffee][buymeacoffee-url]
- 🤝 [Support me on Patreon][patreon-url]
- Bitcoin: `bc1q7lfx6de8jrqt8mcds974l6nrsguhd6u30c6sg8`
- Ethereum: `0x6aF39C917359897ae6969Ad682C14110afe1a0a1`

## Installation

The quickest way to install this integration is via [HACS][hacs-url] by clicking the button below:

[![Add to HACS via My Home Assistant][hacs-install-image]][hasc-install-url]

If it doesn't work, adding this repository to HACS manually by adding this URL:

1. Visit **HACS** → **Integrations** → **...** (in the top right) → **Custom repositories**
1. Click **Add**
1. Paste `https://github.com/denysdovhan/ha-check-weather` into the **URL** field
1. Chose **Integration** as a **Category**
1. **Check Weather** will appear in the list of available integrations. Install it normally.

## Usage

This integration is configurable via UI. On **Devices and Services** page, click **Add Integration** and search for **Check Weather**.

Specify desired configuration options:

![Screenshot 2024-06-21 at 20 45 49](https://github.com/denysdovhan/ha-check-weather/assets/3459374/26056db5-b800-41a5-b4bd-0ba44254a538)

The integration will create a new `binary_sensor` entity that will turn on when the weather fits the set conditions.

![Screenshot 2024-06-21 at 20 46 58](https://github.com/denysdovhan/ha-check-weather/assets/3459374/b5c175d8-b397-4efd-af19-f4481a455839)

You can safely rename the entity to something more meaningful, like **Bike Day** or anything else.

## Translations

Please, help to add more translations and improve existing ones. Here's a list of supported languages:

- English
- Українська (Ukrainian)
- Polski (Polish)
- [Your language?][add-translation]

## Development

Want to contribute to the project?

First, thanks! Check [contributing guideline](./CONTRIBUTING.md) for more information.

## License

MIT © [Denys Dovhan][denysdovhan]

<!-- Badges -->

[gh-release-url]: https://github.com/denysdovhan/ha-check-weather/releases/latest
[gh-release-image]: https://img.shields.io/github/v/release/denysdovhan/ha-check-weather?style=flat-square
[gh-downloads-url]: https://github.com/denysdovhan/ha-check-weather/releases
[gh-downloads-image]: https://img.shields.io/github/downloads/denysdovhan/ha-check-weather/total?style=flat-square
[hacs-url]: https://github.com/hacs/integration
[hacs-image]: https://img.shields.io/badge/hacs-default-orange.svg?style=flat-square
[gh-sponsors-url]: https://github.com/sponsors/denysdovhan
[gh-sponsors-image]: https://img.shields.io/github/sponsors/denysdovhan?style=flat-square
[patreon-url]: https://patreon.com/denysdovhan
[patreon-image]: https://img.shields.io/badge/support-patreon-F96854.svg?style=flat-square
[buymeacoffee-url]: https://buymeacoffee.com/denysdovhan
[buymeacoffee-image]: https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square
[twitter-url]: https://twitter.com/denysdovhan
[twitter-image]: https://img.shields.io/badge/twitter-%40denysdovhan-00ACEE.svg?style=flat-square

<!-- References -->

[home-assistant]: https://www.home-assistant.io/
[denysdovhan]: https://github.com/denysdovhan
[hasc-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=denysdovhan&repository=ha-check-weather&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
[add-translation]: https://github.com/denysdovhan/check-weather/blob/master/contributing.md#how-to-add-translation
