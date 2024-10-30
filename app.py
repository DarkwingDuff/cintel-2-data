import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny.express import output, render, ui
import palmerpenguins
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget

penguins_df = palmerpenguins.load_penguins()
print(penguins_df)

data = penguins_df


ui.page_opts(title="Filling layout", fillable=True)
with ui.layout_columns():

    with ui.card():

        @render_plotly
        def plot1():
            return px.histogram(px.data.tips(), y="tip")

    with ui.card():

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
        selected_species = input.selected_species_list()
        filtered_df = penguins_df[penguins_df['species'].isin(selected_species)]
        fig = px.scatter(
            filtered_df,
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            title="Scatter Plot of Penguin Bill Dimensions"
        )
        return fig
