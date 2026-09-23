"""Same drawing primitives generate editable SVG and Chinese PNG. No 3D renders."""
import csv,html,copy,math,textwrap
from PIL import Image,ImageDraw,ImageFont
from common import *
W,H=1800,1250
FONT=ImageFont.truetype('msyh.ttc',18).path
INDEX=[]
def table(name,head,rows):
 with (ROOT/'tables'/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['revision','layout_sha256']+head);w.writerows([[REV,SHA]+list(row) for row in rows])
class Sheet:
 def __init__(self,title,notes=()):
  self.title=title;self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1250" viewBox="0 0 1800 1250" data-revision="{REV}" data-layout-sha256="{SHA}">'];self.im=Image.new('RGB',(W,H),'#fcfbf6');self.dr=ImageDraw.Draw(self.im);self.rect([0,0,W,H],'#fcfbf6');self.text(45,26,'157FURNISH  /  '+REV,22,'#576858');self.text(45,66,title,34);self.line([(45,119),(1755,119)],'#456653',2)
  self.text(45,1190,'毫米 · X东 Y北 · 概念深化，非施工/下单图 · 仅二维图，无三维渲染',18);self.text(45,1218,'布局 SHA256 '+SHA,14)
  self.notes(notes)
 def rect(self,b,fill='none',stroke=None,width=1,attrs=''):
  x,y,w,h=b;self.svg.append(f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{width}" {attrs}/>')
  if fill!='none':self.dr.rectangle([x,y,x+w,y+h],fill=fill)
  if stroke:self.dr.rectangle([x,y,x+w,y+h],outline=stroke,width=width)
 def text(self,x,y,t,size=18,color='#263c34'):
  self.svg.append(f'<text x="{x:.3f}" y="{y+size:.3f}" font-size="{size}" fill="{color}" font-family="Microsoft YaHei, sans-serif">{html.escape(str(t))}</text>');self.dr.text((x,y),str(t),font=ImageFont.truetype(FONT,size),fill=color)
 def line(self,pts,color='#526159',width=1):
  self.svg.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>');self.dr.line(pts,fill=color,width=width)
 def polygon(self,pts,fill,stroke='#456653'):
  self.svg.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}"/>');self.dr.polygon(pts,fill=fill,outline=stroke)
 def notes(self,notes):
  self.text(1380,150,'读图与条件',22);yy=195
  for i,t in enumerate(notes):
   text=str(i+1)+'. '+t
   for j in range(0,len(text),20):self.text(1380,yy,text[j:j+20],17);yy+=29
   yy+=16
 def plan(self,data=D,crop=None,ops=False,route=None,six=False,baseline=False,services=False,hvac=False,alter=False,labels=True,opened=False):
  before=self.im.copy();self.svg.append('<defs><clipPath id="planClip"><rect x="50" y="145" width="1280" height="970"/></clipPath></defs><g clip-path="url(#planClip)">')
  crop=crop or [-250,-250,15600,10600];cx,cy,cw,ch=crop;s=min(1260/cw,950/ch);ox=55+(1260-cw*s)/2;oy=155+(950-ch*s)/2
  self.crop=crop;self.scale=s;self.pt=lambda x,y:(ox+(x-cx)*s,oy+(cy+ch-y)*s)
  def rb(b):x,y,w,h=b;px,py=self.pt(x,y+h);return [px,py,w*s,h*s]
  self.rb=rb
  def visible(b):return overlap(b,crop)
  for n,r in data['rooms'].items():
   for b in r['boxes']:
    if visible(b):self.rect(rb(b),'#edf0e7' if n in ['bathA','bathB','kitchen','balcony'] else '#f5ead9')
  for n,v in walls(data).items():
   if v['z']<1800 and visible(v['box']):self.rect(rb(v['box']),'#33463e')
  for n,o in openings(data).items():
   if not visible(o['box']):continue
   if o['kind']=='window':self.rect(rb(o['box']),'#b8d9df','#466b74')
   elif o['kind']=='door':
    self.polygon([self.pt(*p) for p in door_poly(o,90 if opened else 0)],'#be9364')
    if opened:
     arc=[self.pt(*door_poly(o,a)[1]) for a in range(0,91,5)];self.line(arc,'#b87943',1)
   elif o['kind']=='sliding':
    self.rect(rb(slide_box(o,opened)),'#aac9c9','#466b74')
    if slide_fixed_box(o):self.rect(rb(slide_fixed_box(o)),'#aac9c9','#466b74')
  if not baseline:
   for n,v in data['furniture'].items():
    b=v['box']
    if not visible(b):continue
    color={'bed':'#cfdbcb','chair':'#a9bfa8','sofa':'#a9bfa8','appliance':'#bdc9cc','glass':'#c3e0e5','shower':'#d9e8e8','wc':'#e3e7e1','basin':'#e3e7e1'}.get(v['kind'],'#dfc39f')
    upper=v['kind']=='cabinet' and v['z']>=1200
    self.rect(rb(b),'none' if upper else color,'#576858',1,f'data-object="{n}" data-mm="{",".join(map(str,b))}" data-transform="{ox},{oy},{s},{cx},{cy+ch}"')
    x,y,w,h=b
    if v['kind']=='bed':
     mw,md=v['mattress'];west=v.get('head')=='west'
     if west:mw,md=md,mw
     self.rect(rb([x+(w-mw)/2,y+(h-md)/2,mw,md]),'#edf0e4','#7b8d7b');self.rect(rb([x+100,y+150,300,min(600,h-300)] if west else [x+150,y+h-450,min(600,w-300),300]),'#fcfbf6','#7b8d7b')
    if v['kind']=='cabinet':
     u=0
     for mm in v.get('modules',[])[:-1]:
      u+=mm;p=[(x+u,y),(x+u,y+h)] if v['front'] in ['north','south'] else [(x,y+u),(x+w,y+u)];self.line([self.pt(*a) for a in p],'#94774e')
    if v['kind'] in ['wc','appliance','chair'] or n=='hob':
     dx,dy={'west':(-1,0),'east':(1,0),'north':(0,1),'south':(0,-1)}[v['front']];mx,my=x+w/2,y+h/2;length=min(w,h)*.30
     self.line([self.pt(mx,my),self.pt(mx+dx*length,my+dy*length)],'#466b74',2)
     self.line([self.pt(mx+dx*length-dx*65-dy*40,my+dy*length-dy*65+dx*40),self.pt(mx+dx*length,my+dy*length),self.pt(mx+dx*length-dx*65+dy*40,my+dy*length-dy*65-dx*40)],'#466b74',2)
    if labels:
     px,py=self.pt(x+30,y+80 if upper else y+h/2);label=v['label'] if crop!=[-250,-250,15600,10600] else n
     if crop!=[-250,-250,15600,10600]:label={'utility_sink':'清洗台','utility_base':'家政下柜'}.get(n,label)
     self.text(px,py,label[:16],max(11,min(16,int(s*120))))
  if six:
   for n,b in data['states']['six_extra'].items():self.rect(rb(b),'#b7c995','#456653',2);px,py=self.pt(b[0],b[1]+b[3]);self.text(px,py,'加端椅',13)
  if ops:
   for n,v in data['operations'].items():
    if visible(v['box']):self.rect(rb(v['box']),'none','#c17b42',2)
  if services:
   occupied=[]
   for i,v in enumerate(data['services']):
    px,py=self.pt(v['x'],v['y']);self.rect([px-5,py-5,10,10],'#ad5443')
    for dx,dy in [(8,-20),(8,2),(-38,-20),(-38,2),(8,24),(-38,24)]:
     bb=[px+dx,py+dy,32,18]
     if all(not overlap(bb,b) for b in occupied) and 55<=bb[0]<=1290 and 150<=bb[1]<=1090:break
    occupied.append(bb);self.text(bb[0],bb[1],'S%02d'%(i+1),13)
  if hvac:
   for v in data['hvac']:
    px,py=self.pt(*v['point'][:2]);self.rect([px-7,py-7,14,14],'#377aa0');self.text(px+12,py,str(v['fresh_m3h'])+' m³/h',16)
  if alter:
   for item in D['demolition']:
    e=next(e for e in D['original']['edges'] if e['id']==item['edge']);self.line([self.pt(*e['a']),self.pt(*e['b'])],'#ca5944',7)
  if route:
   for rr in route:
    if rr['path']:self.line([self.pt(*p) for p in rr['path']],'#286fa1',3)
  # Label reference rooms only in empty baseline, avoiding furniture label collisions.
  if baseline:
   for n,r in data['rooms'].items():
    b=r['boxes'][0];px,py=self.pt(b[0]+b[2]/3,b[1]+b[3]/2);self.text(px,py,r['label'],21)
  self.svg.append('</g>');piece=self.im.crop((50,145,1330,1115));self.im=before;self.im.paste(piece,(50,145));self.dr=ImageDraw.Draw(self.im)
  self.line([(1275,225),(1275,163),(1265,180),(1275,163),(1285,180)],'#33463e',3);self.text(1265,130,'北',18)
  sx,sy=80,1125;self.line([(sx,sy),(sx+1000*s,sy)],'#33463e',3);self.text(sx,sy+6,'1000 mm',14)
 def save(self,name):
  self.svg.append('</svg>');(ROOT/'drawings/svg'/name).write_text('\n'.join(self.svg)+'\n',encoding='utf-8');self.im.save(ROOT/'drawings/png'/name.replace('.svg','.png'));INDEX.append([name,self.title])
