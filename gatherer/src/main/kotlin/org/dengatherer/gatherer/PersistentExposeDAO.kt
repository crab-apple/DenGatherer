package org.dengatherer.gatherer

import org.springframework.context.annotation.Profile
import org.springframework.stereotype.Service

@Service
@Profile("prod", "dev")
class PersistentExposeDAO(val repo: ExposeRepository) : ExposeDAO {

    override fun getAllExposes(): List<Expose> = repo.findAll().toList()

    override fun addIfNotExists(expose: Expose) {
        if (!repo.existsById(expose.id)) {
            repo.save(expose)
        }
    }
}