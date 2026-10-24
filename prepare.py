"""Source excerpt helper; no bundled external source library."""
import re

def select_text(r):
    original=r['hook'] or r['opening_excerpt']
    basis=r.get('extraction','ASR开头摘录')
    if original and original[-1] not in '。！？!?…”）)' and r['asr_opening']:
        raw=re.sub(r'\s+',' ',r['asr_opening']).strip()
        sentences=re.findall(r'.*?[。！？!?](?:[”\"])?',raw)
        result='';target=min(len(original),130)
        for sentence in sentences:
            result+=sentence
            if len(result)>=target:return result,'ASR开头补全句尾（保留原措辞）'
        if result:return result,'ASR起始完整句（保留原措辞）'
    return original,basis