def solar():
 rows=[];lat=math.radians(D['assumptions']['latitude_deg'])
 # Point-ray study only. Includes modeled walls, not unknown external obstructions or curtains.
 for season,decl in [('春分',0),('夏至',23.44),('秋分',0),('冬至',-23.44)]:
  de=math.radians(decl)
  for hour in range(6,19):
   ha=math.radians(15*(hour-12)+(D['assumptions']['longitude_deg']-120));dx=-math.cos(de)*math.sin(ha);dy=math.cos(lat)*math.sin(de)-math.sin(lat)*math.cos(de)*math.cos(ha);dz=math.sin(lat)*math.sin(de)+math.cos(lat)*math.cos(de)*math.cos(ha)
   for n in ['bedA','bedB','bedC']:
    f=D['furniture'][n];x,y,w,h=f['box'];p=[x+w/2,y+h-300,680];first=None
    if dz>0:
     for e in D['edges']:
      horizontal=e['a'][1]==e['b'][1];axis=1 if horizontal else 0;velocity=dy if horizontal else dx
      if abs(velocity)<1e-8:continue
      t=(e['a'][axis]-p[axis])/velocity
      if t<=0:continue
      xx,yy,zz=p[0]+t*dx,p[1]+t*dy,p[2]+t*dz
      along=xx-e['a'][0] if horizontal else yy-e['a'][1]
      if 0<=along<=math.dist(e['a'],e['b']) and 0<=zz<=2700:
       hole=next((o for o in e['openings'] if o['start']<=along<=o['start']+o['width'] and o['sill']<=zz<=o['sill']+o['height']),None)
       # Internal passage does not terminate ray; external glazing identifies possible exposure.
       if hole and not e['external']:continue
       hit='玻璃可达' if hole and hole['kind']=='window' else '墙/门遮挡'
       if first is None or t<first[0]:first=(t,hit,e['id'])
    status='太阳在地平线下' if dz<=0 else first[1] if first else '射线越过室内顶界；未穿窗'
    rows.append([season,hour,n,round(math.degrees(math.asin(dz)),1),status,first[2] if first else ''])
 table('卧室日照点射线.csv',['季节近似','北京时间整点','枕点','太阳高度_deg','结果','首先遇到边界'],rows)
 dump('reports/solar.json',bound({'method':'四季代表赤纬、经度修正的整点枕点射线；未计均时差，非精确日期星历','rows':rows,'limitations':['不计算日照达标、照度或过热','仅检查概念墙洞；未纳入家具遮光及玻璃窗框','外遮挡、帘、窗高和地理位置待核']}))
 return rows
