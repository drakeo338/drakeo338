I build small tools for the coding-agent ecosystem, mostly the unglamorous part:
checking that the things people drop into their agents actually work.

[skillprobe](https://github.com/drakeo338/skillprobe) lints agent skills — will it
trigger, what does it cost you on every turn, does it collide with another one.
Three things that fail silently, so nobody notices until something behaves oddly
and there's nothing in the logs to explain it.

[hookprobe](https://github.com/drakeo338/hookprobe) does the same for Claude Code
hooks, against the real event schema: events that don't exist, tool-name casing
that quietly never matches, matchers on the events that ignore them.

Both got most of their accuracy from being run against real shipped configs
rather than my own fixtures — which is how I found out my fixtures agreed with
my bugs.

The rest of the time I send fixes upstream. Recently to
[langchain-ai/openwiki](https://github.com/langchain-ai/openwiki),
[Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill),
[apache/maka](https://github.com/apache/maka) and
[debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio).
