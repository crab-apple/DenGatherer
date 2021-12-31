package org.dengatherer.gatherer

interface ExposeDAO {

    fun getAllExposes(): List<Expose>

    fun addIfNotExists(expose: Expose)
}