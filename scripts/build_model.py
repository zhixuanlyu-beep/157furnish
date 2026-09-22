"""Editable R2 model; no rendering. Run in Blender background."""
import sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import bpy
from mathutils import Vector
bpy.context.preferences.filepaths.save_version=0
if hasattr(bpy.context.preferences.filepaths,'file_preview_type'):bpy.context.preferences.filepaths.file_preview_type='NONE'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene['revision']=REV;scene['layout_sha256']=SHA;scene['purpose']='概念图模，不作施工；帧1关闭/90开启；无渲染'
scene.frame_end=90
scene['fuel_variant']=FUEL;scene['fuel_status']='燃料未选；现场条件未决'
scene['model_dependencies']=json.dumps(model_dependencies(),sort_keys=True)
materials={}
for name,color in [('warmwhite',(0.89,.87,.79,1)),('wood',(.57,.36,.19,1)),('green',(.24,.40,.30,1)),('fabric',(.66,.66,.57,1)),('glass',(.56,.78,.80,.32)),('metal',(.18,.21,.22,1)),('floor',(.77,.66,.48,1)),('tile',(.75,.77,.73,1)),('check',(1,.25,.06,.15))]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.6
 if name=='glass':bs.inputs['Transmission Weight'].default_value=.55
 materials[name]=m
def coll(n,hidden=False):
 c=bpy.data.collections.new(n);scene.collection.children.link(c);c.hide_render=hidden;c.hide_viewport=hidden;return c
arch=coll('Architecture');furn=coll('Furniture_4');six=coll('Dining_6_extra',True);checks=coll('Inspection_Envelopes',True);ceiling=coll('Ceilings',True);doors=coll('Doors_windows');light=coll('Lights_cameras')
def link(obj,c):
 for old in list(obj.users_collection):old.objects.unlink(obj)
 c.objects.link(obj)
def cube(n,b,z,h,mat='wood',c=furn,parent=None):
 x,y,w,d=b;bpy.ops.mesh.primitive_cube_add(size=1,location=((x+w/2)/1000,(y+d/2)/1000,(z+h/2)/1000));o=bpy.context.object;o.name=n;o.dimensions=(w/1000,d/1000,h/1000);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[mat]);link(o,c)
 if parent:o.parent=parent
 o['expected_center_mm']=[x+w/2,y+d/2,z+h/2];o['expected_size_mm']=[w,d,h];o['layout_sha256']=SHA
 return o
def root(n,c=furn):
 o=bpy.data.objects.new(n,None);c.objects.link(o);o['layout_id']=n;o['layout_sha256']=SHA;return o
