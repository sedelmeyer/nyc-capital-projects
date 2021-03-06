"""
caproj.visualize
~~~~~~~~~~~~~~~~

This module contains functions for visualizing data and model results

**Module functions:**

.. autosummary::

   plot_value_counts
   plot_barplot
   plot_hist_comps
   plot_line
   plot_2d_embed_scatter
   plot_true_pred
   plot_bdgt_sched_scaled
   plot_change_trend
   plot_gam_by_predictor
   plot_coefficients
   load_img_to_numpy
   plot_jpg

"""

from PIL import Image

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score


def plot_value_counts(value_counts, figsize=(9, 3), color="tab:blue"):
    """Generates barplot from pandas value_counts series

    :param value_counts: pandas DataFrame generated using the pandas ``value_counts``
            method
    :type value_counts: DataFrame
    :param figsize: dimensions of resulting plot, defaults to (9, 3)
    :type figsize: tuple, optional
    :param color: color of resulting plotted bars, defaults to "tab:blue"
    :type color: str, optional
    """
    fig, ax = plt.subplots(figsize=figsize)

    max_y = max(value_counts.values)
    n_cats = len(value_counts)

    ax.bar(range(n_cats), value_counts.values, color=color, alpha=0.5)

    [
        ax.text(
            x,
            y + max_y * 0.02,
            "{:,}".format(y),
            color="k",
            fontsize=14,
            horizontalalignment="center",
        )
        for x, y in enumerate(value_counts)
    ]

    plt.xticks(range(n_cats), value_counts.index, fontsize=14)


