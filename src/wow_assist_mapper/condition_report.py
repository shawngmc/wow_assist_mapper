"""
Build a Markdown reference table of every Assisted Combat step gated by a given
condition type, with each step spell's base cooldown and duration.

Cooldowns and durations are the spell's base values from the DB2 tables; talents
and other modifiers are not applied.
"""

import argparse
import logging
import sys

import pandas as pd

from wow_assist_mapper.skeleton import CSV_TABLE_DIR, resolve_build

_logger = logging.getLogger(__name__)

# DifficultyID 0 is the default (non-instance-specific) row for spell tables
DEFAULT_DIFFICULTY = 0

# Hand-maintained movement and buff labels; each *Source column is data, game (in-game knowledge) or unverified
SPELL_NOTES_FILE = "data/SpellNotes.csv"
NOTE_SOURCE_SUFFIXES = {"data": " (spell data)", "game": "", "unverified": " (unverified)"}


def read_table(table, build, **kwargs):
    return pd.read_csv(f"{CSV_TABLE_DIR}/{table}.{build}.csv", **kwargs)


def format_seconds(ms):
    seconds = ms / 1000
    return f"{seconds:g}s"


def get_cooldown(spell_id, cooldowns, categories, charge_categories):
    """Return a readable base cooldown, using the charge recharge time for charge spells."""
    category = categories.get(spell_id)
    if category is not None and category in charge_categories.index:
        charge_category = charge_categories.loc[category]
        recharge = format_seconds(charge_category["ChargeRecoveryTime"])
        max_charges = int(charge_category["MaxCharges"])
        if max_charges > 1:
            return f"{recharge} ({max_charges} charges)"
        return recharge

    cooldown = cooldowns.get(spell_id)
    if cooldown is None or max(cooldown) <= 0:
        return ""
    return format_seconds(max(cooldown))


def get_duration(spell_id, duration_indexes, durations):
    duration_index = duration_indexes.get(spell_id)
    if not duration_index:
        return ""
    duration = durations.get(duration_index)
    if duration is None:
        return ""
    if duration < 0:
        return "until used"
    return format_seconds(duration)


def get_note(spell_id, notes, column):
    """Return a hand-maintained label from SpellNotes.csv, marked with where it came from."""
    if spell_id not in notes.index:
        return ""
    label = notes.at[spell_id, column]
    source = notes.at[spell_id, f"{column}Source"]
    return label + NOTE_SOURCE_SUFFIXES.get(source, f" ({source})")


def build_report(condition_type, build):
    rules = read_table("AssistedCombatRule", build)
    steps = read_table("AssistedCombatStep", build)
    plans = read_table("AssistedCombat", build)
    specs = read_table("ChrSpecialization", build)
    classes = read_table("ChrClasses", build)
    spell_names = read_table("SpellName", build)

    cooldown_table = read_table("SpellCooldowns", build)
    cooldown_table = cooldown_table[cooldown_table["DifficultyID"] == DEFAULT_DIFFICULTY]
    misc_table = read_table("SpellMisc", build, usecols=["DifficultyID", "DurationIndex", "SpellID"])
    misc_table = misc_table[misc_table["DifficultyID"] == DEFAULT_DIFFICULTY]
    category_table = read_table("SpellCategories", build)
    category_table = category_table[category_table["DifficultyID"] == DEFAULT_DIFFICULTY]
    charge_categories = read_table("SpellCategory", build).set_index("ID")
    charge_categories = charge_categories[charge_categories["ChargeRecoveryTime"] > 0]
    duration_table = read_table("SpellDuration", build)

    names = dict(zip(spell_names["ID"], spell_names["Name_lang"]))
    cooldowns = {
        row.SpellID: (row.RecoveryTime, row.CategoryRecoveryTime)
        for row in cooldown_table.itertuples()
    }
    categories = dict(zip(category_table["SpellID"], category_table["ChargeCategory"]))
    duration_indexes = dict(zip(misc_table["SpellID"], misc_table["DurationIndex"]))
    durations = dict(zip(duration_table["ID"], duration_table["Duration"]))
    class_names = dict(zip(classes["ID"], classes["Name_lang"]))
    # keep_default_na=False stops pandas reading the label "None" as a missing value
    notes = pd.read_csv(SPELL_NOTES_FILE, keep_default_na=False).set_index("SpellID")

    gated_steps = steps[steps["ID"].isin(rules[rules["ConditionType"] == condition_type]["AssistedCombatStepID"])]
    gated_steps = gated_steps.merge(plans, left_on="AssistedCombatID", right_on="ID", suffixes=("", "_plan"))
    gated_steps = gated_steps.merge(specs[["ID", "Name_lang", "ClassID"]], left_on="ChrSpecializationID", right_on="ID", suffixes=("", "_spec"))
    gated_steps["ClassName"] = gated_steps["ClassID"].map(class_names)
    gated_steps = gated_steps.sort_values(["ClassName", "Name_lang", "OrderIndex"])

    lines = [
        f"# Steps gated by condition type {condition_type}",
        "",
        f"Build {build}. Cooldowns and durations are base spell values; talents and other modifiers are not applied.",
        "",
        f"Movement and Buff come from {SPELL_NOTES_FILE}: \"(spell data)\" is confirmed by the spell's effects, "
        "unmarked is from in-game knowledge, and blank means the spell has not been reviewed.",
        "",
        "| Class | Spec | Spell | Cooldown | Duration | Movement | Buff |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in gated_steps.itertuples():
        spell_id = int(row.SpellID)
        spell = f"{names.get(spell_id, 'Unknown')} ({spell_id})"
        cooldown = get_cooldown(spell_id, cooldowns, categories, charge_categories)
        duration = get_duration(spell_id, duration_indexes, durations)
        movement = get_note(spell_id, notes, "Movement")
        buff = get_note(spell_id, notes, "Buff")
        lines.append(f"| {row.ClassName} | {row.Name_lang} | {spell} | {cooldown} | {duration} | {movement} | {buff} |")
    return "\n".join(lines) + "\n"


def parse_args(args):
    parser = argparse.ArgumentParser(description="List Assisted Combat steps gated by a condition type")
    parser.add_argument(
        "-t",
        "--type",
        type=int,
        dest="condition_type",
        required=True,
        help="Condition type to report on (e.g. 70)",
    )
    parser.add_argument(
        "-b",
        "--build",
        type=str,
        help="Game build of the CSVs in data/csv_table to use (default: newest available)",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    print(build_report(args.condition_type, resolve_build(args.build)), end="")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