for n,v in walls().items():cube(n,v['box'],v['z'],v['height'],'glass' if n.startswith('balcony_divider') else 'warmwhite',arch)
# Non-overlapping floor tiling follows stepped outline, not room labels or source area labels.
floorboxes=D['footprint_boxes']
for i,b in enumerate(floorboxes):cube('floor_'+str(i),b,-120,120,'floor',arch);cube('ceiling_'+str(i),b,2700,100,'warmwhite',ceiling)
for n,o in openings().items():
 x,y,w,h=o['box']
 if o['kind'] in ['door','sliding','passage']:
  jambs=[[x,y,30,h],[x+w-30,y,30,h]] if o['horizontal'] else [[x,y,w,30],[x,y+h-30,w,30]]
  for i,b in enumerate(jambs):cube(n+'_jamb'+str(i),b,0,o['height'],'warmwhite',doors)
 if o['kind']=='window':cube(n,[x,y+(h-25)/2,w,25] if o['horizontal'] else [x+(w-25)/2,y,25,h],o['sill'],o['height'],'glass',doors)
 if o['kind']=='door':
  poly=door_poly(o,0);cx=sum(p[0] for p in poly)/4;cy=sum(p[1] for p in poly)/4
  origin=o['origin'];length=o['width']-60;hinge=o['hinge'];px=origin[0]+((30+hinge*length) if o['horizontal'] else 0);py=origin[1]+(0 if o['horizontal'] else (30+hinge*length))
  pivot=root(n+'_hinge',doors);pivot.location=(px/1000,py/1000,0)
  b=[min(p[0] for p in poly),min(p[1] for p in poly),max(p[0] for p in poly)-min(p[0] for p in poly),max(p[1] for p in poly)-min(p[1] for p in poly)]
  leaf=cube(n+'_leaf',b,0,2050,'wood',doors);leaf.parent=pivot;leaf.matrix_parent_inverse=pivot.matrix_world.inverted()
  # Parent transform may not yet be updated; set local translation explicitly.
  leaf.location.x-=px/1000;leaf.location.y-=py/1000;leaf.matrix_parent_inverse.identity()
  hp=door_poly(o,0,True);hb=[min(p[0] for p in hp),min(p[1] for p in hp),max(p[0] for p in hp)-min(p[0] for p in hp),max(p[1] for p in hp)-min(p[1] for p in hp)]
  handle=cube(n+'_handle',hb,950,30,'metal',doors);handle.parent=pivot;handle.location.x-=px/1000;handle.location.y-=py/1000
  pivot.rotation_euler.z=0;pivot.keyframe_insert(data_path='rotation_euler',frame=1);pivot.rotation_euler.z=math.radians(o['sign']*90);pivot.keyframe_insert(data_path='rotation_euler',frame=90)
 if o['kind']=='sliding':
  fb=slide_fixed_box(o)
  if fb:cube(n+'_fixed_panel',fb,0,2100,'glass',doors)
  a=slide_box(o);b=slide_box(o,True);ob=cube(n+'_sliding',a,0,2100,'glass',doors);ob.keyframe_insert(data_path='location',frame=1);ob.location.x+=(b[0]-a[0])/1000;ob.location.y+=(b[1]-a[1])/1000;ob.keyframe_insert(data_path='location',frame=90)
def animate_translate(o,dx,dy):
 o.keyframe_insert(data_path='location',frame=1);o.location.x+=dx/1000;o.location.y+=dy/1000;o.keyframe_insert(data_path='location',frame=90)
