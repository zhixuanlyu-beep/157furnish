"""Rebuild from only local source inputs in a fresh temporary workspace."""
import argparse,subprocess,sys,shutil,tempfile
from common import *
def main():
 p=argparse.ArgumentParser();p.add_argument('--blender',required=True);a=p.parse_args();base=(ROOT/'reports').resolve();target=Path(tempfile.mkdtemp(prefix='_clean_rebuild_',dir=base)).resolve()
 try:
  for folder in ['scripts','data']:shutil.copytree(ROOT/folder,target/folder,ignore=shutil.ignore_patterns('__pycache__'))
  for n in ['requirements.txt',D['source_image']]:shutil.copy2(ROOT/n,target/n)
  result=subprocess.run([sys.executable,str(target/'scripts/rebuild.py'),'--blender',a.blender],cwd=target,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (ROOT/'reports/clean_rebuild.log').write_bytes(result.stdout)
  differences=[];count=0
  if result.returncode==0:
   for folder in ['drawings','tables','docs']:
    expected={p.relative_to(ROOT) for p in (ROOT/folder).rglob('*') if p.is_file()};actual={p.relative_to(target) for p in (target/folder).rglob('*') if p.is_file()}
    differences.extend(str(p) for p in expected^actual)
    for rel in expected&actual:
     count+=1
     if hashfile(ROOT/rel)!=hashfile(target/rel):differences.append(str(rel))
   for rel in ['model/projection_snapshot.json','README.md','AGENTS.md']:
    count+=1
    if hashfile(ROOT/rel)!=hashfile(target/rel):differences.append(rel)
  passed=result.returncode==0 and not differences
  dump('reports/clean_rebuild.json',bound({'passed':passed,'subprocess_exit':result.returncode,'compared_files':count,'differences':differences,'inputs':['scripts/','data/','requirements.txt',D['source_image']],'external_project_files_used':False,'environment_dependencies':'Python+Pillow+NumPy+Blender+system Chinese font'}))
  print('CLEAN_REBUILD',passed,'compared',count,'differences',differences)
  if not passed:raise RuntimeError('Clean rebuild failed; see clean_rebuild.log')
 finally:
  # Verify the exact absolute generated target before recursive cleanup; never touch sibling projects.
  if target.parent!=base or not target.name.startswith('_clean_rebuild_'):raise RuntimeError('Unsafe cleanup target')
  shutil.rmtree(target)
if __name__=='__main__':main()
