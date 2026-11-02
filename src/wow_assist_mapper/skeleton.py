
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = wow_assist_mapper.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import os
import re
import sys
import time
from bs4 import BeautifulSoup
import pandas as pd
import json
from pprint import pprint
from enum import Enum

import requests

from wow_assist_mapper import __version__

__author__ = "Shawn McNaughton"
__copyright__ = "Shawn McNaughton"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

CSV_TABLE_DIR = "data/csv_table"

# Spell ID -> name, loaded from the SpellName DB2 table
spell_names = {}


class OutputFormat(Enum):
    RAW = "raw"
    TEXT = "text"

class PlayerClass(Enum):
    DEATH_KNIGHT = "DeathKnight"
    DEMON_HUNTER = "DemonHunter"
    DRUID = "Druid"
    EVOKER = "Evoker"
    HUNTER = "Hunter"
    MAGE = "Mage"
    MONK = "Monk"
    PALADIN = "Paladin"
    PRIEST = "Priest"
    ROGUE = "Rogue"
    SHAMAN = "Shaman"
    WARLOCK = "Warlock"
    WARRIOR = "Warrior"

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from wow_assist_mapper.skeleton import fib`,
# when using this Python module as a library.




# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Map Assist/Single-Button")
    parser.add_argument(
        "--version",
        action="version",
        version=f"wow_assist_mapper {__version__}",
    )
    # parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-c",
        "--class",
        type=str,
        dest="charclass",
        choices=[e.value for e in PlayerClass],
        help=f"Class to Examine ({', '.join(e.value for e in PlayerClass)})",
        required=True
    )
    parser.add_argument(
        "-s",
        "--spec",
        type=str,
        help="Spec to examine (e.g. Balance, Frost, BeastMastery,etc. - if there's a space, use CamelCase with an underscore )",
        required=True
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=[e.value for e in OutputFormat],
        help=f"Output format ({', '.join(e.value for e in OutputFormat)})",
        required=True
    )
    parser.add_argument(
        "-b",
        "--build",
        type=str,
        help="Game build of the CSVs in data/csv_table to use (e.g. 12.1.5.70688; default: newest available)",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stderr, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

def load_spell_names(build):
    spell_name_table = read_db_table('SpellName', build)
    spell_names.clear()
    spell_names.update(zip(spell_name_table['ID'].astype(int), spell_name_table['Name_lang']))


def get_spell_name(spellID):
    name = spell_names.get(int(spellID))
    if name is None:
        _logger.warning(f"Spell {spellID} not found in SpellName table")
        return f"Spell #{spellID}"
    return name


def check_spell_data(spellID):
    spell_data_dir = "data/wowhead/spells"
    spell_file = f'{spell_data_dir}/spell_{spellID}.json'
    if not os.path.exists(spell_file):
        _logger.info(f"Spell data for {spellID} does not exist, scraping from Wowhead")
        spell_data = scrape_spell_from_wowhead(int(spellID))
        if spell_data:
            with open(spell_file, 'w', encoding='utf-8') as f:
                json.dump(spell_data, f, ensure_ascii=False, indent=4)
            return spell_data
    else:
        _logger.info(f"Spell data for {spellID} already exists, loading from {spell_file}")
        with open(spell_file, 'r', encoding='utf-8') as f:
            return json.load(f)


def find_available_builds(csv_dir=CSV_TABLE_DIR):
    """List builds that have AssistedCombat CSVs downloaded, oldest first."""
    builds = []
    for file_name in os.listdir(csv_dir):
        match = re.fullmatch(r"AssistedCombat\.(\d+(?:\.\d+)*)\.csv", file_name)
        if match:
            builds.append(match.group(1))
    return sorted(builds, key=lambda build: tuple(int(part) for part in build.split(".")))


def main(args):
    """Wrapper allowing CLI usage

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting...")

    condition_map = pd.read_csv('data/ConditionTypeMap.csv', quoting=0, engine='python', quotechar='"')
    build = args.build
    if not build:
        available_builds = find_available_builds()
        if not available_builds:
            _logger.error(f"No AssistedCombat CSVs found in {CSV_TABLE_DIR}; run assist_fetch first")
            sys.exit(1)
        build = available_builds[-1]
    _logger.info(f"Using data from build {build}")
    classes, condition_types = parse_and_build_db_dumps(build)

    if args.format == OutputFormat.RAW.value:
        rotation = find_rotation(classes, args.charclass, args.spec)
        pprint(rotation)
    elif args.format == OutputFormat.TEXT.value:
        rotation = get_plaintext_rotation(classes, args.charclass, args.spec, condition_map)
        print(rotation)

    _logger.info("Script ends here")

# def get_file_types_in_cascs():
#     with open('data/casc_filelist/community-listfile.csv', "r") as file:
#         lines = file.readlines()
#     types = {}
#     for line in lines:
#         root, file_type = os.path.splitext(line)
#         file_type = file_type.lower().strip()
#         if file_type not in types:
#             types[file_type] = 0
#         types[file_type] += 1
#     return types


def read_db_table(table, build):
    return pd.read_csv(f'{CSV_TABLE_DIR}/{table}.{build}.csv', quoting=0, engine='python', quotechar='"')


def parse_and_build_db_dumps(build):
    chr_specs = read_db_table('ChrSpecialization', build)
    chr_classes = read_db_table('ChrClasses', build)
    assisted_combat = read_db_table('AssistedCombat', build)
    assisted_combat_rule = read_db_table('AssistedCombatRule', build)
    assisted_combat_step = read_db_table('AssistedCombatStep', build)
    load_spell_names(build)

    # Map character classes
    classes = {}
    for index, row in chr_classes.iterrows():
        _logger.info(f"Class Row {index}: {row.to_dict()}")
        class_key = row['Name_lang']
        classes[class_key] = {}
        classes[class_key]["raw_data"] = row.to_dict()
        classes[class_key]["ID"] = int(row['ID'])
        classes[class_key]["Name"] = row['Name_lang']
        classes[class_key]["specs"] = {}

    # TODO: Fix this - specs on diff classes with same name collide
    # Find the class that matches the spec ID
    # and add the spec to that class
    specs = {}
    for index, row in chr_specs.iterrows():
        _logger.info(f"Spec Row {index}: {row.to_dict()}")
        spec_key = row['ID']
        specs[spec_key] = {}
        specs[spec_key]["raw_data"] = row.to_dict()
        specs[spec_key]["ID"] = int(row['ID'])
        specs[spec_key]["Name"] = row['Name_lang']
        for player_class, class_data in classes.items():
            if class_data["ID"] == row["ClassID"]:
                class_data["specs"][spec_key] = specs[spec_key]

    # Add plans to specs
    assist_plans = {}
    for index, row in assisted_combat.iterrows():
        _logger.info(f"Assisted Combat Row {index}: {row.to_dict()}")
        assist_key = row['ID']
        assist_plans[assist_key] = {}
        assist_plans[assist_key]["steps"] = {}
        assist_plans[assist_key]["ID"] = int(row['ID'])
        for player_spec, spec_data in specs.items():
            if player_spec == row["ChrSpecializationID"]:
                spec_data["assist_plan"] = assist_plans[assist_key]

    # Add steps to plans
    assist_steps = {}
    for index, row in assisted_combat_step.iterrows():
        _logger.info(f"Assisted Combat Step Row {index}: {row.to_dict()}")
        step_key = int(row['ID'])
        assist_key = row['AssistedCombatID']
        assist_steps[step_key] = {}
        assist_steps[step_key]["ID"] = int(row['ID'])
        assist_steps[step_key]["SpellID"] = int(row['SpellID'])
        assist_steps[step_key]["SpellName"] = get_spell_name(assist_steps[step_key]["SpellID"])
        assist_steps[step_key]["OrderIndex"] = int(row['OrderIndex'])
        assist_steps[step_key]["rules"] = {}
        assist_plans[assist_key]["steps"][int(row['OrderIndex'])] = assist_steps[step_key]

    # Add rules to steps
    assist_rules = {}
    condition_types = {}
    for index, row in assisted_combat_rule.iterrows():
        _logger.info(f"Assisted Combat Rule Row {index}: {row.to_dict()}")
        rule_key = int(row['ID'])
        assist_step_key = int(row['AssistedCombatStepID'])
        if int(row['Field_11_1_7_60520_002']) != 0:
            _logger.warning(f"Field Field_11_1_7_60520_002 is non-zero: {row['Field_11_1_7_60520_002']}")
            _logger.warning(row.to_dict())
        assist_rules[rule_key] = {}
        assist_rules[rule_key]["ID"] = int(row['ID'])
        assist_rules[rule_key]["OrderIndex"] = int(row['OrderIndex'])
        assist_rules[rule_key]["raw"] = row.to_dict()
        assist_steps[assist_step_key]["rules"][int(row['OrderIndex'])] = assist_rules[rule_key]
        if not int(row['ConditionType']) in condition_types:
            condition_types[int(row['ConditionType'])] = f"{row['ConditionValue1']},{row['ConditionValue2']},{row['ConditionValue3']}"
    return classes, condition_types

def get_plaintext_rotation(classes, class_name, spec_name, condition_map):
    """Get the rotation for a given class and spec in plaintext format."""
    lines = []
    rotation = find_rotation(classes, class_name, spec_name)
    for index, step in enumerate(rotation, start=1):
        spell_name = step['SpellName']
        lines.append(f"{index}: Spell: {spell_name}")
        for rule_index, rule in sorted(step['rules'].items()):
            # Select conditionmap based on condition type
            cond_type = rule['raw'].get('ConditionType')
            rule_props = condition_map[condition_map['Type'] == cond_type]
            if rule_props.empty:
                raw = rule['raw']
                _logger.warning(f"Condition type {cond_type} is not in ConditionTypeMap.csv")
                lines.append(f"    if unknown condition type {cond_type} ({raw.get('ConditionValue1')},{raw.get('ConditionValue2')},{raw.get('ConditionValue3')})")
                continue

            # Prep vars, including resolving spells
            spell = f"'{spell_name}'"
            arg1 = rule['raw'].get('ConditionValue1')
            if rule_props.iloc[0]['Value1'].lower().startswith("spell"):
                arg1 = f"'{get_spell_name(arg1)}'"
            arg2 = rule['raw'].get('ConditionValue2')
            if rule_props.iloc[0]['Value2'].lower().startswith("spell"):
                arg2 = f"'{get_spell_name(arg2)}'"
            arg3 = rule['raw'].get('ConditionValue3')
            if rule_props.iloc[0]['Value3'].lower().startswith("spell"):
                arg3 = f"'{get_spell_name(arg3)}'"
            template = rule_props.iloc[0]['Description']
            lines.append("    " + eval('f"' + template + '"'))
    return "\n".join(lines)

def find_rotation(classes, class_name, spec_name):
    """Get the rotation for a given class and spec in plaintext format."""
    rotation = []
    clean_class_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', class_name)
    class_data = classes.get(clean_class_name)
    if class_data:
        clean_spec_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', spec_name)
        print(clean_spec_name)
        spec = None
        for spec_key, spec_data in class_data["specs"].items():
            if spec_data["Name"] == clean_spec_name:
                spec = spec_data
        if spec:
            assist_plan = spec.get("assist_plan")
            if assist_plan:
                for _, step in sorted(assist_plan.get("steps", {}).items()):
                    step_object = {}
                    step_object["SpellName"] = step["SpellName"]
                    step_object["rules"] = step["rules"]
                    rotation.append(step_object)
        else:
            _logger.error(f"Spec not found: {clean_spec_name}")   
    else:
        _logger.error(f"Class not found: {clean_class_name}")
    return rotation

def scrape_spell_from_wowhead(spellID):
    """Scrape spell information from Wowhead."""
    url = f"https://www.wowhead.com/spell={spellID}"
    response = requests.get(url)
    # Enforce sleep to not overload the server
    time.sleep(2)
    if response.status_code == 200:
        html_string = response.text

        soup = BeautifulSoup(html_string, 'html.parser')
        spell_name = soup.find("h1", class_="heading-size-1").text.strip()
        
        # Find the icon name
        # They inject via JS; luckily, the JS format looks predictable enough to get the name
        # Find the first instance of '"icon": ' in the raw HTML, then take until next double quote
        icon_name = None
        for line in html_string.splitlines():
            idx = line.find("\"icon\":\"")
            if idx != -1:
                icon_name = line[idx+8:]
                icon_name = icon_name.split("\"")[0]
                icon_url = f"https://wow.zamimg.com/images/wow/icons/large/{icon_name}.jpg"
        return {
            "id": spellID,
            "name": spell_name,
            "icon_name": icon_name,
            "icon_url": icon_url
        }
    return None

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m wow_assist_mapper.skeleton 42
    #
    run()
