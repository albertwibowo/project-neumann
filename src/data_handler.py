import pandas as pd
import plotly.graph_objects as go
from src.algorithms.chi_square import perform_chi_square
from src.algorithms.kolmogorov_smirnov import perform_kolmogorov_smirnov_test
from src.utils.classify_pvalue import classify_pval

# from src.abstract.data_handler_base import DataHandlerBase


class DataHandler():

    def __init__(self, target: pd.DataFrame, 
                 reference: pd.DataFrame):
        self.target = target
        self.reference = reference

        self.type_df = None 
        self.result_df = None 

    def check_columns(self) -> None:
        '''
        Method to identify column types.
        '''
        column_names = []
        column_types = []
        for col in self.reference.columns:

            column_names.append(col)
            if self.reference[col].nunique == self.reference.shape[0]:
                column_types.append('id')
            
            elif self.reference[col].dtype == 'O':
                column_types.append('categorical')

            elif self.reference[col].dtype == 'float64':
                column_types.append('numerical')
            
            elif self.reference[col].dtype == 'int64':
                column_types.append('numerical')

            elif self.reference[col].dtype == 'bool':
                column_types.append('categorical')

            else:
                column_types.append('categorical')

        self.type_df = pd.DataFrame({'column_names': column_names, 
                                     'column_types': column_types})
        return 
    
    def coerce_quality(self) -> None:
        '''
        Method to ensure we only consider columns
        that exist in the reference dataframe.
        '''
        reference_columns = list(self.reference.columns)
        target_columns = [col for col in self.target.columns if col in reference_columns]
        self.target = self.target[target_columns]

        return 
    
    def analye(self, threshold: float) -> None:
        '''
        Method to analyse target and reference datasets.
        '''
        column_names = []
        p_values = []
        conclusions = []

        for _, row in self.type_df.iterrows():
            column_name = row['column_names']
            if row['column_types'] == 'numerical':
                p_value = perform_kolmogorov_smirnov_test(self.target[column_name].dropna(),
                                                          self.reference[column_name].dropna())
                conclusion = classify_pval(pval=p_value, threshold=threshold)
                column_names.append(column_name)
                p_values.append(p_value)
                conclusions.append(conclusion)
                # pass
            
            elif row['column_types'] == 'categorical':

                series_reference = self.reference[column_name].dropna()
                series_target = self.target[column_name].dropna()

                accepted_values = list(series_reference.unique())
                series_target= series_target[series_target.isin(accepted_values)]

                p_value = perform_chi_square(f_obs=series_target.groupby(series_target).size().values,
                                             f_exp=series_reference.groupby(series_reference).size().values)
                
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
    
    def visualise(self, column_name: str):
        '''
        Method to visualise a column.
        '''

        col_type = self.type_df[self.type_df['column_names'] == column_name]['column_types'].item()

        if col_type == 'categorical':
        
            series_reference = self.reference[column_name].dropna()
            series_target = self.target[column_name].dropna()
            accepted_values = list(series_reference.unique())

            series_reference_count = series_reference.groupby(series_reference).size().values
            series_target_count = series_target.groupby(series_target).size().values

            # create plotly object

            fig = go.Figure()
            fig.add_trace(go.Bar(x=accepted_values,
                y=series_reference_count,
                name='reference',
                marker_color='rgb(55, 83, 109)'
                ))
            
            fig.add_trace(go.Bar(x=accepted_values,
                            y=series_target_count,
                            name='target',
                            marker_color='rgb(26, 118, 255)'
                            ))

            fig.update_layout(
                title='Bar chart between reference and target data',
                xaxis_tickfont_size=14,
                yaxis=dict(
                    title='Count',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                legend=dict(
                    x=0,
                    y=1.0,
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'
                ),
                barmode='group',
                bargap=0.15, # gap between bars of adjacent location coordinates.
                bargroupgap=0.1 # gap between bars of the same location coordinate.
            )
            return fig

        elif col_type == 'numerical':
            
            series_reference = self.reference[column_name].dropna()
            series_target = self.target[column_name].dropna()

            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=series_reference,
                histnorm='density',
                name='reference', # name used in legend and hover labels
                xbins=dict( # bins used for histogram
                    start=-4.0,
                    end=3.0,
                    size=0.5
                ),
                marker_color='rgb(55, 83, 109)',
                opacity=0.75
            ))
            fig.add_trace(go.Histogram(
                x=series_target,
                histnorm='density',
                name='target',
                xbins=dict(
                    start=-3.0,
                    end=4,
                    size=0.5
                ),
                marker_color='rgb(26, 118, 255)',
                opacity=0.75
            ))

            fig.update_layout(
                title_text='Bar chart between reference and target data', # title of plot
                xaxis_title_text='Bins', # xaxis label
                yaxis_title_text='Count', # yaxis label
                bargap=0.2, # gap between bars of adjacent location coordinates
                bargroupgap=0.1 # gap between bars of the same location coordinates
            )

            return fig

        else:
            pass

        return 