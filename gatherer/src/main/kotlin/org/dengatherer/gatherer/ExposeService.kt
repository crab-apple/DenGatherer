package org.dengatherer.gatherer

import org.springframework.stereotype.Service

@Service
class ExposeService {

    private val exposes = mutableListOf<Expose>()

    fun getAllExposes(): List<Expose> = exposes

    fun notifyExpose(expose: Expose) {
        exposes.add(expose)
    }

    fun clearExposes() {
        exposes.clear()
    }
}