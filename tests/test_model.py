import unittest
import tempfile
from pathlib import Path
import importlib.util

spec=importlib.util.find_spec('model')
if spec:
    from model import Store, Conflict, summarize, tag_hook
else:
    Store=Conflict=summarize=tag_hook=None

class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.items=[{'id':str(i),'text':t,'tags':tags} for i,(t,tags) in enumerate([
            ('同样用AI，为什么结果不一样？',['问题悬念','对比反差']),
            ('这个报告只用三分钟。',['时间与效率']),
            ('先给你看做好的网页。',['成果展示']),
            ('不会写代码也能做。',['降低门槛'])])]
        self.path=Path(self.tmp.name)/'state.json'
    def store(self):
        self.assertIsNotNone(Store,'缺少本地偏好存储实现')
        return Store(self.path,self.items)
    def test_save_reload_undo_restores_exact_card(self):
        s=self.store();a=s.read();key=a['queue'][0]
        b=s.act('like',key,a['revision'])
        self.assertEqual(b['votes'][key]['choice'],'like')
        reload=self.store();self.assertEqual(reload.read(),b)
        c=reload.act('undo',None,b['revision'])
        self.assertNotIn(key,c['votes']);self.assertEqual(c['queue'][0],key)
    def test_skip_is_not_a_dislike_and_undo_restores_order(self):
        s=self.store();a=s.read();b=s.act('skip',a['queue'][0],a['revision'])
        self.assertEqual(b['votes'],{});self.assertEqual(b['queue'][-1],a['queue'][0])
        c=s.act('undo',None,b['revision']);self.assertEqual(c['queue'],a['queue'])
    def test_stale_and_wrong_card_operations_never_overwrite(self):
        s=self.store();a=s.read();b=s.act('like',a['queue'][0],a['revision'])
        with self.assertRaises(Conflict):s.act('dislike',b['queue'][0],a['revision'])
        with self.assertRaises(ValueError):s.act('like','unknown',b['revision'])
        self.assertEqual(s.read(),b)
    def test_corrupt_primary_recovers_backup_without_fabricating_votes(self):
        s=self.store();a=s.read();b=s.act('like',a['queue'][0],a['revision'])
        s.act('dislike',b['queue'][0],b['revision'])
        self.path.write_text('{broken',encoding='utf-8')
        c=self.store().read();self.assertEqual(len(c['votes']),1)
    def test_stats_only_use_rated_items_and_overlapping_tags(self):
        self.assertIsNotNone(summarize,'缺少偏好统计实现')
        st={'votes':{'0':{'choice':'like'},'1':{'choice':'dislike'}},'history':[]}
        r=summarize(self.items,st)
        self.assertEqual((r['rated'],r['liked'],r['baseline']),(2,1,.5))
        tags={t['name']:t for t in r['tags']}
        self.assertEqual(tags['问题悬念']['seen'],1)
        self.assertEqual(tags['成果展示']['seen'],0)
        self.assertEqual(tags['对比反差']['liked'],1)
    def test_rule_labels_describe_text_not_product_claim_truth(self):
        self.assertIsNotNone(tag_hook,'缺少文字特征识别实现')
        tags=tag_hook('同样用AI，为什么别人三分钟就做完了？不会写代码也能做这个网页。')
        self.assertIn('问题悬念',tags);self.assertIn('对比反差',tags)
        self.assertIn('降低门槛',tags);self.assertIn('时间与效率',tags)
    def test_truncated_source_hook_uses_complete_asr_sentences(self):
        import prepare
        self.assertTrue(hasattr(prepare,'select_text'),'缺少被截短钩子的句尾补全')
        text,basis=prepare.select_text({'hook':'这是我的新工具，它能','asr_opening':'这是我的新工具，它能做课件。现在开始演示。','opening_excerpt':''})
        self.assertEqual(text,'这是我的新工具，它能做课件。')
        self.assertIn('ASR',basis)
    def test_short_asr_does_not_fall_back_to_cut_off_half_sentence(self):
        import prepare
        text,basis=prepare.select_text({'hook':'这个模型到底有多强？参考第一张图，把第二张图片中的人物换成','asr_opening':'这个模型到底有多强？参考第一张图，把第二张图片中的人物换成','opening_excerpt':''})
        self.assertEqual(text,'这个模型到底有多强？')
    def test_held_material_is_not_served_or_counted_in_taste(self):
        import model
        self.items[0]['review']={'status':'hold'}
        s=self.store();a=s.read()
        self.assertTrue(hasattr(s,'public_state'),'缺少审核卡池过滤')
        visible=s.public_state(a)
        self.assertNotIn('0',visible['queue'])
        r=model.summarize(self.items,{'votes':{'0':{'choice':'dislike'}},'history':[]})
        self.assertEqual(r['rated'],0)
    def test_not_a_hook_is_quality_feedback_not_dislike_and_can_undo(self):
        s=self.store();a=s.read();key=a['queue'][0]
        b=s.act('invalid',key,a['revision'])
        self.assertNotIn(key,b['votes']);self.assertIn(key,b['invalid'])
        self.assertEqual(summarize(self.items,b)['rated'],0)
        c=s.act('undo',None,b['revision']);self.assertNotIn(key,c['invalid'])
        self.assertEqual(c['queue'][0],key)
    def test_changed_text_requires_new_choice_but_original_choice_is_retained(self):
        import model
        self.assertTrue(hasattr(model,'migrate_state'),'缺少原句变更后的选择迁移')
        s=self.store();a=s.read();key=a['queue'][0];b=s.act('like',key,a['revision'])
        changed=[dict(x) for x in self.items]
        next(x for x in changed if x['id']==key)['text']='完全不同的新原句。'
        migrated=model.migrate_state(b,self.items,changed)
        self.assertEqual(migrated['legacy_votes'][key]['choice'],'like')
        self.assertEqual(migrated['legacy_votes'][key]['text'],next(x for x in self.items if x['id']==key)['text'])
        self.assertNotIn(key,migrated['votes']);self.assertIn(key,migrated['queue'])

if __name__=='__main__':unittest.main()
