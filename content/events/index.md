---
title: Events
showHero: true 
heroStyle: background
layoutBackgroundHeaderSpace: false
#layout: simple
---

{{< list limit=10 where="Type" value="event_items_upcoming" title="Upcoming Events" cardView=false >}}

{{< list limit=10 where="Type" value="event_items_past" title="Past Events" cardView=false >}}