import pandas as pd
from typing import List
import numpy as np
from pandas.api.extensions import register_dataframe_accessor
import logging
logging.basicConfig(filename='logging_christine.log', level=logging.DEBUG, format='%(asctime)s: %(message)s')
from tqdm import tqdm

class CombinationMaker(object):
    @staticmethod
    def combinations(listofkeys: List[str], totalpairs:int = None) -> (List[List[str]], int):
        """
        makes al possible combinations of a list.
            example input: [a, b, c]
            example output: [[], [a], [b], [c], [a, b], [a, c], [b, c], [a, b, c]]

        :param listofkeys: list of strings that need to be combined
        :param totalpairs: needed for recursion, please keep as None as the script replaces it with the number of total
                           possible combinations
        :return: list of lists with all combinations of strings
        """
        if not totalpairs:
            totalpairs = 2**len(listofkeys) - 1

        if len(listofkeys) == 0:
            return [[]], totalpairs

        combinationlist = []

        for x in CombinationMaker.combinations(listofkeys=(listofkeys[:-1]), totalpairs=totalpairs)[0]:
            combinationlist += [x, x + [listofkeys[-1]]]
        logging.debug(f"now {len(combinationlist)-1} combinations made of {totalpairs} to make")
        return combinationlist, totalpairs


@register_dataframe_accessor("grouper")
class DataFrameGrouper(object):
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._maker = CombinationMaker

    @property
    def frame(self):
        return self._df


    def show_combinations(self, joiner:str =' ') -> List[str]:
        """
        makes the combinations made in CombinationMaker.combinations more readable .
            example df.keys() = [a, b, c]
            example joiner = '-'
            example output = [a, b, c, a-b, a-c, b-c, a-b-c]
        (removes the empty list)
        :param joiner: string that comes between the joined keys
        :return: list of strings of combinations with the joinerstring in between
        """
        listofkeys = [key for key in self.frame.keys()]
        lst = [joiner.join(x) for x in self._maker.combinations(listofkeys)[0] if x != []]
        return lst


    @staticmethod
    def concatenator(df:pd.DataFrame, joiner:str ='-' ) -> pd.DataFrame:
        """
        takes a df, makes all possible combinations of those columns using Combinationmaker.combinations,
        and concatenates them with a joinerstring in between.
            example input df = {a:1, b:2}
            example input joiner = '-'
            example output = {a:1, b:2, a-b:1-2}
        :param df: df that needs concatenating of its combinations
        :param joiner: string between the concatenating of the combinatinos, default='-'
        :return: df that is concatenated with '-' in between
        """

        datatypedict = df.dtypes.to_dict()
        combinationcolumns = CombinationMaker.combinations([key for key in df.keys()])[0]
        for col in combinationcolumns:
            if col != []:
                if len(col) > 1:
                    newcolname = joiner.join(col)
                else:
                    newcolname = col[0]
                df[newcolname] = df[col[0]].astype(str)
                for column in col[1:]:
                    df[newcolname] += joiner
                    df[newcolname] += df[column].astype(str)
        df = df.astype(datatypedict)
        return df

    @staticmethod
    def stringlength(df:pd.DataFrame, joiner:str = '-') -> pd.DataFrame:
        """
        dataframe df gets concatenated (using self.concatenater(df, joiner)) and per new column the mean length of
        the values gets calculated, and added in a new column, returning a new dataframe with only the new columns.
        If a value is not a string, it gets casted as a string while calculating.

        :param df: a dataframe that needs to get concatenated and stringlength counted
        :param joiner: string that is used to join the columns in concatenator, default='-'
        :return: a dataframe that is concatenated and has the stringlength counted
        """
        df_keys = df.keys()
        df_concatenated = DataFrameGrouper.concatenator(df=df, joiner=joiner)
        dictionary = {}
        for header in df_concatenated.keys():
            if header not in df_keys:
                newname = str(header + "_length")
                dictionary[newname] = np.mean(np.vectorize(len)(df_concatenated[header].astype(str)))
        df_end = pd.DataFrame(dictionary, index=range(len(df)))
        return df_end


    def groupbyer(self, sum_on_key: str, group_on_keys:list = None, disabletqdm:bool = False, joiner:str = '-') -> pd.DataFrame:
        """
        makes a list of columnnames on which to group by (group_on_keys or self.frame.keys())
        then concatenates all combinations of those columns with joiner as joiner-string
        then groups the self.frame by each of those columns and sums the sumcolumn on each groupby
        then makes 1 dataframe of this information and returns this dataframe.

        :param sum_on_key: key on which the summing takes place
        :param group_on_keys: list of all keys that need to be combined and grouped by if not all keys in df, default = None
        :param disabletqdm: if True there will be no tqdm shown, default=False
        :param joiner: string that is used to join the columns in concatenator, default='-'
        :return: dataframe
        """
        df = self.frame
        if group_on_keys is None:
            dfkeys = [key for key in df.keys() if key != sum_on_key]
        else:
            dfkeys = group_on_keys
        concatenated = DataFrameGrouper.concatenator(df=df.loc[:, dfkeys], joiner=joiner)
        newdf = pd.concat([df[sum_on_key], concatenated, DataFrameGrouper.stringlength(df=df.loc[:, dfkeys])], axis=1)
        keys = [header for header in concatenated.keys() if header not in dfkeys]
        for i, key in enumerate(tqdm(keys, disable=disabletqdm)):
            logging.debug(f"key number {i+1} ({key}) from {len(keys)} keys")
            newcolumnname = str(key + '_summed')
            newdf2 = newdf.groupby(key)
            newdf[newcolumnname] = newdf2[sum_on_key].transform('sum')
        return newdf


    def evaluator(self, sum_on_keys: str, group_on_keys:list = None, disabletqdm:bool = False, joiner:str = '-') -> pd.DataFrame:
        """
        makes dataframe with the following evaluation-statistics about the groupbyer-dataframe:
        -new_column_name: all combinations of given columns in group_on_keys or self.frame.keys(), joined by joiner
        -unique count: number of unique rows in the groupbyer-dataframe for that combination
        -not_zero: number of rows in the groupbyer-dataframe of which the sum of summed_column is not 0.0
        -string_length: mean string length of the values in that combination-column


        :param sum_on_keys: key on which the summing takes place
        :param group_on_keys: list of all keys that need to be combined and grouped by if not all keys in df, default = None
        :param disabletqdm: if True there will be no tqdm shown on the groupbyer, default=False
        :param joiner: string that is used to join the columns in concatenator, default='-'
        :return: dataframe with evaluation-statistics
        """
        df = self.groupbyer(sum_on_keys, group_on_keys, disabletqdm, joiner=joiner)
        if group_on_keys is None:
            keys = self._maker.combinations([key for key in self.frame.keys() if key != sum_on_keys])[0]
        else:
            keys = self._maker.combinations(group_on_keys)[0]
        keys2 = [joiner.join(key) for key in keys if key != []]
        list_of_dicts = []
        for column in keys2:
            if column not in self.frame.keys():
                dictionary = {
                    'new_column_name': column,
                    'unique_count': df[column].nunique(),
                    'not_zero': len(df[df['{}_summed'.format(column)] != 0.0]),
                    'string_length': df['{}_length'.format(column)][0]
                }
                list_of_dicts.append(dictionary)
        new_df = pd.DataFrame(list_of_dicts)
        return new_df

