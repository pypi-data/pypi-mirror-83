###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

from FinTestCases import FinTestCases, globalTestCaseMode

from financepy.finutils.FinDate import FinDate
from financepy.finutils.FinDayCount import FinDayCount, FinDayCountTypes
import sys
sys.path.append("..//..")


testCases = FinTestCases(__file__, globalTestCaseMode)


def test_FinDayCount():

    testCases.header("DAY_COUNT_METHOD", "START", "END", "ALPHA")

    for dayCountMethod in FinDayCountTypes:

        startDate = FinDate(2019, 1, 1)
        nextDate = startDate
        numDays = 20
        dayCount = FinDayCount(dayCountMethod)

        for _ in range(0, numDays):
            nextDate = nextDate.addDays(7)
            dcf = dayCount.yearFrac(startDate, nextDate, nextDate, 1)

            testCases.print(
                str(dayCountMethod),
                str(startDate),
                str(nextDate),
                dcf[0])


test_FinDayCount()
testCases.compareTestCases()
