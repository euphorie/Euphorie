"""
This script attempts to autotranslate the missing entries in the po files.

It uses the `trans` command line tool to perform translations.
https://github.com/soimort/translate-shell
on macos, you can install it via homebrew: brew install translate-shell

"""

import argparse
import os
import polib
import subprocess


def translate_text(text, target_lang="xx"):
    """Translate text using trans CLI."""
    target_lang = ":" + target_lang
    print(f"Translating {text} to {target_lang}...")
    try:
        result = subprocess.run(
            ["trans", "--brief", target_lang, text], capture_output=True, text=True
        )
        translation = result.stdout.strip() if result.returncode == 0 else None
        print(f"Translation result: {translation}")
        return translation
    except FileNotFoundError:
        return "The 'translate' command is not available on this system."


def translate_po_files(
    i18n_path,
    lang,
    label=None,
    only_num_untranslated=False,
    all_languages=False,
    dry_run=False,
):
    """Translate po files for a specific language or all available languages."""
    available_languages = []
    for ldir in os.listdir(i18n_path):
        lang_path = os.path.join(i18n_path, ldir, "LC_MESSAGES")
        if os.path.isdir(lang_path):
            available_languages.append(ldir)

    print(f"Available languages: {available_languages}")
    languages = [lang] if not all_languages else available_languages
    print("Translating to languages:", languages)
    errors = []

    for lang in languages:
        lang_path = os.path.join(i18n_path, lang, "LC_MESSAGES")
        if not os.path.isdir(lang_path):
            os.makedirs(lang_path, exist_ok=True)
            print(f"Created missing directory: {lang_path}")
        print(f"Translating to {lang}...")
        for file in os.listdir(lang_path):
            if file.endswith(".po"):
                po = polib.pofile(os.path.join(lang_path, file))
                update_counter = 0
                u_num = len(po.untranslated_entries())
                print(f"Untranslated entries in {lang} {file}: {u_num}")
                if only_num_untranslated:
                    continue
                for entry in po.untranslated_entries():
                    # If a specific label is provided, skip other entries
                    if label and entry.msgid != label:
                        continue

                    # Remove the string "Default: " from the comment
                    comment = (
                        entry.comment.replace("Default: ", "")
                        .replace("\n", "")
                        .strip()[1:-1]
                    )
                    if not comment:
                        comment = entry.msgid
                    try:
                        comment_t = translate_text(comment, lang.split("_")[0]).strip()
                        # trans sometimes returns a string with a space before the ${,
                        # so we need to remove that, or our variables break
                        if "$ {" in comment_t:
                            comment_t = comment_t.replace("$ {", "${")
                    except Exception as e:
                        print(f"Error translating '{comment}': {e}")
                        errors.append(f"Error translating '{comment}': {e}")
                        continue
                    if comment_t:
                        update_counter += 1
                        print(f"{entry.msgid}: {comment} | {comment_t}")
                        entry.msgstr = comment_t
                if not dry_run:
                    po.save(os.path.join(lang_path, file))
                if update_counter > 0:
                    print(f"Updated {update_counter} entries in {lang} {file}")

    if len(errors) > 0:
        print("Errors encountered during translation:")
        for error in errors:
            print(error)
        print("Rerun this script with --only-num-untranslated to see untranslated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Auto-translate missing entries in po files."
    )
    parser.add_argument(
        "--label", type=str, help="Specific label to translate (msgid).", default=None
    )
    parser.add_argument(
        "-l", "--lang", type=str, help="Target language (e.g., nl_BE).", default=None
    )
    parser.add_argument(
        "-u",
        "--only-num-untranslated",
        action="store_true",
        help="Only report number of untranslated entries and exit.",
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Translate to all available languages."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't write anything, just report."
    )

    args = parser.parse_args()

    i18n_euphorie = "src/euphorie/deployment/locales"

    if args.all:
        translate_po_files(
            i18n_euphorie,
            None,
            label=args.label,
            only_num_untranslated=args.only_num_untranslated,
            all_languages=True,
            dry_run=args.dry_run,
        )
    elif args.lang:
        translate_po_files(
            i18n_euphorie,
            args.lang,
            label=args.label,
            only_num_untranslated=args.only_num_untranslated,
            dry_run=args.dry_run,
        )
    else:
        print(
            "Please specify a language with --lang or use --all to translate "
            "to all languages. This will not overwrite existing translations."
        )
