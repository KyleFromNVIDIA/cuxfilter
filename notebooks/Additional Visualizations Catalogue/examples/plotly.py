import cudf
import cupy as cp
import numpy as np
import pandas as pd
import panel as pn

from . import PlotBase

pn.extension("plotly")


class Charts(PlotBase):
    def bar_plot(self):
        exec(f"import {self.dtype}")
        import plotly.express as px

        df_lib = cudf if self.dtype == "cudf" else pd
        arr_lib = cp if self.dtype == "cudf" else np
        rand_arr = arr_lib.random.randint(0, 20, self.n)
        rand_vals = df_lib.Series(rand_arr).value_counts()
        df = df_lib.DataFrame(
            {
                "value": df_lib.Series(rand_vals.index),
                "freq": rand_vals,
            }
        )
        # Plotly does not take cuDF directly, convert cudf dataframe to pandas df
        df = df.to_pandas() if type(df) == cudf.DataFrame else df

        # generate Plotly bar chart
        fig = px.bar(df, x="value", y="freq")
        return pn.panel(fig)

    def points_plot(self):
        import plotly.express as px
        from examples.dataset import generate_random_points

        df = generate_random_points(nodes=self.n, dtype=self.dtype)
        # Plotly does not take cuDF directly, convert cudf dataframe to pandas df
        df = df.to_pandas() if type(df) == cudf.DataFrame else df

        # Create scatter chart
        fig = px.scatter(
            df,
            x="x",
            y="y",
            color="cluster",
        )
        return pn.panel(fig)

    def curve_plot(self):
        # Load additional libraries Plotly
        import plotly.express as px
        from examples.dataset import generate_random_points

        df = generate_random_points(
            nodes=self.n, dtype=self.dtype
        ).sort_values(by="x")
        # Plotly does not take cuDF directly, convert cudf dataframe to pandas df
        df = df.to_pandas() if type(df) == cudf.DataFrame else df

        # Create and combine multiple line charts
        fig = px.line(df, x="x", y="y")
        return pn.panel(fig)
