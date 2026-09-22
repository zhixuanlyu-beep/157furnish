"""Standalone full rebuild, never render. Repeat check compares semantic model and deterministic assets."""
import argparse,subprocess,sys,json,hashlib,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def hashes():
 paths=[p for f in ['drawings','tables','docs'] for p in (R/f).rglob('*') if p.is_file()]+[R/'model/projection_snapshot.json',R/'data/layout.json']
 return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
def main():
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--repeat',action='store_true');a=p.parse_args();first=None
 for folder in ['drawings/svg','drawings/png','tables','model','reports','docs']:(R/folder).mkdir(parents=True,exist_ok=True)
 for i in range(2 if a.repeat else 1):
  jobs=[('test_regressions.py',None),('verify_usage.py',None)]+[(s,f) for f in ['gas','electric'] for s in ['build_model.py','verify_model.py']]+[('build_drawings.py',None),('publish_docs.py',None)]
  for script,fuel in jobs:
   args=[a.blender,'--background','--factory-startup','--disable-autoexec','--python-exit-code','1','--python','scripts/'+script] if script in ['build_model.py','verify_model.py'] else [sys.executable,'scripts/'+script]
   env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
   if fuel:env['FURNISH_FUEL']=fuel
   result=subprocess.run(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/'reports'/(script[:-3]+('_'+fuel if fuel else '')+'.log')).write_bytes(result.stdout)
   print('pass'+str(i+1),script,result.returncode,flush=True)
   if result.returncode:print(result.stdout.decode('utf-8',errors='replace')[-2500:]);raise SystemExit(result.returncode)
  current=hashes()
  if first is None:first=current
  else:
   diff=[n for n in set(first)|set(current) if first.get(n)!=current.get(n)];from common import dump,bound
   dump('reports/repeatability.json',bound({'passed':not diff,'compared_files':len(current),'differences':diff,'model_method':'geometry snapshot plus independently reopened blend/GLB; no binary repeatability claim'}))
   if diff:raise RuntimeError('Repeat differs '+str(diff))
  validation=subprocess.run([sys.executable,'scripts/validate_delivery.py'],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
  (R/'reports/validate_delivery.log').write_bytes(validation.stdout)
  if validation.returncode:
   print(validation.stdout.decode('utf-8',errors='replace'));raise SystemExit(validation.returncode)
 print('REBUILD_COMPLETE',flush=True)
if __name__=='__main__':main()
