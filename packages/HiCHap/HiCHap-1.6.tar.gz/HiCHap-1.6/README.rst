HiCHap
******
An integrated package to process diploid Hi-C data

Introduction
============
HiCHap is a Python package designed to process and analyze Hi-C data, primarily the diploid Hi-C data for phased haplotypes. First, the Hi-C reads are split in ligation junction sites, and all split parts are used in mapping to maximumly utilize available SNPs in allele assignment. The noisy reads are next eliminated. Second, except the systematic biases caused by Hi-C experiment, the variable genetic variant density can lead to additional bias in reconstructed diploid (maternal and paternal) Hi-C contact maps because it is potentially easier to assign more allelic contacts in the chromatin regions with denser genetic variants. HiCHap utilizes a novel strategy to correct the systematic biases in diploid Hi-C data. Third, HiCHap identifies compartments, topological domains/boundaries and chromatin loops for constructed diploid Hi-C contact maps, and provides allele-specific testing on these chromatin 3D structures. Finally, HiCHap also supports data processing, bias correction and structural analysis for haploid Hi-C data without separating two homologous chromosomes


Requirements
============
HiCHap is developed and tested on Unix systems. HiCHap utilizes HDF5 and cooler as default data format to keep consistent with 4DN standards. 
To summarize, the following packages are required in installation.


python packages:

1.  Python 2.7+
2.  Multiprocess 
3.  Numpy
4.  Scipy
5.  statsmodels
6.  Scikit-Learn
7.  xml
8.  pysam
9.  ghmm
10. Bio
11. cooler

others:

1.  bowtie2 (version 2.2.9 is tested)
2.  samtools (version 1.5 is tested)


Downloads
=========
- `Source code and manual  here <https://pypi.org/project/HiCHap/#files>`_
- `Code and manual Repository <https://github.com/Prayforhanluo/HiCHap_master>`_ (At GitHub, Track the package issue)

Citation
========
- Luo, H., Li, X., Fu, H. et al. HiCHap: a package to correct and analyze the diploid Hi-C data. BMC Genomics 21, 746 (2020). https://doi.org/10.1186/s12864-020-07165-x