for n,v in D['furniture'].items():
 par=root(n);par['label']=v['label'];par['box_mm']=v['box'];par['height_mm']=v['height'];par['kind']=v['kind'];par['status']=v['status']
 x,y,w,d=v['box'];z=v['z'];h=v['height'];kind=v['kind'];front=v['front']
 def part(s,b,zz,hh,mat='wood'):return cube(n+'__'+s,b,zz,hh,mat,furn,par)
 if kind=='cabinet':
  # Local u across frontage, v from front into cabinet. Every piece stays inside source envelope at frame 1.
  span=w if front in ['north','south'] else d;depth=d if front in ['north','south'] else w
  def local(u,t,ww,dd):
   if front=='south':return [x+u,y+t,ww,dd]
   if front=='north':return [x+u,y+d-t-dd,ww,dd]
   if front=='west':return [x+t,y+u,dd,ww]
   return [x+w-t-dd,y+u,dd,ww]
  part('plinth',local(0,0,span,depth),z,80,'metal');part('top',local(0,0,span,depth),z+h-18,18)
  part('sideL',local(0,0,18,depth),z+80,h-98);part('sideR',local(span-18,0,18,depth),z+80,h-98);part('back',local(18,depth-18,span-36,18),z+80,h-98)
  u=0
  for i,(ww,use) in enumerate(zip(v.get('modules',[span]),v.get('contents',['层板']))):
   if u:part('partition'+str(i),local(u-9,0,18,depth),z+80,h-98)
   shelves,rails,drawers=cabinet_levels(h,use)
   for j,zz in enumerate(shelves):part('shelf%d_%d'%(i,j),local(u+18,30,ww-36,depth-48),z+zz,18)
   for j,zz in enumerate(rails):part('rail%d_%d'%(i,j),local(u+18,depth/2,ww-36,20),z+zz,20,'metal')
   if drawers:
    for j,zz in enumerate(drawers):
     dr=part('drawer%d_%d'%(i,j),local(u+20,35,ww-40,depth-65),z+zz,150)
     dx,dy={'north':(0,450),'south':(0,-450),'east':(450,0),'west':(-450,0)}[front];animate_translate(dr,dx,dy)
   if v.get('door_type')=='sliding':
    door=part('front'+str(i),local(u+2,i%2*20,ww-4,18),z+82,h-102,'warmwhite');shift=ww*.5*(1 if u+ww*1.5<=span else -1);dx,dy=(shift,0) if front in ['north','south'] else (0,shift);door['animation_type']='分轨移门示意';animate_translate(door,dx,dy)
   else:
    leaves=2 if ww>650 else 1
    for j in range(leaves):
     start=u+j*ww/leaves+11;length=ww/leaves-22;door=part('front%d_%d'%(i,j),local(start,0,length,18),z+82,h-102,'warmwhite')
     pivot=root(n+'__hinge%d_%d'%(i,j));pivot.parent=par
     if front in ['north','south']:px,py=x+start,y+9 if front=='south' else y+d-9
     else:px,py=x+9 if front=='west' else x+w-9,y+start
     pivot.location=(px/1000,py/1000,0);door.parent=pivot;door.location.x-=px/1000;door.location.y-=py/1000
     pivot.rotation_euler.z=0;pivot.keyframe_insert(data_path='rotation_euler',frame=1);pivot.rotation_euler.z=math.radians(90 if front in ['north','west'] else -90);pivot.keyframe_insert(data_path='rotation_euler',frame=90);door['animation_type']='概念90度铰链门；实物五金待核'
   u+=ww
 elif kind=='bed':
  mw,md=v['mattress'];part('frame',[x,y,w,d],z+150,180);part('mattress',[x+(w-mw)/2,y+(d-md)/2,mw,md],z+330,230,'fabric');part('head',[x,y+d-70,w,70],z,h)
  for i in range(2 if w>1500 else 1):part('pillow'+str(i),[x+120+i*(w/2),y+d-500,min(600,w/2-150),330],z+560,80,'warmwhite')
  for dx in [30,w-70]:
   for dy in [30,d-70]:part('leg_%s_%s'%(dx,dy),[x+dx,y+dy,40,40],z,150,'wood')
 elif kind in ['table','chair']:
  top=450 if kind=='chair' else h;part('top',[x,y,w,d],z+top-35,35,'wood' if kind=='table' else 'green')
  for dx in [20,w-50]:
   for dy in [20,d-50]:part('leg_%s_%s'%(dx,dy),[x+dx,y+dy,30,30],z,top-35,'metal')
  if kind=='chair':
   back={'north':[x,y,w,35],'south':[x,y+d-35,w,35],'east':[x,y,35,d],'west':[x+w-35,y,35,d]}[front];part('back',back,z+450,h-450,'green')
 elif kind=='sofa':
  part('base',[x,y,w,d],z,450,'fabric');part('back',[x,y,180,d],z+450,h-450,'green')
  for yy in [y,y+d-150]:part('arm'+str(yy),[x,yy,w,150],z+450,180,'fabric')
 elif kind=='appliance':
  part('body',[x,y,w,d],z,h,'metal')
  # Door is kept within body at frame1 and moves out for a service demonstration.
  b=[x,y,20,d] if front=='west' else [x+w-20,y,20,d] if front=='east' else [x,y+d-20,w,20] if front=='north' else [x,y,w,20]
  a=part('service_panel',b,z+150,max(100,h-300),'warmwhite');dx,dy={'west':(-600,0),'east':(600,0),'south':(0,-600),'north':(0,600)}[front];animate_translate(a,dx,dy)
 elif kind=='wc':
  back={'west':[x+w-150,y,150,d],'east':[x,y,150,d],'north':[x,y,w,150],'south':[x,y+d-150,w,150]}[front];part('cistern',back,z,h,'tile');part('bowl',[x,y,w,d],z,420,'tile')
 elif kind=='screen':
  ob=part('body',[x,y,w,d],z,h,'fabric');ob.keyframe_insert(data_path='scale',frame=1);ob.keyframe_insert(data_path='location',frame=1)
  lowered=D['screen_lowered_geometry'];ob.scale.z=lowered['height']/h;ob.location.z=(lowered['z']+lowered['height']/2)/1000;ob.keyframe_insert(data_path='scale',frame=90);ob.keyframe_insert(data_path='location',frame=90)
 else:part('body',[x,y,w,d],z,h,'glass' if kind in ['glass','screen'] else 'tile')
