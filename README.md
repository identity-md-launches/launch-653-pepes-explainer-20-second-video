# $PEPES explainer video

Deliverables:

- `artifacts/video.mp4` — 20.000 s, 1080×1350, 30 fps, H.264/yuv420p video with AAC-LC stereo audio at 48 kHz, fast-start MP4, 1.7 MB.
- `artifacts/video_16x9.mp4` — 20.000 s, 1920×1080 reframe with the same content and audio, 0.7 MB.

The video uses flat, procedurally drawn cartoon frogs, a white background, green/gold accents, bitmap IBM Plex Mono-style captions, six timed voice-over lines, and a low-level generated two-tone beat. The voice-over and captions include the requested hypothetical-scenario and not-financial-advice language. The end card is held from 17.0 s through 20.0 s.

Limitations: the voice is an offline-rendered web TTS voice rather than a recorded human performer; the music and effects are simple synthesized placeholders rather than a separately mastered production cue. The supplied MP4s are well under the 25 MB limit.

Source/build helpers are `build_video.py` and `make_audio.py`; they use the runtime's installed `ffmpeg` executable.
