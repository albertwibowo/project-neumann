import pandas as pd
# from src.abstract.data_handler_base import DataHandlerBase


class DataHandler():

    def __init__(self, target: pd.DataFrame, 
                 source: pd.DataFrame):
        self.target = target
        self.source = source

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
    
    def analye(self) -> None:
        return 