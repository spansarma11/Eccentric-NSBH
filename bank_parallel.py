import numpy as np
import os
import glob
from glue.pipeline import CondorDAGJob, CondorDAGNode, CondorDAG, CondorJob
from Optimised_parallelisation import namelist1e3, namelist5e5, namelist1e6, namelist1p25e6, namelist1p5e6, namelistrest
 
# BASEDIR
RUNDIR = os.getcwd()+'/'

# PSD and population model paths
psd = "/home/spandan.sarma/work_ecc/bank_generation/aligo_O4high.txt"
bank_config = f"{RUNDIR}bank.ini"

#outmax = 600
outheader = "10_300"
outputbank = f"{RUNDIR}outbank/"
out_files = f"{RUNDIR}out_files/"
log_files = f"{RUNDIR}log_files/"
err_files = f"{RUNDIR}err_files/"



os.mkdir(outputbank)
os.mkdir(log_files)
os.mkdir(out_files)
os.mkdir(err_files)


arglist = ['--output-file',
           '--minimal-match',
           '--tolerance',
           '--buffer-length',
           '--full-resolution-buffer-length',
           '--sample-rate',
           '--tau0-threshold',
           '--approximant',
           '--tau0-crawl',
           '--psd-file',
           '--seed',
           '--tau0-start',
           '--tau0-end',
           '--input-config',
           '--low-frequency-cutoff',
           '--max-signal-length',
           '--nprocesses'
          ]

out = '$(out)'
mm = 0.85
tolerance = 0.05
bufferlen = 4
fullresbuff = 1024
samplerate = 2048
tau0_threshold = 0.5
approx = "'teobresums'"
tau0_crawl = 5
maxsignal = 512
tau0startval = '$(tau0startval)'
tau0endval = '$(tau0endval)'
psd_file = psd
seed = 150914
input_config = bank_config
f_low = 20
nproc = 10


argvars = [out,
          mm,
          tolerance,
          bufferlen,
          fullresbuff,
          samplerate,
          tau0_threshold,
          approx,
          tau0_crawl,
          psd_file,
          seed,
          tau0startval,
          tau0endval,
          input_config,
          f_low,
          maxsignal,
          nproc
          ]
#f_low,

# Define the Condor job
djob = CondorDAGJob('vanilla', '/home/spandan.sarma/anaconda3/envs/pycbc_teobfd_new/bin/pycbc_brute_bank')
djob.add_condor_cmd('getenv', 'True')
djob.add_condor_cmd('should_transfer_files', 'YES')
djob.add_condor_cmd('when_to_transfer_output', 'ON_EXIT')
#djob.add_condor_cmd('request_memory','10G')
#djob.add_condor_cmd('request_disk','10G')
djob.add_condor_cmd('request_cpus','10')
djob.add_condor_cmd('accounting_group', 'ligo.prod.o3.cbc.bbh.pycbcoffline')
djob.set_sub_file(f'{RUNDIR}bank_{outheader}.sub')

d = CondorDAG(f'{RUNDIR}bank_toplog_{outheader}')
d.set_dag_file(f'{RUNDIR}bank_dag_{outheader}')

#djob.set_log_file('bank_log_'+outheader+'.$(Cluster).$(Process).log')
#djob.set_stderr_file('bank_error_'+outheader+'.$(Cluster).$(Process).err')
#djob.set_stdout_file('bank_out_'+outheader+'.$(Cluster).$(Process).out')

# Add arguments to the Condor job
for al, av in zip(arglist, argvars):
    djob.add_arg(f'{al} {av}')

djob.add_arg('--verbose')

# Function to write a CondorDAGNode with specific tau0 start and end values
def write_node(index, outputdir, logdir, errdir, outdir, tau0start, tau0end, storage):
#def write_node(index, outputdir, tau0start, tau0end):
    node = djob.create_node()
    outf = f"{outputdir}TEROBResumS_{mm}-{tau0start}-{tau0end}-$(Cluster).hdf"
    logdirf = f"{logdir}bank_log_{mm}-{tau0start}-{tau0end}-$(Cluster).$(Process).log"
    outdirf = f"{outdir}bank_out_{mm}-{tau0start}-{tau0end}-$(Cluster).$(Process).out"
    errdirf = f"{errdir}bank_error_{mm}-{tau0start}-{tau0end}-$(Cluster).$(Process).err"
    
    node.add_macro('out', outf)
    node.add_macro('tau0startval', tau0start)
    node.add_macro('tau0endval', tau0end)
    node.add_macro('logdirdag', logdirf)
    node.add_macro('errdirdag', errdirf)
    node.add_macro('outdirdag', outdirf)
    node.add_macro('diskspace', storage)
    node.add_macro('memspace', storage)
    d.add_node(node)
    
    djob.set_log_file('$(logdirdag)')
    djob.set_stderr_file('$(errdirdag)')
    djob.set_stdout_file('$(outdirdag)')
    djob.add_condor_cmd('request_memory','$(diskspace)')
    djob.add_condor_cmd('request_disk','$(memspace)')

#    djob.set_log_file(log_files+'bank_log'+'.$(Cluster).$(Process).log')
#    djob.set_stderr_file(err_files+'bank_error'+'.$(Cluster).$(Process).err')
#    djob.set_stdout_file(out_files+'bank_out'+'.$(Cluster).$(Process).out')

# # Loop to create and add nodes to the DAG
for i in namelist1e3[::2]:
    step = 1.0
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '5G')

for i in namelist5e5:
    step = 0.5
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '25G')

for i in namelist1e6:
    step = 0.2
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '50G')

for i in namelist1p25e6:
    step = 0.1
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '75G')

for i in namelist1p5e6:
    step = 0.1
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '100G')

for i in namelistrest:
    step = 0.1
    start = round(i + step*0, 1)
    end = round(i + step*1, 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '150G')
    
for i in np.arange(546, 600):
    step = 0.5
    start = step * i
    end = step * (i + 1)
    write_node(i, outputbank, log_files, err_files, out_files, start, end, '15G')
 

# Write the Condor submission files and the DAG itself
d.write_sub_files()
d.write_dag()
