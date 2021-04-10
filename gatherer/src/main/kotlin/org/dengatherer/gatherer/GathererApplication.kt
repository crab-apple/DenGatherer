package org.dengatherer.gatherer

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class GathererApplication

fun main(args: Array<String>) {
	runApplication<GathererApplication>(*args)
}
