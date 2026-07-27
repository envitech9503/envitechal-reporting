# -*- coding: utf-8 -*-
"""Structural immunisation of the Reagent & Standards Prep inventory feed.

Adds dedicated ``cat_no`` and ``brand`` columns to ChemicalLot and backfills
them once from the values the view-layer parser currently derives.

The analyst findings of 27-07-2026 were first closed in the view layer by
parsing free text.  That is correct for the conventions in use today but not
structural: a new way of typing either field in Karachi or Lahore would
silently reintroduce both faults.  From here the two values live in their own
columns and cannot be lost to a change of convention.

``lot_no`` and ``remarks`` are deliberately NOT rewritten.
"""
from django.db import migrations, models
import re as _re

_CLEAN_RX = _re.compile(r'^\s*(NO\.?|NUMBER)?\s*[:.\-]?\s*', _re.I)
_BRAND_RX = _re.compile(r'brand(?:\s*name)?\s*[:\-]?\s*([^;|\n]+)', _re.I)


def _clean(x):
    return _CLEAN_RX.sub('', x or '').strip()


def _split_cat_lot(raw):
    raw = (raw or '').strip()
    if not raw:
        return '', ''
    up = raw.upper()
    ci, li = up.find('CAT'), up.find('LOT')
    if ci != -1 and li != -1:
        if ci < li:
            return _clean(raw[ci + 3:li]), _clean(raw[li + 3:])
        return _clean(raw[ci + 3:]), _clean(raw[li + 3:ci])
    if li != -1:
        return '', _clean(raw[li + 3:])
    if ci != -1:
        return _clean(raw[ci + 3:]), ''
    if raw.count('/') == 1:
        left, right = [p.strip() for p in raw.split('/')]
        if (left and right and ' ' not in left and ' ' not in right
                and len(left) <= 40 and len(right) <= 40):
            return right, left
    return '', raw


def _brand_from(remarks, notes):
    for src in (remarks or '', notes or ''):
        m = _BRAND_RX.search(src)
        if m:
            b = m.group(1).strip(' .;,')
            if b:
                return b
    return ''


def forwards(apps, schema_editor):
    ChemicalLot = apps.get_model('EnviTechAlApp', 'ChemicalLot')
    total = filled_cat = filled_brand = 0
    for lot in ChemicalLot.objects.select_related('item').iterator():
        total += 1
        changed = []
        if not (lot.cat_no or '').strip():
            cat, _lot = _split_cat_lot(lot.lot_no)
            if cat:
                lot.cat_no = cat[:80]
                changed.append('cat_no')
                filled_cat += 1
        if not (lot.brand or '').strip():
            notes = getattr(lot.item, 'notes', '') if lot.item_id else ''
            b = _brand_from(lot.remarks, notes)
            if b:
                lot.brand = b[:120]
                changed.append('brand')
                filled_brand += 1
        if changed:
            lot.save(update_fields=changed)
    print('    backfill: lots=%d cat_no filled=%d brand filled=%d'
          % (total, filled_cat, filled_brand))


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('EnviTechAlApp', '0020_reagentstandardisation_aliquot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemicallot',
            name='cat_no',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AddField(
            model_name='chemicallot',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.RunPython(forwards, backwards),
    ]
