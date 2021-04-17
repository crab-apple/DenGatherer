package org.dengatherer.gatherer

import java.math.BigDecimal

/**
 * Parses a decimal number string with up to two fractional digits, optionally with thousands separators,
 * and allowing for both dot and comma as thousands or fraction separators.
 *
 * The intended usage for this method is to parse scraped strings indicating either rent prices or surfaces
 * in square meters, which never seem to use more than two fractional digits.
 */
fun parseUpToTwoFractionalDigits(input: String): BigDecimal {

    val matchingRegex = listOf(
        SeparatorOption(',', '.'),
        SeparatorOption('.', ','),
    ).flatMap { separators ->
        listOf(
            Regex("""^(?<integer>(\d+))(?<fractional>[${separators.fraction}]\d{1,2})?$"""),
            Regex("""^(?<integer>(\d{1,3}([${separators.thousands}]\d{3})*))(?<fractional>[${separators.fraction}]\d{1,2})?$"""),
        )
    }.firstOrNull { input.matches(it) } ?: throw IllegalArgumentException()

    val result = matchingRegex.matchEntire(input)!!

    val integerPart = result.groups["integer"]!!.value
    val fractionalPart = result.groups["fractional"]?.value?.drop(1)

    val integerWithoutSeparators = integerPart
        .replace(",", "")
        .replace(".", "")

    if (fractionalPart == null) {
        return integerWithoutSeparators.toBigDecimal()
    }

    return (integerWithoutSeparators + fractionalPart).toBigDecimal().movePointLeft(fractionalPart.length)
}

private data class SeparatorOption(val thousands: Char, val fraction: Char)

