### Hi, I'm building the verification layer for coding agents

Agent configuration fails quietly. A skill whose description never matches, a
hook wired to an event name that doesn't exist, a context budget nobody is
measuring — none of these raise an error. They just make your agent quietly
worse, and you conclude the tooling wasn't that useful.

I build small, offline, zero-config tools that tell you before that happens.

**[skillprobe](https://github.com/paranoyouz-collab/skillprobe)** — lints agent
skills. Will they trigger, what do they cost you on *every turn*, and do any of
them collide? Run against a real skills directory it found a 1,624-token
standing cost and a name/directory mismatch nobody had noticed.

**[hookprobe](https://github.com/paranoyouz-collab/hookprobe)** — lints Claude
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

Also contributing upstream where the agent ecosystem is being built — currently
an arXiv data-source connector for
[cognee](https://github.com/topoteretes/cognee-community/pull/192).

📫 azougamine25@icloud.com
