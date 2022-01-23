package org.dengatherer.gatherer

import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document
import org.springframework.data.mongodb.core.mapping.Field
import java.math.BigDecimal
import java.time.Instant

@Document("exposes")
data class Expose(

    @Id
    val id: String,

    @Field("source")
    val source: String,

    @Field("url")
    val url: String,

    @Field("provider")
    val provider: String?,

    @Field("imageUrl")
    val imageUrl: String?,

    @Field("title")
    val title: String,

    @Field("address")
    val address: String?,

    @Field("district")
    val district: String?,

    @Field("locationLat")
    val locationLat: Double?,

    @Field("locationLong")
    val locationLong: Double?,

    @Field("size")
    val size: BigDecimal,

    @Field("rooms")
    val rooms: BigDecimal?,

    @Field("coldRent")
    val coldRent: BigDecimal,

    @Field("comments")
    val comments: String?,

    @Field("originalData")
    val originalData: String?,

    @Field("dateReceived")
    val dateReceived: Instant,
)
