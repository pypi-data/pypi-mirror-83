###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import sys
import matplotlib.pyplot as plt
import numpy as np
import time as time

from FinTestCases import FinTestCases, globalTestCaseMode

from financepy.finutils.FinDate import FinDate
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinCalendar import FinCalendarTypes
from financepy.products.funding.FinIborFRA import FinIborFRA
from financepy.products.funding.FinIborFuture import FinIborFuture
from financepy.products.funding.FinIborDeposit import FinIborDeposit
from financepy.products.funding.FinIborSwap import FinIborSwap
from financepy.finutils.FinCalendar import FinBusDayAdjustTypes
from financepy.market.curves.FinInterpolate import FinInterpTypes
from financepy.finutils.FinMath import ONE_MILLION
from financepy.finutils.FinGlobalTypes import FinSwapTypes
from financepy.market.curves.FinInterpolate import FinInterpTypes

from financepy.products.funding.FinIborSingleCurve import FinIborSingleCurve
from financepy.products.funding.FinIborDualCurve import FinIborDualCurve
from financepy.products.funding.FinOISCurve import FinOISCurve



sys.path.append("..//..")

testCases = FinTestCases(__file__, globalTestCaseMode)

PLOT_GRAPHS = False

###############################################################################

def buildOIS(valuationDate):
    ''' Build the OIS funding curve from futures (FRAs) and OIS '''

    dccType = FinDayCountTypes.THIRTY_E_360_ISDA
    depos = []

    spotDays = 0
    spotDays = 0
    settlementDate = valuationDate.addWeekDays(spotDays)
    swapType = FinSwapTypes.PAYER

    fras = []
    # 1 x 4 FRA
    
    swaps = []
    fixedFreqType = FinFrequencyTypes.SEMI_ANNUAL
    fixedDCCType = FinDayCountTypes.ACT_365F

    # swapRate = 0.000022
    # maturityDate = settlementDate.addMonths(24)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                         fixedFreqType, fixedDCCType)
    # swaps.append(swap)

    # swapRate += 0.000
    # swapType = FinSwapTypes.PAYER
    # maturityDate = settlementDate.addMonths(36)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType, fixedDCCType)
    # swaps.append(swap)

    # swapRate += 0.000
    # maturityDate = settlementDate.addMonths(48)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    swapRate = 0.000
    maturityDate = settlementDate.addMonths(60)
    swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
                        fixedFreqType,
                        fixedDCCType)
    swaps.append(swap)

    # maturityDate = settlementDate.addMonths(72)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(84)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(96)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(108)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate, 
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(120)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(132)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(144)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(180)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(240)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(300)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    # maturityDate = settlementDate.addMonths(360)
    # swap = FinIborSwap(settlementDate, maturityDate, swapType, swapRate,
    #                     fixedFreqType,
    #                     fixedDCCType)
    # swaps.append(swap)

    oisCurve = FinOISCurve(valuationDate,
                           [],
                           fras,
                           swaps)

    return oisCurve

###############################################################################


def test_bloombergPricingExample():

    ''' This is an example of a replication of a BBG example from
    https://github.com/vilen22/curve-building/blob/master/Bloomberg%20Curve%20Building%20Replication.xlsx

    '''
    valuationDate = FinDate(6, 6, 2018)

    # We do the O/N rate which settles on trade date
    spotDays = 0
    settlementDate = valuationDate.addWeekDays(spotDays)
    depoDCCType = FinDayCountTypes.ACT_360
    depos = []
    depositRate = 0.0231381
    maturityDate = settlementDate.addMonths(3)
    depo = FinIborDeposit(settlementDate, maturityDate, depositRate,
                           depoDCCType)
    depos.append(depo)

    futs = []
    fut = FinIborFuture(valuationDate, 1); futs.append(fut)
    fut = FinIborFuture(valuationDate, 2); futs.append(fut)
    fut = FinIborFuture(valuationDate, 3); futs.append(fut)
    fut = FinIborFuture(valuationDate, 4); futs.append(fut)
    fut = FinIborFuture(valuationDate, 5); futs.append(fut)
    fut = FinIborFuture(valuationDate, 6); futs.append(fut)

    fras = [None]*6
    fras[0] = futs[0].toFRA(97.6675, -0.00005)
    fras[1] = futs[1].toFRA(97.5200, -0.00060)
    fras[2] = futs[2].toFRA(97.3550, -0.00146)
    fras[3] = futs[3].toFRA(97.2450, -0.00263)
    fras[4] = futs[4].toFRA(97.1450, -0.00411)
    fras[5] = futs[5].toFRA(97.0750, -0.00589)

    accrual = FinDayCountTypes.THIRTY_E_360
    freq = FinFrequencyTypes.SEMI_ANNUAL

    spotDays = 2
    settlementDate = valuationDate.addWeekDays(spotDays)
    notional = ONE_MILLION
    swapType = FinSwapTypes.PAYER

    swaps = []
    swap = FinIborSwap(settlementDate, "2Y", swapType, (2.77417+2.77844)/200, freq, accrual, notional); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "3Y", swapType, (2.86098+2.86582)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "4Y", swapType, (2.90240+2.90620)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "5Y", swapType, (2.92944+2.92906)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "6Y", swapType, (2.94001+2.94499)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "7Y", swapType, (2.95352+2.95998)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "8Y", swapType, (2.96830+2.97400)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "9Y", swapType, (2.98403+2.98817)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "10Y", swapType, (2.99716+3.00394)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "11Y", swapType, (3.01344+3.01596)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "12Y", swapType, (3.02276+3.02684)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "15Y", swapType, (3.04092+3.04508)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "20Y", swapType, (3.04417+3.05183)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "25Y", swapType, (3.03219+3.03621)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "30Y", swapType, (3.01030+3.01370)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "40Y", swapType, (2.96946+2.97354)/200, freq, accrual); swaps.append(swap)
    swap = FinIborSwap(settlementDate, "50Y", swapType, (2.91552+2.93748)/200, freq, accrual); swaps.append(swap)

    liborCurve = FinIborSingleCurve(valuationDate, depos, fras, swaps,
                                    FinInterpTypes.LINEAR_SWAP_RATES,
                                    True)
