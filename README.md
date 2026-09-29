<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg">
  <img alt="Y.B. (drakeo338). 32 open-source fixes merged into 23 projects, including LangChain OpenWiki, MapLibre GL JS, Tencent BrowserSkill, Bazel rules_rust, Pake, VoiceStudio, Hindsight and DB-GPT. In memory of Drakeo the Ruler (1993-2021)." src="assets/card-light.svg" width="100%">
</picture>

### Merged upstream

<!-- merged:start -->
| Project | Stars | Fix |
|---|--:|---|
| [tw93/Pake #1393](https://github.com/tw93/Pake/pull/1393) | 61.8k | Set `StartupWMClass` so Linux docks match the window to its launcher |
| [debpalash/VoiceStudio #2174](https://github.com/debpalash/VoiceStudio/pull/2174) | 45.6k | Name every Kokoro language from the installed table |
| [vectorize-io/hindsight #4752](https://github.com/vectorize-io/hindsight/pull/4752) | 41.7k | Pass `anthropic.Timeout` so requests stop failing on anthropic 1.x |
| [t8y2/dbx #10275](https://github.com/t8y2/dbx/pull/10275) | 21.6k | Suggest columns inside select-list function calls (Fixes #10170) |
| [dream-num/univer #7744](https://github.com/dream-num/univer/pull/7744) | 21.5k | Reposition help card as formula text grows |
| [eosphoros-ai/DB-GPT #3264](https://github.com/eosphoros-ai/DB-GPT/pull/3264) | 20.1k | Connector confirm endpoints now require the API key |
| [langchain-ai/openwiki #914](https://github.com/langchain-ai/openwiki/pull/914) | 16.9k | Replace a legacy OpenWiki section instead of appending a duplicate |
| [maplibre/maplibre-gl-js #8553](https://github.com/maplibre/maplibre-gl-js/pull/8553) | 11.8k | Globe camera no longer throws when padding exceeds the viewport |
| [maplibre/maplibre-gl-js #8554](https://github.com/maplibre/maplibre-gl-js/pull/8554) | 11.8k | Color relief no longer packs to NaN when a DEM channel factor is 0 |
| [Tencent/BrowserSkill #283](https://github.com/Tencent/BrowserSkill/pull/283) | 7.8k | Re-arm lazy tools from history after a plugin reload |
| [MakazhanAlpamys/Soup #1256](https://github.com/MakazhanAlpamys/Soup/pull/1256) | 7.5k | Slice per-layer config lists so shrunk models save again |
| [MakazhanAlpamys/Soup #1377](https://github.com/MakazhanAlpamys/Soup/pull/1377) | 7.5k | Strip ANSI/wrap before asserting the #808 guard stayed silent |
| [MakazhanAlpamys/Soup #1382](https://github.com/MakazhanAlpamys/Soup/pull/1382) | 7.5k | Resolve the #361 harness's source SHA from soup_cli's tree, not the checkout's HEAD |
| [eugeniughelbur/obsidian-second-brain #310](https://github.com/eugeniughelbur/obsidian-second-brain/pull/310) | 4.6k | Resolve `bash` by path so WSL's launcher never runs the test suite |
| [skyhook-io/radar #1895](https://github.com/skyhook-io/radar/pull/1895) | 3.5k | Detect revisioned `istiod` deployments by label |
| [neomjs/neo #19154](https://github.com/neomjs/neo/pull/19154) | 3.3k | `isA()` walks past `component.Base` to any ancestor |
| [snapotter-hq/SnapOtter #1229](https://github.com/snapotter-hq/SnapOtter/pull/1229) | 2.8k | Auto-orient no longer re-compresses photos at default quality |
| [snapotter-hq/SnapOtter #1230](https://github.com/snapotter-hq/SnapOtter/pull/1230) | 2.8k | Reject non-finite zoom so a zero-distance pinch can't store NaN |
| [snapotter-hq/SnapOtter #1231](https://github.com/snapotter-hq/SnapOtter/pull/1231) | 2.8k | Log a failed deep-enhance pass instead of swallowing it |
| [snapotter-hq/SnapOtter #1247](https://github.com/snapotter-hq/SnapOtter/pull/1247) | 2.8k | Importer catches dropped rows on a pre-populated `--force` target |
| [jsverse/transloco #1026](https://github.com/jsverse/transloco/pull/1026) | 2.3k | Honor the sort option for `.pot` output |
| [zzet/gortex #826](https://github.com/zzet/gortex/pull/826) | 1.8k | Skip comments and string literals in the VB.NET call scan |
| [unstablebuild/rune #141](https://github.com/unstablebuild/rune/pull/141) | 1.2k | Space toggles multi-select boxes, and Enter no longer submits nil |
| [reticlehq/reticle #1169](https://github.com/reticlehq/reticle/pull/1169) | 915 | Read a native label for any labelable element, not just form fields |
| [reticlehq/reticle #1170](https://github.com/reticlehq/reticle/pull/1170) | 915 | Stop telling a bare-getter store that no store is registered |
| [reticlehq/reticle #1182](https://github.com/reticlehq/reticle/pull/1182) | 915 | Stop treating a bumped version token as a dropped write |
| [rust-fuzz/arbitrary #242](https://github.com/rust-fuzz/arbitrary/pull/242) | 883 | Move `derive_arbitrary` to syn 3 and raise the MSRV to 1.71 |
| [bazelbuild/rules_rust #4282](https://github.com/bazelbuild/rules_rust/pull/4282) | 846 | Set the Apple deployment target for rustc from the linker args |
| [desplega-ai/agent-swarm #1652](https://github.com/desplega-ai/agent-swarm/pull/1652) | 839 | Accept the dsh provider in PricingProviderSchema |
| [Harry-kp/vortix #361](https://github.com/Harry-kp/vortix/pull/361) | 696 | Add h/l as panel-nav aliases to help and docs |
| [apmantza/pi-lens #3486](https://github.com/apmantza/pi-lens/pull/3486) | 446 | Mark late auxiliary coverage at notify time, not at ceiling expiry |
| [apmantza/pi-lens #3643](https://github.com/apmantza/pi-lens/pull/3643) | 446 | Match latency report by path, not length delta (closes #3642) |
<!-- merged:end -->
