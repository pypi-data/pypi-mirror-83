###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

# TODO Set up test cases correctly

from FinTestCases import FinTestCases, globalTestCaseMode
from financepy.finutils.FinCalendar import FinDateGenRuleTypes
from financepy.finutils.FinCalendar import FinBusDayAdjustTypes
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinCalendar import FinCalendarTypes
from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinDate import FinDate


from financepy.products.bonds.FinBondAnnuity import FinBondAnnuity

testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinBondAnnuity():

    settlementDate = FinDate(20, 6, 2018)

    #   print("==============================================================")
    #   print("SEMI-ANNUAL FREQUENCY")
    #   print("==============================================================")

    maturityDate = FinDate(20, 6, 2019)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.SEMI_ANNUAL
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    basisType = FinDayCountTypes.ACT_360
    face = 1000000

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

#    print("===============================================================")
#    print("QUARTERLY FREQUENCY")
#    print("===============================================================")

    maturityDate = FinDate(20, 6, 2028)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.SEMI_ANNUAL
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    basisType = FinDayCountTypes.ACT_360

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

#    print("==================================================================")
#    print("MONTHLY FREQUENCY")
#    print("==================================================================")

    maturityDate = FinDate(20, 6, 2028)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.MONTHLY
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    basisType = FinDayCountTypes.ACT_360

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

#    print("==================================================================")
#    print("FORWARD GEN")
#    print("==================================================================")

    maturityDate = FinDate(20, 6, 2028)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.ANNUAL
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.FORWARD
    basisType = FinDayCountTypes.ACT_360

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

#    print("==================================================================")
#    print("BACKWARD GEN WITH SHORT END STUB")
#    print("==================================================================")

    maturityDate = FinDate(20, 6, 2028)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.ANNUAL
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.FORWARD
    basisType = FinDayCountTypes.ACT_360

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

#    print("==================================================================")
#    print("FORWARD GEN WITH LONG END STUB")
#    print("==================================================================")

    maturityDate = FinDate(20, 6, 2028)
    coupon = 0.05
    frequencyType = FinFrequencyTypes.SEMI_ANNUAL
    calendarType = FinCalendarTypes.WEEKEND
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.FORWARD
    basisType = FinDayCountTypes.ACT_360

    annuity = FinBondAnnuity(
        maturityDate,
        coupon,
        frequencyType,
        calendarType,
        busDayAdjustType,
        dateGenRuleType,
        basisType,
        face)

    annuity.calculateFlowDatesPayments(settlementDate)

    testCases.header("Date", "Flow")
    numFlows = len(annuity._flowDates)
    for i in range(1, numFlows):
        dt = annuity._flowDates[i]
        flow = annuity._flowAmounts[i]
        testCases.print(dt, flow)

##########################################################################


test_FinBondAnnuity()
testCases.compareTestCases()
