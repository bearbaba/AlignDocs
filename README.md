# AlignDocs

Compare a community article to official GenLayer docs.
`resolve` fetches both pages and stores one label: aligned, contradicts, outdated, off_topic.

## Live (Studio Next, chain 61997 / 0xF22D)

- App: https://bearbaba.github.io/AlignDocs/
- Contract: `0x62060f5eAbEdf65d9FfDe18048f5481e8520BA0d`
- Studio: https://studio-next.genlayer.com/?import-contract=0x62060f5eAbEdf65d9FfDe18048f5481e8520BA0d

## Verified

| id | sample | label |
| --- | --- | --- |
| 0 | samples/contradicts.md | contradicts |

## How to check

1. Open Studio Next on the contract above.
2. Call `get_case(0)` — expect `contradicts`.
3. New cases: `submit` then `resolve` in Studio (browser wallets on this RC often reject `eth_sendRawTransaction`).
4. The app Read button shows case 0; live writes belong in Studio.