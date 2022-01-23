package org.dengatherer.gatherer

import org.springframework.data.mongodb.core.mapping.Field
import java.time.Instant

data class Availability(

    @Field("dateReceived")
    val dateReceived: Instant,

    @Field("lastSeenUp")
    val lastSeenUp: Instant?,

    @Field("firstSeenDown")
    val firstSeenDown: Instant?,
) {

    companion object {
        fun new(dateReceived: Instant) = Availability(dateReceived, null, null)
    }
}

