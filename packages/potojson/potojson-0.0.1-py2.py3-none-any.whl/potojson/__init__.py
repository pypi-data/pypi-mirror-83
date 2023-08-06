import json

import polib

__version__ = '0.0.1'
__version_info__ = tuple([int(i) for i in __version__.split('.')])
__title__ = 'potojson'
__description__ = 'Pofile to JSON conversion without pain.'
__all__ = ("pofile_to_json",)


def pofile_to_json(content, fallback_to_msgid=False, fuzzy=False,
                   pretty=False, indent=2, language=None, plural_forms=None):
    response = {}
    po = polib.pofile(content)
    for entry in po:
        if not fuzzy and entry.fuzzy:
            continue
        if entry.msgctxt:
            if entry.msgctxt not in response:
                response[entry.msgctxt] = {}
            if entry.msgid_plural:
                response[entry.msgctxt][entry.msgid] = list(
                    value if value else (
                        (entry.msgid_plural if i != 0 else entry.msgid)
                        if fallback_to_msgid else value)
                    for i, value in enumerate(entry.msgstr_plural.values())
                )
            else:
                response[entry.msgctxt][entry.msgid] = \
                    entry.msgstr if entry.msgstr else (
                        entry.msgid if fallback_to_msgid else entry.msgstr)
        else:
            if entry.msgid_plural:
                # ``fallback_to_msgid`` based on enumeration it's only valid
                # for most common languages the most correct way would be to
                # parse plural_forms, if provided and redirect the fallback
                # msgids accordingly, but  it's too of little benefit to add
                # such complexity
                response[entry.msgid] = list(
                    value if value else (
                        (entry.msgid_plural if i != 0 else entry.msgid)
                        if fallback_to_msgid else value)
                    for i, value in enumerate(entry.msgstr_plural.values())
                )
            else:
                response[entry.msgid] = entry.msgstr if entry.msgstr else (
                    entry.msgid if fallback_to_msgid else entry.msgstr)
    if not language and 'Language' in po.metadata:
        language = po.metadata["Language"]
    if not plural_forms and 'Plural-Forms' in po.metadata:
        plural_forms = po.metadata['Plural-Forms']
    if language or plural_forms:
        response[""] = {}
        if language:
            response[""]["language"] = language
        if plural_forms:
            response[""]["plural-forms"] = plural_forms
    if pretty and indent is None:
        indent = 2
    return json.dumps(response, indent=indent if pretty else None)
