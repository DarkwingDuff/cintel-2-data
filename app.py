from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny.express import output, render, ui
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget
import seaborn as sns
import matplotlib.pyplot as plt
import palmerpenguins
import plotly.express as px
from io import BytesIO
import base64

penguins_df = palmerpenguins.load_penguins()
print(penguins_df)

data = penguins_df


ui.page_opts(title="Filling layout", fillable=True, class_="scrollable")

with ui.layout_columns(class_="scrollable"):

    with ui.card(class_="scrollable"):

        @render_plotly
        def plot1():
            return px.histogram(px.data.tips(), y="tip")

    with ui.card(class_="scrollable"):

        @render_plotly
        def plot2():
            return px.histogram(px.data.tips(), y="total_bill")


with ui.layout_columns():
    with ui.card():

        @render.data_frame
        def plot3():
            return render.DataTable(data, selection_mode="row")

    with ui.card():

        @render.data_frame
        def plot4():
            return render.DataGrid(data, selection_mode="row")


with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Penguin Metric",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_numeric("plotly_bin_count", "Number of Bins", 50)
    ui.input_slider("seaborn_bin_count", "Seaborn Bins", 0, 100, 50)
    ui.input_checkbox_group(
        "Selected_Species_List",
        "Species Selection",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    ui.hr()
    ui.a(
        "Github",
        href="https://github.com/DarkwingDuff/cintel-02-data/tree/main",
        target="_blank",
    )

with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_widget
    def scatter_plot():
        selected_species = input.Selected_Species_List()
        selected_attribute = input.selected_attribute()
        filtered_df = penguins_df[penguins_df["species"].isin(selected_species)]
        fig = px.scatter(
            filtered_df,
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            title="Scatter Plot of Penguin Bill Dimensions",
        )
        return fig


with ui.layout_columns():
    with ui.card(full_screen=True):

        @output
        @render.ui
        def seaborn_histogram():
            # Reactive inputs
            selected_attribute = input.selected_attribute()
            bin_count = input.seaborn_bin_count()

            # Filter the data based on species selection
            selected_species = input.Selected_Species_List()
            filtered_df = penguins_df[penguins_df["species"].isin(selected_species)]

            # Create the Seaborn histogram plot
            plt.figure(figsize=(8, 6))
            sns.histplot(
                filtered_df[selected_attribute].dropna(), bins=bin_count, kde=True
            )
            plt.xlabel(selected_attribute)
            plt.title(f"Seaborn Histogram of {selected_attribute}")

            # Save plot to a bytes buffer and encode as base64
            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close()
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode("utf-8")

            # Return the base64-encoded image as an HTML <img> tag
            return ui.HTML(f'<img src="data:image/png;base64,{image_base64}" />')
