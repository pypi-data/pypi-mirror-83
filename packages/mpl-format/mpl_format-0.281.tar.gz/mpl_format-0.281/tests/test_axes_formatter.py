from unittest.case import TestCase

from pandas import Series

from mpl_format.axes import AxesFormatter


class TestAxesFormatter(TestCase):

    def setUp(self) -> None:

        self.data = Series({
            1000: 3, 2000: 5, 3000: 4, 4000: 6, 5000: 5
        })
        self.pct_data = Series({
            0.1: 3, 0.2: 5, 0.3: 4, 0.4: 6, 0.5: 5
        })

    def test_set_format_integer_bar(self):

        axf = AxesFormatter()
        self.data.plot.bar(ax=axf.axes)
        axf.x_axis.set_format_integer(categorical=True)
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['1,000', '2,000', '3,000', '4,000', '5,000']
        self.assertListEqual(expected, actual)

    def test_set_format_integer_line(self):

        axf = AxesFormatter()
        self.data.plot.line(ax=axf.axes)
        axf.x_axis.set_format_integer()
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['500', '1,000', '1,500', '2,000', '2,500',
                    '3,000', '3,500', '4,000', '4,500', '5,000', '5,500']
        self.assertListEqual(expected, actual)

    def test_set_format_currency_bar(self):

        axf = AxesFormatter()
        self.data.plot.bar(ax=axf.axes)
        axf.x_axis.set_format_currency(categorical=True)
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['$1,000', '$2,000', '$3,000', '$4,000', '$5,000']
        self.assertListEqual(expected, actual)

    def test_set_format_currency_line(self):

        axf = AxesFormatter()
        self.data.plot.line(ax=axf.axes)
        axf.x_axis.set_format_currency()
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['$500', '$1,000', '$1,500', '$2,000', '$2,500',
                    '$3,000', '$3,500', '$4,000', '$4,500', '$5,000', '$5,500']
        self.assertListEqual(expected, actual)

    def test_set_format_percent_bar(self):

        axf = AxesFormatter()
        self.pct_data.plot.bar(ax=axf.axes)
        axf.x_axis.set_format_percent(categorical=True)
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['10%', '20%', '30%', '40%', '50%']
        self.assertListEqual(expected, actual)

    def test_set_format_percent_line(self):

        axf = AxesFormatter()
        self.pct_data.plot.line(ax=axf.axes)
        axf.x_axis.set_format_percent()
        axf.show()
        actual = [t.get_text() for t in axf.x_axis.axis.get_ticklabels()]
        expected = ['5%', '10%', '15%', '20%', '25%',
                    '30%', '35%', '40%', '45%', '50%', '55%']
        self.assertListEqual(expected, actual)
