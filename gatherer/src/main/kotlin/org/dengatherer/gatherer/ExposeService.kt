package org.dengatherer.gatherer

import org.springframework.stereotype.Service
import java.time.Instant

@Service
class ExposeService(val exposeDAO: ExposeDAO) {

    fun getAllExposes(): List<Expose> = exposeDAO.getAllExposes()

    fun notifyExpose(expose: Expose) {
        expose.dateReceived = Instant.now()
        exposeDAO.addIfNotExists(expose)
    }

}