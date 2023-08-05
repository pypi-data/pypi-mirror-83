###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

from FinTestCases import FinTestCases, globalTestCaseMode


from financepy.products.fx.FinFXForward import FinFXForward
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinCalendar import FinCalendarTypes
from financepy.products.funding.FinIborSingleCurve import FinIborSingleCurve
from financepy.products.funding.FinIborDeposit import FinIborDeposit

from financepy.finutils.FinDate import FinDate
import sys
sys.path.append("..//..")

testCases = FinTestCases(__file__, globalTestCaseMode)

##########################################################################


def test_FinFXForward():

    #  https://stackoverflow.com/questions/48778712
    #  /fx-vanilla-call-price-in-quantlib-doesnt-match-bloomberg

    valueDate = FinDate(13, 2, 2018)
    expiryDate = valueDate.addMonths(12)
    # Forward is on EURUSD which is expressed as number of USD per EUR
    # ccy1 = EUR and ccy2 = USD
    forName = "EUR"
    domName = "USD"
    currencyPair = forName + domName  # Always ccy1ccy2
    spotFXRate = 1.300  # USD per EUR
    strikeFXRate = 1.365  # USD per EUR
    ccy1InterestRate = 0.02  # USD Rates
    ccy2InterestRate = 0.05  # EUR rates

    ###########################################################################

    spotDays = 0
    settlementDate = valueDate.addWeekDays(spotDays)
    maturityDate = settlementDate.addMonths(12)
    notional = 100.0
    calendarType = FinCalendarTypes.TARGET

    depos = []
    fras = []
    swaps = []
    depositRate = ccy1InterestRate
    depo = FinIborDeposit(settlementDate, maturityDate, depositRate,
                           FinDayCountTypes.ACT_360, notional, calendarType)
    depos.append(depo)
    forDiscountCurve = FinIborSingleCurve(settlementDate, depos, fras, swaps)

    depos = []
    fras = []
    swaps = []
    depositRate = ccy2InterestRate
    depo = FinIborDeposit(settlementDate, maturityDate, depositRate,
                           FinDayCountTypes.ACT_360, notional, calendarType)
    depos.append(depo)
    domDiscountCurve = FinIborSingleCurve(settlementDate, depos, fras, swaps)

    notional = 100.0
    notionalCurrency = forName

    fxForward = FinFXForward(expiryDate,
                             strikeFXRate,
                             currencyPair,
                             notional,
                             notionalCurrency)

    testCases.header("SPOT FX", "FX FWD", "VALUE_BS")

    fwdValue = fxForward.value(valueDate, spotFXRate,
                               domDiscountCurve, forDiscountCurve)

    fwdFXRate = fxForward.forward(valueDate, spotFXRate,
                                  domDiscountCurve,
                                  forDiscountCurve)

    testCases.print(spotFXRate, fwdFXRate, fwdValue)

###############################################################################


test_FinFXForward()
testCases.compareTestCases()
