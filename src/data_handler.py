import pandas as pd
from src.algorithms.chi_square import perform_chi_square
from src.algorithms.kolmogorov_smirnov import perform_kolmogorov_smirnov_test
from src.utils.classify_pvalue import classify_pval

# from src.abstract.data_handler_base import DataHandlerBase


class DataHandler():

    def __init__(self, target: pd.DataFrame, 
                 source: pd.DataFrame):
        self.target = target
        self.source = source

        self.type_df = None 
        self.result_df = None 

    def check_columns(self) -> None:

        column_names = []
        column_types = []
        for col in self.source.columns:

            column_names.append(col)
            if self.source[col].nunique == self.source.shape[0]:
                column_types.append('id')
            
            elif self.source[col].dtype == 'O':
                column_types.append('categorical')
            
            else:
                column_types.append('numerical')

        self.type_df = pd.DataFrame({'column_names': column_names, 
                                     'column_types': column_types})
        return 
    
    def coerce_quality(self) -> None:
        '''
        Method to ensure we only consider columns
        that exist in the source dataframe.
        '''
        source_columns = list(self.source.columns)
        target_columns = [col for col in self.target.columns if col in source_columns]
        self.target = self.target[target_columns]

        return 
    
    def analye(self, threshold:float) -> None:

        column_names = []
        p_values = []
        conclusions = []

        for _, row in self.type_df.iterrows():
            column_name = row['column_names']
            if row['column_types'] == 'numerical':
                p_value = perform_kolmogorov_smirnov_test(self.target[column_name].dropna(),
                                                          self.source[column_name].dropna())
                conclusion = classify_pval(pval=p_value, threshold=threshold)
                column_names.append(column_name)
                p_values.append(p_value)
                conclusions.append(conclusion)
                # pass
            
            elif row['column_types'] == 'categorical':

                series_source = self.source[column_name].dropna()
                series_target = self.target[column_name].dropna()

                accepted_values = list(series_source.unique())
                series_target= series_target[series_target.isin(accepted_values)]

                p_value = perform_chi_square(f_obs=series_source.groupby(series_source).size().values,
                                             f_exp=series_target.groupby(series_target).size().values)
                
                conclusion = classify_pval(pval=p_value, threshold=threshold)
                column_names.append(column_name)
                p_values.append(p_value)
                conclusions.append(conclusion)
            
            else:
                pass


        self.result_df = pd.DataFrame({'column_names': column_names, 
                                     'p_values': p_values,
                                     'statistical_conclusions': conclusions})

        return 