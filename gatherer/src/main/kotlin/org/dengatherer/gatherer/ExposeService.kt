package org.dengatherer.gatherer

import org.springframework.stereotype.Service

@Service
class ExposeService {

    private val exposes = mutableListOf<Expose>()

    fun getAllExposes(): List<Expose> = exposes

    fun notifyExpose(exposeJson: String) {
        exposes.add(ExposeParser().parse(exposeJson))
    }

    fun clearExposes(){
        exposes.clear()
    }
}