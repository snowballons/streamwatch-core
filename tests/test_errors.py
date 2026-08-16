"""Tests for the error taxonomy."""

from streamwatch_core.errors import (
    BrowserRequiredError,
    NoPluginError,
    NoStreamsError,
    PluginError,
    StreamlinkCoreError,
    classify_error,
    is_browser_error,
)


class TestBrowserErrorDetection:
    def test_cloudflare(self):
        assert is_browser_error("Cloudflare protection triggered")

    def test_chromium(self):
        assert is_browser_error("requires chromium-based web browser")

    def test_forbidden(self):
        assert is_browser_error("403 client error: forbidden")

    def test_plain_error_not_browser(self):
        assert not is_browser_error("Plugin failed to load")


class TestClassification:
    def test_browser(self):
        err = classify_error("https://kick.com/x", "kick", "requires a browser")
        assert isinstance(err, BrowserRequiredError)

    def test_plugin(self):
        err = classify_error("https://twitch.tv/x", "twitch", "stream went offline")
        assert isinstance(err, PluginError)
        assert err.platform == "twitch"
        assert err.url == "https://twitch.tv/x"


class TestErrorHierarchy:
    def test_all_subclass_base(self):
        for exc in (NoPluginError, NoStreamsError, BrowserRequiredError, PluginError):
            assert issubclass(exc, StreamlinkCoreError)

    def test_constructors_carry_url(self):
        assert NoPluginError("u").url == "u"
        assert NoStreamsError("u").url == "u"
        assert BrowserRequiredError("u").url == "u"
