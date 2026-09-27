"""Client work shown as looping browser-window cards.

`clip` is (start, duration) in seconds inside the showcase recording made by
`bun run showcase <site>` in the meui-creative repo. Every recording is
1440x900 @ 60 fps, so a 16:10 window crops nothing.
"""

WORK = [
    {
        "slug": "bezove-udoli",
        "name": "V Bezovém Údolí",
        "line": "Boutique hotel in a 17th-century timbered cottage",
        "domain": "vbezovemudoli.cz",
        "url": "https://vbezovemudoli.cz",
        "stack": "Payload · Next.js · CZ/EN/DE",
        "clip": (0.6, 7.0),
    },
    {
        "slug": "3mag-events",
        "name": "3mag Events",
        "line": "Event platform for the CZ · DE · PL border region",
        "domain": "events.3mag.eu",
        "url": "https://events.3mag.eu",
        "stack": "MapLibre · Meilisearch · Gemini",
        "clip": (12.6, 7.0),
    },
    {
        "slug": "artglass",
        "name": "Artglass",
        "line": "Hand-made crystal chandeliers, Jablonec since 1993",
        "domain": "artglass.cz",
        "url": "https://artglass.cz",
        "stack": "Payload · GSAP · video",
        "clip": (1.0, 8.0),
    },
    {
        "slug": "masher",
        "name": "Masher",
        "line": "Protein porridge e-shop with a build-your-own box",
        "domain": "masher-store.cz",
        "url": "https://masher-store.cz",
        "stack": "E-commerce · configurator",
        "clip": (7.6, 7.0),
    },
    {
        "slug": "escapeboom",
        "name": "Escape Boom",
        "line": "Booking engine for five escape rooms and vouchers",
        "domain": "escapeboom.cz",
        "url": "https://escapeboom.cz",
        "stack": "Bookings · custom admin",
        "clip": (0.2, 6.6),
    },
    {
        "slug": "bitez",
        "name": "Bitez",
        "line": "Restaurant marketing, run from a phone app",
        "domain": "bitez.cz",
        "url": "https://bitez.cz",
        "stack": "SaaS · Capacitor app",
        "clip": (0.4, 6.4),
    },
]
