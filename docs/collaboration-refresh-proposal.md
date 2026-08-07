# USMCC Website: Audit, Restructuring & Content Refresh Proposal

*Goal: shift the site from "a site about muon colliders" to "the home of the US Muon
Collider Collaboration" — who we are, how we're organized, what our goals are, and how
to join — while keeping the muon-collider science case as a strong, prominent pillar.*

---

## 1. Executive summary

The site is currently organized around **the muon collider as a machine and physics
case**, not around **the USMCC as an organization**. The physics content is genuinely
strong. But a newcomer who lands here to ask *"What is this collaboration, and how do I
join it?"* has to hunt: the collaboration's identity, structure, and org chart live
under **Contact**, "How to join" is a single `mailto:` line, and the mailing lists are
never explained.

The good news: **most of the raw material for a collaboration-centric site already
exists** — an org chart, elected leadership, a Leadership Strategy Group, a charter, ~300
members across ~80 institutions, a dedicated Indico, an events calendar, a seminar
series, and press. It is scattered and framed as "muon-collider info" rather than
"here is our collaboration." This is primarily an **information-architecture and framing**
problem, not a missing-content problem — which makes it high-impact and relatively
low-effort to fix.

This document proposes: (2) an audit, (3) a new navigation/IA, (4) a homepage refresh,
(5) new and rewritten pages, (6) new community features, (7) a phased rollout, and
(8) the handful of inputs we'd need from leadership to execute.

---

## 2. Audit

### 2.1 What's already here and working

- **Science & motivation** — `Why a muon collider?` / `Why now?` on the homepage; deep
  R&D pages for Accelerator, Detector, Physics, and Software (`content/posts/*`).
- **People** — ~300 members across ~80 institutions, auto-generated from a Google Sheet
  (`scripts/getPeople.py`), with area/career-stage pie charts.
- **Organizational assets** — an org chart (light/dark + PDF), six elected leadership
  profiles, the Leadership Strategy Group, a Speakers Committee, and a link to the
  Charter (currently buried in Resources).
- **Activity** — 6 upcoming + 21 past events, a dedicated Indico
  (`indico.muoncollider.us`), the weekly *Worlds Collide* seminar series, and highlighted
  recorded talks.
- **Outreach** — 13 press items, a resources/papers/logos library, merch, and social
  presence (Instagram, LinkedIn).
- **Solid technical base** — Hugo + Blowfish, auto-deploy to GitHub Pages, data-driven
  list sections (events/press) that new sections can copy.

### 2.2 The core problem

**The site conflates "the muon collider" (the machine/physics) with "the USMCC" (the
organization).** Concretely:

| Signal | Today | Should be |
|---|---|---|
| Homepage | An essay: *"Why a muon collider?"* | Introduces the collaboration first; science is a strong second |
| "About" menu | About the *physics* (Accel/Detector/Physics/Software R&D) | About the *collaboration* (mission, structure, join) |
| Collaboration identity, org chart | Hidden under **Contact** | A top-level "The Collaboration" area |
| How to join | One `mailto:` line at the bottom of the homepage | A prominent, step-by-step "Join Us" path |
| Mailing lists | Not explained; only two addresses appear | A directory of lists + how to subscribe |
| Collaboration goals | Not stated in plain language (Charter is a buried Drive link) | A clear Mission & Goals page |

### 2.3 Specific gaps — things a visitor cannot currently find

1. **What is the USMCC?** A one-paragraph identity (who we are, what we do, our
   relationship to IMCC / Fermilab / the national labs).
2. **Our mission and goals** — as an organization, distinct from "why a muon collider is
   scientifically compelling."
3. **How we're structured and governed** — the elected leadership model (leadership was
   elected in Aug 2025; the Coordinating Committee was the interim body from Snowmass
   2021), working groups/focus areas, and the charter in plain language.
4. **How to join** — who can join, what membership means, the registration form, and
   what's expected. Today this is a single email link.
5. **Which mailing lists exist and how to subscribe** — explicitly requested and
   essentially absent.
6. **Where the work happens** — working groups / focus areas with leads, scope, meeting
   links, and a "join this group" path.
