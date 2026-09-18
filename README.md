# AlignDocs

Compare a community article to official GenLayer docs.
`resolve` fetches both pages and stores one label: aligned, contradicts, outdated, off_topic.

## Live (Studio Next / studio-dev, chain 61997, 0xF22D)

- App: https://bearbaba.github.io/AlignDocs/
- Contract: `0x62060f5eAbEdf65d9FfDe18048f5481e8520BA0d`
- Studio: https://studio-next.genlayer.com/?import-contract=0x62060f5eAbEdf65d9FfDe18048f5481e8520BA0d
- RPC: `https://studio-dev.genlayer.com/api`
- App SDK: `genlayer-js@2.0.0-rc.1`

## Verified cases

| id | sample | label |
| --- | --- | --- |
| 0 | samples/contradicts.md | contradicts |
| 1 | samples/aligned.md | aligned |
| 2 | samples/outdated.md | contradicts |
| 3 | samples/off_topic.md | off_topic |
| 4 | samples/outdated.md (rewrite) | contradicts |

`outdated` is implemented in the contract. These outdated samples were labeled `contradicts` against current docs.

## How to use

1. Open Studio Next on the contract above.
2. `submit(article_url, docs_url)`.
3. `resolve(id)`, wait, then `get_case(id)`.