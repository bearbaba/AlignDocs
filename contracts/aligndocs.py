# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
import json
import typing

OFFICIAL_HOSTS = (
    "docs.genlayer.com",
    "genlayer.com",
    "portal.genlayer.foundation",
)

VALID_LABELS = (
    "aligned",
    "contradicts",
    "outdated",
    "off_topic",
)

MAX_URL = 300
MAX_REASON = 240
MAX_CLAIM_CHARS = 280
FETCH_CHARS = 8000


def _host(url: str) -> str:
    if not url.startswith("https://"):
        return ""
    rest = url[8:]
    host = rest.split("/")[0].split(":")[0].lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def _is_official(url: str) -> bool:
    return _host(url) in OFFICIAL_HOSTS


def _ok_url(url: str) -> bool:
    if len(url) < 12 or len(url) > MAX_URL:
        return False
    if not url.startswith("https://"):
        return False
    return "." in _host(url)


def _pair_key(article_url: str, docs_url: str) -> str:
    return article_url + "||" + docs_url


def _as_dict(raw: typing.Any) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        text = raw.strip()
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise gl.vm.UserError("resolver did not return JSON")
        return json.loads(text[start : end + 1])
    raise gl.vm.UserError("resolver returned unknown type")


@allow_storage
@dataclass
class Case:
    article_url: str
    docs_url: str
    label: str
    reason: str
    wrong_claims: str
    resolved: bool
    submitter: Address


class AlignDocs(gl.Contract):
    cases: DynArray[Case]
    pair_to_id: TreeMap[str, u256]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.view
    def is_official(self, url: str) -> bool:
        return _is_official(url)

    @gl.public.view
    def case_count(self) -> u256:
        return self.next_id

    @gl.public.view
    def get_case(self, case_id: u256) -> typing.Any:
        n = int(self.next_id)
        i = int(case_id)
        if i >= n:
            raise gl.vm.UserError("unknown case")
        c = self.cases[i]
        return {
            "id": str(i),
            "article_url": str(c.article_url),
            "docs_url": str(c.docs_url),
            "label": str(c.label),
            "reason": str(c.reason),
            "wrong_claims": str(c.wrong_claims),
            "resolved": bool(c.resolved),
            "submitter": str(c.submitter),
        }

    @gl.public.view
    def get_by_pair(self, article_url: str, docs_url: str) -> typing.Any:
        key = _pair_key(article_url, docs_url)
        stored = self.pair_to_id.get(key, u256(0))
        if stored == u256(0):
            return {"found": False}
        return {"found": True, "id": str(int(stored) - 1)}

    @gl.public.view
    def list_by_label(self, label: str) -> typing.Any:
        wanted = str(label).strip().lower()
        if wanted not in VALID_LABELS:
            raise gl.vm.UserError("label must be aligned, contradicts, outdated, or off_topic")
        ids = []
        n = int(self.next_id)
        i = 0
        while i < n:
            c = self.cases[i]
            if bool(c.resolved) and str(c.label) == wanted:
                ids.append(str(i))
            i += 1
        return {"label": wanted, "ids": ids, "count": str(len(ids))}

    @gl.public.view
    def list_resolved(self) -> typing.Any:
        rows = []
        n = int(self.next_id)
        i = 0
        while i < n:
            c = self.cases[i]
            if bool(c.resolved):
                rows.append(
                    {
                        "id": str(i),
                        "label": str(c.label),
                        "article_url": str(c.article_url),
                    }
                )
            i += 1
        return {"count": str(len(rows)), "cases": rows}

    @gl.public.write
    def submit(self, article_url: str, docs_url: str) -> u256:
        if not _ok_url(article_url):
            raise gl.vm.UserError("article_url must be https and short")
        if not _ok_url(docs_url):
            raise gl.vm.UserError("docs_url must be https and short")
        if not _is_official(docs_url):
            raise gl.vm.UserError("docs_url host is not official GenLayer")
        if _host(article_url) in OFFICIAL_HOSTS:
            raise gl.vm.UserError("article_url must be community text, not official docs")
        key = _pair_key(article_url, docs_url)
        if self.pair_to_id.get(key, u256(0)) != u256(0):
            raise gl.vm.UserError("this pair was already submitted")
        case_id = self.next_id
        case = Case(
            article_url=article_url,
            docs_url=docs_url,
            label="",
            reason="",
            wrong_claims="",
            resolved=False,
            submitter=gl.message.sender_address,
        )
        self.cases.append(case)
        self.pair_to_id[key] = case_id + u256(1)
        self.next_id = case_id + u256(1)
        return case_id

    @gl.public.write
    def resolve(self, case_id: u256) -> str:
        n = int(self.next_id)
        i = int(case_id)
        if i >= n:
            raise gl.vm.UserError("unknown case")
        if self.cases[i].resolved:
            raise gl.vm.UserError("already resolved")
        article_url = str(self.cases[i].article_url)
        docs_url = str(self.cases[i].docs_url)

        def get_input() -> str:
            article_page = gl.nondet.web.render(article_url, mode="text")
            docs_page = gl.nondet.web.render(docs_url, mode="text")
            return (
                "ARTICLE_URL: " + article_url
                + "\nDOCS_URL: " + docs_url
                + "\n\n--- ARTICLE TEXT ---\n" + str(article_page)[:FETCH_CHARS]
                + "\n\n--- OFFICIAL DOCS TEXT ---\n" + str(docs_page)[:FETCH_CHARS]
            )

        task = "Compare ARTICLE TEXT to OFFICIAL DOCS TEXT. Return JSON with keys label, reason, wrong_claims. label is aligned, contradicts, outdated, or off_topic. aligned = matches docs. contradicts = article conflicts with docs. outdated = article lags live docs. off_topic = not about this page. wrong_claims empty if aligned or off_topic."
        criteria = "Valid JSON. label is one of the four values. Judgment uses only the two fetched texts. Missing detail is not a contradiction."
        raw = gl.eq_principle.prompt_non_comparative(get_input, task=task, criteria=criteria)
        data = _as_dict(raw)
        label = str(data.get("label", "")).strip().lower()
        if label not in VALID_LABELS:
            raise gl.vm.UserError("invalid label")
        reason = str(data.get("reason", "")).strip()[:MAX_REASON]
        claims_raw = data.get("wrong_claims", [])
        if claims_raw is None:
            claims_raw = []
        if isinstance(claims_raw, str):
            claims_list = [claims_raw]
        elif isinstance(claims_raw, list):
            claims_list = [str(x) for x in claims_raw][:3]
        else:
            claims_list = []
        cleaned = []
        for item in claims_list:
            item = item.strip()
            if item:
                cleaned.append(item[:MAX_CLAIM_CHARS])
        if label in ("aligned", "off_topic"):
            cleaned = []
        self.cases[i].label = label
        self.cases[i].reason = reason
        self.cases[i].wrong_claims = " | ".join(cleaned)
        self.cases[i].resolved = True
        return label