#    print(liborCurve)

    principal = 0.0

    testCases.banner("======================================================")
    testCases.banner("SINGLE CURVE VALUATION")
    testCases.header("LABEL", "VALUE")
    testCases.print("VALUE:", swaps[0].value(valuationDate, liborCurve, liborCurve, None, principal))
    testCases.print("FIXED:", swaps[0].fixedLegValue(valuationDate, liborCurve, principal))
    testCases.print("FLOAT:", swaps[0].floatLegValue(valuationDate, liborCurve, liborCurve, None, principal))

    testCases.banner("======================================================")
    testCases.banner("SINGLE CURVE VALUATION TO SWAP SETTLEMENT DATE")
    testCases.header("LABEL", "VALUE")
    testCases.print("VALUE:", swaps[0].value(settlementDate, liborCurve, liborCurve, None, principal))
    testCases.print("FIXED:", swaps[0].fixedLegValue(settlementDate, liborCurve, principal))
    testCases.print("FLOAT:", swaps[0].floatLegValue(settlementDate, liborCurve, liborCurve, None, principal))
    testCases.banner("======================================================")

#    swaps[0].printFixedLegPV()
#    swaps[0].printFloatLegPV()

    oisCurve = buildOIS(valuationDate)
#    print(oisCurve)

    liborDualCurve = FinIborDualCurve(valuationDate, oisCurve, depos, fras, swaps,
                                      FinInterpTypes.LINEAR_SWAP_RATES, True)
#    print(liborDualCurve) 
    
    # The valuation of 53714.55 is very close to the spreadsheet value 53713.96

    testCases.header("VALUATION TO TODAY DATE"," PV")
    testCases.print("VALUE:", swaps[0].value(valuationDate, oisCurve, liborDualCurve, None, principal))
    testCases.print("FIXED:", swaps[0].fixedLegValue(valuationDate, oisCurve, principal))
    testCases.print("FLOAT:", swaps[0].floatLegValue(valuationDate, oisCurve, liborCurve, None, principal))

    testCases.header("VALUATION TO SWAP SETTLEMENT DATE"," PV")
    testCases.print("VALUE:", swaps[0].value(settlementDate, oisCurve, liborDualCurve, None, principal))
    testCases.print("FIXED:", swaps[0].fixedLegValue(settlementDate, oisCurve, principal))
    testCases.print("FLOAT:", swaps[0].floatLegValue(settlementDate, oisCurve, liborDualCurve, None, principal))

#    swaps[0].printFixedLegPV()
#    swaps[0].printFloatLegPV()

    PLOT = False
    if PLOT is True:

        years = np.linspace(0, 5, 21)
        dates = settlementDate.addYears(years)
    
        singleCurveFwds = liborCurve.fwd(dates)    
        plt.plot(years, singleCurveFwds, label="Single Libor Curve")
 
        oisCurveFwds = oisCurve.fwd(dates)    
        plt.plot(years, oisCurveFwds, label="OIS Curve")

        indexCurveFwds = liborDualCurve.fwd(dates)    
        plt.plot(years, indexCurveFwds, label="Libor Index Curve")
        
        plt.legend()
    
    # swaps[0].printFixedLegPV()
    # swaps[0].printFloatLegPV()

###############################################################################


test_bloombergPricingExample()

testCases.compareTestCases()
