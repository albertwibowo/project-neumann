def classify_pval(pval:float, threshold:float) -> str:
    if pval <= threshold:
        return 'drift detected'
    else:
        return 'drift not detected'