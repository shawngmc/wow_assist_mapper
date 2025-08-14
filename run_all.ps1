mkdir out


New-Item -ItemType Directory -Path out/demonhunter -Force
assist_mapper.exe -c DemonHunter -s Havoc -f text > ./out/demonhunter/havoc.txt
assist_mapper.exe -c DemonHunter -s Vengeance -f text > ./out/demonhunter/vengeance.txt

New-Item -ItemType Directory -Path out/deathknight -Force
assist_mapper.exe -c DeathKnight -s Blood -f text > ./out/deathknight/blood.txt
assist_mapper.exe -c DeathKnight -s Frost -f text > ./out/deathknight/frost.txt
assist_mapper.exe -c DeathKnight -s Unholy -f text > ./out/deathknight/unholy.txt

New-Item -ItemType Directory -Path out/druid -Force
assist_mapper.exe -c Druid -s Balance -f text > ./out/druid/balance.txt
assist_mapper.exe -c Druid -s Restoration -f text > ./out/druid/restoration.txt
assist_mapper.exe -c Druid -s Feral -f text > ./out/druid/feral.txt
assist_mapper.exe -c Druid -s Guardian -f text > ./out/druid/guardian.txt

New-Item -ItemType Directory -Path out/evoker -Force
assist_mapper.exe -c Evoker -s Augmentation -f text > ./out/evoker/augmentation.txt
assist_mapper.exe -c Evoker -s Devastation -f text > ./out/evoker/devastation.txt
assist_mapper.exe -c Evoker -s Preservation -f text > ./out/evoker/preservation.txt

New-Item -ItemType Directory -Path out/hunter -Force
assist_mapper.exe -c Hunter -s BeastMastery -f text > ./out/hunter/beastmastery.txt
assist_mapper.exe -c Hunter -s Marksmanship -f text > ./out/hunter/marksmanship.txt
assist_mapper.exe -c Hunter -s Survival -f text > ./out/hunter/survival.txt

New-Item -ItemType Directory -Path out/mage -Force
assist_mapper.exe -c Mage -s Fire -f text > ./out/mage/fire.txt
assist_mapper.exe -c Mage -s Frost -f text > ./out/mage/frost.txt
assist_mapper.exe -c Mage -s Arcane -f text > ./out/mage/arcane.txt

New-Item -ItemType Directory -Path out/monk -Force
assist_mapper.exe -c Monk -s Brewmaster -f text > ./out/monk/brewmaster.txt
assist_mapper.exe -c Monk -s Mistweaver -f text > ./out/monk/mistweaver.txt
assist_mapper.exe -c Monk -s Windwalker -f text > ./out/monk/windwalker.txt

New-Item -ItemType Directory -Path out/paladin -Force
assist_mapper.exe -c Paladin -s Holy -f text > ./out/paladin/holy.txt
assist_mapper.exe -c Paladin -s Protection -f text > ./out/paladin/protection.txt
assist_mapper.exe -c Paladin -s Retribution -f text > ./out/paladin/retribution.txt

New-Item -ItemType Directory -Path out/priest -Force
assist_mapper.exe -c Priest -s Holy -f text > ./out/priest/holy.txt
assist_mapper.exe -c Priest -s Discipline -f text > ./out/priest/discipline.txt
assist_mapper.exe -c Priest -s Shadow -f text > ./out/priest/shadow.txt

New-Item -ItemType Directory -Path out/rogue -Force
assist_mapper.exe -c Rogue -s Assassination -f text > ./out/rogue/assassination.txt
assist_mapper.exe -c Rogue -s Subtlety -f text > ./out/rogue/subtlety.txt
assist_mapper.exe -c Rogue -s Outlaw -f text > ./out/rogue/outlaw.txt

New-Item -ItemType Directory -Path out/shaman -Force
assist_mapper.exe -c Shaman -s Elemental -f text > ./out/shaman/elemental.txt
assist_mapper.exe -c Shaman -s Enhancement -f text > ./out/shaman/enhancement.txt
assist_mapper.exe -c Shaman -s Restoration -f text > ./out/shaman/restoration.txt

New-Item -ItemType Directory -Path out/warlock -Force
assist_mapper.exe -c Warlock -s Demonology -f text > ./out/warlock/demonology.txt
assist_mapper.exe -c Warlock -s Affliction -f text > ./out/warlock/affliction.txt
assist_mapper.exe -c Warlock -s Destruction -f text > ./out/warlock/destruction.txt

New-Item -ItemType Directory -Path out/warrior -Force
assist_mapper.exe -c Warrior -s Protection -f text > ./out/warrior/protection.txt
assist_mapper.exe -c Warrior -s Fury -f text > ./out/warrior/fury.txt
assist_mapper.exe -c Warrior -s Arms -f text > ./out/warrior/arms.txt
