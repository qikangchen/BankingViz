class IBankingDataConverter():

    CSV_HEADER = ("date", "usage", "amount", "debitor")

    '''
        Convert the files in to the agreed csv file format. 

        The banking data need to need exactly this rows in this order [date, usage, amount, name] 
        where the elements have following syntax:

        date: yyyy-mm-dd; example: 2019-12-24
        usage: purpose of the spending or earning; example: "Loan may 2019"
        amount: float that has a '.' as floating point. if the amount is negativ it's a spending,
                if positive it's an earning; example: -313.2
        name: name of the debitor, example: Google Inc.
    '''

    def convert(self) -> str:
        '''
        Convert the files into the agreed csv file format. Return the destination of the converted file.

        :return: Destination converted file
        '''
        raise NotImplementedError
