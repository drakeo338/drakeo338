### Hi, I'm building the verification layer for coding agents

Agent configuration fails quietly. A skill whose description never matches, a
hook wired to an event name that doesn't exist, a context budget nobody is
measuring — none of these raise an error. They just make your agent quietly
worse, and you conclude the tooling wasn't that useful.

I build small, offline, zero-config tools that tell you before that happens.

**[skillprobe](https://github.com/drakeo338/skillprobe)** — lints agent
skills. Will they trigger, what do they cost you on *every turn*, and do any of
them collide? Run against a real skills directory it found a 1,624-token
standing cost and a name/directory mismatch nobody had noticed.

**[hookprobe](https://github.com/drakeo338/hookprobe)** — lints Claude
Code hooks. A mistyped event, a lowercase tool name, a matcher on one of the ten
events that ignore matchers: all load fine and never run. It catches them
against the real 33-event schema.

Both are deterministic, need no API key, and exit non-zero so they work as CI
gates.

---

**How I work.** Both tools shipped with bugs caught by running them against real
repositories rather than my own fixtures. skillprobe's first reference check
produced four confident errors against a real project and every one was wrong.
hookprobe reported `MultiEdit` as an unknown tool because my list came from
memory. Those cases are regression tests now, each naming where it came from.
Fixtures written from the same assumption as the code will agree with the code.

**Upstream.** A fix in [VoiceStudio](https://github.com/debpalash/VoiceStudio/pull/2174)
is merged: an error message listed the languages Kokoro supports from a
hardcoded map instead of the installed table it validates against, so it named
eight of nine and told users to switch engines when they didn't need to. Review
caught something my own tests missed — the message advertised a label the
resolver still rejected, because I had asserted what the message *says* and
never that what it says can be passed back in. I write that round-trip
assertion by default now. Also open: a packaged-artifact size gate for
[Maka](https://github.com/apache/maka/pull/5455), a Windows hook-quoting fix
for [munder-difflin](https://github.com/chaitanyagiri/munder-difflin/pull/556),
and an arXiv connector for
[cognee](https://github.com/topoteretes/cognee-community/pull/192).

📫 paranoyouz@gmail.com
