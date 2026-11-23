"""Information budget: bits needed to name an n-state 2-symbol TM (modulo state relabeling,
start state fixed) versus bits needed to name the K215 source DAG."""
import math
def tm_bits(n):
    return 2*n*math.log2(4*(n+1)) - math.lgamma(n)/math.log(2)
def dag_bits(internal, leaf_kinds):
    return 2*internal*math.log2(internal+leaf_kinds) - math.lgamma(internal+1)/math.log(2)
if __name__ == '__main__':
    for n in (50, 80, 100, 131, 150, 215):
        print(f'{n:4d}-state TM: ~{tm_bits(n):5.0f} bits')
    print(f'K215 source DAG (179 internal, 23 leaf kinds): ~{dag_bits(179, 23):.0f} bits')