def plot_barplot(
    value_counts, title, height=6, varname=None, color="k", label_space=0.01
):
    """Generates a horizontal barplot from a pandas value_counts series

    :param value_counts: pd.Series object generated by pandas value_counts()
                         method
    :param title: string, the printed title of the plot
    :param height: integer, the desired height of the plot (default is 6)
    :param varname: string or None, text to print for plot's y-axis title
    :param color: string, the matplotlib color name for the color you would
                  like for the plotted bars (default is 'k' or black)
    :param label_space: float, a coefficient used to space the count label
                        an appropriate distance from the plotted bar
                        (default is 0.01)
    :return: a matplotlib plot. No objects are returned
    """
    fig, ax = plt.subplots(figsize=(12, height))

    max_y = max(value_counts.values)
    n_cats = len(value_counts)

    ax.barh(range(n_cats), value_counts.values, color=color, alpha=1)

    [
        ax.text(
            y + max_y * label_space,
            x,
            "{:,}".format(y),
            color="k",
            fontsize=12,
            verticalalignment="center",
        )
        for x, y in enumerate(value_counts)
    ]

    plt.title(title, fontsize=18)
    plt.yticks(range(n_cats), value_counts.index, fontsize=12)
    plt.xlabel("count", fontsize=14)
    if varname:
        plt.ylabel(varname, fontsize=14)

    plt.grid(":", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_hist_comps(df, metric_1, metric_2, y_log=False, bins=20):
    """Plots side-by-side histograms for comparison with log yscale option

    Plots 2 subplots, no objects are returned

    :param df: pd.DataFrame object containing the data you wish to plot
    :param metric_1: string, name of column containing data for the first plot
    :param metric_2: string, name of column containing data for second plot
    :param y_log: boolean, indicating whether the y-axis should be plotted
                  with a log scale (default False)
    :param bins: integer, the number of bins to use for the histogram
                 (default 20)
    """
    metrics_list = [metric_1, metric_2]
    metrics_str = [metric.replace("_", " ").upper() for metric in metrics_list]

    fig, ax = plt.subplots(1, 2, sharey=True, figsize=(12, 4))

    plt.suptitle("Projects by {} and {}".format(*metrics_str), fontsize=18, y=1)

    for (i, ax), metric_col, metric_name in zip(
        enumerate(ax), metrics_list, metrics_str
    ):
        ax.hist(df[metric_col], bins=bins, alpha=0.7)
        ax.axvline(df[metric_col].mean(), color="k", label="mean")
        ax.axvline(
            df[metric_col].quantile(q=0.5),
            color="k",
            linestyle="--",
            label="median",
        )
        ax.axvline(
            df[metric_col].quantile(q=0.025),
            color="k",
            linestyle=":",
            label="95% range",
        )
        ax.axvline(df[metric_col].quantile(q=0.975), color="k", linestyle=":")

        ax.set_xlabel(metric_name, fontsize=14)
        ax.grid(":", alpha=0.4)
        if i == 0:
            ax.set_ylabel("frequency", fontsize=12)
            ax.legend(edgecolor="k", fontsize=12)
        if y_log:
            ax.set_yscale("log")
            if i == 0:
                ax.set_ylabel("frequency (log scale)", fontsize=12)

    plt.tight_layout()
    plt.show()


def plot_line(x_vals, y_vals, title, x_label, y_label, height=3.5):
    """Generates line plot given input x, y values
    """
    fig, ax = plt.subplots(figsize=(12, height))

    plt.title(title, fontsize=19)

    plt.plot(
        x_vals, y_vals, "ko-",
    )

    plt.xlabel(x_label, fontsize=16)
    plt.xticks(fontsize=14)
    plt.ylabel(y_label, fontsize=16)
    plt.yticks(fontsize=14)
    plt.grid(":", alpha=0.4)
    plt.tight_layout()
    plt.show()


def plot_2d_embed_scatter(
    data1,
    data2,
    title,
    xlabel,
    ylabel,
    data1_name="training obs",
    data2_name="TEST obs",
    height=5,
    point_size=None,
):
    """Plots 2D scatterplot of dimension-reduced embeddings for train and test

    2D matplotlib scatterplot, no objects are returned.

    NOTE: This function assumes the data inputs are 2D np.array objects of
          share (n, 2), and that two separate sets of encoded embeddings
          are going to be plotted together (i.e. the train and the test
          observations). 2D pd.DataFrame objects can be passed, and are
          converted to np.array within the plotting function.

    :param data1: np.array 2D containing 2 encoded dimensions
    :param data2: a second np.array 2D containing 2 encoded dimensions
    :param title: str, text used for plot title
    :param xlabel: string representing the label for the x axis
    :param ylabel: string representing the label for the y axis
    :param data1_name: string representing the name of the first dataset,
                  this will be the label given to those points in the
                  plot's legend (default 'training obs')
    :param data2_name: string representing the name of the first dataset,
                  this will be the label given to those points in the
                  plot's legend (default 'TEST obs')
    :param height: integer that determines the hieght of the plot
                   (default is 5)
    :param point_size: integer or None, default of None will revert to
                       matplotlib scatter default, integer entered will
                       override the default marker size
    """

    # if y inputs are pandas dataframes, convert to numpy array
    if type(data1) == pd.core.frame.DataFrame:
        data1 = data1.copy().values
    if type(data2) == pd.core.frame.DataFrame:
        data2 = data2.copy().values

    fig, ax = plt.subplots(figsize=(12, height))
    plt.title(title, fontsize=18)
    plt.scatter(
        *data1.T, color="silver", alpha=1, s=point_size, label=data1_name
    )
    plt.scatter(*data2.T, color="k", alpha=1, s=point_size, label=data2_name)
    plt.ylabel(ylabel, fontsize=14)
    plt.xlabel(xlabel, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(":", alpha=0.4)
    plt.legend(fontsize=14, edgecolor="k")
    plt.tight_layout()
    plt.show()


def plot_true_pred(
    model_dict=None,
    dataset="train",
    y_true=None,
    y_pred=None,
    model_descr=None,
    y1_label=None,
    y2_label=None,
):
    """Plots model prediction results directly from model_dict or input arrays

    Generates 5 subplots, (1) true values with predicted values overlay,
    each y variable on its own axis, (2) output variable 1 true vs. predicted
    on each axis,(3) output variable 2 true vs. predicted on each axis
    (4) output variable 1 true vs. residuals, (5) output variable 2 true
    vs. residuals (no objects are returned)

    This plotting function only really requires that a model_dict from the
    ``generate_model_dict()`` function be used as input. However, through use of
    the y_true, y_pred, model_descr, and y1 and y2 label parameters, predictions
    stored in a shape (n,2) array can be plotted directly wihtout the use of
    a model_dict

    NOTE: This plotting function requires y to consist of 2 output variables.
          Therefore, it will not work with y data not of shape=(n, 2).

    :param model_dict: dictionary or None, if model results from the
                       generate_model_dict func is used, function defaults to
                       data from that dict for plot, if None plot expects y_true,
                       y_pred, model_descr, and y1/y2 label inputs for plotting
    :param dataset: string, 'train' or 'test', indicates whether to plot training or
                    test results if using model_dict as data source, and labels
                    plots accordingly if y_pred and y_true inputs are used (default
                    is 'train')
    :param y_true, y_pred: None or pd.DataFrame and np.array shape=(n,2) data sources
                           accepted and used for plotting if model_dict=None
                           (default for both is None)
    :param model_descr: None or string of max length 80 used to describe model in
                        title. If None, model_descr defaults to description in
                        model_dict, if string is entered, that string overrides the
                        description in model_dict, if using y_true/y_test as data
                        source model_descr must be specified as a string (default
                        is None)
    :param y1_label, y2_label: None or string of max length 40 used to describe
                               the 2 output y variables being plotted. These values
                               appear along the plot axes and in the titles of
                               subplots. If None, the y_variables names from the
                               model_dict are used. If strings are entered, those
                               strings are used to override the model_dict values.
                               If using y_true/y_test as data source, these values
                               must be specified (default is None for both label)
    """
    # create placeholder var_labels list for easier handling of conditionals
    var_labels = [None, None]

    # extract required objects from model_dict if not None
    if type(model_dict) == dict:
        y_true = model_dict["y_values"][dataset]
        y_pred = model_dict["predictions"][dataset]
        r2_scores = model_dict["score"][dataset]
        var_labels = [
            var.replace("_", " ") for var in model_dict["y_variables"]
        ]

        if model_descr is None:
            model_descr = model_dict["description"]
    # calculate r2 scores if model_dict not provided
    else:
        r2_scores = r2_score(y_true, y_pred, multioutput="raw_values")

    # Set y labels or overwrite y labels if specified as not None
    if y1_label is not None:
        var_labels[0] = y1_label
    if y2_label is not None:
        var_labels[1] = y2_label

    # if y inputs are pandas dataframes, convert to numpy array
    if type(y_true) == pd.core.frame.DataFrame:
        y_true = y_true.copy().values
    if type(y_pred) == pd.core.frame.DataFrame:
        y_pred = y_pred.copy().values

    # GENERATE PLOT 1
    fig, ax = plt.subplots(figsize=(12, 6))

    plt.title(
        "{} predictions vs. true values for\n{}\n".format(
            "TEST" if dataset.lower() == "test" else "TRAINING", model_descr
        ),
        fontsize=18,
    )

    plt.scatter(
        *y_true.T,
        color="silver",
        alpha=1,
        edgecolor="gray",
        marker="s",
        s=90,
        label="True values"
    )
    plt.scatter(
        *y_pred.T,
        color="c",
        alpha=1,
        edgecolor="k",
        marker="o",
        s=90,
        label="Predicted values"
    )

    ax.set_xlabel(var_labels[0], fontsize=12)
    ax.set_ylabel(var_labels[1], fontsize=12)

    ax.legend(fontsize=12, edgecolor="k")

    ax.grid(":", alpha=0.4)
    plt.tight_layout()
    plt.show()

    # GENERATE SUBPLOTS 2 AND 3
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    plt.suptitle(
        "Predictions and residuals vs. true values by output variable",
        y=1,
        fontsize=16,
    )

    for i, (ax, true, pred) in enumerate(zip(axes.flat, y_true.T, y_pred.T)):
        ax.scatter(true, pred, color="k", alpha=0.5, edgecolor="w", s=90)
        ax.set_title(
            "{}\n$R^2={:.3f}$".format(var_labels[i], r2_scores[i]), fontsize=14
        )
        ax.set_xlabel("True value", fontsize=12)
        if i == 0:
            ax.set_ylabel("Predicted value", fontsize=12)
        ax.axis("equal")
        ax.grid(":", alpha=0.4)

    plt.tight_layout()
    plt.show()

    # GENERATE SUBPLOTS 4 AND 5
    fig, axes = plt.subplots(1, 2, figsize=(12, 3))

    for i, (ax, true, pred) in enumerate(zip(axes.flat, y_true.T, y_pred.T)):
        ax.scatter(true, pred - true, color="k", alpha=0.5, edgecolor="w", s=90)
        ax.axhline(0, color="k", linestyle="--")
        ax.set_title("Residuals", fontsize=14)
        ax.set_xlabel("True value", fontsize=12)
        if i == 0:
            ax.set_ylabel("Prediction error", fontsize=12)
        ax.grid(":", alpha=0.4)

    plt.tight_layout()
    plt.show()


def plot_bdgt_sched_scaled(
    X,
    X_scaled,
    scale_descr,
    X_test=None,
    X_test_scaled=None,
    bdgt_col="Budget_Start",
    sched_col="Duration_Start",
):
    """Plots original vs scaled versions of budget and schedule input data

    Generates 1x2 subplotted scatterplots, no objects returned

    :param X: Dataframe or 2D array with original budget and schedule train data
    :param X_scaled: Dataframe or 2D array with scaled budget and schedule train data
    :param scale_descr: Short string description of scaling transformation used
                        to title scaled data plot (e.g. 'Sigmoid Standardized')
    :param X_test: Optional, Dataframe or 2D array with original test data, which
                   will plot test data as overlay with training data (default is
                   X_test=None, which does not plot any overlay)
    :param X_test_scaled: Optional, Dataframe or 2D array with original test data,
                          which plots overlay similar to X_test (default is
                          X_test_scaled=None)
    :param bdgt_col: string name of budget values column for input dataframes
                     (default bdgt_col='Budget_Start')
    :param sched_col: string name of budget values column for input dataframes
                      (default bdgt_col='Duration_Start')
    """
    corr = np.corrcoef(X.T)[0, 1]
    corr_scaled = np.corrcoef(X_scaled.T)[0, 1]

    cols = [bdgt_col, sched_col]

    # if y inputs are pandas dataframes, convert to numpy array
    if type(X) == pd.core.frame.DataFrame:
        X = X[cols].copy().values
    if type(X_scaled) == pd.core.frame.DataFrame:
        X_scaled = X_scaled[cols].copy().values
    if type(X_test) == pd.core.frame.DataFrame:
        X_test = X_test[cols].copy().values
    if type(X_test_scaled) == pd.core.frame.DataFrame:
        X_test_scaled = X_test_scaled[cols].copy().values

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    plt.suptitle(
        "Original budget and duration values vs. {} scaled values".format(
            scale_descr
        ),
        y=1,
        fontsize=18,
    )

    for i, (data, data_test) in enumerate(
        zip([X, X_scaled], [X_test, X_test_scaled])
    ):
        ax[i].scatter(
            *data.T,
            # data[bdgt_col],
            # data[sched_col],
            color="k",
            alpha=0.5,
            edgecolor="w",
            s=80,
            label="training obs"
        )
        ax[i].set_title(
            "Original data\n({:.2f} pearson coefficient)".format(corr)
            if i == 0
            else "{} scaled\n({:.2f} pearson coefficient)".format(
                scale_descr, corr_scaled
            ),
            fontsize=14,
        )
        ax[i].set_xlabel("Budget", fontsize=12)
        if i == 0:
            ax[i].set_ylabel("Duration (days)", fontsize=12)

        if np.all(X_test) is not None:
            ax[i].scatter(
                *data_test.T,
                # data_test[bdgt_col],
                # data_test[sched_col],
                color="tab:orange",
                alpha=1,
                edgecolor="w",
                marker="s",
                s=80,
                label="test obs"
            )

        ax[i].grid(":", alpha=0.4)

    ax[0].legend(fontsize=12, edgecolor="k", loc=4)
    plt.tight_layout()
    plt.show()


def plot_change_trend(trend_data, pid_data, pid, interval=None):
    """Plots 4 subplots showing project budget and duration forecast change trend

    Generates image of 4 subplots, no objects are returned.

    :param trend_data: pd.DataFrame, the cleaned dataset of all project change
                       records (i.e. 'Capital_Projects_clean.csv' dataframe)
    :param pid_data: pd.DataFrame, the prediction_interval dataframe produced
                     using this project's data generator function
                     (i.e. 'NYC_Capital_Projects_3yr.csv' dataframe)
    :param pid: integer, the PID for the project you wish to plot
    :param interval: integer or None, indicating the max Change_Year you wish
                     to plot, if None all change records are plotted for the
                     specified pid (default, interval=None)
    """
    # sets default for converting datetimes in matplotlib
    from pandas.plotting import register_matplotlib_converters
    from matplotlib.dates import YearLocator, DateFormatter

    register_matplotlib_converters()

    years = YearLocator()
    years_fmt = DateFormatter("%Y")

    def set_date_axis(ax, years, years_fmt):
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)

    # set sup_title reference fontsize
    fs = 16

    # subset project record data (results from data generator)
    pid_record = pid_data.copy().loc[pid_data["PID"] == pid]

    # subset project changes data (clean original dataset)
    changes_loc = (
        (trend_data["PID"] == pid) & (trend_data["Change_Year"] <= interval)
        if interval
        else trend_data["PID"] == pid
    )
    pid_changes = trend_data.copy().loc[changes_loc]

    # convert datetime field to correct data type
    pid_changes["Date_Reported_As_Of"] = pd.to_datetime(
        pid_changes["Date_Reported_As_Of"]
    )

    # calculate project duration array
    project_duration = pid_record["Duration_Start"].values[0] + np.cumsum(
        pid_changes["Latest_Schedule_Changes"].values
    )

    perc_bdgt_change = (
        pid_changes["Budget_Forecast"].values[-1]
        - pid_record["Budget_Start"].values[0]
    ) / pid_record["Budget_Start"].values[0]

    perc_sched_change = (
        project_duration[-1] - pid_record["Duration_Start"].values[0]
    ) / pid_record["Duration_Start"].values[0]

    # generate subplots
    fig, ax = plt.subplots(2, 2, sharex=True, figsize=(12, 6))

    plt.suptitle(
        r"""        PID {}
        {}
        Category: {}
        Borough: {}
        Original Budget: \${:.2f} million
        Original Duration: {:,.0f} days""".format(
            pid,
            pid_record["Project_Name"].values[0][:88],
            pid_record["Category"].values[0],
            pid_record["Borough"].values[0],
            pid_record["Budget_Start"].values[0] / 1e6,
            pid_record["Duration_Start"].values[0],
        ),
        fontsize=fs,
        y=1,
    )

    # plot budget forecast
    ax[0, 0].plot(
        pid_changes["Date_Reported_As_Of"],
        pid_changes["Budget_Forecast"] / 1e6,
        "ko-",
    )
    ax[0, 0].axhline(
        pid_record["Budget_Start"].values[0] / 1e6,
        color="k",
        linestyle=":",
        label="Original forecasted",
    )
    ax[0, 0].set_title(
        "Total budget forecast\n({:.2%} total change)".format(perc_bdgt_change),
        fontsize=fs - 2,
    )
    ax[0, 0].set_ylabel("USD (millions)", fontsize=fs - 4)
    ax[0, 0].legend(edgecolor="k", fontsize=fs - 6)

    # plot budget forecast percent change
    ax[1, 0].plot(
        pid_changes["Date_Reported_As_Of"],
        (
            (pid_changes["Latest_Budget_Changes"])
            / (
                pid_changes["Budget_Forecast"]
                - pid_changes["Latest_Budget_Changes"]
            ).replace(0, 1)
        )
        * 100,
        "ko-",
    )
    ax[1, 0].axhline(0, color="gray", linestyle="-", alpha=0.4)
    ax[1, 0].set_title("Percentage budget change", fontsize=fs - 2)
    ax[1, 0].set_ylabel("percent change", fontsize=fs - 4)

    ax[1, 0].set_xlabel("project change date", fontsize=fs - 4)

    # plot duration forecast
    ax[0, 1].plot(
        pid_changes["Date_Reported_As_Of"], project_duration / 1e3, "ko-"
    )
    ax[0, 1].axhline(
        pid_record["Duration_Start"].values[0] / 1e3, color="k", linestyle=":",
    )
    ax[0, 1].set_title(
        "Total forecasted project duration\n({:.2%} total change)".format(
            perc_sched_change
        ),
        fontsize=fs - 2,
    )
    ax[0, 1].set_ylabel("days (thousands)", fontsize=fs - 4)

    # plot duration change
    ax[1, 1].plot(
        pid_changes["Date_Reported_As_Of"],
        (
            pid_changes["Latest_Schedule_Changes"]
            / (
                project_duration - pid_changes["Latest_Schedule_Changes"]
            ).replace(0, 1)
        )
        * 100,
        "ko-",
    )
    ax[1, 1].axhline(0, color="gray", linestyle="-", alpha=0.4)
    ax[1, 1].set_title("Percentage duration change", fontsize=fs - 2)
    ax[1, 1].set_ylabel("percent change", fontsize=fs - 4)

    ax[1, 1].set_xlabel("project change date", fontsize=fs - 4)

    for a in ax.flat:
        a.grid(":", alpha=0.4)
        set_date_axis(a, years, years_fmt)

    plt.tight_layout()
    plt.show()


def plot_gam_by_predictor(
    model_dict, model_index, X_data, y_data, dataset="train", suptitle_y=1
):
    """Calculates and plots the partial dependence and 95% CIs for a GAM model

    Plots a set of subplots for each predictor contained in your X data. No objects
    are returned.

    :param model_dict: model dictionary containing the fitted PyGAM models
                       you wish to plot
    :param model_index: integer indicating the index of the model stored
                        in yur model_dict that you wish to plot
    :param X_data: pd.DataFrame containing the matching predictor set you
                   wish to plot beneath your predictor contribution lines
    :param y_data: pd.DataFrame containing the matching outcome set you
                   wish to plot beneath your predictor contribution lines
    :param dataset: string, 'train' or 'test' indicating the type of
                    X and y data you have entered for the X_data and
                    y_data arguments (default='train)
    :param suptitle: float > 1.00 indicating the spacing required to
                     prevent your plot from overlapping your title text
                     (default=1.04)
    """
    # reset indices to prevent index match errors
    X_data = X_data.copy().reset_index(drop=True)
    y_data = y_data.copy().reset_index(drop=True)

    idx = model_index
    model = model_dict["model"][idx]
    X_varnames = X_data.columns
    y_varname = model_dict["y_variables"][idx].replace("_", " ")
    model_desc = model_dict["description"]

    n_X_vars = len(X_varnames)
    n_rows = np.ceil(n_X_vars / 2).astype(int)

    # generate deviance residuals
    res = model.deviance_residuals(X_data, y_data.iloc[:, idx])

    # plot all predictors against price to visualize relationship
    fig, axes = plt.subplots(n_rows, 2, sharey=False, figsize=(12, 4 * n_rows))

    plt.suptitle(
        "{} predictions:\nContribution of each predictor to overall function "
        "(partial dependence and 95% CI)\n{}\n"
        "Illustrated with {} observations".format(
            y_varname.upper(),
            model_desc,
            "training" if dataset == "train" else "TEST",
        ),
        fontsize=18,
        y=suptitle_y,
    )

    for (i, ax), term in zip(enumerate(axes.flat), model.terms):
        if term.isintercept:
            continue

        XX = model.generate_X_grid(term=i)
        pdep, confi = model.partial_dependence(term=i, X=XX, width=0.95)
        pdep2, _ = model.partial_dependence(term=i, X=X_data, width=0.95)

        ax.scatter(
            X_data.iloc[:, term.feature], pdep2 + res, color="silver", alpha=1,
        )
        ax.plot(XX[:, term.feature], pdep, "k-")
        ax.plot(XX[:, term.feature], confi, c="k", ls="--")

        ax.set_title(X_varnames[i], fontsize=14)
        ax.set_xlabel("observed values", fontsize=12)
        ax.grid(":", alpha=0.4)

        if i % 2 == 0:
            ax.set_ylabel("partial dependence", fontsize=12)

    # hide all markings for final missing axes in odd number predictors
    n_fewer = n_X_vars % 2
    if n_fewer != 0:
        for pos in ["right", "top", "bottom", "left"]:
            axes[n_rows - 1, -n_fewer].spines[pos].set_visible(False)
        axes[n_rows - 1, -n_fewer].tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        axes[n_rows - 1, -n_fewer].tick_params(
            axis="y", which="both", right=False, left=False, labelleft=False
        )

    plt.tight_layout()
    plt.show()


def plot_coefficients(
    model_dict, subplots=(1, 2), fig_height=8, suptitle_spacing=1
):
    """Plots coefficients from statsmodels linear regression model

    Generates a plotted series of subplots illustrating estimated coefficients
    and 95% CIs. No objects are returned

    :param model_dict: model dictionary object from generate model dict function,
                containing fitted Statsmodels linear regression model objects
                (NOTE: this function is compatible with statsmodels models
                only)
    :type model_dict: dict
    :param subplots: to plot each of the 2 predicted y variables, provides the
                dimension of subplots for the figure
                (NOTE: currently this function is only configured to plot 2
                columns of subplots, therefore no other value other than two is
                accepted for the subplots width dimension), defaults to (1, 2)
    :type subplots: tuple
    :param fig_height: this value is passed directly to the
                ``figsize`` parameter of ``plt.subplots()`` and determines the
                overall height of your plot, defaults to 8
    :type fig_height: int or float
    :param suptitle_spacing: this value is passed to the 'y'
                parameter for ``plt.suptitle()``, defaults to 1.10
    :type suptitle_spacing: float
    """
    # plot comparison of model coefficients

    model_list = model_dict["model"]
    y_vars = model_dict["y_variables"]
    descr = model_dict["description"]

    # set values required for plotting
    coef_list = [list(model.params.values)[::-1] for model in model_list]
    feat_list = [list(model.params.index)[::-1] for model in model_list]
    ci0_list = [list(model.conf_int()[0].values)[::-1] for model in model_list]
    ci1_list = [list(model.conf_int()[1].values)[::-1] for model in model_list]

    # make plot
    fig, axes = plt.subplots(*subplots, sharey=True, figsize=(12, fig_height))

    plt.suptitle(
        "{}:\nCoefficient values and 95% confidence intervals by outcome "
        "variable".format(descr),
        fontsize=16,
        y=suptitle_spacing,
    )

    for (i, ax), y_var, coefs, features, ci0s, ci1s in zip(
        enumerate(axes.flat), y_vars, coef_list, feat_list, ci0_list, ci1_list
    ):
        if i < 9:
            ax.set_title(
                "{} Model".format(y_var.replace("_", " ")), fontsize=16
            )

            ax.axvline(0, c="r", linestyle="--", alpha=0.5)

            ax.plot(
                coefs, features, lw=0, marker="o", alpha=1, ms=10, color="k",
            )

            for ci0, ci1, feature in zip(ci0s, ci1s, features):
                ax.plot(
                    [ci0, ci1], [feature, feature], "k-", alpha=1,
                )

            ax.set_xlabel("coefficient estimate", fontsize=12)
            ax.grid(":", alpha=0.5)
            ax.tick_params("both", labelsize=11)

        if i % 2 == 0:
            ax.set_ylabel("predictor", fontsize=14)

    # hide all markings for axes if there is no corresponding subplot
    if i < np.product(subplots) - 1:
        for pos in ["right", "top", "bottom", "left"]:
            axes[subplots[0] - 1, 1].spines[pos].set_visible(False)
        axes[subplots[0] - 1, 1].tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        axes[subplots[0] - 1, 1].tick_params(
            axis="y", which="both", right=False, left=False, labelleft=False
        )

    plt.xticks(fontsize=12)
    plt.tight_layout()
    plt.show()


def load_img_to_numpy(filepath):
    """Loads an image from file, converts it to np.array and returns the array

    :param filepath: path to image file
    :type filepath: str
    :return: numpy representation of image
    :rtype: array
    """
    img = Image.open(filepath)
    img.load()
    img_array = np.asarray(img, dtype="int32")
    return img_array


def plot_jpg(filepath, title, figsize=(16, 12)):
    """Plots a jpeg image from file

    :param filepath: path to file for plotting
    :type filepath: str
    :param title: plot title text
    :type title: str
    :param figsize: dimensions of resulting plot, defaults to (16, 12)
    :type figsize: tuple
    """
    fig, ax = plt.subplots(
        figsize=figsize, subplot_kw={"xticks": [], "yticks": []}
    )

    plt.title(
        "{}\n".format(title), fontsize=18,
    )

    plt.imshow(load_img_to_numpy(filepath))
    for pos in ["right", "top", "bottom", "left"]:
        ax.spines[pos].set_visible(False)

    plt.tight_layout()
    plt.show()
