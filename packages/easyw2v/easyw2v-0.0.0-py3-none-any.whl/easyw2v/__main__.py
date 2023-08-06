from gensim.models import Word2Vec
from pathlib import Path
import numpy as np
import pyper
import xarray as xr
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--corpus', help='Path to a corpus, from which you want to derive semantic vectors.')

args = parser.parse_args()

if __name__ == '__main__':
    inpath = args.corpus
    with open(inpath, 'r') as f:
        corpus = f.readlines()
    corpus = [ i.strip().split(' ') for i in corpus ]
    corpus = [ i for i in corpus if i != '' ]
    model = Word2Vec(corpus, min_count=5, workers=32, size=100)

    inpath = Path(inpath)
    #model_path = str(inpath.parent) + '/' + inpath.stem + '.model'
    #model.save(model_path)

    words = { i: model.wv[i] for i in model.wv.vocab.keys() }
    weights = np.vstack([ i for i in words.values() ])
    rows = list(words.keys())
    cols = [ 's' + str(i) for i in range(weights.shape[1]) ]
    #weights = xr.DataArray(weights, coords=[rows, cols], dims=["word", "semantics"])
    #weight_path = str(inpath.parent) + '/' + inpath.stem + '.nc'
    #weights.to_netcdf(weight_path)

    weight_path = str(inpath.parent) + '/' + inpath.stem + '.Rdata'

    r = pyper.R()
    r.assign('weights', weights)
    r.assign('rows', np.array(rows))
    r.assign('cols', np.array(cols))
    r('rownames(weights) = rows')
    r('colnames(weights) = cols')
    r.assign('opath', weight_path)
    r('save(list=c("weights"), file=opath)')


