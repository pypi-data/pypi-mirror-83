import openjij as oj
import cxxjij as cj
import numpy as np

import unittest


class TestSamplers(unittest.TestCase):
    def setUp(self):
        self.num_ind = {
            'h': {0: -1, 1: -1, 2: 1, 3: 1},
            'J': {(0, 1): -1, (3, 4): -1}
        }
        str_ind = ['a', 'b', 'c', 'd', 'e']
        self.str_ising = {
            'h': {str_ind[i] for i in self.num_ind['h'].keys()},
            'J': {(str_ind[i], str_ind[j]) for i, j in self.num_ind['J'].keys()}
        }
        self.ground_state = [1, 1, -1, -1, -1]
        self.e_g = -1-1-1-1 + (-1-1)
        self.g_sample = {i: self.ground_state[i]
                         for i in range(len(self.ground_state))}
        self.g_samp_str = {k: self.ground_state[i]
                           for i, k in enumerate(str_ind)}

        self.qubo = {
            (0, 0): -1, (1, 1): -1, (2, 2): 1, (3, 3): 1, (4, 4): 1,
            (0, 1): -1, (3, 4): 1
        }
        self.str_qubo = {(str_ind[i], str_ind[j]): qij
                         for (i, j), qij in self.qubo.items()}
        self.ground_q = [1, 1, 0, 0, 0]
        self.e_q = -1-1-1

        # for antiferromagnetic one-dimensional Ising model
        N = 30
        self.afih = {0: -10}
        self.afiJ = {(i, i+1): 1 for i in range(N-1)}
        self.afiground = {i:(-1)**i for i in range(N)}

    def samplers(self, sampler, init_state=None, init_q_state=None, schedule=None):
        res = sampler.sample_ising(
            self.num_ind['h'], self.num_ind['J'], schedule=schedule,
            initial_state=init_state, seed=1)
        self._test_response(res, self.e_g, self.ground_state)
        res = sampler.sample_qubo(self.qubo,
                                  initial_state=init_q_state, schedule=schedule, seed=2)
        self._test_response(res, self.e_q, self.ground_q)

    def _test_response(self, res, e_g, s_g):
        # test openjij response interface
        self.assertEqual(len(res.states), 1)
        self.assertListEqual(s_g, list(res.states[0]))
        self.assertEqual(res.energies[0], e_g)
        # test dimod interface
        self.assertEqual(len(res.record.sample), 1)
        self.assertListEqual(s_g, list(res.record.sample[0]))
        self.assertEqual(res.record.energy[0], e_g)

    def _test_response_num(self, res, num_reads):
        # test openjij response interface
        self.assertEqual(len(res.states), num_reads)
        self.assertEqual(len(res.energies), num_reads)
        # test dimod interface
        self.assertEqual(len(res.record.sample), num_reads)
        self.assertEqual(len(res.record.energy), num_reads)

    def _test_num_reads(self, sampler_cls):
        num_reads = 10
        sampler = sampler_cls()
        res = sampler.sample_ising(
            self.num_ind['h'], self.num_ind['J'],
            num_reads=num_reads,
            seed=2
        )
        self._test_response_num(res, num_reads)

        sampler = sampler_cls(num_reads=num_reads)
        res = sampler.sample_ising(
            self.num_ind['h'], self.num_ind['J'],
        )
        self._test_response_num(res, num_reads)


    def test_sa(self):
        sampler = oj.SASampler()
        self.samplers(sampler)
        self.samplers(sampler, 
            init_state=[1 for _ in range(len(self.ground_state))],
            init_q_state=[1 for _ in range(len(self.ground_state))])
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))}
            )

        # schedule [[beta, one_mc_steps], ...]
        # schedule test (list of list)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[[0.1, 10], [1, 10], [10, 10]]
            )

        # schedule test (list of tuple)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[(0.1, 10), (1, 10), (10, 10)]
            )

        self._test_num_reads(oj.SASampler)

        #antiferromagnetic one-dimensional Ising model
        sampler = oj.SASampler(num_reads=100)
        res = sampler.sample_ising(self.afih, self.afiJ, seed=1)
        self.assertDictEqual(self.afiground, res.first.sample)
        #antiferromagnetic one-dimensional Ising model
        sampler = oj.SASampler(num_reads=100)
        res = sampler.sample_ising(self.afih, self.afiJ, updater='swendsen wang', seed=1)
        self.assertDictEqual(self.afiground, res.first.sample)

    def test_sa_sparse(self):
        #sampler = oj.SASampler()
        #self.samplers(sampler)
        #self.samplers(sampler, 
        #    init_state=[1 for _ in range(len(self.ground_state))],
        #    init_q_state=[1 for _ in range(len(self.ground_state))])
        #self.samplers(sampler, 
        #    init_state={i: 1 for i in range(len(self.ground_state))}
        #    )

        ## schedule [[beta, one_mc_steps], ...]
        ## schedule test (list of list)
        #self.samplers(sampler, 
        #    init_state={i: 1 for i in range(len(self.ground_state))},
        #    schedule=[[0.1, 10], [1, 10], [10, 10]]
        #    )

        ## schedule test (list of tuple)
        #self.samplers(sampler, 
        #    init_state={i: 1 for i in range(len(self.ground_state))},
        #    schedule=[(0.1, 10), (1, 10), (10, 10)]
        #    )

        #self._test_num_reads(oj.SASampler)

        #antiferromagnetic one-dimensional Ising model
        sampler = oj.SASampler(num_reads=100)
        res = sampler.sample_ising(self.afih, self.afiJ, sparse=True, seed=1)
        self.assertDictEqual(self.afiground, res.first.sample)

    def test_sqa(self):
        sampler = oj.SQASampler()
        
        self.samplers(sampler)
        self.samplers(sampler, 
            init_state=[1 for _ in range(len(self.ground_state))],
            init_q_state=[1 for _ in range(len(self.ground_state))])
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))}
            )

        # schedule [[s, one_mc_steps], ...]
        # schedule test (list of list, temperature fixed)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[[0.1, 10], [0.5, 10], [0.9, 10]]
            )

        # schedule test (list of tuple, temperature fixed)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[(0.1, 10), (0.5, 10), (0.9, 10)]
            )

        # schedule [[s, beta, one_mc_steps], ...]
        # schedule test (list of list, temperature non-fixed)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[[0.1, 0.1, 10], [0.5, 1, 10], [0.9, 10, 10]]
            )

        # schedule test (list of tuple, temperature non-fixed)
        self.samplers(sampler, 
            init_state={i: 1 for i in range(len(self.ground_state))},
            schedule=[(0.1, 0.1, 10), (0.5, 1, 10), (0.9, 10, 10)]
            )

        self._test_num_reads(oj.SQASampler)

        #antiferromagnetic one-dimensional Ising model
        sampler = oj.SQASampler(num_reads=100)
        res = sampler.sample_ising(self.afih, self.afiJ, seed=1)
        self.assertDictEqual(self.afiground, res.first.sample)

    def test_csqa(self):
        #FIXME: This test is instable. Make sure if there is no bug in ContinuousIsing solver.
        #FIXME: Or is there some intristic reasons for this instability?
        #sampler = oj.CSQASampler(gamma=5, num_sweeps=500)
        #self.samplers(sampler,
        #        init_state=[1 for _ in range(len(self.ground_state))],
        #        init_q_state=[1 for _ in range(len(self.ground_state))])

        #antiferromagnetic one-dimensional Ising model
        sampler = oj.CSQASampler(num_reads=200)
        res = sampler.sample_ising(self.afih, self.afiJ, seed=1)
        self.assertDictEqual(self.afiground, res.first.sample)


if __name__ == '__main__':
    unittest.main()
