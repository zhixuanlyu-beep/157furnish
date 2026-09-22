"""Reopen blend and GLB independently; compare actual geometry to mm source."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import bpy
from mathutils import Vector
def inspect():
 errors=[];results={}
 for n,v in D['furniture'].items():
  o=next((o for o in bpy.data.objects if o.get('layout_id')==n),None)
  if not o:errors.append('missing '+n);continue
  children=list(o.children_recursive);points=[q.matrix_world@Vector(p) for q in children if q.type=='MESH' for p in q.bound_box]
  if not points:errors.append('no meshes '+n);continue
  actual=[min(p[i] for p in points)*1000 for i in range(3)]+[max(p[i] for p in points)*1000 for i in range(3)]
  x,y,w,h=v['box'];z=v['z'];expected=[x,y,z,x+w,y+h,z+v['height']]
  err=max(abs(a-b) for a,b in zip(actual,expected));results[n]=round(err,4)
  if err>.1:errors.append(n+' bounds '+str(err))
  if v['kind']=='bed':
   mattress=bpy.data.objects.get(n+'__mattress');pts=[mattress.matrix_world@Vector(p) for p in mattress.bound_box];dims=[(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(2)]
   if max(abs(a-b) for a,b in zip(dims,v['mattress']))>.1:errors.append(n+' mattress mismatch')
  # Orientation is checked using real child meshes, not only the parent's envelope.
  parts=[]
  if v['kind']=='chair':parts=[(n+'__back',True)]
  if v['kind']=='appliance':parts=[(n+'__service_panel',False)]
  if v['kind']=='wc':parts=[(n+'__cistern',True)]
  if v['kind']=='cabinet':parts=[(p.name,False) for p in children if p.type=='MESH' and p.name.startswith(n+'__front')]
  for name,opposite in parts:
   part=bpy.data.objects.get(name)
   if not part:errors.append('missing directional part '+name);continue
   pts=[part.matrix_world@Vector(p) for p in part.bound_box];axis=0 if v['front'] in ['east','west'] else 1;center=(min(p[axis] for p in pts)+max(p[axis] for p in pts))*500;mid=(x+w/2) if axis==0 else (y+h/2);positive=v['front'] in ['east','north']
   if opposite:positive=not positive
   if (center>mid)!=positive:errors.append('orientation '+name)
 hob=bpy.data.objects.get('hob')
 fuel_meshes=[p.name for p in hob.children_recursive if p.type=='MESH'] if hob else []
 if FUEL=='gas' and sum('gas_burner' in n for n in fuel_meshes)!=2:errors.append('gas concept burners missing')
 if FUEL=='electric' and not any('induction_glass' in n for n in fuel_meshes):errors.append('electric concept glass missing')
 return errors,results
bpy.ops.wm.open_mainfile(filepath=str(ROOT/('model/'+MODEL_STEM+'.blend')))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
assert bpy.context.scene['layout_sha256']==SHA
assert bpy.context.scene['fuel_variant']==FUEL
assert json.loads(bpy.context.scene['model_dependencies'])==model_dependencies()
errors,bounds=inspect();mesh_errors=[]
for o in bpy.data.objects:
 if o.type!='MESH' or 'expected_center_mm' not in o:continue
 # Hidden inspection envelopes and alternatives have no parent; use evaluated coordinates as saved.
 pts=[o.matrix_world@Vector(p) for p in o.bound_box];center=[(max(p[i] for p in pts)+min(p[i] for p in pts))*500 for i in range(3)];size=[(max(p[i] for p in pts)-min(p[i] for p in pts))*1000 for i in range(3)]
 if max(abs(a-b) for a,b in zip(center+size,list(o['expected_center_mm'])+list(o['expected_size_mm'])))>.1:mesh_errors.append(o.name)
frame1={o.name:list(o.matrix_world.translation) for o in bpy.data.objects};bpy.context.scene.frame_set(90);bpy.context.view_layer.update();animated=sum((Vector(frame1[o.name])-o.matrix_world.translation).length>.001 for o in bpy.data.objects)
blend={'furniture_max_error_mm':bounds,'errors':errors,'mesh_transform_errors':mesh_errors,'animated_objects_at_frame90':animated}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(ROOT/('model/'+MODEL_STEM+'.glb')));bpy.context.view_layer.update();err,bb=inspect()
report=bound({'blend':blend,'glb':{'furniture_max_error_mm':bb,'errors':err},'passed':not(errors or err or mesh_errors),'blend_sha256':hashfile(ROOT/('model/'+MODEL_STEM+'.blend')),'glb_sha256':hashfile(ROOT/('model/'+MODEL_STEM+'.glb'))})
report['fuel']=FUEL
report['dependencies']=model_dependencies()
dump('reports/model_verification_'+FUEL+'.json',report)
if FUEL=='gas':dump('reports/model_verification.json',report)
print(json.dumps(report,ensure_ascii=False))
if not report['passed']:raise RuntimeError('Model verification failed')
