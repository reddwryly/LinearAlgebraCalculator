import re
# text = "((0.0 - (0.0 - 66.0 + 9.0 * ((0.0 - (0.0 - 66.0)) / 4.000000000000001) + 0.0 * t + (1.0 * -5.0) * ((0.0 - (0.0 - 66.0 + 9.0 * ((0.0 - (0.0 - 66.0)) / 4.000000000000001) + 0.0 * t)) / 2.2) + 10.0 * ((0.0 - (0.0 - 66.0)) / 4.000000000000001) + 0.0 * t)) / 5.0) ((0.0 - (0.0 - 66.0 + 9.0 * ((0.0 - (0.0 - 66.0)) / 4.000000000000001) + 0.0 * t)) / 2.2) ((0.0 - (0.0 - 66.0)) / 4.000000000000001)" 
text = "((0.0 - (0.0 - 66.0)) / 4.000000000000001)"
simplify = re.sub(r"\b0\.0\b\*\b", "", text) # 0.0 *
simplify = re.sub(r"\b\*\b0\.0", "", simplify) # * 0.0
simplify = re.sub(r"\s-\s0\.0", "", simplify) # - 0.0
simplify = re.sub(r"\b0\.0\s-\s", "", simplify) # 0.0 -
simplify = re.sub(r"\s\+\s0\.0", "", simplify) # + 0.0
simplify = re.sub(r"\b0\.0\s\+\s", "", simplify) # 0.0 +
simplify = re.sub(r"-\s\(-\s", "", simplify) # double negative
simplify = re.sub(r"\+\s-", "-", simplify) # redundant positive
simplify = re.sub(r"\b1\.0\b\*\b", "", simplify) # 1.0 *
simplify = re.sub(r"\b\*\b1\.0", "", simplify) # * 1.0
while re.search(r"\((\d+\.\d)\)", simplify): #single digit wrapped in parentheses ex: ((77.0)) -> 77.0
    simplify = re.sub(r"\((\d+\.\d)\)", r"\1", simplify)
print(simplify)
