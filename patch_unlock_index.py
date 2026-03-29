#!/usr/bin/env python3
"""
Patch all issue HTML files to use unlockAtIndex in setupPlayer/runPlayer.
The question unlocks when the final (question) audio starts — not after it finishes.
"""
import re, os

FILES = [
    'issue-001-narrated.html',
    'issue-002-narrated.html',
    'issue-003-narrated.html',
    'issue-005-narrated.html',
    'issue-006-narrated.html',
    'issue-007-narrated.html',
    'jungle-001-narrated.html',
]

BASE = '/Users/leohiem/.openclaw/workspace/projects/math-blast'

# ── 1. Update setupPlayer function signature ─────────────────────────────────
OLD_SETUP_SIGS = [
    'function setupPlayer(id,files,labels,storyId,lockId)',
    'function setupPlayer(id, files, labels, storyId, lockId)',
    'function setupPlayer(id,files,labels,storyId,lockId,onDone)',
    'function setupPlayer(id, files, labels, storyId, lockId, onDone)',
]
NEW_SETUP_SIG = 'function setupPlayer(id,files,labels,storyId,lockId,onDone,unlockAtIndex)'

# ── 2. Update setupPlayer body ────────────────────────────────────────────────
OLD_SETUP_BODY = r'playerConfigs\[id\]=\{files,labels,storyId,lockId,onDone,active:false\}'
NEW_SETUP_BODY = r'playerConfigs[id]={files,labels,storyId,lockId,onDone,unlockAtIndex:unlockAtIndex??files.length,active:false}'

# ── 3. Update runPlayer to unlock at unlockAtIndex ────────────────────────────
# Old: quiz unlocks only after ALL files finish
# New: quiz unlocks when file at unlockAtIndex starts
OLD_UNLOCK_BLOCK = (
    r'if\(cfg\.lockId\)\{const lock=document\.getElementById\(cfg\.lockId\);'
    r'if\(lock\)lock\.style\.display=\'none\';\}const quizId=cfg\.lockId\?cfg\.lockId\.replace\(\'lock-\',\'quiz-\'\):null;'
    r'if\(quizId\)\{const quiz=document\.getElementById\(quizId\);'
    r'if\(quiz\)\{quiz\.classList\.add\(\'show\'\);setTimeout\(\(\)=>quiz\.scrollIntoView\(\{behavior:\'smooth\',block:\'nearest\'\}\),200\);\}\}if\(cfg\.onDone\)cfg\.onDone\(\);cfg\.active=false;activePlayerId=null;return;'
)
NEW_UNLOCK_AFTER_ALL = (
    'if(cfg.onDone)cfg.onDone();cfg.active=false;activePlayerId=null;return;'
)

# What to inject at the start of playNext loop (before playing file)
UNLOCK_AT_INDEX_INJECT = (
    'if(fileIdx===cfg.unlockAtIndex){'
    'if(cfg.lockId){const lock=document.getElementById(cfg.lockId);if(lock)lock.style.display=\'none\';}'
    'const quizId=cfg.lockId?cfg.lockId.replace(\'lock-\',\'quiz-\'):null;'
    'if(quizId){const quiz=document.getElementById(quizId);if(quiz&&!quiz.classList.contains(\'show\')){'
    'quiz.classList.add(\'show\');setTimeout(()=>quiz.scrollIntoView({behavior:\'smooth\',block:\'nearest\'}),200);}}'
    '}'
)

