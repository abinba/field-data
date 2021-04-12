from lighthouse import GooglePageAnalysis


def test_lighthouse_report():
    lighthouse = GooglePageAnalysis('https://zappos.com')
    lighthouse.get_report()

    assert lighthouse.report != {}
