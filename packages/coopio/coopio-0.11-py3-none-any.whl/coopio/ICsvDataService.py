from abc import ABC, abstractmethod
import pandas as pd
import os
from typing import TypeVar, Dict, List
from coopio.IDataService import IDataService

T = TypeVar('T')

class ICsvDataService(IDataService):

    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.create_file_if_not_exists(self.data_file_path)
        IDataService.__init__(self)

    def read_in_data(self, file_path: str):
        df = pd.read_csv(file_path)
        return df


    def write_data(self, df: pd.DataFrame, obj_identifier: str, file_path: str):
        self.create_file_if_not_exists(file_path)
        df[obj_identifier] = df[obj_identifier].astype(str)
        df.to_csv(file_path, index=False)
        return True

    def create_file_if_not_exists(self, file_path):
        if not os.path.exists(file_path):
            with open(file_path, "w"):
                pass

    def add_or_update(self, obj_identifier: str, objs: List[T]) -> List[T]:
        try:
            all_data = self.read_in_data(self.data_file_path)
            all_data[obj_identifier] = all_data[obj_identifier].astype(str)
        except pd.errors.EmptyDataError:
            all_data = None
        except Exception as e:
            raise e

        if all_data is not None:
            updated_data = pd.DataFrame([vars(obj) for obj in objs])
            updated_data[obj_identifier] = updated_data[obj_identifier].astype(str)

            all_data = (pd.concat([all_data, updated_data])
                            .drop_duplicates([obj_identifier], keep='last')
                            .sort_values(by=[obj_identifier], ascending=True)
                            .reset_index(drop=True))

        else:
            all_data = pd.DataFrame([vars(obj) for obj in objs])

        if self.write_data(all_data, obj_identifier, self.data_file_path):
            return self.retrieve_objs(obj_identifier=obj_identifier, ids=[str(vars(obj)[obj_identifier]) for obj in objs])
        else:
            raise Exception("Unable to update objects")

    def retrieve_objs(self, obj_identifier: str, ids: List[str] = None) -> List[T]:

        df = self.retrieve_df(obj_identifier, ids)

        ret = []
        if df is not None:
            ret = self.translate_from_data_rows(df)

        return ret

    def retrieve_df(self, obj_identifier: str, ids: List[str] = None) -> pd.DataFrame:
        try:
            existing_data = self.read_in_data(self.data_file_path)
        except:
            existing_data = None

        if existing_data is not None and ids is not None:
            existing_data = existing_data[existing_data[obj_identifier].isin(ids)]

        return existing_data


    def delete(self, obj_identifier: str, ids: List[str]) -> Dict[str, bool]:
        try:
            existing_data = self.read_in_data(self.data_file_path)
        except:
            existing_data = None

        if existing_data is None:
            return {id: True for id in ids}

        ret = {}
        new_data = existing_data
        for id in ids:
            try:
                existing_indexes = [i for i, line in existing_data.iterrows() if str(line[obj_identifier]) == id]

                new_data = new_data.drop(existing_indexes)
                ret[id] = True
            except:
                ret[id] = False

        self.write_data(new_data, obj_identifier, self.data_file_path)
        return ret

    @abstractmethod
    def translate_from_data_rows(self, df: pd.DataFrame) -> List[T]:
        pass
