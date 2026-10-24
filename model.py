"""Local-only hook preference storage and descriptive statistics."""
import json, re, secrets, shutil, threading, copy, os
from pathlib import Path
from datetime import datetime, timezone

RULES = {
    '问题悬念': r'[？?]|为什么|能不能|有没有|到底|你知道|没想到',
    '对比反差': r'同样|别人|而我|而你|之前|之后|以前|现在|变成|不一样|区别|差距|竟然|居然|但是|却',
    '痛点卡住': r'不会|不懂|不知道|卡住|麻烦|重复|繁琐|手动|崩溃|搞不定|做不到|听不懂|失败|困扰|头疼',
    '成果展示': r'给你看|给大家看|这个是|这是我|效果|成品|做出来|生成了|做了一个|搭了一个|做好|做好的|直接交付|变成这样的|做出一个',
    '时间与效率': r'分钟|小时|一下午|一天|几天|秒钟|[一二三四五六七八九十百\d]+秒|省下|效率|提效|自动化|重复劳动',
    '降低门槛': r'零基础|小白|新手|不会写代码|不用写代码|不用学代码|不需要.*代码|不用.*代码|一句话|说句话|手把手|从零|免费|直接复制',
    '明确受众': r'老师|教师|学生|上班族|打工人|运营|财务|设计师|程序员|老板|创作者|新手|小白|普通人|内容创作|博主',
    '亲身经历': r'我发现|我最近|最近我|我做|我用|我花|我试|我给|我的|我把|我刚|前两天|昨天|这两天|粉丝|评论区',
    '强烈判断': r'最强|最.*的|彻底|全部|所有|一定|千万|必须|颠覆|神器|炸裂|震撼|天花板|史诗|保姆|奶妈',
    '数字信息': r'\d|[一二三四五六七八九十百千万]+[个种条步分钟天倍]',
}

def tag_hook(text):
    return [name for name,pattern in RULES.items() if re.search(pattern,text,re.I)]

class Conflict(Exception):pass

def eligible(item):return item.get('review',{}).get('status','approved')=='approved'

def migrate_state(old,old_items,new_items):
    previous={x['id']:x for x in old_items};new={x['id']:x for x in new_items}
    normalize=lambda t:re.sub(r'[^\w]','',t).lower()
    s=copy.deepcopy(old);s['legacy_history']=s['history'];s['history']=[];s['revision']=0;s['invalid']={}
    s['legacy_votes']={key:{**v,'text':previous[key]['text'],'author':previous[key].get('author',''),'tags':previous[key].get('tags',[])} for key,v in old['votes'].items()}
    retained={key:v for key,v in old['votes'].items() if eligible(new[key]) and normalize(previous[key]['text'])==normalize(new[key]['text'])}
    recheck=[key for key in old['votes'] if key not in retained]
    s['votes']=retained;s['queue']=recheck+s['queue'];s['data_version']='20261022-semantic-v2'
    s['migration_note']='旧版选择及当时展示的原句完整保留；改文或待审材料不计入新偏好，原句完全一致的通过审核项沿用。'
    return s

