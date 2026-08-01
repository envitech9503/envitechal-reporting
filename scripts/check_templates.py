#!/usr/bin/env python3
"""Guard the template layer. Run before every deploy; runs in CI on every push.

Each check corresponds to a fault that has actually reached production:

  1. a template that does not compile                     (a {% load %} placed
     below its first {% static %} use is a silent parse error)
  2. a {% static %} key that points at no file            (aborts collectstatic)
  3. a non-canonical key: '/js/app.js', '\\assets\\x.gif' (fails the manifest
     lookup at render time, 500s the page)
  4. a hard-coded /static/... path                        (bypasses the manifest,
     so that asset silently loses cache-busting)
  5. a re-introduced ?v= stamp                            (content hashing has
     made it redundant; a stale one misleads)
  6. a sidebar copied back out of its partial             (this is how Detox and
     Noise LAeq came to exist only on the home page)

Exits non-zero and names the file and the offending text on any failure.
"""
import glob
import os
import re
import sys

VERBATIM = re.compile(r'\{%\s*verbatim\s*%\}.*?\{%\s*endverbatim\s*%\}', re.S)
STATIC_TAG = re.compile(r'\{%\s*static\s+([\'"])([^\'"]*)\1\s*%\}')
HARDCODED = re.compile(r'(?:src|href)\s*=\s*"?/static/')
LOAD = re.compile(r'\{%\s*load\s+[^%]*\bstatic\b[^%]*%\}')
STAMP = re.compile(r'\?v=\d{6,}')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, 'templates')
STATIC = os.path.join(ROOT, 'static')

# Partials that own a block no other template may copy.
SOLE_OWNER = {
    'formMainDiv': '_reports_sidebar.html',
    'etqcSidebar': '_qc_sidebar.html',
}

failures = []


def fail(path, message):
    failures.append('%s: %s' % (os.path.relpath(path, ROOT), message))


def template_files():
    for path in sorted(glob.glob(os.path.join(TEMPLATES, '**', '*'), recursive=True)):
        if not os.path.isfile(path):
            continue
        try:
            yield path, open(path, encoding='utf-8').read()
        except UnicodeDecodeError:
            continue


def check_compiles(files):
    """Compile every template. Needs Django, so it is skipped if unavailable."""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EnviTechAlApp.settings')
        sys.path.insert(0, ROOT)
        django.setup()
        from django.template import engines
    except Exception as exc:                       # pragma: no cover
        print('  ! skipped the compile check: %s' % str(exc)[:90])
        return 0
    engine = engines['django']
    for path, text in files:
        try:
            engine.from_string(text)
        except Exception as exc:
            fail(path, 'does not compile: %s' % str(exc)[:120])
    return 1


def check_static_tags(files):
    for path, text in files:
        body = VERBATIM.sub('', text)
        for quote, key in STATIC_TAG.findall(body):
            canonical = key.replace('\\', '/').strip().split('?')[0].lstrip('/')
            while '//' in canonical:
                canonical = canonical.replace('//', '/')
            if key != canonical:
                fail(path, "{%% static '%s' %%} should be '%s' - a leading slash, "
                           "a backslash or a query string breaks the manifest lookup"
                           % (key, canonical))
            if not os.path.exists(os.path.join(STATIC, canonical)):
                fail(path, "{%% static '%s' %%} points at no file under static/" % key)


def check_no_hardcoded(files):
    for path, text in files:
        body = VERBATIM.sub('', text)
        for match in HARDCODED.finditer(body):
            line = body.count('\n', 0, match.start()) + 1
            snippet = body[match.start():match.start() + 60].split('\n')[0]
            fail(path, 'line %d hard-codes a static path, use {%% static %%}: %s'
                       % (line, snippet))


def check_load_before_use(files):
    for path, text in files:
        body = VERBATIM.sub('', text)
        first_use = body.find('{% static')
        if first_use == -1:
            continue
        load = LOAD.search(body)
        if load is None:
            fail(path, 'uses {% static %} without {% load static %}')
        elif load.start() > first_use:
            fail(path, '{% load static %} appears after the first {% static %} - '
                       'the parser reads in order, so this is a parse error')


def check_no_stamps(files):
    for path, text in files:
        for match in STAMP.finditer(text):
            fail(path, 'carries a %s cache stamp; content hashing replaced those'
                       % match.group(0))


def check_sole_owners(files):
    for marker, owner in SOLE_OWNER.items():
        holders = [os.path.basename(p) for p, t in files if marker in t]
        if owner not in holders:
            failures.append('%s: expected to define "%s" and does not' % (owner, marker))
        strays = [h for h in holders if h != owner]
        if strays:
            failures.append('"%s" belongs only in %s but was also found in: %s'
                            % (marker, owner, ', '.join(sorted(strays))))


def main():
    files = list(template_files())
    print('checking %d templates' % len(files))
    compiled = check_compiles(files)
    check_static_tags(files)
    check_no_hardcoded(files)
    check_load_before_use(files)
    check_no_stamps(files)
    check_sole_owners(files)

    if failures:
        print('\n%d problem(s):\n' % len(failures))
        for line in failures:
            print('  %s' % line)
        return 1
    print('all checks passed%s' % ('' if compiled else ' (compile check skipped)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
