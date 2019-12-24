import pandas as pd

import config
from converter.base_converter import IBankingDataConverter


class Sparkasse_csv_camt_german(IBankingDataConverter):
    '''
    Converter for Sparkasse csv files.

    Following headers will be extracted for the agreed csv format:
    "Buchungstag" => date
    "Verwendungszweck" => purpose
    "Betrag" => amount
    "Beguenstigter/Zahlungspflichtiger" => debitor

    TODO: cross referencing constant
    The date will be converted from '%d.%m.%y' to config.DATE_FORMAT
    '''

    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination

    def convert(self) -> str:
        # TODO sphynx for inherented docs
        # Read spk csv
        raw_df = pd.read_csv(self.source, sep=";", decimal=",")

        # Convert into right csv format
        banking_data = self.__prepare_data(raw_df)

        # TODO: Error handling if no file found
        banking_data.to_csv(path_or_buf=self.destination, index=False)

        return self.destination

    def __prepare_data(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        # extract only the necessary columns and rename them
        df = pd.DataFrame(data=df_raw[["Buchungstag", "Verwendungszweck", "Betrag",
                                       "Beguenstigter/Zahlungspflichtiger"]])
        df.columns = self.CSV_HEADER

        # Convert to the right date format
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%y')
        df['date'] = df['date'].dt.strftime(config.DATE_FORMAT)

        return df
