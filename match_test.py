import numpy as np
import warnings
warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")
import lal as _lal
import pycbc.waveform
from pycbc.waveform import get_td_waveform, get_fd_waveform
import pycbc.psd
from pycbc.psd import from_numpy_arrays
from pycbc.filter.matchedfilter import match
import os
import h5py
import logging
import pickle
import concurrent.futures
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Opt:
    psd_model = None
    psd_file = "aligo_O4high_psd.txt"
    asd_file = None
    psd_estimation = None
    psd_extra_args = {}
    psd_file_xml_ifo_string = None
    psd_file_xml_root_name = 'psd'
    psd_inverse_length = None
    invpsd_trunc_method = None
    psd_output = None    
    psdvar_segment = None
    psdvar_short_segment = None
    psdvar_long_segment = None
    psdvar_psd_duration = None
    psdvar_psd_stride = None
    psdvar_low_freq = None
    psdvar_high_freq = None
    psd_segment_length = None
    psd_segment_stride = None
    psd_num_segments = None

opt = Opt()

low_frequency_cutoff = 12.0
delta_f = 1/1024.
tlen = int(1024. * 9990.756)
flen = tlen // 2 + 1

psd = pycbc.psd.from_cli(opt, flen, delta_f, low_frequency_cutoff)
print("psd done")

injection_file = {}
with h5py.File('/home/spandan.sarma/work_ecc/fitting_factor_tests/manual_ff_tests_11/new_injections_100.hdf', 'r') as injection_file_hdf:
    injection_file['mass1'] = injection_file_hdf['mass1'][:]
    injection_file['mass2'] = injection_file_hdf['mass2'][:]
    injection_file['spin1z'] = injection_file_hdf['spin1z'][:]
    injection_file['spin2z'] = injection_file_hdf['spin2z'][:]
    injection_file['eccentricity'] = injection_file_hdf['eccentricity'][:]
    injection_file['inj_id'] = injection_file_hdf['inj_id'][:]

inj_indices = np.arange(0, 10)

#The part above loads the injections I want to find the match of.
#Below I am loading the waveforms from a pickle file. These are the waveforms from the bank that I had generated and loaded onto a pickle file.
#The process of generating a waveform and loading them into a pickle file was a much faster process than doing it all in one python file.
print("Injection done")
def match_find(bank_file_gen, injection_hp_index, psd):
    start_time = time.time()
    match_values = {}
    print(f"For {bank_file_gen.split('/')[-1]}, running in PID {os.getpid()}")
    for inj_id in injection_hp_index:
        injection_hp, _ = get_fd_waveform(approximant="teobresums", mass1=injection_file['mass1'][inj_id], mass2=injection_file['mass2'][inj_id], lambda1=0.,lambda2=0., spin1z=injection_file['spin1z'][inj_id], spin2z=injection_file['spin2z'][inj_id], eccentricity = injection_file['eccentricity'][inj_id], f_lower=12., delta_f=1/1024.)
        print(f"For {bank_file_gen.split('/')[-1]}, inj_id {inj_id}, running in PID {os.getpid()}")
        with open(bank_file_gen, 'rb') as bank_file_load:
            i=0
            for _ in np.arange(int(bank_file_gen.split('/')[-1].split('_')[2]), int(bank_file_gen.split('/')[-1].split('_')[-1][:-4])):
                start_time_int = time.time()
                obj = pickle.load(bank_file_load)
                print(list(obj.items())[0][0])
                bank_hp = obj[list(obj.items())[0][0]]
                id_resize = np.argmin(np.array([len(injection_hp), len(bank_hp), len(psd)]))
                if id_resize == 0:
                    bank_hp_copy = bank_hp.copy()
                    bank_hp_copy.resize(len(injection_hp))
                    psd_copy = psd.copy()
                    psd_copy.resize(len(injection_hp))
                    injection_hp_copy = injection_hp.copy()

                elif id_resize == 1:
                    injection_hp_copy = injection_hp.copy()
                    injection_hp_copy.resize(len(bank_hp))
                    psd_copy = psd.copy()
                    psd_copy.resize(len(bank_hp))
                    bank_hp_copy = bank_hp.copy()

                elif id_resize == 2:
                    injection_hp_copy = injection_hp.copy()
                    injection_hp_copy.resize(len(psd))
                    bank_hp_copy = obj[list(obj.items())[0][0]].copy()
                    bank_hp_copy.resize(len(psd))
                    psd_copy = psd.copy()

                #Calculating the match part
                match_values[f"bank_{list(obj.items())[0][0][15:]}_inj_{inj_id}"] = match(injection_hp_copy, bank_hp_copy, psd=psd_copy, low_frequency_cutoff=12., high_frequency_cutoff=None)[0]
                i+=1
                print("time for one loop inj_id {inj_id}, running in PID {os.getpid()}, {time.time() - start_time_int}")

        print(time.time()-start_time)
        print(f"number={i}")
    return [match_values, f"bank_{bank_file_gen.split('/')[-1].split('_')[2]}_{bank_file_gen.split('/')[-1].split('_')[-1][:-4]}_inj_0_10"]

num_processes = 5
#pkl_list = ['bank_files/generated_bank_1017750_1018000.pkl', 'bank_files/generated_bank_104500_104750.pkl', 'bank_files/generated_bank_116250_116500.pkl', 'bank_files/generated_bank_122250_122500.pkl', 'bank_files/generated_bank_123750_124000.pkl']
#pkl_list = np.loadtxt(open("/home/spandan.sarma/work_ecc/wave_match_calc/set_1/bank_list.txt", 'rt').readlines(), dtype=str)[0:5]
pkl_list = ['/home/spandan.sarma/work_ecc/wave_gen_match_bank/bank_files/generated_bank_97250_97500.pkl', '/home/spandan.sarma/work_ecc/wave_gen_match_bank/bank_files/generated_bank_215250_215500.pkl', '/home/spandan.sarma/work_ecc/wave_gen_match_bank/bank_files/generated_bank_206750_207000.pkl', '/home/spandan.sarma/work_ecc/wave_gen_match_bank/bank_files/generated_bank_200500_200750.pkl', '/home/spandan.sarma/work_ecc/wave_gen_match_bank/bank_files/generated_bank_190500_190750.pkl']

with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
    futures = [executor.submit(match_find, f"{pkl_file}", inj_indices, psd) for pkl_file in pkl_list]

with open(f"/home/spandan.sarma/work_ecc/wave_match_calc/set_1/match_values/match_values_{pkl_list[0].split('/')[-1].split('_')[2]}_{pkl_list[-1].split('/')[-1].split('_')[-1][:-4]}_inj_0_10.pkl", 'wb') as match_file:
    for future in concurrent.futures.as_completed(futures):
        pickle.dump({f"waveform_store_{future.result()[1]}": future.result()[0]}, match_file)
