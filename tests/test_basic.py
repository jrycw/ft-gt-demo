import fastcore

from ft_gt import gt2fasthtml


def test_dec_without_parentheses(gtbl):
    @gt2fasthtml  # gt2fasthtml, without parentheses
    def get_gtbl():
        return gtbl

    div_comp = get_gtbl()

    assert isinstance(div_comp, fastcore.xml.FT)


def test_dec_with_parentheses(gtbl):
    @gt2fasthtml()  # gt2fasthtml(), with parentheses
    def get_gtbl():
        return gtbl

    div_comp = get_gtbl()

    assert isinstance(div_comp, fastcore.xml.FT)


def test_dec_with_div_kwargs(gtbl):
    @gt2fasthtml(id="gt")
    def get_gtbl():
        return gtbl

    div_comp = get_gtbl()

    assert isinstance(div_comp, fastcore.xml.FT)
    assert div_comp.attrs["id"] == "gt"


def test_func_with_parentheses(gtbl):
    def get_gtbl():
        return gtbl

    get_gtbl = gt2fasthtml(get_gtbl)
    div_comp = get_gtbl()

    assert isinstance(div_comp, fastcore.xml.FT)


def test_func_with_div_kwargs(gtbl):
    def get_gtbl():
        return gtbl

    get_gtbl = gt2fasthtml(get_gtbl, id="gt")
    div_comp = get_gtbl()

    assert isinstance(div_comp, fastcore.xml.FT)
    assert div_comp.attrs["id"] == "gt"
