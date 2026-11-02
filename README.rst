.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/wow_assist_mapper.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/wow_assist_mapper
    .. image:: https://readthedocs.org/projects/wow_assist_mapper/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://wow_assist_mapper.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/wow_assist_mapper/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/wow_assist_mapper
    .. image:: https://img.shields.io/pypi/v/wow_assist_mapper.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/wow_assist_mapper/
    .. image:: https://img.shields.io/conda/vn/conda-forge/wow_assist_mapper.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/wow_assist_mapper
    .. image:: https://pepy.tech/badge/wow_assist_mapper/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/wow_assist_mapper
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/wow_assist_mapper

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=================
wow_assist_mapper
=================

Why?
- We may be able to recommend improvements to the rotation
- You can learn the rotation better by seeing why it decides what it does
- You can mix between single button and one/two spells to improve GCD loss

Usage
- assist_fetch: download the game data tables from wago.tools (latest retail build by default)
- assist_mapper -c Druid -s Balance -f text: print one spec's rotation as text
- assist_html: write every spec's rotation to out/rotations.html, with the data in out/rotations.json beside it (serve the folder to view it, e.g. python -m http.server in out/)
- assist_condition_report -t 70: list every step gated by a condition type

Suspected useless rules
Some resources (rage, runic power, soul shards, lunar power, pain, insanity) are stored at 10x or 100x their displayed value,
and the output converts them. A few rules come out far below the spell's own cost, so they can never block the step;
they look like values entered in display units by mistake. Tested in game on Guardian: Maul is suggested at 40-79 rage.
- Guardian Druid, Maul: "at least 8 rage" (stored 80); Maul costs 40 rage
- Frost Death Knight, Frost Strike: "at least 8 runic power" (stored 80); costs 35 runic power
- Frost Death Knight, Glacial Advance: "at least 8 runic power" (stored 80); costs 35 runic power
- Frost Death Knight, Empower Rune Weapon: "at most 8 runic power" (stored 80), while a second Empower Rune Weapon step uses "at most 80"

Example rotation for a Balance Druid:
```
1: Spell: Mark of the Wild
    if talent 'Mark of the Wild' is taken
    if player has resources to cast spell 'Mark of the Wild'
    if spell 'Mark of the Wild' is off cooldown
    if player has buff/debuff 'Mark of the Wild Highlight'
2: Spell: Moonkin Form
    if talent 'Moonkin Form' is taken
    if player has resources to cast spell 'Moonkin Form'
    if spell 'Moonkin Form' is off cooldown
    if player does not have buff/debuff 'Moonkin Form'
3: Spell: Sunfire
    if talent 'Sunfire' is taken
    if player has resources to cast spell 'Sunfire'
    if spell 'Sunfire' is off cooldown
    if target does not have buff/debuff 'Sunfire'
4: Spell: Force of Nature
    if talent 'Force of Nature' is taken
    if player has resources to cast spell 'Force of Nature'
    if spell 'Force of Nature' is off cooldown
    if player has buff/debuff 'Dream Surge'
5: Spell: Moonfire
    if talent 'Moonfire' is taken
    if player has resources to cast spell 'Moonfire'
    if spell 'Moonfire' is off cooldown
    if target does not have buff/debuff 'Moonfire'
    if player does not have buff/debuff 'Harmony of the Grove'
6: Spell: Celestial Alignment
    if talent 'Celestial Alignment' is taken
    if player has resources to cast spell 'Celestial Alignment'
    if spell 'Celestial Alignment' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if unknown condition 70 is met (seen gating cooldown and movement steps)
7: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if there are at least 3 targets within 10 yards of target
    if player does not have buff/debuff 'Lunar Eclipse Override'
    if player has buff/debuff 'Eclipse'
8: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if player does not have buff/debuff 'Lunar Calling'
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if there are at most 2 targets within 10 yards of target
    if player has buff/debuff 'Lunar Eclipse Override'
    if player has buff/debuff 'Eclipse'
9: Spell: Fury of Elune
    if talent 'Fury of Elune' is taken
    if player has resources to cast spell 'Fury of Elune'
    if spell 'Fury of Elune' is off cooldown
    if spell 'Fury of Elune' is within allowed range
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has at least 55 lunar power
10: Spell: Solar Eclipse
    if player has buff/debuff 'Eclipse'
    if player has resources to cast spell 'Solar Eclipse'
    if spell 'Solar Eclipse' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has at least 60 lunar power
11: Spell: Starfall
    if talent 'Starfall' is taken
    if player has resources to cast spell 'Starfall'
    if spell 'Starfall' is off cooldown
    if there are at least 3 targets within 45 yards of player
    if player has at least 90 lunar power
12: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if there are at most 2 targets within 45 yards of player
    if player has at least 90 lunar power
13: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player does not have buff/debuff 'Lunar Eclipse Override'
    if player has at most 59.9 lunar power
14: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has buff/debuff 'Lunar Eclipse Override'
    if player has at most 59.9 lunar power
15: Spell: Starfall
    if talent 'Starfall' is taken
    if player has resources to cast spell 'Starfall'
    if spell 'Starfall' is off cooldown
    if player has buff/debuff 'Starweaver's Warp'
16: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if player has buff/debuff 'Starweaver's Weft'
17: Spell: Starfall
    if talent 'Starfall' is taken
    if player has resources to cast spell 'Starfall'
    if spell 'Starfall' is off cooldown
    if there are at least 3 targets within 45 yards of player
18: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if there are at most 2 targets within 45 yards of player
19: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if player has at least 50 lunar power
20: Spell: Convoke the Spirits
    if talent 'Convoke the Spirits' is taken
    if player has resources to cast spell 'Convoke the Spirits'
    if spell 'Convoke the Spirits' is off cooldown
    if player has buff/debuff 'Eclipse (Solar)'
21: Spell: Convoke the Spirits
    if talent 'Convoke the Spirits' is taken
    if player has resources to cast spell 'Convoke the Spirits'
    if spell 'Convoke the Spirits' is off cooldown
    if player has buff/debuff 'Eclipse (Lunar)'
22: Spell: Fury of Elune
    if talent 'Fury of Elune' is taken
    if player has resources to cast spell 'Fury of Elune'
    if spell 'Fury of Elune' is off cooldown
    if spell 'Fury of Elune' is within allowed range
23: Spell: Wild Mushroom
    if talent 'Wild Mushroom' is taken
    if player has resources to cast spell 'Wild Mushroom'
    if spell 'Wild Mushroom' is off cooldown
    if target does not have buff/debuff 'Fungal Growth'
24: Spell: New Moon
    if talent 'New Moon' is taken
    if player has resources to cast spell 'New Moon'
    if spell 'New Moon' is off cooldown
25: Spell: Starfire
    if there are at least 3 targets within 10 yards of target
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if spell 'Starfire' can be successfully cast
    if spell 'Starfire' is within allowed range
26: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player has buff/debuff 'Lunar Calling'
    if spell 'Starfire' can be successfully cast
    if spell 'Starfire' is within allowed range
27: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if spell 'Wrath' can be successfully cast
    if spell 'Wrath' is within allowed range
28: Spell: Moonfire
```


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
