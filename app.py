from functools import cache

import polars as pl
from fasthtml.common import H2, Card, Div, Form, Grid, Input, Main, Title, H1, fast_app
from great_tables import GT, html
from great_tables.data import sza

from ft_gt import gt2fasthtml

app, rt = fast_app()


@cache
def get_sza_pivot():
    return (
        pl.from_pandas(sza)
        .filter((pl.col("latitude") == "20") & (pl.col("tst") <= "1200"))
        .select(pl.col("*").exclude("latitude"))
        .drop_nulls()
        .pivot(values="sza", index="month", on="tst", sort_columns=True)
    )


@gt2fasthtml(id="gt")
def get_gtbl(color1: str = "#663399", color2: str = "#FFA500"):
    return (
        GT(get_sza_pivot(), rowname_col="month")
        .data_color(
            domain=[90, 0],
            palette=[color1, "white", color2],
            na_color="white",
        )
        .tab_header(
            title="Solar Zenith Angles from 05:30 to 12:00",
            subtitle=html("Average monthly values at latitude of 20&deg;N."),
        )
        .sub_missing(missing_text="")
    )


@app.post("/submit")
def post(d: dict):
    return get_gtbl(**d)


@app.get("/")
def homepage():
    return (
        Title("FastHTML-GT Website"),
        H1("Great Tables shown in FastHTML", style="text-align:center"),
        Main(
            Form(
                hx_post="/submit",
                hx_target="#gt",
                hx_trigger="input",
                hx_swap="outerHTML",
            )(
                Grid(
                    Div(),
                    Card(
                        H2("Color1"), Input(type="color",
                                            id="color1", value="#663399")
                    ),
                    Card(
                        H2("Color2"), Input(type="color",
                                            id="color2", value="#FFA500")
                    ),
                    Div(),
                )
            ),
            get_gtbl(),
            cls="container",
        ),
    )