# Fuel-specific visible concept top stays within the shared hob envelope.
x,y,w,d=D['furniture']['hob']['box']
par=bpy.data.objects['hob'];par['fuel_variant']=FUEL;par['requirements']='；'.join(D['fuel_variants'][FUEL]['requirements'])
if FUEL=='gas':
 for yy in [y+180,y+d-380]:cube('hob__gas_burner_'+str(yy),[x+180,yy,220,200],832,18,'metal',furn,par)
else:cube('hob__induction_glass',[x+120,y+120,430,d-240],842,8,'metal',furn,par)
for n,v in D['operations'].items():o=cube(n,v['box'],0,1800,'check',checks);o.display_type='WIRE'
for n,b in D['states']['six_extra'].items():
 x,y,w,d=b;cube(n+'_seat',b,415,35,'green',six);cube(n+'_back',[x if n.endswith('w') else x+w-35,y,35,d],450,350,'green',six)
 for dx in [20,w-50]:
  for dy in [20,d-50]:cube(n+'_leg_'+str(dx)+'_'+str(dy),[x+dx,y+dy,30,30],0,415,'metal',six)
for n,pos,target in D['model_setup']['cameras']:
 pos=[v/1000 for v in pos];target=[v/1000 for v in target]
 ca=bpy.data.cameras.new(n);ob=bpy.data.objects.new('Camera_'+n,ca);light.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ca.lens=24
 if n=='Top':ca.type='ORTHO';ca.ortho_scale=18
for n,loc in D['model_setup']['lights']:
 loc=[v/1000 for v in loc]
 ld=bpy.data.lights.new(n,'AREA');ld.energy=600;ld.shape='DISK';ld.size=6;ob=bpy.data.objects.new(n,ld);light.objects.link(ob);ob.location=loc
scene.camera=bpy.data.objects['Camera_Whole'];scene.world.color=(.3,.3,.3)
scene.frame_set(1);bpy.context.view_layer.update()
snapshot={}
for n,v in D['furniture'].items():
 pts=[child.matrix_world@Vector(corner) for child in bpy.data.objects[n].children_recursive if child.type=='MESH' for corner in child.bound_box]
 mins=[min(p[i] for p in pts)*1000 for i in range(3)];maxs=[max(p[i] for p in pts)*1000 for i in range(3)]
 snapshot[n]={'box':[mins[0],mins[1],maxs[0]-mins[0],maxs[1]-mins[1]],'z':mins[2],'height':maxs[2]-mins[2]}
projection=bound({'generator_sha256':hashfile(__file__),'dependencies':model_dependencies(),'fuel':FUEL,'furniture':snapshot,'state':'frame1'})
dump('model/projection_snapshot_'+FUEL+'.json',projection)
if FUEL=='gas':dump('model/projection_snapshot.json',projection)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/('model/'+MODEL_STEM+'.blend')))
bpy.ops.object.select_all(action='DESELECT')
for c in [arch,furn,doors]:
 for o in c.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/('model/'+MODEL_STEM+'.glb')),export_format='GLB',use_selection=True,export_animations=False,export_extras=True)
dump('model/scene_config_'+FUEL+'.json',bound({'units':'metres','furniture':{n:{'box_m':[x/1000 for x in v['box']],'height_m':v['height']/1000,'z_m':v['z']/1000} for n,v in D['furniture'].items()},'blender':bpy.app.version_string,'cameras':7,'rendered':False}))
print('MODEL_BUILD_COMPLETE')

if FUEL=='gas':(ROOT/'model/scene_config.json').write_bytes((ROOT/'model/scene_config_gas.json').read_bytes())
