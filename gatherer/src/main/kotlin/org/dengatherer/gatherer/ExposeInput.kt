package org.dengatherer.gatherer

import java.math.BigDecimal

data class ExposeInput(
    val id: String,
    val source: String,
    val url: String,
    val provider: String?,
    val imageUrl: String?,
    val title: String,
    val address: String?,
    val district: String?,
    val locationLat: Double?,
    val locationLong: Double?,
    val size: BigDecimal,
    val rooms: BigDecimal?,
    val coldRent: BigDecimal,
    val comments: String?,
    val originalData: String?,
)
