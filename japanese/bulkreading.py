# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bulk update of readings.
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from japanese.reading import mecab, srcFields, dstFields
from aqt import mw

# Bulk updates
##########################################################################


def multi_regen(nid, src_fields, dst_fields, mecab):
    note = mw.col.getNote(nid)
    if "japanese" not in note.model()['name'].lower():
        return
    src = None
    for fld in src_fields:
        if fld in note:
            src = fld
            break
    if not src:
        # no src field
        return
    dst = None
    for fld in dst_fields:
        if fld in note:
            dst = fld
            break
    if not dst:
        # no dst field
        return
    if note[dst]:
        # already contains data, skip
        return
    srcTxt = mw.col.media.strip(note[src])
    if not srcTxt.strip():
        return
    try:
        note[dst] = mecab.reading(srcTxt)
    except Exception, e:
        mecab = None
        raise
    note.flush()


def regenerateReadings(nids):
    global mecab
    mw.checkpoint("Bulk-add Readings")
    mw.progress.start()
    for nid in nids:
        for s, d in zip(srcFields, dstFields):
            multi_regen(nid, [s], [d], mecab)
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    a = QAction("Bulk-add Readings", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onRegenerate(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onRegenerate(browser):
    regenerateReadings(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
