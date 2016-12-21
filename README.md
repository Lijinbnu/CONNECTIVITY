# CONNECTIVITY
# original main code was from our lab, see "extract-roi-tc.py"
# made some modification for my own use: 
  1) 3mm resolution
  2) subject specific seed mask: core face regions for each subjects (Thus, we need to combine some ROIs like STS. see combine_roi_v1.py)
  3) subject specific seed mask is made by: using the peak activation coordinate to create a sphere, and intersect with subjects' specific rest data
     (see spc_sphroi.py)
  4) extract time series (see regional_FC_node.py)
  5) calculate regional wise FC for each subj (cal_roi_FC.py)
     this part is extramely difficult.... 
