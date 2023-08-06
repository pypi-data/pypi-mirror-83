from  math import e
from itertools import product
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from DataTypeIdentifier.data_type_identifier import DataTypeIdentifier
from sklearn.preprocessing import LabelEncoder
from seaborn import heatmap
from scipy import stats as ss
import VariableSelection.constants as const
import numpy as np
import pandas as pd


class FeatureSelector():
    """
    Feature selection with:
        Symmetric measures:
            - Pearson coefficient of correlation(for numerical variables)
            - Cramers' V(for categorical variables)
        Assymmetric measures:
            - Entropy coefficient(for categorical variables)
            - Out-of-bag score(for both variable types)        
    """
    def __init__(self, data):
        data_type_identifier = DataTypeIdentifier()
        self.__label_encoder = LabelEncoder()
        self.__data_copy = data_type_identifier.keep_initial_data_types(data.copy(deep=True))
        self.__predictions = data_type_identifier.predict(data, verbose=0) 
        cat_check = self.__predictions.values == const.CATEGORICAL
        num_check = self.__predictions.values==const.NUMERICAL
        self.__categorical_variable_names = self.__predictions[cat_check].index
        self.__numerical_variable_names = self.__predictions[num_check].index
        self.__categorical_variables = data[self.__categorical_variable_names]
        self.__numerical_variables = data[self.__numerical_variable_names]
        
        #Random forest variables
        self.__additional_estimators = None
        self.__n_estimators = None
        self.__max_depth = None
        self.__min_samples_split = None 
        self.__min_samples_leaf = None
        self.__min_weight_fraction_leaf = None
        self.__max_features = None
        self.__max_leaf_nodes = None
        self.__min_impurity_decrease = None
        self.__min_impurity_split = None
        self.__n_jobs = None 
        self.__random_state = None
        self.__verbose = None
        self.__bootstrap = True
        self.__oob_score = True
        self.__warm_start = True
        
    
    def __replace_nan_values(self):
        """
        Replaces empty cells with initial values in the features dataset:
            - mode for categorical variables 
            - median for numerical variables

        Returns
        -------
        None
        """
        #Calculating medians and modes
        medians = self.__data_copy[self.__numerical_variable_names].median()
        modes = self.__data_copy[self.__categorical_variable_names].mode().iloc[0]
        new_values = pd.concat([medians, modes])

        #Replacing initial_guesses in the dataset
        self.__data_copy.fillna(new_values, inplace=True)
        
        
    def __encode_feature(self, feature):
        """
        Parameters
        ----------
        feature : pandas.core.frame.DataFrame

        Returns
        -------
        encoded_feature : pandas.core.frame.DataFrame
        """
        encoded_feature = feature
        if self.__predictions.loc[feature.name].any() == const.CATEGORICAL:
            encoded_feature = pd.get_dummies(feature)
        else:
            encoded_feature = np.array(feature).reshape(-1, 1)
        return encoded_feature
   
             
    def __encode_target(self, target):
        """
        Parameters
        ----------
        target : pandas.core.frame.DataFrame

        Returns
        -------
        target_encoded : pandas.core.frame.DataFrame
        """
        target_encoded = target
        if self.__predictions.loc[target.name].any() == const.CATEGORICAL:
            target_encoded = self.__label_encoder.fit_transform(target)
        return target_encoded
   
         
    def __build_ensemble_model(self, feature, target):
        """
        Parameters
        ----------
        feature : pandas.core.frame.DataFrame

        target : pandas.core.frame.DataFrame

        Returns
        -------
        float
        """
        if self.__data_copy.isnull().any().any():
            self.__replace_nan_values()
            
        print(f" TREATING (Feature: {feature.name.upper()}," 
              f" Target: {target.name.upper()})")
        if feature.name != target.name:
            Model = {"categorical":RandomForestClassifier,
                     "numerical":RandomForestRegressor}
            type_ = self.__predictions.loc[target.name].any()
            encoded_feature = self.__encode_feature(feature)
            encoded_target = self.__encode_target(target)
            estimator = Model[type_](n_estimators=self.__n_estimators,
                                     max_depth=self.__max_depth, 
                                     min_samples_split=self.__min_samples_split, 
                                     min_samples_leaf=self.__min_samples_leaf, 
                                     min_weight_fraction_leaf=self.__min_weight_fraction_leaf, 
                                     max_features=self.__max_features, 
                                     max_leaf_nodes=self.__max_leaf_nodes, 
                                     min_impurity_decrease=self.__min_impurity_decrease, 
                                     min_impurity_split=self.__min_impurity_split, 
                                     bootstrap=self.__bootstrap, 
                                     oob_score=self.__oob_score, 
                                     n_jobs=self.__n_jobs, 
                                     random_state=self.__random_state, 
                                     verbose=self.__verbose,
                                     warm_start=self.__warm_start) 
            precedent_out_of_bag_score = 0
            current_out_of_bag_score = 0
            while (current_out_of_bag_score > precedent_out_of_bag_score or not 
                   current_out_of_bag_score):
                estimator.fit(encoded_feature, encoded_target) 
                precedent_out_of_bag_score = current_out_of_bag_score
                current_out_of_bag_score = estimator.oob_score_
                estimator.n_estimators += self.__additional_estimators 
            return precedent_out_of_bag_score
        return 1
       
     
    def corr_coef(self, X, Y):
        """
        Parameters
        ----------
        X : pandas.core.frame.DataFrame
        
        Y : pandas.core.frame.DataFrame

        Returns
        -------
        coeff_corr : TYPE
            DESCRIPTION.

        """
        print(f" TREATING (X: {X.name.upper()}," 
              f" Y: {Y.name.upper()})")
        coeff_corr,_ = ss.pearsonr(X,Y)
        return coeff_corr
        
    
    def cramers_v(self, X, Y):
        """
        Parameters
        ----------
        X : TYPE
            DESCRIPTION.
        Y : TYPE
            DESCRIPTION.

        Returns
        -------
        float
        """
        print(f" TREATING (X: {X.name.upper()}," 
              f" Y: {Y.name.upper()})")
        confusion_matrix = pd.crosstab(X,Y)
        chi2 = ss.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.values.sum()
        phi2 = chi2/n
        r,k = confusion_matrix.shape
        phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
        rcorr = r-((r-1)**2)/(n-1)
        kcorr = k-((k-1)**2)/(n-1)
        return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
      
        
    def conditional_entropy(self, Y, X, log_base=e):
        """
        Parameters
        ----------
        Y : pandas.core.frame.DataFrame
        
        X : pandas.core.frame.DataFrame
        
        log_base : TYPE, optional
            The default is e.

        Returns
        -------
        dict
        """
        confusion_matrix = pd.crosstab(Y,X)
        prob_X=confusion_matrix.sum(axis=0)/confusion_matrix.values.sum()
        joint_prob_Y_X = confusion_matrix/confusion_matrix.values.sum()
        cond_prob_Y_X = joint_prob_Y_X/prob_X
        log_cond_prob_Y_X = np.log(cond_prob_Y_X.mask(cond_prob_Y_X==0)).fillna(0) / np.log(log_base)
        H_Y_X = -(joint_prob_Y_X * log_cond_prob_Y_X).values.sum()
        return {"conditional_entropy":H_Y_X, "confusion_matrix":confusion_matrix}
     
        
    def entropy_coefficient(self, Y, X, log_base=e):
        """
        Parameters
        ----------
        Y : pandas.core.frame.DataFrame
        
        X : pandas.core.frame.DataFrame
        
        log_base : TYPE, optional
            The default is e.

        Returns
        -------
        float
        """
        print(f" TREATING (X: {X.name.upper()}," 
              f" Y: {Y.name.upper()})")
        cond_ent_conf_mat = self.conditional_entropy(Y, X)
        confusion_matrix = cond_ent_conf_mat["confusion_matrix"]
        H_Y_X = cond_ent_conf_mat["conditional_entropy"]
        prob_Y=confusion_matrix.sum(axis=1)/confusion_matrix.values.sum()
        H_Y = ss.entropy(prob_Y, base=log_base)
        U_Y_X = (H_Y - H_Y_X) / H_Y
        if H_Y==0:
            return 1
        return U_Y_X


    def __build_matrix(self, data, method=None):
        """
        Parameters
        ----------
        data : pandas.core.frame.DataFrame
        
        method : method, optional
            The default is None.
        Returns
        -------
        corr_matrix : pandas.core.frame.DataFrame
        """
        coordinates = list(product(data, repeat=2))
        n_columns = len(data.columns)
        data_columns = data.columns
        matrix_list = [method(data[row], data[column]) 
                       for row, column in coordinates]
        corr_matrix_reshaped = np.reshape(matrix_list, (n_columns, n_columns))
        corr_matrix = pd.DataFrame(corr_matrix_reshaped, 
                                   index=data_columns,                               
                                   columns=data_columns)
        return corr_matrix

    
    def get_numerical_variables(self):
        """
        Returns
        -------
        pandas.core.frame.DataFrame
        """
        return self.__numerical_variables

    
    def get_categorical_variables(self):
        """
        Returns
        -------
        pandas.core.frame.DataFrame.
        """
        return self.__categorical_variables

    
    def get_variables_type_predictions(self):
        """
        Returns
        -------
        pandas.core.frame.DataFrame
        """
        return self.__predictions
   
                 
    def get_corr_coef_matrix(self):
        """        
        Returns
        -------
        results : pandas.core.frame.DataFrame
        """
        print("\nComputing Correlation coef matrix...\n")
        results = self.__build_matrix(data=self.__numerical_variables, 
                                      method=self.corr_coef)
        print("\nDONE!\n")
        return results
   
    
    def get_cramer_v_matrix(self):
        """
        Returns
        -------
        results : pandas.core.frame.DataFrame
        """
        print("\nComputing Cramer's V matrix...\n")
        results = self.__build_matrix(data=self.__categorical_variables, 
                                      method=self.cramers_v)
        print("\nDONE!\n")
        return results
    
    
    def get_entropy_coef_matrix(self):
        """
        Returns
        -------
        results : pandas.core.frame.DataFrame
        """
        print("\nComputing Entropy coef matrix...\n")
        results = self.__build_matrix(data=self.__categorical_variables, 
                                      method=self.entropy_coefficient)
        print("\nDONE!\n")
        return results
    
    
    def get_oob_score_matrix(self,
                             additional_estimators=20,
                             n_estimators=30,
                             max_depth=None,
                             min_samples_split=20,
                             min_samples_leaf=20,
                             min_weight_fraction_leaf=0.0, 
                             max_features=None,
                             max_leaf_nodes=None,
                             min_impurity_decrease=0.0,
                             min_impurity_split=None,
                             n_jobs=-1,
                             random_state=None,
                             verbose=0):
        """
        Parameters
        ----------
        additional_estimators : int, optional
            The default is 20.
        n_estimators : int, optional
            The default is 30.
        max_depth : int, optional
            The default is None
        min_samples_split : int, optional
            The default is 20.
        min_samples_leaf : int, optional
            The default is 20.
        min_weight_fraction_leaf : float, optional
            The default is 0.0.
        max_features : str, optional
            The default is 'auto'.
        max_leaf_nodes : int, optional
            The default is None
        min_impurity_decrease : float, optional
            The default is 0.0.
        min_impurity_split : float, optional
            The default is None
        n_jobs : int, optional
            DESCRIPTION. The default is -1.
        random_state : int, optional
            DESCRIPTION. The default is None
        verbose : int, optional
            The default is 0.

        Returns
        -------
        results : pandas.core.frame.DataFrame
        """
        print("\nComputing Out-of-bag-score matrix...\n")
        self.__additional_estimators = additional_estimators
        self.__n_estimators = n_estimators
        self.__max_depth = max_depth
        self.__min_samples_split = min_samples_split 
        self.__min_samples_leaf = min_samples_leaf
        self.__min_weight_fraction_leaf = min_weight_fraction_leaf
        self.__max_features = max_features
        self.__max_leaf_nodes = max_leaf_nodes
        self.__min_impurity_decrease = min_impurity_decrease
        self.__min_impurity_split = min_impurity_split
        self.__n_jobs = n_jobs 
        self.__random_state = random_state
        self.__verbose = verbose
        results = self.__build_matrix(data=self.__data_copy, 
                                      method=self.__build_ensemble_model)
        print("\nDONE!\n")
        return results
        
    
    def show_matrix_graph(self, matrix, title=""):
        """
        Parameters
        ----------
        matrix : pandas.core.frame.DataFrame
        
        title : str, optional
            The default is "".

        Returns
        -------
        None.

        """
        ax = heatmap(matrix, annot=True)
        ax.set_title(title)
        

