---
title: "Dedicated Software"
description: ""
cascade:
  showReadingTime: false
---

**Great progress has been made towards identifying signals and reject muon beam-induced background, but there's still much more to do. Check out software packages [here](https://github.com/MuonColliderSoft), and join the [meetings](https://indico.cern.ch/category/18214/) hosted by IMCC.**

## Software and Simulation Needs

In the next 3–5 years, studies towards a muon collider are expected to expand and encompass both accelerator and detector design. To support such studies, an adequate computing infrastructure and software suite is needed. Most of the contribution is focused on the needs for detector design studies, with the assumption that local resources will suffice for most of the accelerator studies, unless noted.

In terms of infrastructure, the requirements are driven by the large size of BIB simulations, which range from 0.08 to 36 GB per event, depending on the level of truth information and energy threshold of particles stored. Existing resources outside the US provide O(100-200) PB of storage, with different authentication methods. CPU requirements are also driven by full simulation studies and BIB simulations; in particular a large memory footprint and lack of multi-threading support currently limits the efficiency of using HPC resources. A toy model that assesses what type and how many studies should be supported in parallel was used to assess that ~500 TB of disk space and ~2M CPU hours a year would be needed to satisfy the most urgent needs in the next few years. Work on a unified authentication mechanism and easy solutions for transferring files across the different storage system available is a high priority.

In terms of the software suite, different domains were considered: theory, detector and accelerator studies. For theory, there’s a well maintained set of software tools already available; it is envisaged that close collaboration with detector studies will be highly beneficial. For accelerator-related studies, lots of dedicated programs are used; a point of attention is the recent move from MARS to FLUKA to simulate BIB, and the open question of keeping support and development of MARS active or not. On the detector side, a taskforce within IMCC is being setup to address the most urgent needs of the community in the coming years; points of attention include the migration to the key4hep framework, support for fast simulations, the development of a complete software development model, including building and validation of software releases, and a well-maintained documentation and user support channel. A significant need for further developing realistic reconstruction algorithms is also apparent to strengthen the robustness of the physics message.

Dedicated computing resources in US will be useful to support a growing community; in the short-term, we should make best use of what is already available; in the medium-term, we need to prepare to acquire dedicated resources that are easily compatible with existing ones and prepare to make use of HPC centers efficiently.