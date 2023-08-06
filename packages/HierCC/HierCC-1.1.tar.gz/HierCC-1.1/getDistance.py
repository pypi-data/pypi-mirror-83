import numpy as np, numba as nb
from multiprocessing import shared_memory

class getDistance(object) :
    def __init__(self, data, func_name, pool, start=0):
        func = eval(func_name)
        self.mat_buf = shared_memory.SharedMemory(create=True, size=data.nbytes)
        mat = np.ndarray(data.shape, dtype=data.dtype, buffer=self.mat_buf.buf)
        mat[:] = data[:]
        self.dist_buf = shared_memory.SharedMemory(create=True, size=int((mat.shape[0] - start) * mat.shape[0] * 4))
        self.dist = np.ndarray([mat.shape[0] - start, mat.shape[0]], dtype=np.int32, buffer=self.dist_buf.buf)
        self.dist[:] = 0
        parallel_dist(self.mat_buf, func, self.dist_buf, mat.shape, pool, start)
        self.mat_buf.close()
        self.mat_buf.unlink()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dist_buf.close()
        self.dist_buf.unlink()
        return


def parallel_dist(mat_buf, func, dist_buf, mat_shape, pool, start=0) :
    n_pool = len(pool._pool)
    tot_cmp = (mat_shape[0] * mat_shape[0] - start * start)/n_pool
    s, indices = start, []
    for _ in np.arange(n_pool) :
        e = np.sqrt(s*s+tot_cmp)
        indices.append([s, e])
        s = e
    indices = (np.array(indices)+0.5).astype(int)
    for _ in pool.imap_unordered(dist_wrapper, [[func, mat_buf.name, dist_buf.name, mat_shape, s, e, start] for s, e in indices ]) :
        pass

def dist_wrapper(data) :
    func, mat_buf_id, dist_buf_id, mat_shape, s, e, start = data
    mat_buf = shared_memory.SharedMemory(name=mat_buf_id, create=False)
    dist_buf = shared_memory.SharedMemory(name=dist_buf_id, create=False)
    mat = np.ndarray(mat_shape, dtype=int, buffer=mat_buf.buf)
    dist = np.ndarray([mat_shape[0]-start, mat_shape[0]], dtype=np.int32, buffer=dist_buf.buf)
    func(mat[:, 1:], s, e, dist, start)
    mat_buf.close()
    dist_buf.close()

@nb.jit(nopython=True)
def syn_dist(mat, s, e, dist, start=0):
    n_loci = mat.shape[1]
    for i in range(s, e+1) :
        ql = np.sum(mat[i] > 0)
        for j in range(i) :
            rl, ad, al = 0., 0., 0.
            for k in range(n_loci) :
                if mat[j, k] > 0 :
                    rl += 1
                    if mat[i, k] > 0 :
                        al += 1
                        if mat[i, k] != mat[j, k] :
                            ad += 1
            ll = max(ql, rl) - 0.03 * n_loci
            if ll > al :
                ad += ll - al
                al = ll
            if al > 0 :
                dist[i-start, j] = int(ad/al * n_loci + 0.5)
            else :
                dist[i-start, j] = int(n_loci)

@nb.jit(nopython=True)
def asyn_dist(mat, s, e, dist, start=0):
    n_loci = mat.shape[1]
    for i in range(s, e+1) :
        ql = np.sum(mat[i] > 0)
        for j in range(i) :
            rl, ad, al = 0., 0., 0.
            for k in range(n_loci) :
                if mat[j, k] > 0 :
                    if mat[i, k] > 0 :
                        al += 1
                        if mat[i, k] != mat[j, k] :
                            ad += 1
            ll = ql - 0.03 * n_loci
            if ll > al :
                ad += ll - al
                al = ll
            if al > 0 :
                dist[i-start, j] = int(ad/al * n_loci + 0.5)
            else :
                dist[i-start, j] = int(n_loci)

@nb.jit(nopython=True)
def p_dist(mat, s, e, dist, start=0):
    n_loci = mat.shape[1]
    for i in range(s, e+1) :
        for j in range(i) :
            ad, al = 0., 0.
            for k in range(n_loci) :
                if mat[j, k] > 0 :
                    if mat[i, k] > 0 :
                        al += 1
                        if mat[i, k] != mat[j, k] :
                            ad += 1
            dist[i-start, j] = int( -np.log(1.-(ad+0.5)/(al+1.0)) * n_loci * 100. + 0.5)
