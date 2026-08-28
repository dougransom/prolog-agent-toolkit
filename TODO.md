# Project TODOs & Release Announcement Checklist

## Release Announcement Plan

Checklist of communities and platforms to announce `prolog-agent-toolkit` once ready for official release:

### 1. Prolog & Logic Programming Communities
- [ ] **SWI-Prolog Discourse**: Post announcement in the *Announcements / Projects* category at [discourse.swi-prolog.org](https://discourse.swi-prolog.org).
- [ ] **Reddit r/prolog**: Post to [r/prolog](https://www.reddit.com/r/prolog/).
- [ ] **Scryer Prolog Community**: Share in Matrix channel (`#scryer:matrix.org`) / GitHub Discussions.
- [ ] **Awesome Lists**: Submit a PR to add `prolog-agent-toolkit` to `awesome-prolog`.

### 2. AI & Developer Community Aggregators
- [ ] **Hacker News (`Show HN`)**: Post with title such as *"Show HN: Prolog Agent Toolkit – Pure ISO/Scryer/SWI Prolog integration for AI Coding Agents"*.
- [ ] **Reddit r/Python**: Post as a Python developer project release.
- [ ] **Reddit r/LocalLLaMA & r/ArtificialIntelligence**: Frame around **Neurosymbolic AI** (LLMs for heuristics + Prolog for ground-truth verification).

### 3. Package & GitHub Release
- [ ] **PyPI**: Publish `prolog-agent-toolkit` package so `pip install prolog-agent-toolkit` / `uv add prolog-agent-toolkit` works out of the box.
- [ ] **GitHub Release**: Tag release `v0.1.0` following `prolog-agent release` guidelines in [.agents/skills/prolog-release/SKILL.md](.agents/skills/prolog-release/SKILL.md).

### 4. Content & Social Media
- [ ] **Technical Blog Post**: Publish short intro article on Dev.to / Hashnode / Medium.
- [ ] **Social Media Demo**: Share demo video / GIF on X (Twitter) and LinkedIn with `#Prolog` and `#AIAgents`.

---

## Post-First-Release Workflow Setup Prompt

When you are ready to cut the initial `v0.1.0` release and transition to a staged `main`/`dev` branch workflow, copy and send the prompt below to your AI assistant:

```markdown
Please execute the post-release branch and repository setup for prolog-agent-toolkit:

1. **Cut First Release to `main`**:
   - Run `prolog-agent release --version 0.1.0` to synchronize all version numbers.
   - Create a clean `main` branch from the current release commit.
   - Tag the commit as `v0.1.0` (`git tag -a v0.1.0 -m "Release v0.1.0"`).
   - Push `main` and tags (`v0.1.0`) to remote.

2. **Establish `dev` Staging Branch**:
   - Create and push a `dev` branch from `main` for ongoing staging.
   - Set `dev` as the default repository branch using GitHub CLI: `gh repo edit dougransom/prolog-agent-toolkit --default-branch dev`.

3. **PR Template & Guidelines**:
   - Create `.github/PULL_REQUEST_TEMPLATE.md` indicating that all incoming PRs should target the `dev` branch.
   - Update `CONTRIBUTING.md` to document the `main` (stable releases) vs `dev` (staging & PRs) workflow.

4. **Push & Verify**:
   - Push all configuration updates and confirm that `dev` is set as the default branch.
```