def patch_file(fname):
    path = os.path.join(BASE, fname)
    with open(path, 'r') as f:
        html = f.read()
    
    original = html
    changed = False

    # Skip if already patched
    if 'unlockAtIndex:unlockAtIndex' in html:
        print(f'  ⏭  {fname} — already patched')
        return

    # 1. Fix setupPlayer signature
    for old_sig in OLD_SETUP_SIGS:
        if old_sig in html:
            html = html.replace(old_sig, NEW_SETUP_SIG, 1)
            changed = True
            break

    # 2. Fix setupPlayer body (store unlockAtIndex)
    html = re.sub(
        r'playerConfigs\[id\]=\{files,labels,storyId,lockId,onDone,active:false\}',
        r'playerConfigs[id]={files,labels,storyId,lockId,onDone,unlockAtIndex:unlockAtIndex??files.length,active:false}',
        html
    )

    # Also handle variant without onDone
    html = re.sub(
        r'playerConfigs\[id\]=\{files,labels,storyId,lockId,active:false\}',
        r'playerConfigs[id]={files,labels,storyId,lockId,onDone:null,unlockAtIndex:unlockAtIndex??files.length,active:false}',
        html
    )

    # 3. In runPlayer, inject unlock-at-index check at the top of playNext,
    #    and remove the unlock block from the "all files done" section.
    #
    #    Find the pattern where unlock happens after all files finish and remove it,
    #    then add the index-based unlock at the right place.

    # Remove unlock-at-completion block (various forms)
    html = re.sub(
        r'if\(cfg\.lockId\)\{const lock=document\.getElementById\(cfg\.lockId\);if\(lock\)lock\.style\.display=\'none\';\}'
        r'const quizId=cfg\.lockId\?cfg\.lockId\.replace\(\'lock-\',\'quiz-\'\):null;'
        r'if\(quizId\)\{const quiz=document\.getElementById\(quizId\);if\(quiz\)\{quiz\.classList\.add\(\'show\'\);'
        r'setTimeout\(\(\)=>quiz\.scrollIntoView\(\{behavior:\'smooth\',block:\'nearest\'\}\),200\);\}\}\}',
        r'}',
        html
    )

    # Also handle variant with !quiz.classList.contains already
    html = re.sub(
        r'if\(cfg\.lockId\)\{const lock=document\.getElementById\(cfg\.lockId\);if\(lock\)lock\.style\.display=\'none\';\}'
        r'const quizId=cfg\.lockId\?cfg\.lockId\.replace\(\'lock-\',\'quiz-\'\):null;'
        r'if\(quizId\)\{const quiz=document\.getElementById\(quizId\);if\(quiz&&!quiz\.classList\.contains\(\'show\'\)\)\{'
        r'quiz\.classList\.add\(\'show\'\);setTimeout\(\(\)=>quiz\.scrollIntoView\(\{behavior:\'smooth\',block:\'nearest\'\}\),200\);\}\}\}',
        r'}',
        html
    )

    # 4. Add the unlock-at-index injection before "const file=cfg.files[fileIdx]"
    INJECT = (
        "if(fileIdx===cfg.unlockAtIndex){"
        "if(cfg.lockId){const lock=document.getElementById(cfg.lockId);if(lock)lock.style.display='none';}"
        "const quizId=cfg.lockId?cfg.lockId.replace('lock-','quiz-'):null;"
        "if(quizId){const quiz=document.getElementById(quizId);if(quiz&&!quiz.classList.contains('show')){"
        "quiz.classList.add('show');setTimeout(()=>quiz.scrollIntoView({behavior:'smooth',block:'nearest'}),200);}}"
        "}"
    )

    # Only inject if not already there
    if 'fileIdx===cfg.unlockAtIndex' not in html:
        html = html.replace(
            "const file=cfg.files[fileIdx];",
            INJECT + "const file=cfg.files[fileIdx];"
        )

    # 5. Add unlockAtIndex param to all setupPlayer() calls that are missing it
    #    Pattern: setupPlayer('id', [...], [...], 'storyId', 'lockId', null);  (ends with null)
    #    or setupPlayer('id', [...], [...], 'storyId', 'lockId', null)  (various whitespace)
    #    We add the file count - 1 as unlockAtIndex
    def add_unlock_index(m):
        call = m.group(0)
        # Count files in the array
        files_match = re.search(r'\[([^\]]+)\]', call)
        if not files_match:
            return call
        files_content = files_match.group(1)
        file_count = files_content.count('.mp3')
        unlock_idx = file_count - 1
        # Replace the closing ); adding the index
        call = re.sub(r',\s*null\s*\)\s*;', f', null, {unlock_idx});', call)
        call = re.sub(r',\s*null\s*\)\s*$', f', null, {unlock_idx})', call)
        return call

    html = re.sub(
        r"setupPlayer\('[^']+',\s*\[[^\]]+\],\s*\[[^\]]+\],\s*'[^']*',\s*'[^']*',\s*null\s*\)\s*;",
        add_unlock_index,
        html
    )

    if html != original:
        with open(path, 'w') as f:
            f.write(html)
        print(f'  ✅ {fname} — patched')
    else:
        print(f'  ⚠️  {fname} — no changes made (check manually)')

if __name__ == '__main__':
    print('Patching unlockAtIndex into all issue files...')
    for fname in FILES:
        patch_file(fname)
    print('\nDone!')
