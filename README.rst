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

TODOs
- Make an HTML visual representation of the rotations
- Figure out why some rules are contradictory (implied ORs?)
- Audit these - balance druid step 17 (Moonfire w/o rules) should never be worked past?

Example rotation for a Balance Druid:
```
1: Spell: Sunfire
    if talent 'Sunfire' is taken
    if player has resources to cast spell 'Sunfire'
    if spell 'Sunfire' is off cooldown
    if target does not have buff/debuff 'Sunfire'
2: Spell: Moonfire
    if talent 'Moonfire' is taken
    if player has resources to cast spell 'Moonfire'
    if spell 'Moonfire' is off cooldown
    if target does not have buff/debuff 'Moonfire'
    if player does not have buff/debuff 'Harmony of the Grove'
3: Spell: Starfall
    if talent 'Starfall' is taken
    if player has resources to cast spell 'Starfall'
    if spell 'Starfall' is off cooldown
    if there are more than 3 targets within 45 yards of player
4: Spell: Force of Nature
    if talent 'Force of Nature' is taken
    if player has resources to cast spell 'Force of Nature'
    if spell 'Force of Nature' is off cooldown
    if player has buff/debuff 'Dream Surge'
5: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if there are less than 2 targets within 45 yards of player
6: Spell: Fury of Elune
    if talent 'Fury of Elune' is taken
    if player has resources to cast spell 'Fury of Elune'
    if spell 'Fury of Elune' is off cooldown
    if spell 'Fury of Elune' is within allowed range
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has more than 550 lunar power
7: Spell: New Moon
    if talent 'New Moon' is taken
    if player has resources to cast spell 'New Moon'
    if spell 'New Moon' is off cooldown
8: Spell: Wild Mushroom
    if talent 'Wild Mushroom' is taken
    if player has resources to cast spell 'Wild Mushroom'
    if spell 'Wild Mushroom' is off cooldown
    if target does not have buff/debuff 'Fungal Growth'
9: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if spell 'Wrath' can be successfully cast
    if spell 'Wrath' is within allowed range
10: Spell: Starfire
    if there are more than 3 targets within 10 yards of target
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if spell 'Starfire' can be successfully cast
    if spell 'Starfire' is within allowed range
11: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player has buff/debuff 'Lunar Calling'
    if spell 'Starfire' can be successfully cast
    if spell 'Starfire' is within allowed range
12: Spell: Starfall
    if talent 'Starfall' is taken
    if player has resources to cast spell 'Starfall'
    if spell 'Starfall' is off cooldown
    if there are more than 3 targets within 45 yards of player
    if player has more than 900 lunar power
13: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if player has more than 900 lunar power
    if there are less than 2 targets within 45 yards of player
14: Spell: Moonkin Form
    if talent 'Moonkin Form' is taken
    if player has resources to cast spell 'Moonkin Form'
    if spell 'Moonkin Form' is off cooldown
    if player does not have buff/debuff 'Moonkin Form'
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
17: Spell: Moonfire
18: Spell: Starsurge
    if talent 'Starsurge' is taken
    if player has resources to cast spell 'Starsurge'
    if spell 'Starsurge' is off cooldown
    if player has more than 500 lunar power
19: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has buff/debuff 'Eclipse'
    if there are more than 3 targets within 10 yards of target
    if player does not have buff/debuff 'Lunar Eclipse Override'
20: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has buff/debuff 'Lunar Eclipse Override'
    if player has buff/debuff 'Eclipse'
    if player does not have buff/debuff 'Lunar Calling'
    if there are less than 2 targets within 10 yards of target
21: Spell: Starfire
    if talent 'Starfire' is taken
    if player has resources to cast spell 'Starfire'
    if spell 'Starfire' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has buff/debuff 'Lunar Eclipse Override'
    if player has less than 599 lunar power
22: Spell: Wrath
    if talent 'Wrath' is taken
    if player has resources to cast spell 'Wrath'
    if spell 'Wrath' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player does not have buff/debuff 'Lunar Eclipse Override'
    if player has less than 599 lunar power
23: Spell: Solar Eclipse
    if player has buff/debuff 'Eclipse'
    if player has resources to cast spell 'Solar Eclipse'
    if spell 'Solar Eclipse' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if player has more than 600 lunar power
24: Spell: Celestial Alignment
    if talent 'Celestial Alignment' is taken
    if player has resources to cast spell 'Celestial Alignment'
    if spell 'Celestial Alignment' is off cooldown
    if player does not have buff/debuff 'Eclipse (Solar)'
    if player does not have buff/debuff 'Eclipse (Lunar)'
    if unknown condition 70 is met (seen gating cooldown and movement steps)
25: Spell: Convoke the Spirits
    if talent 'Convoke the Spirits' is taken
    if player has resources to cast spell 'Convoke the Spirits'
    if spell 'Convoke the Spirits' is off cooldown
    if player has buff/debuff 'Eclipse (Solar)'
26: Spell: Convoke the Spirits
    if talent 'Convoke the Spirits' is taken
    if player has resources to cast spell 'Convoke the Spirits'
    if spell 'Convoke the Spirits' is off cooldown
    if player has buff/debuff 'Eclipse (Lunar)'
27: Spell: Mark of the Wild
    if talent 'Mark of the Wild' is taken
    if player has resources to cast spell 'Mark of the Wild'
    if spell 'Mark of the Wild' is off cooldown
    if player has buff/debuff 'Mark of the Wild Highlight'
28: Spell: Fury of Elune
    if talent 'Fury of Elune' is taken
    if player has resources to cast spell 'Fury of Elune'
    if spell 'Fury of Elune' is off cooldown
    if spell 'Fury of Elune' is within allowed range
```


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
