"""Parity tests for URL parsing and metadata extraction."""

from tukiwatch_core.metadata import (
    extract_category_from_json,
    extract_category_keywords,
    extract_platform_from_url,
    extract_viewer_count,
    generate_fallback_thumbnail,
    parse_url_metadata,
)


class TestPlatformExtraction:
    def test_twitch(self):
        assert extract_platform_from_url("https://www.twitch.tv/someone") == "twitch"

    def test_youtube(self):
        assert (
            extract_platform_from_url("https://www.youtube.com/watch?v=x") == "youtube"
        )
        assert extract_platform_from_url("https://youtu.be/abc") == "youtube"

    def test_kick(self):
        assert extract_platform_from_url("https://kick.com/someone") == "kick"

    def test_unknown(self):
        assert extract_platform_from_url("https://example.com/foo") == "example"
        assert extract_platform_from_url("not-a-url") == "unknown"


class TestUrlParsing:
    def test_twitch_channel(self):
        meta = parse_url_metadata("https://www.twitch.tv/someuser123")
        assert meta.platform == "Twitch"
        assert meta.username == "someuser123"
        assert meta.url_type == "channel"

    def test_youtube_video(self):
        meta = parse_url_metadata("https://www.youtube.com/watch?v=abcdefghijk")
        assert meta.platform == "YouTube"
        assert meta.username == "abcdefghijk"
        assert meta.url_type == "video"

    def test_youtube_channel_handle(self):
        meta = parse_url_metadata("https://www.youtube.com/@myhandle")
        assert meta.platform == "YouTube"
        assert meta.username == "myhandle"

    def test_kick_channel(self):
        meta = parse_url_metadata("https://kick.com/streamer")
        assert meta.platform == "Kick"
        assert meta.username == "streamer"

    def test_invalid(self):
        meta = parse_url_metadata("garbage")
        assert meta.url_type == "parse_error"


class TestCategoryExtraction:
    def test_twitch_uses_game(self):
        result = extract_category_from_json(
            {"metadata": {"game": "Just Chatting", "title": "hello everyone"}}, "Twitch"
        )
        assert result == "Just Chatting"

    def test_twitch_falls_back_to_title(self):
        result = extract_category_from_json(
            {"metadata": {"title": "League of Legends stream"}}, "Twitch"
        )
        assert result == "League"

    def test_youtube_skips_short_first_word(self):
        result = extract_category_from_json(
            {"metadata": {"title": "is this the new meta?"}}, "YouTube"
        )
        assert result == "is this the"

    def test_youtube_short_article_not_in_skip_list(self):
        result = extract_category_from_json(
            {"metadata": {"title": "bg music for study"}}, "YouTube"
        )
        assert result == "music for study"

    def test_youtube_no_data(self):
        assert extract_category_from_json({}, "YouTube") == "N/A"

    def test_kick_splits_on_colon(self):
        result = extract_category_from_json(
            {"metadata": {"title": "Gaming: late night session"}}, "Kick"
        )
        assert result == "Gaming"

    def test_string_form_failure(self):
        assert extract_category_keywords((False, "error"), "Twitch") == "N/A"

    def test_string_form_bad_json(self):
        assert extract_category_keywords((True, "{not json"), "Twitch") == "N/A"


class TestViewerCount:
    def test_viewers(self):
        assert extract_viewer_count({"viewers": "1200"}) == 1200

    def test_viewer_count_key(self):
        assert extract_viewer_count({"viewer_count": 42}) == 42

    def test_online_key(self):
        assert extract_viewer_count({"online": 7}) == 7

    def test_missing(self):
        assert extract_viewer_count({}) is None

    def test_negative_ignored(self):
        assert extract_viewer_count({"viewers": -1}) is None

    def test_non_numeric(self):
        assert extract_viewer_count({"viewers": "abc"}) is None


class TestThumbnail:
    def test_kick_text_color(self):
        url = generate_fallback_thumbnail("kick", "Streamer")
        assert "color=000000" in url

    def test_twitch_purple(self):
        url = generate_fallback_thumbnail("twitch", "Streamer")
        assert "background=9146FF" in url

    def test_default_gray(self):
        url = generate_fallback_thumbnail("unknown", "Streamer")
        assert "background=6B7280" in url
