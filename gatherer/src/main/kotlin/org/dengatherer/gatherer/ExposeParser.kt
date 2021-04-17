package org.dengatherer.gatherer

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

class ExposeParser {

    fun parse(exposeJson: String): Expose {
        val json = Json { ignoreUnknownKeys = true }
        val dto = json.decodeFromString(ExposeDTO.serializer(), exposeJson)
        return Expose(
            dto.id,
            dto.image,
            dto.url,
            dto.title,
            parseUpToTwoFractionalDigits(dto.rooms),
            parseUpToTwoFractionalDigits(words(dto.price).first()),
            parseUpToTwoFractionalDigits(words(dto.size).first()),
            dto.address,
            dto.crawler,
        )
    }

    private fun words(input: String): List<String> {
        return input.split(Regex("\\s")).filterNot { it.isEmpty() }
    }
}

@Serializable
private class ExposeDTO(
    val id: Int,
    val image: String,
    val url: String,
    val title: String,
    val rooms: String,
    val price: String,
    val size: String,
    val address: String,
    val crawler: String,
)