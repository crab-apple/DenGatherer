package org.dengatherer.gatherer

import kotlinx.serialization.Serializable

@Serializable
class ExposeDTO(
    private val id: Int,
    private val image: String,
    private val url: String,
    private val title: String,
    private val rooms: String,
    private val price: String,
    private val size: String,
    private val address: String,
    private val crawler: String
) {
    fun toExpose(): Expose {
        return Expose(
            id,
            image,
            url,
            title,
            parseUpToTwoFractionalDigits(rooms),
            parseUpToTwoFractionalDigits(words(price).first()),
            parseUpToTwoFractionalDigits(words(size).first()),
            address,
            crawler,
        )
    }

    private fun words(input: String): List<String> {
        return input.split(Regex("\\s")).filterNot { it.isEmpty() }
    }
}