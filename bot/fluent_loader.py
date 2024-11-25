from pathlib import Path

from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization() -> FluentLocalization:
    locale_dir = Path(__file__).parent.joinpath("locale", "{locale}")
    loader = FluentResourceLoader(str(locale_dir.absolute()))
    return FluentLocalization(["current"], ["strings.ftl"], loader)
