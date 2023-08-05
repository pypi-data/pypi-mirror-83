# coopio
Library for creating data services

CsvDataService Example:
```
class Dummy:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"a: {self.a}, b: {self.b}, c: {self.c}"

    def __repr__(self):
        return self.__str__()

class CsvDataService_Dummy(ICsvDataService):

    def __init__(self, data_file_path: str):
        ICsvDataService.__init__(self, data_file_path)

    def translate_from_data_rows(self, df: pd.DataFrame) -> List[T]:
        ret_dummies = []

        for i, row in df.iterrows():
            new_dummy = Dummy(
                a=row['a'],
                b=row['b'],
                c=row['c']
            )
            ret_dummies.append(new_dummy)

        return ret_dummies

```

After Establishing the data service, data can be stored or retrieved as follows:
```
    dummies = []
    for ii in range(0, 5):
        dummies.append(Dummy(ii, 2, 3))

    data_service.add_or_update(obj_identifier='a', objs=dummies)

    stored = data_service.retrieve_data(obj_identifier='a')
```