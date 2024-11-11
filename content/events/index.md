---
title: Events
showHero: true 
heroStyle: background
layoutBackgroundHeaderSpace: false
#layout: simple
---

<!-- Dates in the future can't be used for sorting. This list is sorted using weights. -->
{{< list limit=10 where="Type" value="event_items_upcoming" title="Upcoming Events" cardView=false >}}

<!-- This list is sorted by the date flag (must delete weights to move to here). -->
{{< list limit=100 where="Type" value="event_items_past" title="Past Events" cardView=false >}}