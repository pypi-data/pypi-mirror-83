
import logging
log = logging.getLogger(__name__)

from scipy.sparse import csr_matrix

from .matrixFile import MatrixFile


class Hicpro(MatrixFile, object):

    def __init__(self, pMatrixFile, pBedFile):
        super().__init__(pMatrixFileName=pMatrixFile, pBedFile=pBedFile)

    def load(self):
        instances = []
        features = []
        data = []
        with open(self.matrixFileName, 'r') as matrix_file:
            for line in matrix_file:
                x, y, value = line.strip().split('\t')
                instances.append(int(x) - 1)
                features.append(int(y) - 1)
                data.append(float(value))
        cut_intervals = []
        with open(self.bedFile, 'r') as bed_file:
            for line in bed_file:
                chrom, start, end, value = line.strip().split('\t')
                cut_intervals.append((chrom, int(start), int(end), int(value)))

        shape = len(cut_intervals)

        matrix = csr_matrix((data, (instances, features)), shape=(shape, shape))

        nan_bins = None
        distance_counts = None
        correction_factors = None
        return matrix, cut_intervals, nan_bins, distance_counts, correction_factors
