package org.dengatherer.gatherer

import org.springframework.stereotype.Service
import java.time.Instant

@Service
class ExposeService(val exposeDAO: ExposeDAO) {

    fun getAllExposes(): List<Expose> = exposeDAO.getAllExposes()

    fun notifyExpose(exposeInput: ExposeInput) {

        val expose = Expose(
            exposeInput.id,
            exposeInput.source,
            exposeInput.url,
            exposeInput.provider,
            exposeInput.imageUrl,
            exposeInput.title,
            exposeInput.address,
            exposeInput.district,
            exposeInput.locationLat,
            exposeInput.locationLong,
            exposeInput.size,
            exposeInput.rooms,
            exposeInput.coldRent,
            exposeInput.comments,
            exposeInput.originalData,
            Availability.new(Instant.now()),
        )

        exposeDAO.addIfNotExists(expose)
    }
}