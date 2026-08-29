# AlignDocs

Compare a public article against official GenLayer docs.
Validators fetch both URLs and store one label on-chain:

- aligned
- contradicts
- outdated
- off_topic

Not a prediction oracle. Not an escrow.

Official hosts allowed as docs_url:
- docs.genlayer.com
- genlayer.com
- portal.genlayer.foundation

## Run

1. Open https://studio.genlayer.com/contracts
2. Paste contracts/aligndocs.py
3. Deploy
4. submit(article_url, docs_url)
5. resolve(id)
6. get_case(id)

Sample docs page:
https://docs.genlayer.com/understand-genlayer-protocol/what-is-genlayer
