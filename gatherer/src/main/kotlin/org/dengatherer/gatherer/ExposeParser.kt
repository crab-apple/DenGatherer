package org.dengatherer.gatherer

import kotlinx.serialization.json.Json

class ExposeParser {

    fun parse(exposeJson: String): Expose {
        val json = Json { ignoreUnknownKeys = true }
        return json.decodeFromString(ExposeDTO.serializer(), exposeJson)
            .toExpose()
    }

}

