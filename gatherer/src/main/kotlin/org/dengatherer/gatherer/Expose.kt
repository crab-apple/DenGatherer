package org.dengatherer.gatherer

import kotlinx.serialization.Serializable

@Serializable
class Expose(
    val id: Int,
    val image: String,
    val url: String,
    val title: String,
    val address: String,
    val crawler: String
) {
}