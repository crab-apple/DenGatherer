package org.dengatherer.gatherer

import org.springframework.stereotype.Service

@Service
class ExposeService(val exposeDAO: ExposeDAO) {

    fun getAllExposes(): List<Expose> = exposeDAO.getAllExposes()

    fun notifyExpose(expose: Expose) {
        exposeDAO.addIfNotExists(expose)
    }

}