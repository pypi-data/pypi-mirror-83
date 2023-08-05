# replaCy Issue Boundary

A replaCy component to fix issue boundary, fix signle or double space at start, extend to next word if facing casing issue.

## Warning

Add after joiner to work

## Install

`poetry add replacy_issue_boundary`

or

`pip install replacy_issue_boundary`

## Usage

```python
import en_core_web_sm
from replacy import ReplaceMatcher
from replacy.db import load_json
from replacy_issue_boundary import IssueBoundary
from spacy.util import filter_spans


nlp = en_core_web_sm.load()
replaCy = ReplaceMatcher(nlp, load_json('path to match dict(s)'))
issue_boundary = IssueBoundary()
replaCy.add_pipe(name="span_filter", component=filter_spans, before="joiner")
replaCy.add_pipe(issue_boundary, name="article_agreer", after="joiner")
```

## Developing

The CI/CD in this project is great. GitHub Actions run linting and tests on any PR. If you merge into master, [release-drafter](https://github.com/marketplace/actions/release-drafter) drafts a new release based on PR commits and tags (e.g. if the PR is tagged `feature` and `minor` it will create a minor version bump with the changes labeled as Features).

I can't figure out the automatic versioning bit... leaving it in a broken state for now :/
