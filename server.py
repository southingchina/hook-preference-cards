from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json,argparse,csv,io
from model import Store,Conflict,summarize

BASE=Path(__file__).resolve().parent

def make_server(port,state_path):
    items=json.loads((BASE/'data'/'hooks.json').read_text(encoding='utf-8'))
    store=Store(state_path,items)
    class Handler(BaseHTTPRequestHandler):
        def send(self,status,payload,ctype='application/json; charset=utf-8',filename=None):
            raw=json.dumps(payload,ensure_ascii=False).encode() if isinstance(payload,(dict,list)) else payload
            self.send_response(status);self.send_header('Content-Type',ctype)
            self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'self'")
            if filename:self.send_header('Content-Disposition',f'attachment; filename="{filename}"')
            self.end_headers();self.wfile.write(raw)
        def envelope(self):
            s=store.read();return {'state':store.public_state(s),'stats':summarize(items,s),'recovered':store.recovered}
        def do_GET(self):
            path=urlparse(self.path).path
            if path=='/api/bootstrap':return self.send(200,{'items':items,**self.envelope()})
            if path=='/api/state':return self.send(200,self.envelope())
            if path=='/api/export':return self.send(200,{'schema':'hook-preference-export-v1',**self.envelope(),'items':items},filename='hook-preferences.json')
            if path=='/api/likes.csv':
                s=store.read();out=io.StringIO();w=csv.writer(out);w.writerow(['作品ID','钩子原句','作者','点赞快照','点赞','特征标签','链接'])
                for x in items:
                    if s['votes'].get(x['id'],{}).get('choice')=='like':
                        row=[x['id'],x['text'],x['author'],x['snapshot'],x['likes'],' / '.join(x['tags']),x['url']]
                        w.writerow(["'"+str(v) if str(v).startswith(('=','+','-','@')) else v for v in row])
                return self.send(200,('\ufeff'+out.getvalue()).encode('utf-8'),'text/csv; charset=utf-8','liked-hooks.csv')
            files={'/':'index.html','/index.html':'index.html','/style.css':'style.css','/app.js':'app.js'}
            if path in files:
                f=BASE/'static'/files[path];ctype={'html':'text/html','css':'text/css','js':'text/javascript'}[f.suffix[1:]]
                return self.send(200,f.read_bytes(),ctype+'; charset=utf-8')
            return self.send(404,{'error':'页面不存在'})
        def do_POST(self):
            if self.path!='/api/action':return self.send(404,{'error':'接口不存在'})
            origin=self.headers.get('Origin')
            allowed={f'http://127.0.0.1:{port}',f'http://localhost:{port}'}
            if origin and origin not in allowed:return self.send(403,{'error':'仅接受本地页面操作'})
            if not self.headers.get('Content-Type','').startswith('application/json'):return self.send(415,{'error':'需要JSON格式'})
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<4096:raise ValueError('请求大小无效')
                data=json.loads(self.rfile.read(n));store.act(data.get('action'),data.get('id'),data.get('revision'))
                return self.send(200,self.envelope())
            except Conflict as e:return self.send(409,{'error':str(e),**self.envelope()})
            except (ValueError,TypeError) as e:return self.send(400,{'error':str(e)})
            except OSError:return self.send(500,{'error':'本地文件保存失败；当前选择尚未确认，请重试。'})
        def log_message(self,*args):pass
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8769);p.add_argument('--state',type=Path,default=BASE/'runtime'/'preferences-v2.json');a=p.parse_args()
    srv=make_server(a.port,a.state);print(f'Hook Match Local: http://127.0.0.1:{a.port}',flush=True)
    try:srv.serve_forever()
    except KeyboardInterrupt:pass
