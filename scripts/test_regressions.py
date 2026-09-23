"""Safety-critical geometry regressions, no rendering or external inputs."""
import copy,unittest
import numpy as np
from common import *
from verify_usage import find_path,route_grid

class Regressions(unittest.TestCase):
 def test_single_candidate_isolated_and_repartitioned(self):
  before=copy.deepcopy(D);c=next(v for v in D['candidates'] if v['id']=='single_bath_utility');data=candidate_data(c)
  self.assertEqual(D,before)
  self.assertNotIn('bath_AB',{e['id'] for e in data['edges']})
  self.assertNotIn('store_w',{e['id'] for e in data['edges']})
  self.assertNotIn('bathB_entry',openings(data));self.assertNotIn('store_entry',openings(data))
  self.assertEqual(sum(v['kind']=='wc' for v in data['furniture'].values()),1)
  self.assertEqual(data['furniture']['laundry']['room'],'utility')
  self.assertEqual(data['operations']['laundry_use']['parts'],c['changes']['operations']['laundry_use']['parts'])
  self.assertNotIn('主卫',data['routes'])
  self.assertEqual(data['rooms']['utility']['boxes'][0][2]+120+data['rooms']['wet']['boxes'][0][2],c['study']['envelope'][2])
  self.assertEqual(data['rooms']['wash']['boxes'][0][3]+120+data['rooms']['wet']['boxes'][0][3],c['study']['envelope'][3])
 def test_toilet_old_fronts_are_rejected(self):
  for n,old in [('wcB',370),('wcA',180)]:
   v=D['original']['furniture'][n];glass=D['original']['furniture']['glass'+n[-1]]
   self.assertEqual(v['box'][1]-glass['box'][1]-glass['box'][3],old)
   self.assertLess(old,600)
   self.assertEqual(D['furniture'][n]['front'],'west')
   self.assertGreaterEqual(D['operations'][n+'_use']['box'][2],750)
 def test_sliding_intermediate_outside_is_detectable(self):
  o=copy.deepcopy(openings()['kitchen_balcony']);o['slide_shift']=5000
  b=slide_box(o,1)
  self.assertTrue(any(not inside(x,y) for x,y in rect(b)))
  self.assertNotEqual(slide_box(o,.5),slide_box(o,False))
 def test_luggage_old_obstruction_removed(self):
  old=D['original']['furniture'];self.assertEqual(old['bedC']['box'][0]-(old['luggage']['box'][0]+old['luggage']['box'][2]),70)
  self.assertNotIn('luggage',D['furniture'])
  self.assertFalse(overlap(D['states']['luggage_open']['luggage'],D['operations']['bedC_west']['box']))
 def test_growth_target_moves_with_bed_and_desk(self):
  c=candidate_data(next(c for c in D['candidates'] if c['id']=='A_growth'))
  b=c['furniture']['bedA']['box'];r=next(v for v in c['routes'].values() if v.get('target_box')==[2700,5500,550,900])
  self.assertGreaterEqual(r['target_box'][0],b[0]+b[2]);self.assertEqual(c['furniture']['bedA']['mattress'][0],1500)
  self.assertNotEqual(c['furniture']['deskA']['box'],D['furniture']['deskA']['box'])
 def test_target_region_survives_obsolete_point(self):
  g=np.ones((20,20),dtype=bool);g[10,10]=False
  path,_=find_path(g,50,[100,100],[500,500],[400,400,300,300],100)
  self.assertTrue(path)
 def test_laundry_panel_not_its_own_operator(self):
  op=D['operations']['laundry_use'];self.assertFalse(overlap(op['parts']['moving'],op['parts']['operator']))
  _,_,obs=route_grid(D,500,'laundry_open');self.assertEqual(obs['laundry_moving'],op['parts']['moving']);self.assertNotIn('laundry_operation',obs)
 def test_dependency_staleness_rejected(self):
  snap={'layout_sha256':SHA,'dependencies':model_dependencies()};assert_projection_current(snap)
  snap['dependencies']['common.py']='old'
  with self.assertRaises(AssertionError):assert_projection_current(snap)
 def test_balcony_uses_inner_walls(self):
  self.assertEqual(D['balcony']['net_box'][3],9974-100-(8671+60))
  self.assertEqual(D['balcony']['net_box'][3]-600,543)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressions))
 dump('reports/regressions.json',bound({'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':[str(x) for x in result.failures+result.errors]}))
 raise SystemExit(0 if result.wasSuccessful() else 1)
