# HackerTube for Roku

The latest app browses and plays the **6,454-video HackerTube catalog** with a
native thumbnail grid, search, topic filters and sorting. No account is needed.
See [installation, controls and validation](docs/CATALOG_BUILD_2.md).
Build it with Node 22 using `bash tools/build_catalog_app.sh`; install
`dist/hackertube-roku-catalog-build-2.zip`. The owner confirmed real-video playback
and transport controls in the preceding two-video milestone; this new catalog
UI awaits a TV test. The bundled catalog is the 2026-10-31 export snapshot.
The `vendor/playlet/` derivative retains Playlet's AGPL-3.0 license separately
from the original MIT diagnostic prototype below.

## Original diagnostic prototype

The original `roku/` app contains the **playback diagnostic milestone**, not the
full HackerTube catalog browser. Official YouTube integration remains unverified;
see [the feasibility report](docs/PLAYBACK_FEASIBILITY.md). The owner confirmed
installation, the 12-second test video, Play/Pause and Back on a Roku TV. The owner also confirmed OK-button pause/resume in build 3. Build 5
restores native player focus and seek controls, with an OK pause/resume fallback;
this combination awaits a device retest. Audio and exact model/OS
have not been confirmed. This repository is a prototype checkpoint.

## Build and check

Requirements: Python 3.10+, Node.js/npm; ffmpeg for the diagnostic media.

```sh
npm ci
npx bsc --project bsconfig.json
python3 -m unittest discover -s tests -v
python3 tools/package.py
```

Output: `dist/hackertube-roku-m0.zip` and its SHA-256 checksum. The ZIP has the
Roku manifest at its root. It is a developer sideload ZIP, not a signed `.pkg`.
Builds with identical source and sample URL produce identical ZIP bytes.

## Run the original test clip

```sh
sh tools/make_diagnostic.sh
python3 tools/serve_diagnostic.py --bind 0.0.0.0 --port 8080
```

Keep that terminal running. Find your Mac's LAN IP in System Settings → Network.
In another terminal, replacing `YOUR-MAC-IP`:

```sh
python3 tools/package.py --sample-url http://YOUR-MAC-IP:8080/diagnostic.mp4
```

Do not use localhost: on Roku it means the Roku itself. The generated clip is an
original test pattern with a 440 Hz tone. Turn the TV volume down before testing.
No network service is necessary for the default diagnostic menu; actual playback
requires the configured server. Stop the server with Ctrl-C when finished.

## Sideload

1. Put the Roku and Mac on the same LAN. Enable Roku developer mode with
   **Home ×3, Up ×2, Right, Left, Right, Left, Right**.
2. Follow the TV instructions, record the Roku IP, set a developer password,
   and reboot as directed.
3. On your Mac, visit `http://ROKU-IP`. Log in as `rokudev` with that password.
4. Upload `dist/hackertube-roku-m0.zip` using the Development Application Installer.
5. Press OK to start the diagnostic. During playback, OK or Play/Pause pauses/resumes. Left/Rewind and Right/Fast-forward use the native
   player seek controls. Back stops it;
   Back again exits. Record results in the feasibility report.

Only one sideloaded developer app is supported; installing replaces the previous
one. To update or roll back, upload the desired saved ZIP again. Registry
retention across reinstalls is not assumed (this spike stores no user data).

If the installer is unreachable, recheck the Roku IP after reboot and ensure
both devices share a LAN without client isolation or VPN interference. If login
fails, use the password set on the Roku. If installation reports a manifest
error, rebuild with the command above rather than zipping the parent folder.
For playback errors check the Mac IP, running server and firewall. Inspect the
Roku debug console on device port 8085 for `DIAGNOSTIC` state/error messages.
Installation and basic video playback were confirmed by the owner; remaining
device checks are tracked in docs/TEST_PLAN.md.

## Scope

The full planned product includes all videos, topics, search, details, favorites
and Watch Later. The owner chose to stop after the playback prototype;
full browser and phone-to-YouTube fallback development are not approved. Neither a catalog entry nor a handoff proves a video is playable
or watched. No YouTube extraction, media proxy, API credentials, analytics or
undocumented cross-app launch is included.

The official export is downloaded to ignored `data/hackertube-data.zip` for schema
inspection. See [attribution](ATTRIBUTION.md). Code is MIT licensed; dataset terms
are separate.
