from pandas import read_csv
from os.path import join
from feature_selector import FeatureSelector
"""
############################################
############  MAIN OBJECT  ################
############################################
"""
data = read_csv(join("data", "data.csv")) 
feature_selector = FeatureSelector(data)

"""
############################################
############ DATA RETRIEVAL  ###############
############################################
"""
entropy_coef_matrix = feature_selector.get_entropy_coef_matrix()
cramer_v_matrix = feature_selector.get_cramer_v_matrix()
corr_coef_matrix = feature_selector.get_corr_coef_matrix()
oob_matrix = feature_selector.get_oob_score_matrix(n_estimators=100, 
                                                   additional_estimators=100, 
                                                   min_samples_split=30)
mean_oobscore = oob_matrix.mean()
"""
############################################
############ MATRICES DISPLAY  #############
############################################
"""
feature_selector.show_matrix_graph(corr_coef_matrix, "Corr coef matrix")
feature_selector.show_matrix_graph(cramer_v_matrix, "Cramer's v matrix")
feature_selector.show_matrix_graph(entropy_coef_matrix, "Entropy coef_matrix")
feature_selector.show_matrix_graph(oob_matrix, "Out of bag error matrix")




