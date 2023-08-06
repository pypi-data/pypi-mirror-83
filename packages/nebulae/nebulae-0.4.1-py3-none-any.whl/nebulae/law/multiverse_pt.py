#!/usr/bin/env python
'''
engine_mx
Created by Seria at 12/02/2019 3:45 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
import torch
import os
import multiprocessing as mp
from apex import parallel



class Multiverse(object):
    '''
    Args:
    nworld: world size
    '''
    def __init__(self, universe, nworld=1):
        self.universe = universe
        self.nworld = nworld
        self.rank = -1
        self.env = os.environ.copy()
        self.env["MASTER_ADDR"] = '127.0.0.1'
        self.env["MASTER_PORT"] = '29500'
        self.env["WORLD_SIZE"] = str(nworld)
        self.env["OMP_NUM_THREADS"] = '1'

    def __call__(self):
        mp.set_start_method('spawn')
        ps = []
        for r in range(self.nworld):
            self.rank = r
            self.env['RANK'] = str(r)
            self.env['LOCAL_RANK'] = str(r)
            p = mp.Process(target=self.universe, args=(self,))
            p.start()
            ps.append(p)
        for p in ps:
            p.join()

    def init(self):
        for k, v in self.env.items():
            os.environ[k] = v
        torch.backends.cudnn.benchmark = True
        torch.distributed.init_process_group(backend='nccl', init_method='env://')

    def collect(self, model):
        model = parallel.convert_syncbn_model(model)
        model = model.to(torch.device('cuda:%d'%self.rank))
        model = parallel.DistributedDataParallel(model, delay_allreduce=True)
        return model

    def reduce(self, tensor):
        rt = tensor.clone()
        torch.distributed.all_reduce(rt, op=torch.distributed.ReduceOp.SUM)
        rt /= self.nworld
        return rt