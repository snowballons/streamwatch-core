"""Domain models shared across StreamWatch consumers."""

from typing import Any

from pydantic import BaseModel, Field


class StreamStatus(BaseModel):
    """Status of a single stream URL after a liveness check."""

    url: str
    status: str = Field(description="online | offline | error")
    title: str = ""
    author: str = ""
    thumbnail: str = ""
    error: str = ""
    category: str = ""
    stream_id: str = ""
    platform: str = ""
    error_details: dict[str, Any] | None = None


class StreamResolution(BaseModel):
    """Full stream details including playback URLs."""

    status: str = Field(description="online | offline | error")
    title: str | None = None
    author: str | None = None
    thumbnail: str | None = None
    best_quality: str | None = None
    all_qualities: dict[str, str] | None = None
    error: str | None = None
    original_url: str | None = None
    category: str | None = None
    stream_id: str | None = None
    platform: str | None = None
    stream_types: list[str] | None = None
    error_details: dict[str, Any] | None = None


class UrlMetadata(BaseModel):
    """Parsed platform/username/type from a stream URL."""

    platform: str = "Unknown"
    username: str = "unknown_stream"
    url_type: str = "unknown"


class StreamMetadata(BaseModel):
    """Normalized metadata extracted from a stream."""

    title: str = ""
    author: str = ""
    category: str = ""
    stream_id: str = ""
    platform: str = ""
    thumbnail: str = ""
    viewer_count: int | None = None
    stream_types: list[str] = Field(default_factory=list)
