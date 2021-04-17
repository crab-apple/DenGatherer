package org.dengatherer.gatherer

import java.math.BigDecimal

class Expose(
    val id: Int,
    val image: String,
    val url: String,
    val title: String,
    val rooms: BigDecimal,
    val price: BigDecimal,
    val size: BigDecimal,
    val address: String,
    val crawler: String,
)
