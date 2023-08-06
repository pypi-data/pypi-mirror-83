# 📦 potojson

[![PyPI](https://img.shields.io/pypi/v/potojson)](https://pypi.org/project/potojson/) [![Tests](https://img.shields.io/travis/mondeja/potojson?label=tests&logo=travis)](https://travis-ci.com/github/mondeja/potojson) [![Coveralls](https://img.shields.io/coveralls/github/mondeja/potojson?logo=coveralls)](https://coveralls.io/github/mondeja/potojson)

Pofile to JSON conversion without pain.

## Installation

```bash
pip install potojson
```

## Documentation

### API

<a name="pofile_to_json" href="#pofile_to_json">#</a> <b>pofile_to_json</b>(<i>content</i>, <i>fallback_to_msgid=False</i>, <i>fuzzy=False</i>, <i>pretty=False</i>, <i>indent=2</i>, <i>language=None</i>, <i>plural_forms=None</i>) ⇒ `str`

Converts a pofile passed as string or filepath and returns a JSON formatted output with next style:

```json
{
  "": {
    "language": "es",
    "plural-forms": "nplurals=2; plural=n != 1;",
  },
  "msgid": "msgstr",
  "msgctxt": {
    "msgid": "msgstr",
  },
  "msgid": ["msgstr[0]", "msgstr[1]", "msgstr[2]"],
  "msgctxt": {
    "msgid": ["msgstr[0]", "msgstr[1]", "msgstr[2]"],
  }
}
```

This output can be customized tuning the parameters of the function.

- **content** (str) Content or filepath of the pofile to convert.
- **fallback_to_msgid** (bool) Use msgid if translation is missing.
- **fuzzy** (bool) Include fuzzy messages.
- **pretty** (bool) Pretty-print JSON output.
- **indent** (int) Number of spaces for indentation used pretty-printing JSON output. Only takes effect if ``pretty is True``.
- **language** (str) Language for the translations. Will be inserted in the empty key of the JSON output. If not provided and the passed pofile includes the "Language" header, will be extrated from it.
- **plural_forms** (str) Plural forms for the language of the translations. Will be insertedin the empty key of the JSON output. If not provided and the passed pofile includes the "Plural-Forms" header, will be extrated from it.

### CLI

```
usage: potojson [-h] [-v] [-m] [-f] [-p] [-i N] [-l LANGUAGE] [-s PLURAL_FORMS] PO_FILEPATH_OR_CONTENT

Pofile to JSON conversion without pain.

positional arguments:
  PO_FILEPATH_OR_CONTENT
                        Path to pofile or pofile content as a string. If not provided, will be read from STDIN.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show program version number and exit.
  -m, --fallback-to-msgid
                        Use msgid if translation is missing.
  -f, --fuzzy           Include fuzzy messages.
  -p, --pretty          Pretty-print JSON output.
  -i N, --indent N      Number of spaces for indentation used pretty-printing JSON output. Only takes effect passing '--fuzzy' option.
  -l LANGUAGE, --language LANGUAGE
                        Language for the translations. Will be inserted in the empty key of the JSON output. If not provided and the passed pofile includes the "Language" header, will be extrated from it.
  -s PLURAL_FORMS, --plural-forms PLURAL_FORMS
                        Plural forms for the language of the translations. Will be insertedin the empty key of the JSON output. If not provided and the passed pofile includes the "Plural-Forms" header, will be extrated from it.
```