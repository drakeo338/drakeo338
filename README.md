<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg">
  <img alt="Y.B. (drakeo338). Open-source fixes merged into LangChain OpenWiki, MapLibre GL JS, Tencent BrowserSkill, Bazel rules_rust, Pake, Hindsight, VoiceStudio, Neo.mjs, SnapOtter, Transloco and Rune. In memory of Drakeo the Ruler (1993-2021)." src="assets/card-light.svg" width="100%">
</picture>

### Merged upstream

| Project | Fix |
|---|---|
| [langchain-ai/openwiki #914](https://github.com/langchain-ai/openwiki/pull/914) | Replace a legacy OpenWiki section instead of appending a duplicate |
| [maplibre/maplibre-gl-js #8553](https://github.com/maplibre/maplibre-gl-js/pull/8553) | Globe camera no longer throws when padding exceeds the viewport |
| [maplibre/maplibre-gl-js #8554](https://github.com/maplibre/maplibre-gl-js/pull/8554) | Color relief no longer packs to NaN when a DEM channel factor is 0 |
| [Tencent/BrowserSkill #283](https://github.com/Tencent/BrowserSkill/pull/283) | Re-arm lazy tools from history after a plugin reload |
| [bazelbuild/rules_rust #4282](https://github.com/bazelbuild/rules_rust/pull/4282) | Set the Apple deployment target for rustc from the linker args |
| [tw93/Pake #1393](https://github.com/tw93/Pake/pull/1393) | Set `StartupWMClass` so Linux docks match the window to its launcher |
| [vectorize-io/hindsight #4752](https://github.com/vectorize-io/hindsight/pull/4752) | Pass `anthropic.Timeout` so requests stop failing on anthropic 1.x |
| [debpalash/VoiceStudio #2174](https://github.com/debpalash/VoiceStudio/pull/2174) | Name every Kokoro language from the installed table |
| [neomjs/neo #19154](https://github.com/neomjs/neo/pull/19154) | `isA()` walks past `component.Base` to any ancestor |
| [snapotter-hq/SnapOtter #1229](https://github.com/snapotter-hq/SnapOtter/pull/1229) | Auto-orient no longer re-compresses photos at default quality |
| [snapotter-hq/SnapOtter #1230](https://github.com/snapotter-hq/SnapOtter/pull/1230) | Reject non-finite zoom so a zero-distance pinch can't store NaN |
| [snapotter-hq/SnapOtter #1247](https://github.com/snapotter-hq/SnapOtter/pull/1247) | Importer catches dropped rows on a pre-populated `--force` target |
| [jsverse/transloco #1026](https://github.com/jsverse/transloco/pull/1026) | Honor the sort option for `.pot` output |
| [unstablebuild/rune #141](https://github.com/unstablebuild/rune/pull/141) | Space toggles multi-select boxes, and Enter no longer submits nil |
