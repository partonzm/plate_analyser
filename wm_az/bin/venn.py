
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from matplotlib_venn import venn3, venn3_circles

## Creates venn2 based on wtv by combining plate and well and overlapping
def vn2(a, b):
    a0 = pd.read_csv(a)
    b0 = pd.read_csv(a)

    plate_well_a = set(a['plt_nm'].map(str) + '_' + a['well'])
    plate_well_b = set(b['plt_nm'].map(str) + '_' + b['well'])

    venn2(subsets= (plate_well_a, plate_well_b))

    plt.savefig('')

## Creates venn2 based on wtv by combining plate and well and overlapping
def vn3(a, b, c):
    a0 = pd.read_csv(a)
    b0 = pd.read_csv(a)
    c0 = pd.read_csv(c)

    plate_well_a = set(a['plt_nm'].map(str) + '_' + a['well'])
    plate_well_b = set(b['plt_nm'].map(str) + '_' + b['well'])
    plate_well_ = set(a['plt_nm'].map(str) + '_' + a['well'])

    venn3(subsets= (plate_well_a, plate_well_b, plate_well_c))

    plt.savefig('')
