package org.dengatherer.gatherer

import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.`is`
import org.junit.jupiter.api.DynamicTest
import org.junit.jupiter.api.DynamicTest.dynamicTest
import org.junit.jupiter.api.TestFactory
import org.junit.jupiter.api.assertThrows
import java.math.BigDecimal

internal class DecimalParserTest {

    @TestFactory
    fun `parses integers without thousands separator`(): List<DynamicTest> {
        return `test parse up to two fractional digits`(
            "1" to BigDecimal.ONE,
            "0" to BigDecimal.ZERO,
            "12" to BigDecimal.valueOf(12),
            "1234" to BigDecimal.valueOf(1234),
        )
    }

    @TestFactory
    fun `parses integers with thousands separator`(): List<DynamicTest> {
        return `test parse up to two fractional digits`(
            "1,000" to BigDecimal.valueOf(1000),
            "1.000" to BigDecimal.valueOf(1000),
            "1,234,567" to BigDecimal.valueOf(1234567),
            "1.234.567" to BigDecimal.valueOf(1234567),
            "12.345.678" to BigDecimal.valueOf(12345678),
        )
    }

    @TestFactory
    fun `parses decimals with two fractional digits`(): List<DynamicTest> {
        return `test parse up to two fractional digits`(
            "1.23" to "1.23".toBigDecimal(),
            "1,23" to "1.23".toBigDecimal(),
            "1000,23" to "1000.23".toBigDecimal(),
            "1.000,23" to "1000.23".toBigDecimal(),
            "1000.23" to "1000.23".toBigDecimal(),
            "1,000.23" to "1000.23".toBigDecimal(),
        )
    }

    @TestFactory
    fun `parses decimals with one fractional digit`(): List<DynamicTest> {
        return `test parse up to two fractional digits`(
            "1.2" to "1.2".toBigDecimal(),
            "1,2" to "1.2".toBigDecimal(),
            "1000,2" to "1000.2".toBigDecimal(),
            "1.000,2" to "1000.2".toBigDecimal(),
            "1000.2" to "1000.2".toBigDecimal(),
            "1,000.2" to "1000.2".toBigDecimal(),
        )
    }

    @TestFactory
    fun `doesn't accept more than two fractional digits`(): List<DynamicTest> {
        return listOf(
            "1.2345",
            "1,2345",
            "1.234,567",
            "1,234.567",
        ).map { input ->
            dynamicTest("\"$input\" → throws") {
                assertThrows<IllegalArgumentException> { parseUpToTwoFractionalDigits(input) }
            }
        }
    }

    private fun `test parse up to two fractional digits`(vararg params: Pair<String, BigDecimal>): List<DynamicTest> {
        return params.toList().map { (input, expected) ->
            dynamicTest("\"$input\" → $expected") {
                assertThat(parseUpToTwoFractionalDigits(input), `is`(expected))
            }
        }
    }
}