7. **A newcomer "Start Here" path** — computing, software tutorials, which meetings to
   attend, who to contact.
8. **Orphaned content** — the *Common Misconceptions* page and the *Worlds Collide*
   seminar series / recorded talks exist but aren't in the navigation (the seminars live
   only inside `sociallinks.md`).

---

## 3. Proposed information architecture

Reframe the top nav so the **collaboration** leads and the **science** is its own clearly
labeled pillar.

### Before

```
About ▾ (Accelerator R&D · Detector R&D · Physics Case · Dedicated Software ·
         National Lab Study Group · IMCC)
Press · Events · Resources · Contact · People · Merch
```

### After

```
The Collaboration ▾   Mission & Goals · Structure & Governance ·
                      Member Institutions · Leadership (+ archive)
Join Us ▾   (prominent / button)   How to Join · Mailing Lists ·
                      Start Here (newcomers) · Open Positions
Science ▾   Why a Muon Collider · Physics Case · Accelerator R&D ·
                      Detector R&D · Software & Computing · Common Misconceptions
Meetings & Events ▾   Events · Seminars (Worlds Collide) · Collaboration Meetings
News            (rename of "Press"; adds collaboration announcements)
Resources
People
About ▾   Related efforts (IMCC · National Lab Study Group) · Contact · Merch
```

Key moves:
- **New "The Collaboration"** pillar — pulls the org identity out of "Contact."
- **New "Join Us"** pillar, styled as the primary call to action.
- **"About" → "Science"** — the current R&D content, honestly labeled, plus the
  orphaned *Misconceptions* page.
- **Related orgs (IMCC, National Lab Study Group)** move to a slim "About/Related"
  area rather than sitting alongside our own R&D.
- **"Press" → "News"** so we can post our own announcements, not only external coverage.

---

## 4. Homepage refresh

The homepage is currently a physics essay. Reframe it to introduce the collaboration
first, keep the science case as a strong section, and add clear calls to action.

Proposed flow:

