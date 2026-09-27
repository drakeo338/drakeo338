<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg">
  <img alt="Y.B. (drakeo338). 21 open-source fixes merged into 17 projects, including LangChain OpenWiki, MapLibre GL JS, Tencent BrowserSkill, Bazel rules_rust, Pake, VoiceStudio, Hindsight and DB-GPT. In memory of Drakeo the Ruler (1993-2021)." src="assets/card-light.svg" width="100%">
</picture>

### Merged upstream

| Project | Stars | Fix |
|---|--:|---|
| [tw93/Pake #1393](https://github.com/tw93/Pake/pull/1393) | 61.8k | Set `StartupWMClass` so Linux docks match the window to its launcher |
| [debpalash/VoiceStudio #2174](https://github.com/debpalash/VoiceStudio/pull/2174) | 39.8k | Name every Kokoro language from the installed table |
| [vectorize-io/hindsight #4752](https://github.com/vectorize-io/hindsight/pull/4752) | 37.1k | Pass `anthropic.Timeout` so requests stop failing on anthropic 1.x |
| [eosphoros-ai/DB-GPT #3264](https://github.com/eosphoros-ai/DB-GPT/pull/3264) | 20.1k | Connector confirm endpoints now require the API key |
| [langchain-ai/openwiki #914](https://github.com/langchain-ai/openwiki/pull/914) | 16.8k | Replace a legacy OpenWiki section instead of appending a duplicate |
| [maplibre/maplibre-gl-js #8553](https://github.com/maplibre/maplibre-gl-js/pull/8553) | 11.8k | Globe camera no longer throws when padding exceeds the viewport |
| [maplibre/maplibre-gl-js #8554](https://github.com/maplibre/maplibre-gl-js/pull/8554) | 11.8k | Color relief no longer packs to NaN when a DEM channel factor is 0 |
| [Tencent/BrowserSkill #283](https://github.com/Tencent/BrowserSkill/pull/283) | 7.5k | Re-arm lazy tools from history after a plugin reload |
| [MakazhanAlpamys/Soup #1256](https://github.com/MakazhanAlpamys/Soup/pull/1256) | 7.4k | Slice per-layer config lists so shrunk models save again |
| [eugeniughelbur/obsidian-second-brain #310](https://github.com/eugeniughelbur/obsidian-second-brain/pull/310) | 4.6k | Resolve `bash` by path so WSL's launcher never runs the test suite |
| [skyhook-io/radar #1895](https://github.com/skyhook-io/radar/pull/1895) | 3.5k | Detect revisioned `istiod` deployments by label |
| [neomjs/neo #19154](https://github.com/neomjs/neo/pull/19154) | 3.3k | `isA()` walks past `component.Base` to any ancestor |
| [snapotter-hq/SnapOtter #1229](https://github.com/snapotter-hq/SnapOtter/pull/1229) | 2.8k | Auto-orient no longer re-compresses photos at default quality |
| [snapotter-hq/SnapOtter #1230](https://github.com/snapotter-hq/SnapOtter/pull/1230) | 2.8k | Reject non-finite zoom so a zero-distance pinch can't store NaN |
| [snapotter-hq/SnapOtter #1231](https://github.com/snapotter-hq/SnapOtter/pull/1231) | 2.8k | Log a failed deep-enhance pass instead of swallowing it |
| [snapotter-hq/SnapOtter #1247](https://github.com/snapotter-hq/SnapOtter/pull/1247) | 2.8k | Importer catches dropped rows on a pre-populated `--force` target |
| [jsverse/transloco #1026](https://github.com/jsverse/transloco/pull/1026) | 2.3k | Honor the sort option for `.pot` output |
| [unstablebuild/rune #141](https://github.com/unstablebuild/rune/pull/141) | 1.2k | Space toggles multi-select boxes, and Enter no longer submits nil |
| [rust-fuzz/arbitrary #242](https://github.com/rust-fuzz/arbitrary/pull/242) | 883 | Move `derive_arbitrary` to syn 3 and raise the MSRV to 1.71 |
| [bazelbuild/rules_rust #4282](https://github.com/bazelbuild/rules_rust/pull/4282) | 845 | Set the Apple deployment target for rustc from the linker args |
| [apmantza/pi-lens #3486](https://github.com/apmantza/pi-lens/pull/3486) | 443 | Mark late auxiliary coverage at notify time, not at ceiling expiry |
