# VOX "The Odyssey" Friday Showtime Notifier

Checks this page every 15 minutes and pushes a phone notification the moment
Friday (July 24, 2026) tickets open at VOX City Centre Almaza:

https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&m=the-odyssey&d=20260724

It stops notifying repeatedly once it's fired once (tracked in `state.txt`).

## Setup (10 minutes, no coding required)

1. **Create a GitHub account** if you don't have one (github.com) — free.
2. **Create a new repository** (public is simplest — Actions minutes are
   unlimited on public repos). Name it anything, e.g. `vox-odyssey-checker`.
3. **Upload these three files**, keeping the folder structure:
   - `check_showtimes.py`
   - `.github/workflows/check.yml`
   - `README.md` (optional, just for reference)

   Easiest way: on the repo page, click **Add file → Upload files**, drag
   all three in (GitHub will recreate the `.github/workflows/` folder
   automatically if you drag the whole folder, or create it manually first
   if uploading one by one).

4. **Get a notification channel** — install the free **ntfy** app
   ([iOS](https://apps.apple.com/app/ntfy/id1625396347) /
   [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)),
   open it, and subscribe to a topic name you make up — make it long and
   random so strangers can't guess it, e.g. `odyssey-almaza-x7k9q2`.

5. **Tell the script your topic name**: in your GitHub repo go to
   **Settings → Secrets and variables → Actions → Variables tab → New
   repository variable**:
   - Name: `NTFY_TOPIC`
   - Value: the topic you picked, e.g. `odyssey-almaza-x7k9q2`

6. **Turn it on**: go to the **Actions** tab of your repo. If prompted,
   click "I understand my workflows, enable them". Then open the "Check VOX
   Showtimes" workflow and click **Run workflow** once to test it
   immediately instead of waiting 15 minutes.

7. Check the run's log to confirm it says `available=False` (expected,
   since Friday isn't open yet). Once tickets open, you'll get a push
   notification titled "VOX showtimes open!" within 15 minutes.

## Notes / honest caveats

- I couldn't test this against the real VOX site myself — their site
  blocks automated tools from fetching it, so I built this from the page
  structure you showed me (looking for the exact phrase *"No showtimes
  could be found"* disappearing, plus a time like `7:30 PM` appearing).
  If VOX's site has bot-protection (Cloudflare etc.) the Action might fail
  outright — if so, paste me the error from the Actions log and I'll help
  adjust it.
- To re-arm it for testing, edit `state.txt` in the repo back to `waiting`.
- To stop it once you've booked, just disable the workflow (Actions tab →
  "..." menu → Disable workflow), or delete the repo.
