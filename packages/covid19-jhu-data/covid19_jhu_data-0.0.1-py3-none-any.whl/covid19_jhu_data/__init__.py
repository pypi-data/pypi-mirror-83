import datetime
import pandas as pd

class GlobalDailyReport:
    def get_latest(self):
        """
        This method returns the latest global daily report as a DataFrame.
        """
        latest_date = datetime.date.today()
        day_delta = datetime.timedelta(days=1)
        fmt = '%m-%d-%Y'
        while True:
            try:
                latest_date_fmt = latest_date.strftime(fmt)
                csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv".format(latest_date_fmt)
                daily_report = pd.read_csv(csv_url)
                print("載入了 {} 的每日報告。".format(latest_date_fmt))
                break
            except:
                latest_date_fmt = latest_date.strftime(fmt)
                print("尚未有 {} 的每日報告。".format(latest_date_fmt))
                latest_date -= day_delta
        return daily_report
    def get_historic(self, year, month, day):
        """
        This method returns the historic global daily report with specified date as a DataFrame.
        """
        csv_file_name = "{}-{}-{}".format(month, day, year)
        csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv".format(csv_file_name)
        try:
            daily_report = pd.read_csv(csv_url)
            print("載入了 {} 的每日報告。".format(csv_file_name))
            return daily_report
        except:
            print("沒有 {} 的每日報告。".format(csv_file_name))
