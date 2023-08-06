from typing import Dict


def same_value(src, tgt):
    if type(src) is bool or type(tgt) is bool:
        return str(src).lower() == str(tgt).lower()
    if type(src) is dict and type(tgt) is dict:
        for key in list(src.keys()):
            if key in tgt:
                return same_value(src[key], tgt[key])
            else:
                print(f'Key "{key}" not found in tgt! Flag specs as different.')
                return False
    return src == tgt


def same_as_target(src_dict: Dict, tgt_dict: Dict):
    diff = 0
    if not src_dict or not tgt_dict:
        diff += 1
    for key in list(src_dict.keys()):
        if key in tgt_dict:
            if not same_value(src_dict[key], tgt_dict[key]):
                print(f'Values of key "{key} are different ...')
                diff += 1
        else:
            print(f'Key "{key}" not found in existing cluster specs ...')
            diff += 1
    return True if diff == 0 else False
