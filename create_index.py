import sys

from utils import create_index
from configs import pc

if __name__ == '__main__':
    index_name = sys.argv[1]
    create_index(index_name, pc)
