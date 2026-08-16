"""streamwatch-core: shared stream-watching domain logic."""

from streamwatch_core.errors import (
    BrowserRequiredError,
    NoPluginError,
    NoStreamsError,
    PluginError,
    StreamlinkCoreError,
    classify_error,
    is_browser_error,
)
from streamwatch_core.metadata import (
    extract_category_from_json,
    extract_category_keywords,
    extract_platform_from_url,
    extract_viewer_count,
    generate_fallback_thumbnail,
    get_stream_types_from_streams,
    normalize_stream_metadata,
    parse_url_metadata,
)
from streamwatch_core.models import (
    StreamMetadata,
    StreamResolution,
    StreamStatus,
    UrlMetadata,
)
from streamwatch_core.resolution import StreamResolver, resolve_stream_details
from streamwatch_core.session_pool import StreamlinkSessionPool

__all__ = [
    "BrowserRequiredError",
    "NoPluginError",
    "NoStreamsError",
    "PluginError",
    "StreamlinkCoreError",
    "StreamlinkSessionPool",
    "StreamMetadata",
    "StreamResolution",
    "StreamResolver",
    "StreamStatus",
    "UrlMetadata",
    "classify_error",
    "extract_category_from_json",
    "extract_category_keywords",
    "extract_platform_from_url",
    "extract_viewer_count",
    "generate_fallback_thumbnail",
    "get_stream_types_from_streams",
    "is_browser_error",
    "normalize_stream_metadata",
    "parse_url_metadata",
    "resolve_stream_details",
]

__version__ = "0.1.0"
