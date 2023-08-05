import numpy as np
import pandas as pd
from fbprophet import Prophet
from sparkles.fbprophet_hacks import suppress_stdout_stderr

# declare variables for testing
store = "KT220"
tank = "7"
fc_url = "https://fc.bbdev.host3.capspire.com"


def decompose_sales(sales_data: pd.DataFrame):

    # not enough data
    if sales_data is None or len(sales_data) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    # fit model for weekly seasonality
    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        seasonality_mode="multiplicative",
    )
    with suppress_stdout_stderr():
        m.fit(sales_data)

    # calculate weekly seasonality
    future = m.make_future_dataframe(periods=1, freq="1D")
    forecast = m.predict(future)
    forecast_reduced = forecast.loc[:, ["ds", "yearly", "weekly"]]
    forecast_reduced["dow"] = forecast_reduced.ds.dt.weekday
    forecast_reduced["doy"] = forecast_reduced.ds.dt.dayofyear
    forecast_reduced["woy"] = forecast_reduced.ds.dt.week

    weekly_seasonality = forecast_reduced.groupby("dow")["weekly"].mean() + 1

    if len(weekly_seasonality) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    if len(sales_data) < 350:
        return pd.Series([1] * 53), weekly_seasonality

    # if nearly a full year, or more of data exists, calculate yearly seasonality
    forecast_reduced = forecast_reduced.iloc[-366:]
    forecast_reduced.sort_values(by=["woy", "dow"], inplace=True)
    year_trend = forecast_reduced.groupby("woy").mean()
    year_trend = year_trend["yearly"] + 1

    yearly_seasonality = ensure_53_weeks(year_trend)

    if len(weekly_seasonality) == 7 and len(yearly_seasonality) == 53:
        return yearly_seasonality, weekly_seasonality

    return pd.Series([1] * 53), pd.Series([1] * 7)


def ensure_53_weeks(initial: pd.DataFrame) -> pd.DataFrame:
    """
    takes a shorter dataframe and ensures at least 53 rows by wrapping the first rows onto the end
    """
    extra_weeks_needed = 53 - len(initial)
    if extra_weeks_needed > 0:
        ret = pd.concat([initial, initial[:extra_weeks_needed]], ignore_index=True)
    else:
        ret = initial.copy()
    return ret


def decompose_tank(tank_history: pd.DataFrame):

    if tank_history is None or len(tank_history) < 48:
        return generic_hh_seasonality

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode="multiplicative",
    )
    with suppress_stdout_stderr():
        m.fit(tank_history)

    future = m.make_future_dataframe(periods=1, freq="30min")
    forecast = m.predict(future)

    forecast_reduced = forecast.loc[:, ["ds", "daily"]]
    forecast_reduced["time"] = forecast_reduced["ds"].dt.time
    forecast_reduced.drop(columns="ds", inplace=True)
    day_trend = forecast_reduced.groupby("time").mean()
    day_trend.sort_values(by=["time"], inplace=True)

    if len(day_trend) != 48:
        return generic_hh_seasonality

    hh_seasonality = day_trend["daily"] + 1

    return hh_seasonality


generic_weekly_seasonality = [0.95, 1.0, 1.05, 1.05, 1.2, 0.95, 0.8]
generic_yearly_seasonality = [
    0.95,
    0.95,
    *np.repeat(0.9, 10),
    0.925,
    0.95,
    0.975,
    *np.repeat(1, 7),
    1.025,
    1.05,
    *np.repeat(1.075, 11),
    1.05,
    1.025,
    *np.repeat(1, 7),
    *np.repeat(0.95, 9),
]
generic_hh_seasonality = [
    1.0,
    0.85,
    0.7,
    0.55,
    0.4,
    0.25,
    0.1,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
    2.0,
    2.0,
    2.0,
    1.9,
    1.8,
    1.7,
    1.6,
    1.5,
    1.4,
    1.3,
    1.2,
    1.1,
]

if __name__ == "__main__":
    pass
