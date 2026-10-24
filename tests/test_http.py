import unittest,tempfile,threading,json,urllib.request,urllib.error,csv,io
from pathlib import Path
from server import make_server

class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.server=make_server(0,Path(self.tmp.name)/'test.json')
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.base='http://127.0.0.1:'+str(self.server.server_address[1])
        self.addCleanup(self.server.server_close);self.addCleanup(self.server.shutdown)
    def get(self,path):
        with urllib.request.urlopen(self.base+path) as r:return r.read()
    def action(self,action,s,key=None):
        req=urllib.request.Request(self.base+'/api/action',data=json.dumps({'action':action,'id':key,'revision':s['revision']}).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as r:return json.loads(r.read())
    def test_real_http_save_restore_stats_export_and_conflict(self):
        boot=json.loads(self.get('/api/bootstrap'));s=boot['state']
        self.assertEqual(len(boot['items']),20);self.assertEqual(len(s['votes']),0)
        first=s['queue'][0];data=self.action('like',s,first);s=data['state']
        self.assertEqual(data['stats']['liked'],1)
        with self.assertRaises(urllib.error.HTTPError) as err:self.action('dislike',boot['state'],first)
        self.assertEqual(err.exception.code,409)
        restored=json.loads(self.get('/api/state'));self.assertEqual(restored['state'],s)
        exported=json.loads(self.get('/api/export'));self.assertEqual(exported['state'],s)
        rows=list(csv.reader(io.StringIO(self.get('/api/likes.csv').decode('utf-8-sig'))))
        self.assertEqual(len(rows),2);self.assertEqual(rows[1][0],first)
        undone=self.action('undo',s);self.assertEqual(undone['stats']['rated'],0)
        self.assertEqual(undone['state']['queue'][0],first)
    def test_only_fixed_static_routes_are_served(self):
        self.assertIn('钩子心选',self.get('/').decode())
        with self.assertRaises(urllib.error.HTTPError) as e:self.get('/runtime/preferences.json')
        self.assertEqual(e.exception.code,404)
        with self.assertRaises(urllib.error.HTTPError):self.get('/../model.py')
    def test_foreign_page_cannot_submit_choices(self):
        s=json.loads(self.get('/api/state'))['state']
        req=urllib.request.Request(self.base+'/api/action',data=json.dumps({'action':'like','id':s['queue'][0],'revision':s['revision']}).encode(),headers={'Content-Type':'application/json','Origin':'https://example.com'})
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
        self.assertEqual(e.exception.code,403)
        self.assertEqual(json.loads(self.get('/api/state'))['stats']['rated'],0)

if __name__=='__main__':unittest.main()