1. **Hero** — "The US Muon Collider Collaboration" + a one-line identity
   (*"A community of ~300 researchers at ~80 institutions working to bring the energy
   frontier back to US soil."*) + two CTAs: **[Join the collaboration]** and
   **[Why a muon collider?]**
2. **"What we are" stat strip** — member count, institution count, founding/again, and
   IMCC partnership. These numbers are already computed in `getPeople.py` and can be
   generated automatically.
3. **"What we do / our goals"** — 3–4 cards: Accelerator R&D · Detector & Physics ·
   Strategy & Advocacy · Community & Training.
4. **"Why a muon collider?"** — a condensed version of today's pitch with "read more →"
   into the Science section (keeps the science front-and-center without burying the org).
5. **"Get involved" in three steps** — join the list · come to a meeting · find a
   working group — with the upcoming-events list pulled in.
6. **Latest news** — collaboration announcements + press.

---

## 5. New & rewritten pages (content refresh)

**New pages**

- **Mission & Goals** — plain-language mission and the collaboration's *organizational*
  goals: coordinate US muon-collider R&D, advocate through the P5 / strategy process,
  interface with IMCC, and train the next generation. Derive from the Charter.
- **Structure & Governance** — the org chart (already have it), how leadership is elected,
  the Leadership Strategy Group, working groups/focus areas (the accelerator/detector
  subgroups already listed in the leadership archive), and a plain-language charter
  summary with the PDF linked prominently (not buried in Resources).
- **How to Join** — eligibility (open to all career stages and institutions, no cost),
  what membership entails, the member registration form, and what to expect.
- **Mailing Lists** — a directory of the lists (coordination, speakers, and any
  announce / working-group lists) with a one-line purpose each and subscribe
  instructions. *(We'll need the actual list roster + subscribe links — see §8.)*
- **Start Here (newcomers)** — computing accounts, the software tutorials and
  `MuonColliderSoft`, which meetings to attend, and who to contact.

**Rewritten / re-homed**

- **Homepage** — per §4.
- **Contact** — slimmed to actual contact info; the org identity moves to "The
  Collaboration."
- **Common Misconceptions** — surfaced under Science (currently orphaned).
- **Seminars** — promote *Worlds Collide* + recorded talks out of `sociallinks.md` into a
  real page.
- **Science section** — light reframing so each R&D page opens with "how this fits the
  collaboration's goals / how to get involved in this area," not only the technical case.

---

## 6. New features useful for the community

Prioritized by (impact × ease). Items 1–4 are the highest impact for the least effort.

1. **Prominent "Join" flow** — a header button and hero CTA leading to the How-to-Join +
   Mailing Lists pages. *(Low effort, high impact.)*
2. **Mailing-list directory with subscribe links** — directly answers a top newcomer
   question. *(Low effort.)*
3. **Working-groups hub** — one card/page per working group: lead, scope, meeting link,
   "join this group." Turns the static org chart into living entry points. *(Medium.)*
4. **Jobs / opportunities board** — postdoc, student, and engineer openings across member
   institutions. Excellent recruiting tool for a growing collaboration; can reuse the
   data-driven `list` pattern already used for events/press. *(Medium.)*
5. **Interactive member map** — a US map of member institutions (the institution list
   already exists in the people data). Communicates "this is a real national
   collaboration" at a glance. *(Medium.)*
6. **Publications / results feed** — collaboration papers, notes, and key plots (today
   only external "overview papers" appear in Resources); an INSPIRE-HEP feed or curated
   list. *(Medium.)*
7. **Seminar archive with recordings** — browsable *Worlds Collide* + highlighted-talk
   archive with Panopto/Indico links and a calendar. *(Low–medium.)*
8. **Collaboration news / announcements** — leadership election, charter adoption,
   milestones — not just external press. *(Low.)*
9. **Calendar subscription (iCal)** for events and seminars. *(Low.)*
10. **Newcomer onboarding checklist / membership benefits.** *(Low.)*
11. **Governance transparency for members** — bylaws, meeting minutes, election info;
    could link to a members' area on Indico. *(Medium.)*
12. **Press / outreach kit** — consolidate logos, misconceptions, and press into one kit
    for journalists and members giving talks. *(Low.)*

---

## 7. Phased rollout

**Phase 1 — Framing (low effort, high impact).** Rewrite the homepage; add Mission &
Goals, How to Join, and Mailing Lists; reframe the nav (The Collaboration / Join Us /
Science); surface Misconceptions and the Seminar series. *This alone accomplishes the
core ask.*

**Phase 2 — Structure.** Structure & Governance page; Working-groups hub; interactive
member map; Start-Here newcomer guide.

**Phase 3 — Community features.** Jobs board; publications feed; seminar archive with
recordings; collaboration news; iCal; press/outreach kit.

---

## 8. What we'd need from leadership to execute

- **Mailing-list roster** — the authoritative list of lists (beyond `usmcc-coord@fnal.gov`
  and `usmcc-speakers@fnal.gov`), each list's purpose, and its subscribe link/instructions.
- **Member registration form URL** — the sign-up form that feeds the People Google Sheet,
  to link from "How to Join."
- **Mission & goals text** — a short approved statement (I can draft from the Charter for
  review).
- **Working-group definitions** — names, leads, scope, and meeting links for the WG hub.
- **Confirmation on scope** — whether to implement Phase 1 now or review this proposal
  first.

---

## 9. Technical feasibility

Almost everything here is markdown + menu reordering + a few new data-driven sections:

- **New sections** (jobs, news, seminars) copy the existing `list` shortcode pattern that
  already powers `events` and `press` — no theme surgery.
- **Homepage stat tiles** can reuse the member/area counters already computed in
  `scripts/getPeople.py`.
- **Member map** can be a lightweight static SVG/JS map fed by the existing institution
  list.
- **Nav changes** are edits to `config/_default/menus.en.toml`.
- **Orphaned content** (Misconceptions, Seminars) just needs menu entries and, for
  seminars, a small content move out of `sociallinks.md`.

No hosting or framework changes required; all of this deploys through the existing
GitHub Pages pipeline.
