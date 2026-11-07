# HackerTube for Roku — M0 playback spike

This repository currently contains the **playback diagnostic milestone**, not the
full HackerTube catalog browser. Authorized native YouTube playback is blocked;
see [the feasibility report](docs/PLAYBACK_FEASIBILITY.md). No physical Roku was
available for validation. Nothing has been published to GitHub.

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
python3 -m http.server 8080 --bind 0.0.0.0 --directory media
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
5. Press OK to start the diagnostic. Play/Pause pauses/resumes. Back stops it;
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
These steps still need end-to-end device verification.

## Scope and next decision

The full planned product includes all videos, topics, search, details, favorites
and Watch Later. Its implementation is pending acceptance of the phone-to-official-
YouTube fallback. Neither a catalog entry nor a handoff proves a video is playable
or watched. No YouTube extraction, media proxy, API credentials, analytics or
undocumented cross-app launch is included.

The official export is downloaded to ignored `data/hackertube-data.zip` for schema
inspection. See [attribution](ATTRIBUTION.md). Code is MIT licensed; dataset terms
are separate.
