# CDH Work Recap: Sumanth Gudla (Dec 2021 – Sep 2026)

A record of what I worked on in **Pega Customer Decision Hub** (repo `Pega-Customer-Decision-Hub/cdh-core`). It was built from git commits and GitHub PRs.

## Files
| File | What's inside |
|---|---|
| [feature-areas.md](feature-areas.md) | **Start here.** Features I built, grouped into 8 areas |
| [features-detailed.md](features-detailed.md) | **From Agile Studio:** each story's description, acceptance criteria, epic and points, grouped by release |
| [agile-insights.md](agile-insights.md) | **From Agile Studio:** epics, story points (198), and bugs by release, category and severity |
| [data/agile-studio-items.csv](data/agile-studio-items.csv) | All 233 Agile Studio items: status, release, epic, category, customer, description |
| [timeline-by-year.md](timeline-by-year.md) | Every work item, listed by year and then area |
| [resume-bullets.md](resume-bullets.md) | Ready-to-use bullets for a resume or appraisal |
| [data/work-items.csv](data/work-items.csv) | Raw list: date, Jira ID, type, category, title, commit |
| [data/github-prs.csv](data/github-prs.csv) | My 83 GitHub PRs (Nov 2025 onward, after the move from Bitbucket) |

## At a glance
- **About 650 commits** in total. With cherry-picks across release branches merged, that is **298 unique work items**.
- **39 user stories, 9 enhancements, 185 bugs, 23 hotfixes and 5 tasks.** The remaining 37 items have no Jira ID (mostly test automation).

| Year | Items | Main focus |
|---|---|---|
| 2021 | 2 | Onboarding; dev-environment and interaction fixes |
| 2022 | 53 | CPV, treatments (revert, dynamic SMS), withdrawn actions, Selenium suites |
| 2023 | 52 | Contact policies, Lock & Roll, lever weighting, personas, custom channels |
| 2024 | 55 | **Brand Voice (GenAI)**, multi-level contact policies, emergency exclusions, email templates |
| 2025 | 77 | **BeeFree email authoring and templates**, treatment sets, many hotfixes |
| 2026 | 59 | Plain-text/multipart email, BeeFree hardening, Infinity Studio alignment, Playwright |

| Area | Items |
|---|---|
| Treatments & Channels | 62 |
| Customer Profile Viewer & Personas | 58 |
| Email Authoring (BeeFree) & Templates | 40 |
| Brand Voice & GenAI | 32 |
| Test Automation | 30 |
| Ops Manager / Change Requests | 26 |
| Contact Policies & Emergency Exclusions | 25 |
| App Overview, Localization & Platform | 21 |

## How to refresh this later
Run this from the cdh-core repo in WSL:
```bash
git log --all --no-merges -i --author=sumanth --author=sumag --date=short --format='%ad|%h|%s'
gh pr list --author sumag_pega --state all --limit 1000
```

> **Limits:** this covers only `cdh-core`. Story details come from Agile Studio. Everything else comes from commit and PR titles. Areas are assigned by keyword, so a few items may sit in a slightly wrong area.
