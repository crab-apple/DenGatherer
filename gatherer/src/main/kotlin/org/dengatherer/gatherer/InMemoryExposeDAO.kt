package org.dengatherer.gatherer

import org.springframework.context.annotation.Profile
import org.springframework.stereotype.Service

@Service
@Profile("test")
class InMemoryExposeDAO : ExposeDAO {

    private val exposes = mutableMapOf<String, Expose>()

    override fun getAllExposes(): List<Expose> = exposes.values.toList()

    override fun addIfNotExists(expose: Expose) {
        exposes.putIfAbsent(expose.id, expose)
    }

    fun clearExposes() {
        exposes.clear()
    }
}