def main():
 snap=json.loads((ROOT/'model/projection_snapshot.json').read_text(encoding='utf-8'));assert_projection_current(snap)
 for fuel in D['fuel_variants']:assert_projection_current(json.loads((ROOT/('model/projection_snapshot_'+fuel+'.json')).read_text(encoding='utf-8')))
 for n,v in D['furniture'].items():assert max(abs(a-b) for a,b in zip(v['box'],snap['furniture'][n]['box']))<.1,(n,'model differs')
 U=json.loads((ROOT/'reports/usage.json').read_text(encoding='utf-8'));assert U['layout_sha256']==SHA
 q=Sheet('01 原始尺寸基线 / 尺寸链与假设分离',D['source_notes'][:5]+['黑墙为R1原始概念边界，非实测。','总宽15077，总深10074。']);original=copy.deepcopy(D);original['edges']=D['original']['edges'];original['rooms']=D['original']['rooms'];q.plan(data=original,baseline=True)
 for vals,axis in [(D['dimensions'][0]['value'],'x'),(D['dimensions'][2]['value'],'y')]:
  at=0
  for v in vals:
   if axis=='x':a=q.pt(at,10350);b=q.pt(at+v,10350);q.line([a,b]);q.text((a[0]+b[0])/2-15,a[1]-24,str(v),16)
   else:a=q.pt(-180,at);b=q.pt(-180,at+v);q.line([a,b]);q.text(a[0]-40,(a[1]+b[1])/2,str(v),14)
   at+=v
 q.save('01-baseline.svg')
 q=Sheet('02 R2推荐研究 / 三房两卫与客餐厨一体', ['B主卧、A儿童、C客房。','原厨房拟开放；无水岛＋餐桌。','阳台两端烹饪／洗烘分别进出。','燃气、电灶均附条件；不锁定燃料。','总图编号对应家具表及逐室图。','所有门关闭；开启与错时另图。']);q.plan();q.save('02-plan.svg')
 for state,title in [('normal4','四人正常就座'),('normal6','六人增加端椅'),('chairs_pulled','餐椅拉出450状态'),('laundry_open','洗烘开启/装卸状态')]:
  data=copy.deepcopy(D)
  if state=='chairs_pulled':
   for n,v in D['operations'].items():
    if n.startswith('dining_pull'):data['furniture'][v['owner']]['box']=v['box']
  q=Sheet('使用情景 / '+title,['蓝线为620mm方篮可达路线。','棕框为使用包络；不代表同时可用。','餐桌1600×850；六人端位需试坐。','所有通行门按完全开启。','洗烘红框开启件／绿框操作者。','失败记录保留，不画虚假通过线。']);q.plan(data=data,ops=state=='chairs_pulled',six=state=='normal6',opened=True,route=[r for r in U['routes'] if r['state']==state and r['width_mm']==620 and r['name']=='洗烘'])
  if state=='laundry_open':
   for part,b in D['operations']['laundry_use']['parts'].items():q.rect(q.rb(b),'none','#ca5944' if part=='moving' else '#36765a',3)
  q.save('03-'+state+'.svg')
 q=Sheet('04 门柜开启与使用包络',['房门为实际90°位置及弧线。','衣柜使用移门，600站人；床头三抽独立设置。','柜体棕框为操作包络，非实体。','普通柜门为概念90度铰链；五金待核。','详见操作状态表及逐度门扇检查。']);q.plan(ops=True,opened=True);q.save('04-operations.svg')
 q=Sheet('05 500 / 600 / 620 / 900 路线研究',['蓝线示500单人路线。','网格50，轴对齐方形包络；端点吸附误差≤25。','含门框、全开门及把手。','900主要通路目标未全面满足，不能标为通过。','路线包含入户、睡眠、备餐、就餐、洗烘和到窗。']);q.plan(opened=True,route=[r for r in U['routes'] if r['state']=='normal4' and r['width_mm']==500]);q.save('05-routes.svg')
 for c in D['candidates']:
  data=candidate_data(c)
  if c['id'] in ['B_rotated','C_rotated']:data['furniture']['bedB' if c['id']=='B_rotated' else 'bedC']['head']='west'
  if c['id']=='A_growth':data['furniture']['bedA']['mattress']=[1500,2000]
  q=Sheet('候选 / '+c['label'],c['conditions']+['候选独立表达，不替代推荐模型。','排序：实体、必要通路、操作、收纳、拆改。']);q.plan(data=data,alter=c['id']=='open_kitchen')
  if 'sink_box' in c:q.rect(q.rb(c['sink_box']),'#b8d9df','#466b74',2);px,py=q.pt(*c['sink_box'][:2]);q.text(px,py,'辅助槽条件位',13)
  q.save('06-candidate-'+c['id']+'.svg')
 q=Sheet('07 拟拆改 / 厨房西隔墙与南入口墙',['红线为拟拆两段隔墙及旧门。','结构性质未核，不能按图拆墙。','阳台分界墙、梁柱、外墙和烟道保留。','优先沿用阳台现有洞口。','条件受阻见单列回退图。']);q.plan(alter=True);q.save('07-alterations.svg')
 for fuel,v in D['fuel_variants'].items():
  q=Sheet('阳台燃料并列 / '+v['label'],['净深1143，源于墙内侧；未实测。','东灶朝西；西洗烘朝东。','洗衣路线不穿过灶前。']+v['requirements']+['两案均须排烟，禁止默认直排外立面。']);q.plan(crop=[8650,8200,6500,1950],ops=True,opened=True);q.save('14-balcony-'+fuel+'.svg')
 q=Sheet('端部窗区条件 / 平面关系',['原窗台100；灶台850。','西端洗烘叠放高1950。','设备背后需固定不燃衬板。','开启扇、支承、防水保温待专项设计。','北侧可开窗与检修不能被封堵。','高度关系见下一张；不表示已批准改窗。']);q.plan(crop=[8650,8450,6500,1700],opened=True);q.save('15-window-conditions.svg')
 q=Sheet('端部窗区条件 / 高度关系示意',['蓝框为原概念低窗区。','棕框为设备外包络，不是封窗范围。','不燃背衬与设备固定须专业节点。','不得把设备支承在未核窗框上。','北侧可开启扇、通风及检修另核。'])
 for i,n in enumerate(['laundry','hob']):
  v=D['furniture'][n];bx=150+i*600;by=1030;s=.27;window=openings()['balcony_w_window' if n=='laundry' else 'balcony_e_window'];q.rect([bx,by-(window['sill']+window['height'])*s,420,window['height']*s],'#e0ecee','#466b74',2);q.rect([bx+60,by-v['height']*s,240,v['height']*s],'#dfc39f','#576858',2);q.text(bx,220,v['label'],20);q.text(bx,265,'设备高'+str(v['height'])+'／原窗台'+str(window['sill']),18);q.text(bx,by+20,'高度示意；窗宽／节点待实测',16)
 q.save('15-window-elevation.svg')
 for state,title in [('temporary_drying','临时晾晒'),('cooking','烹饪操作者'),('luggage_open','行李架展开'),('screen_lowered','投影幕布放下')]:
  q=Sheet('分状态 / '+title,['橙色为该状态增加的占用。','所有状态分别检查；不承诺并用。','对应500/600/620/900失败见路线表。']);q.plan(opened=True)
  for n,b in D['states'][state].items():q.rect(q.rb(b),'none','#ca5944',3)
  q.save('16-state-'+state+'.svg')
 q=Sheet('公共区关系 / 取物—洗切—烹饪—上桌',['沙发至幕布平面间距约2150。','眼点/投射比/幕宽须按设备试验。','卷幕收起释放横向通行，放下另查。','阳台入口路线在北侧，不能占用灶前。','遮光帘与对流通风需兼容。']);q.plan(crop=[8750,800,6250,9100],opened=True,route=[r for r in U['routes'] if r['state']=='normal4' and r['width_mm']==500 and r['name'] in ['备餐','阳台烹饪','就餐','洗烘']]);q.save('17-public-flow.svg')
 for n,r in D['rooms'].items():
  bs=r['boxes'];x=min(b[0] for b in bs)-250;y=min(b[1] for b in bs)-250;xx=max(b[0]+b[2] for b in bs)+250;yy=max(b[1]+b[3] for b in bs)+250
  fs=[(k,v) for k,v in D['furniture'].items() if v['room']==n]
  notes=r['functions']+[v['label']+' '+ '×'.join(str(a) for a in v['box'][2:])+ ' 高'+str(v['height']) for k,v in fs]
  q=Sheet('逐室 / '+r['label'],notes[:12]);q.plan(crop=[x,y,xx-x,yy-y],opened=True)
  if n in ['bathA','bathB']:
   wc='wc'+n[-1];b=D['operations'][wc+'_use']['box'];q.rect(q.rb(b),'none','#ca5944',2);px,py=q.pt(b[0]+30,b[1]+b[3]-80);q.text(px,py,'前方750目标',16)
  q.save('08-room-'+n+'.svg')
 # Cabinet interiors and true orthogonal depth sections.
 for n,v in D['furniture'].items():
  if v['kind']!='cabinet':continue
  cap=capacity(n,v);notes=[f"模块{a['module']}：{a['use']}，净宽{a['net_width']}，净深{a['net_depth']}" for a in cap]+['板厚18，背板18、门18、台面18均概念。','柜门90度概念铰链；移门分轨示意。','挂杆、层板与抽屉需依据衣物及厂家五金深化。']
  q=Sheet('柜体内视立面与深度剖面 / '+v['label'],notes)
  span=v['box'][2] if v['front'] in ['north','south'] else v['box'][3];depth=v['box'][3] if v['front'] in ['north','south'] else v['box'][2];height=v['height'];s=min(850/span,730/height,290/depth);bx,by=100,1050
  q.rect([bx,by-height*s,span*s,height*s],'#f0e2ca','#526159',2);u=0
  for a in cap:
   width=a['width'];q.line([(bx+u*s,by),(bx+u*s,by-height*s)],'#8c795b',2);q.text(bx+(u+20)*s,by-height*s+35,a['use'],16)
   shelves,rails,drawers=cabinet_levels(height,a['use'])
   for z in shelves:q.line([(bx+(u+18)*s,by-z*s),(bx+(u+width-18)*s,by-z*s)],'#967245',2)
   for z in rails:q.line([(bx+(u+18)*s,by-z*s),(bx+(u+width-18)*s,by-z*s)],'#6b7f69',4)
   for z in drawers:q.rect([bx+(u+20)*s,by-(z+150)*s,(width-40)*s,150*s],'none','#967245',2)
   q.text(bx+(u+20)*s,by+15,str(width),18);u+=width
  secx=1020;q.rect([secx,by-height*s,depth*s,height*s],'#edddc3','#526159',2)
  shelves,rails,drawers=cabinet_levels(height,cap[0]['use'])
  for z in shelves:q.line([(secx+30*s,by-z*s),(secx+(depth-18)*s,by-z*s)],'#967245',2)
  for z in drawers:q.rect([secx+35*s,by-(z+150)*s,(depth-65)*s,150*s],'none','#967245',2)
  q.text(secx,by+15,'深'+str(depth),18);q.text(bx,200,'正立面：宽'+str(span)+' × 高'+str(height),23);q.text(secx,235,'深度剖面',21);q.save('09-cabinet-'+n+'.svg')
 q=Sheet('10 设备安装、取物及检修包络',['棕框按设备门600+站人450。','冰箱、洗烘、洗碗机尺寸均占位，未锁定型号。','高柜蒸烤/微波须独立核散热、层高与插座。','阳台叠放720×800×1950需防倾倒连接。','装卸须收起晾晒并腾空路线。']);q.plan(ops=True,opened=True);q.save('10-equipment.svg')
 q=Sheet('11 水电概念点位',['红点S编号对应右侧清单及CSV。','主槽留东侧；阳台两燃料接口待核。','地插、防溅、防冻与回路由专业深化。']);q.plan(services=True,labels=False)
 for i,v in enumerate(D['services']):q.text(1380,450+i*29,'S%02d  '%(i+1)+v['id'],16)
 q.save('11-services.svg')
 q=Sheet('12 空调新风预留研究',['蓝点为送风位置概念，不表示管线已穿梁。','主卧60、儿童30、客房30、公共区90 m³/h为选型讨论输入。','不是规范计算或设备额定风量。','卫生间独立排风；厨房排烟不接新风。','回风、噪声、冷凝水、吊顶净高及室外机现场核。']);q.plan(hvac=True);q.save('12-hvac.svg')
 rows=solar()
 for n in ['bedA','bedB','bedC']:
  room=D['furniture'][n]['room'];b=D['rooms'][room]['boxes'][0];notes=['继承北京40°N/116.5°E，图示北。','四季赤纬近似，整点枕点射线。','外遮挡、玻璃透过及窗帘未知。','仅作遮光窗帘与床头方向讨论，不作日照合规。']+[season+'：穿窗时点 '+','.join(str(r[1]) for r in rows if r[0]==season and r[2]==n and r[4]=='玻璃可达') for season in ['春分','夏至','秋分','冬至']]
  q=Sheet('13 卧室日照点射线 / '+D['rooms'][room]['label'],notes);q.plan(crop=[b[0]-300,b[1]-300,b[2]+600,b[3]+600]);q.save('13-solar-'+room+'.svg')
 table('家具尺寸.csv',['ID','名称','房间','X','Y','宽','深','Z','高','来源'],[[n,v['label'],v['room'],*v['box'],v['z'],v['height'],v['status']] for n,v in D['furniture'].items()])
 table('床架外伸.csv',['床','床架宽','床架深','床垫宽','床垫深','每侧外伸','头尾各外伸','说明'],[[n,*v['box'][2:],*v['mattress'],(v['box'][2]-v['mattress'][0])/2,(v['box'][3]-v['mattress'][1])/2,'实体与路线按床架外包络核验'] for n,v in D['furniture'].items() if v['kind']=='bed'])
 caps=[a for n,v in D['furniture'].items() for a in capacity(n,v)]
 table('收纳容量.csv',list(caps[0]),[list(a.values()) for a in caps])
 table('尺寸来源.csv',['ID','值','性质','说明'],[[v['id'],str(v['value']),v['status'],v['note']] for v in D['dimensions']]+[[n,str(v['box'])+' 高'+str(v['height']),'概念设计',v['status']] for n,v in D['furniture'].items()]+[[n,str(v['box'])+' 高'+str(v['height']),'概念门窗',v['status']] for n,v in openings().items()])
 table('逐室功能.csv',['空间','功能','原图面积_仅抄录'],[[v['label'],'；'.join(v['functions']),v['source_area_m2']] for v in D['rooms'].values()])
 table('水电点位.csv',['索引','点号','X','Y','Z','专业','关联家具','条件'],[['S%02d'%(i+1),v['id'],v['x'],v['y'],v['z'],v['kind'],v.get('attached_to',''),v['note']] for i,v in enumerate(D['services'])])
 table('路线核验.csv',['路线','状态','宽mm','可达','说明'],[[r['name'],r['state'],r['width_mm'],r['reachable'],r['status']] for r in U['routes']])
 table('设备预留.csv',['设备','空间','X','Y','宽','深','高','操作框','条件'],[[v['label'],v['room'],*v['box'],v['height'],str(D['operations'].get(n+'_use',{}).get('box')),'型号未选；另核接口、散热、脚部、开门、检修、运输'] for n,v in D['furniture'].items() if v['kind']=='appliance' or n in ['tower','hob','sink']])
 table('操作状态.csv',['操作','所有者','范围','实体命中','说明'],[[n,v['owner'],str(v['box']),','.join(U['operation_fixed_hits'][n]),v['kind']] for n,v in D['operations'].items()])
 table('门窗洞口.csv',['ID','类型','参考框','名义宽','扣框净宽假设','高度','来源'],[[n,v['kind'],str(v['box']),v['width'],v['width']-60,v['height'],v['status']] for n,v in openings().items()])
 table('空调新风.csv',['空间','位置','新风讨论值m3h','条件'],[[v['room'],str(v['point']),v['fresh_m3h'],v['condition']] for v in D['hvac']])
 cmp=json.loads((ROOT/'reports/comparison.json').read_text(encoding='utf-8'))['candidates'];table('方案取舍.csv',['候选','固定命中','单人路线通过数','路线总数','挂杆净长mm','拆改排序','条件'],[[c['label'],str(c['fixed_hits']),c['single_routes_passed'],c['route_count'],c['storage_rail_mm'],c['cost_rank'],'；'.join(c['conditions'])] for c in cmp])
 from single_bath import drawings
 drawings(Sheet,table)
 dump('reports/drawing_index.json',INDEX)
 # Retire only generated sheets absent from the current index; R1 remains in Git history.
 for folder,ext in [('svg','.svg'),('png','.png')]:
  keep={Path(n).stem for n,_ in INDEX}
  for p in (ROOT/'drawings'/folder).glob('*'+ext):
   if p.stem not in keep:p.unlink()
 dump('reports/png_state.json',bound({'engine':'Pillow / Microsoft YaHei','font':FONT,'size':[W,H],'assets':{n:{'svg_sha256':hashfile(ROOT/'drawings/svg'/n),'png_sha256':hashfile(ROOT/'drawings/png'/n.replace('.svg','.png'))} for n,_ in INDEX}}))
 figures=''.join(f'<figure id="{n[:-4]}"><figcaption>{html.escape(t)} · <a href="../drawings/svg/{n}">编辑SVG</a> · <a href="../drawings/png/{n[:-4]}.png">PNG</a></figcaption><img loading="lazy" src="../drawings/png/{n[:-4]}.png" alt="{html.escape(t)}"></figure>' for n,t in INDEX)
 links=''.join(f'<li><a href="../tables/{p.name}">{p.name}</a></li>' for p in sorted((ROOT/'tables').glob('*.csv')))
 navigation=''.join(f'<li><a href="#{n[:-4]}">{html.escape(t)}</a></li>' for n,t in INDEX)
 page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>157furnish R2 离线方案册</title><style>body{background:#f5f2e8;color:#273e34;font:17px/1.7 "Microsoft YaHei",sans-serif;margin:0}main{max-width:1400px;margin:auto;padding:30px}header{background:#294a3a;color:#fff;padding:35px}a{color:#366e51}figure{background:white;margin:25px 0;padding:16px}img{width:100%;height:auto}aside{background:#eadfc9;padding:24px;margin:20px 0}details{padding:16px;background:#fff}li{margin:5px} @media print{details{display:none}figure{break-inside:avoid}main{padding:0}} </style><main><header><h1>157furnish · R2</h1><p>三房两卫 · 可关闭厨房 · 无水岛台 · 两处淋浴</p><p>本地可编辑图模交付；没有生成三维效果图。</p></header><aside>全部尺寸为原图标注、推导或显式概念参数。固定实体及500单人基线通过不等于全部使用通过：携篮、900目标、设备开启及多人操作存在限制。请先读核验摘要和现场条件。</aside><p><a href="verification.md">核验摘要</a> · <a href="constraints.md">现场条件</a> · <a href="design.md">设计取舍</a> · <a href="handoff.md">接手重建</a> · <a href="../model/157furnish_R2_gas.blend">Blender</a> · <a href="../model/157furnish_R2_gas.glb">GLB</a> · <a href="../IMG20260921-135355869.jpg">原始户型图</a></p><details><summary>图纸目录</summary><ul>'''+navigation+'</ul></details>'+figures+'<h2>表格</h2><ul>'+links+'</ul><p>R2 / SHA256 '+SHA+'</p></main></html>'
 (ROOT/'docs/方案册.html').write_text(page,encoding='utf-8');print('DRAWINGS',len(INDEX))
if __name__=='__main__':main()
