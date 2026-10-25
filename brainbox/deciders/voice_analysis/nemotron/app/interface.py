from typing import Iterable
from foundation_kaia.marshalling import FileLike, service, JSON
from foundation_kaia.brainbox_utils import brainbox_endpoint, brainbox_websocket


@service
class INemotron:
    @brainbox_endpoint
    def transcribe(
            self,
            file: FileLike,
            language: str = 'auto',
            model: str | None = None,
            phrases: list[str] | None = None,
            boost: float = 2.0,
    ) -> JSON:
        """Transcribes a WAV file and returns `text`, detected `language` and word-level `words`.
        `phrases` (names, commands) are recognized more readily, the more the larger `boost` is (2-3 is typical)."""
        ...

    @brainbox_websocket
    def transcribe_stream(
            self,
            audio: Iterable[bytes] | FileLike,
            language: str = 'auto',
            sample_rate: int = 16000,
            model: str | None = None,
            phrases: list[str] | None = None,
            boost: float = 2.0,
    ) -> Iterable[dict[str, JSON]]:
        """Transcribes an audio stream (WAV stream, or raw mono PCM16 at `sample_rate`), yielding partial and final results as the audio arrives.
        `phrases` and `boost` are as in `transcribe`."""
        ...
