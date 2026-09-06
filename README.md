# AlignDocs

Compare a public article against official GenLayer docs.
Validators fetch both URLs and store one label on-chain:

- aligned
- contradicts
- outdated
- off_topic

Not a prediction oracle. Not an escrow.

Official hosts allowed as `docs_url`:

- docs.genlayer.com
- genlayer.com
- portal.genlayer.foundation

## Live

- App: https://bearbaba.github.io/AlignDocs/
- Hackathon contract (Studio): `0x422961567DCEEcd4CD4CC4Fd7f75239eC3884De8`
- Source: `contracts/aligndocs.py`

This build adds `list_by_label(label)` and `list_resolved()`.

## Verified cases on 0x4229…4De8

| id | sample | label |
| --- | --- | --- |
| 0 | samples/contradicts.md | contradicts |
| 1 | samples/aligned.md | aligned |
| 2 | samples/outdated.md | outdated |
| 3 | samples/off_topic.md | off_topic |

Docs URL used for all four:

https://docs.genlayer.com/understand-genlayer-protocol/what-is-genlayer

## Run in Studio

1. Open https://studio.genlayer.com
2. Paste `contracts/aligndocs.py` or load the address above
3. `submit(article_url, docs_url)`
4. `resolve(id)`
5. `get_case(id)` or `list_by_label("contradicts")`