class Store:
    def __init__(self,path,items):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        self.backup=self.path.with_suffix('.backup.json');self.ids=[x['id'] for x in items]
        self.enabled={x['id'] for x in items if eligible(x)};self.items={x['id']:x for x in items}
        self.lock=threading.RLock();self.recovered=False
        if not self.path.exists():
            queue=self.ids[:];secrets.SystemRandom().shuffle(queue)
            self._write({'schema':'hook-preference-v1','revision':0,'votes':{},'queue':queue,'history':[],'updated_at':None})
        else:
            try:self._load()
            except (ValueError, OSError, KeyError, TypeError):
                if not self.backup.exists():raise RuntimeError('选择文件损坏且没有备份；请保留原件，勿自动重置。')
                self._validate(json.loads(self.backup.read_text(encoding='utf-8')))
                shutil.copy2(self.path,self.path.with_suffix('.damaged-'+datetime.now().strftime('%Y%m%d%H%M%S')+'.json'))
                shutil.copy2(self.backup,self.path);self.recovered=True

    def _validate(self,s):
        if not isinstance(s,dict) or s.get('schema')!='hook-preference-v1':raise ValueError('未知选择格式')
        if not isinstance(s['revision'],int) or not isinstance(s['history'],list):raise ValueError('选择文件格式错误')
        q=s['queue'];v=s['votes'];invalid=s.get('invalid',{});known=set(self.ids)
        if len(q)!=len(set(q)) or set(q)&set(v) or set(q)&set(invalid) or set(v)&set(invalid) or set(q)|set(v)|set(invalid)!=known:raise ValueError('选择与队列不一致')
        if any(x.get('choice') not in ('like','dislike') for x in v.values()):raise ValueError('选择值无效')
        return s

    def _load(self):return self._validate(json.loads(self.path.read_text(encoding='utf-8')))

    def _write(self,s):
        self._validate(s)
        tmp=self.path.with_suffix('.tmp')
        with tmp.open('w',encoding='utf-8') as f:
            json.dump(s,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
        if self.path.exists():shutil.copy2(self.path,self.backup)
        os.replace(tmp,self.path)

    def read(self):
        with self.lock:return copy.deepcopy(self._load())

    def public_state(self,s):
        s=copy.deepcopy(s);s['queue']=[key for key in s['queue'] if key in self.enabled];return s

    def act(self,action,item_id,revision):
        with self.lock:
            s=self._load()
            if revision!=s['revision']:raise Conflict('另一个页面已更新选择，已刷新到最新进度，请再选一次。')
            if action=='undo':
                if not s['history']:raise ValueError('还没有可撤销的操作')
                event=s['history'].pop();key=event['id']
                if event['action']=='skip':
                    s['queue'].remove(key)
                elif event['action']=='invalid':s['invalid'].pop(key)
                else:s['votes'].pop(key)
                s['queue'].insert(event.get('index',0),key)
            elif action in ('like','dislike','skip','invalid'):
                visible=[key for key in s['queue'] if key in self.enabled]
                if not visible or visible[0]!=item_id:raise ValueError('当前卡片已变化，请刷新后重试')
                index=s['queue'].index(item_id);s['queue'].pop(index)
                if action=='skip':s['queue'].append(item_id)
                elif action=='invalid':s.setdefault('invalid',{})[item_id]={'at':datetime.now(timezone.utc).isoformat(),'text':self.items[item_id]['text']}
                else:s['votes'][item_id]={'choice':action,'at':datetime.now(timezone.utc).isoformat()}
                s['history'].append({'id':item_id,'action':action,'index':index})
            else:raise ValueError('不支持的操作')
            s['revision']+=1;s['updated_at']=datetime.now(timezone.utc).isoformat()
            self._write(s);return copy.deepcopy(s)

def summarize(items,state):
    votes=state['votes'];approved=[x for x in items if eligible(x)];rated=[x for x in approved if x['id'] in votes]
    liked=[x for x in rated if votes[x['id']]['choice']=='like']
    baseline=len(liked)/len(rated) if rated else 0
    names=list(RULES)
    for x in items:
        for tag in x['tags']:
            if tag not in names:names.append(tag)
    def group(name,selected):
        good=sum(votes[x['id']]['choice']=='like' for x in selected);seen=len(selected)
        rate=good/seen if seen else None
        return {'name':name,'seen':seen,'liked':good,'rate':rate,'lift':rate-baseline if rate is not None else None}
    tags=[group(tag,[x for x in rated if tag in x['tags']]) for tag in names]
    buckets=[('短开场 · 60字以内',lambda n:n<=60),('中开场 · 61–120字',lambda n:60<n<=120),('长开场 · 120字以上',lambda n:n>120)]
    lengths=[group(name,[x for x in rated if rule(len(x['text']))]) for name,rule in buckets]
    invalid=state.get('invalid',{});total=len(approved)-len(invalid)
    return {'rated':len(rated),'liked':len(liked),'disliked':len(rated)-len(liked),'remaining':total-len(rated),
        'pool_total':total,'held_total':len(items)-len(approved),'invalid_count':len(invalid),'legacy_count':len(state.get('legacy_votes',{})),
        'legacy_preserved':sum(key in votes for key in state.get('legacy_votes',{})),
        'baseline':baseline,'tags':tags,'lengths':lengths,'sample_ready':len(rated)>=20,
        'liked_ids':[x['id'] for x in liked], 'rules':RULES}
