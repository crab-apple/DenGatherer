package org.dengatherer.gatherer

import org.springframework.stereotype.Service

@Service
class ExposeDAO {

    private val exposes = mutableMapOf<String, Expose>()

    fun getAllExposes(): List<Expose> = exposes.values.toList()

    fun addIfNotExists(expose: Expose) {
        exposes.putIfAbsent(expose.id, expose)
    }

    fun clearExposes() {
        exposes.clear()
    }
}