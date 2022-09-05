import os


def get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__), path))


CORE_DICT_PATH = get_module_path('core_dict.txt')
REGEX_DICT_PATH = get_module_path('regex_dict.txt')
STOP_WORDS_PATH = get_module_path('stop_words.txt')

CRF_CUT_MODEL_PATH = get_module_path('98_and_netease.seg.crf.json')
CRF_POS_MODEL_PATH = get_module_path('1998.pos.crf.json')

HMM_CUT_MODEL_PATH = get_module_path('hmm_seg_1998')
HMM_POS_MODEL_PATH = get_module_path('hmm_pos_1998')
HMM_POS_ENHANCE_MODEL_PATH = get_module_path('hmm_pos_enhance_1998')

DL_CUT_MODEL_PATH = get_module_path('pd1998_msra_seg_bilstmcrf')
DL_POS_MODEL_PATH = get_module_path('lac_pos_bilstmcrf')
