# AlignDocs

Compare a public article against official GenLayer docs.
The contract stores one on-chain label: aligned, contradicts, outdated, off_topic.

## Live (Studio Next, chain 61997)

- App: https://bearbaba.github.io/AlignDocs/
- Contract: `0x3681aC016717f269D1bF1D6347816D027A6148FC`
- Studio: https://studio-next.genlayer.com/?import-contract=0x3681aC016717f269D1bF1D6347816D027A6148FC

Demo case 0: `aligned`, `resolved: true`.

## How to reproduce

1. Open the app and click Read verdict with case id 0.
2. Writes: in Studio Next call `submit` then `resolve` (browser wallets on this RC reject eth_sendRawTransaction).
3. Read `get_case` in Studio or in the app.