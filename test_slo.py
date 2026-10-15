import copy
import unittest
from slo import report
class Tests(unittest.TestCase):
    def config(self): return {'availability_target':.9,'latency_threshold_ms':100,'observations':[{'request_id':str(i),'status':500 if i==0 else 200,'latency_ms':i*20} for i in range(10)]}
    def test_boundary_budget(self):
        r=report(self.config());self.assertTrue(r['availability_met']);self.assertEqual(r['error_budget_remaining_requests'],0)
    def test_percentile_nearest_rank(self):
        r=report(self.config());self.assertEqual(r['p50_latency_ms'],80);self.assertEqual(r['p95_latency_ms'],180)
    def test_4xx_is_not_server_failure(self):
        c=self.config();c['observations'][0]['status']=404;self.assertEqual(report(c)['failed_requests'],0)
    def test_duplicate_request(self):
        c=self.config();c['observations'][1]['request_id']='0'
        with self.assertRaises(ValueError): report(c)
    def test_empty_window(self):
        c=self.config();c['observations']=[]
        with self.assertRaises(ValueError): report(c)
    def test_nonfinite_latency(self):
        c=self.config();c['observations'][0]['latency_ms']=float('nan')
        with self.assertRaises(ValueError): report(c)
    def test_invalid_target(self):
        c=self.config();c['availability_target']=1
        with self.assertRaises(ValueError): report(c)
    def test_no_mutation(self):
        c=self.config();b=copy.deepcopy(c);report(c);self.assertEqual(c,b)
if __name__=='__main__': unittest.main()
